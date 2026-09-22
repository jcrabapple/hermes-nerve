from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hermes_jev.remote.bridge import RemoteEventBridge
from hermes_jev.work import hooks, runtime
from hermes_jev.work.models import RunIdentity
from hermes_jev.work.store import SupervisionStore
from hermes_jev.work.supervisor import CardSupervisor


class Result:
    def __init__(self,value,confidence=0.95,probabilities=None):
        self.value=value; self.confidence=confidence; self.probabilities=probabilities or {value:confidence}; self.receipt_id="receipt"

class Engine:
    def __init__(self,*a,**k): pass
    def decide(self,**kwargs): return Result("REPLAN",0.96,{"REPLAN":.96,"CONTINUE":.01,"WATCH":.02,"BLOCK":.01})
    def verify(self,**kwargs): return Result("PASS",.99,{"PASS":.99})

class Accept:
    value="ACCEPT";confidence=1.;receipt_id="accept"

class FakeKanban:
    def __init__(self): self.calls=[]
    def request_review(self,**kwargs): self.calls.append(kwargs); return True,None


class MidTaskControlTests(unittest.TestCase):
    def make(self, mode="advisory"):
        td=tempfile.TemporaryDirectory(); store=SupervisionStore(Path(td.name)/"s.db")
        sup=CardSupervisor(store=store,engine_factory=Engine,mode=mode,control_confidence=.8)
        bound=sup.bind_contract(task_id="t",goal="ship",criteria=[{"id":"c","description":"prove it","estimated_tokens":100}],reserve_tokens=20,preflight_result=Accept())
        ident=RunIdentity("t",1,bound["contract"]["contract_hash"],"claim","worker")
        sup.bind_run(ident); return td,sup,ident

    def test_advisory_replan_blocks_new_work_until_checkpoint(self):
        td,sup,ident=self.make()
        self.addCleanup(td.cleanup)
        a=sup.assess_trajectory(ident,trigger="25%")
        self.assertEqual(a.control,"REPLAN")
        self.assertEqual(sup.control_for_run(ident)["control"],"REPLAN")
        runtime.set_supervisor_for_tests(sup,enabled_value=True)
        env={"HERMES_KANBAN_TASK_ID":"t","HERMES_KANBAN_RUN_ID":"1","HERMES_JEV_DOD_HASH":ident.contract_hash,"HERMES_KANBAN_CLAIM_IDENTITY":"claim","HERMES_KANBAN_WORKER_ID":"worker"}
        with patch.dict(os.environ,env,clear=False):
            directive=hooks.pre_tool_call("terminal",{"command":"python build.py"},task_id="t")
        self.assertEqual(directive["action"],"block")
        sup.checkpoint_packet(ident,decision_id=a.decision_id,reason="replan",complete=True)
        self.assertIsNone(sup.control_for_run(ident))

    def test_remote_checkpoint_requests_exact_run_review_and_stop(self):
        td,sup,ident=self.make()
        self.addCleanup(td.cleanup)
        sup.assess_trajectory(ident,trigger="failure")
        fake=FakeKanban(); bridge=RemoteEventBridge(sup,ident,reviewer="reviewer",kanban_adapter=fake)
        bridge.consume({"type":"tool_use","name":"jev_work_event","input":{"event_type":"CHECKPOINT_READY","task_id":"t","run_id":1,"contract_hash":ident.contract_hash,"claim_identity":"claim","payload":{"reason":"bad trajectory","current_plan":"saved"}}})
        self.assertTrue(bridge.stop_requested)
        self.assertEqual(len(fake.calls),1)
        self.assertEqual(fake.calls[0]["expected_run_id"],1)
        self.assertEqual(fake.calls[0]["task_id"],"t")
        self.assertIsNone(sup.control_for_run(ident))

    def test_stale_remote_event_is_rejected(self):
        td,sup,ident=self.make()
        self.addCleanup(td.cleanup)
        bridge=RemoteEventBridge(sup,ident,kanban_adapter=FakeKanban())
        bridge.consume({"type":"tool_use","name":"jev_work_event","input":{"event_type":"PLAN_CHANGED","task_id":"t","run_id":999,"contract_hash":ident.contract_hash,"payload":{}}})
        self.assertEqual(bridge.rejected,1)

if __name__=="__main__":unittest.main()
