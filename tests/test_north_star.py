from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hermes_nerve.remote.bridge import RemoteEventBridge
from hermes_nerve.work.models import RunIdentity, WorkEvent
from hermes_nerve.work.store import SupervisionStore
from hermes_nerve.work.supervisor import CardSupervisor


class Decision:
    def __init__(self,value,confidence=.99,probabilities=None):
        self.value=value;self.confidence=confidence;self.probabilities=probabilities or {value:confidence};self.receipt_id="r-"+value

class ScriptedEngine:
    trajectory="REPLAN"
    def decide(self,**kwargs):
        contract=kwargs.get("contract")
        if contract=="work-trajectory/v1":return Decision(self.trajectory,.97,{self.trajectory:.97,"CONTINUE":.01,"WATCH":.01,"BLOCK":.01})
        return Decision("ACCEPT")
    def verify(self,**kwargs):return Decision("PASS")

class Accept: value="ACCEPT";confidence=1.;receipt_id="accept"
class Review:
    def __init__(self):self.calls=[]
    def request_review(self,**kw):self.calls.append(kw);return True,None


class NorthStarTests(unittest.TestCase):
    def test_bad_remote_run_is_cut_off_and_successor_resumes_verified_frontier(self):
        with tempfile.TemporaryDirectory() as td:
            sup=CardSupervisor(store=SupervisionStore(Path(td)/"work.db"),engine_factory=ScriptedEngine,mode="advisory",control_confidence=.8)
            b=sup.bind_contract(task_id="root/A",goal="Implement remote cancellation safely",criteria=[
                {"id":"transport","description":"request reaches worker","estimated_tokens":100},
                {"id":"stale","description":"stale run cannot cancel successor","estimated_tokens":200,"depends_on":["transport"]},
            ],reserve_tokens=50,checkpoint_fractions=[.2,.5,.75],preflight_result=Accept())
            h=b["contract"]["contract_hash"]
            run1=RunIdentity("root/A",1,h,"claim-1","ssh:lab")
            sup.bind_run(run1)
            sup.record_event(run1,WorkEvent("e1","CRITERION_CLAIMED_PASS","transport",{},"remote_worker"))
            sup.observe_evidence(run1,value="integration test passed",criterion_id="transport",source="controller_observed_remote")
            self.assertEqual(sup.verify_criterion(run1,"transport")["state"],"VERIFIED_PASS")
            budget=sup.record_usage(run1,consumed_tokens=90,source="remote_provider_usage")
            self.assertIn(.2,budget["newly_crossed"])
            a=sup.assess_trajectory(run1,trigger="budget_checkpoint:0.2")
            self.assertEqual(a.control,"REPLAN")
            review=Review();bridge=RemoteEventBridge(sup,run1,kanban_adapter=review)
            bridge.consume({"type":"tool_use","name":"nerve_work_event","input":{"event_type":"CHECKPOINT_READY","task_id":"root/A","run_id":1,"contract_hash":h,"claim_identity":"claim-1","payload":{"current_plan":"preserve transport; redesign stale-run fence","test_summary":"transport green"}}})
            self.assertTrue(bridge.stop_requested)
            self.assertEqual(review.calls[0]["expected_run_id"],1)

            # Orchestrator sends canonical card back to implementation; a new run
            # binds to the SAME locked DoD. Previously verified facts survive.
            run2=RunIdentity("root/A",2,h,"claim-2","local:replacement")
            p2=sup.bind_run(run2)
            self.assertEqual(p2.verified_required,1)
            self.assertEqual(p2.frontier,("stale",))
            sup.observe_evidence(run2,value="stale run fence integration test passed",criterion_id="stale")
            self.assertEqual(sup.verify_criterion(run2,"stale")["state"],"VERIFIED_PASS")
            done=sup.verify_completion(run2,{"summary":"both criteria proven"})
            self.assertTrue(done.allow)
            final=sup.projection("root/A")
            self.assertEqual(final.verified_percent,100.0)
            self.assertEqual(final.frontier,())

if __name__=="__main__":unittest.main()
