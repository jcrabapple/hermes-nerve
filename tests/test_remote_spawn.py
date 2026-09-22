from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

from hermes_jev.remote.spawn import KanbanRemoteSpawn, RemoteRoute
from hermes_jev.work.models import RunIdentity
from hermes_jev.work.store import SupervisionStore
from hermes_jev.work.supervisor import CardSupervisor


class Accept:
    value = "ACCEPT"
    confidence = 1.0
    receipt_id = "r"


class FakeEngine:
    def decide(self, **kwargs): return Accept()


class FakeExecution:
    def status(self): return {"runner_pid": 4321}


class FakeManager:
    def __init__(self): self.calls=[]
    def start(self, **kwargs): self.calls.append(kwargs); return FakeExecution()


@dataclass
class Task:
    id: str = "t1"
    title: str = "Build thing"
    body: str = "body"
    assignee: str = "remote"
    current_run_id: int = 9
    claim_lock: str = "claim-9"


class SpawnTests(unittest.TestCase):
    def test_remote_route_reuses_canonical_run_identity(self):
        with tempfile.TemporaryDirectory() as td:
            sup=CardSupervisor(store=SupervisionStore(Path(td)/"s.db"),engine_factory=FakeEngine,mode="shadow")
            bound=sup.bind_contract(task_id="t1",goal="g",criteria=[{"id":"c1","description":"proof","estimated_tokens":10}],preflight_result=Accept())
            manager=FakeManager()
            adapter=KanbanRemoteSpawn(default_spawn=lambda *a,**k:111,routes={"remote":RemoteRoute("lab")},supervisor=sup,manager=manager)
            pid=adapter(Task(),"repo",board="b")
            self.assertEqual(pid,4321)
            ident=manager.calls[0]["identity"]
            self.assertEqual((ident.task_id,ident.run_id,ident.claim_identity),("t1",9,"claim-9"))
            self.assertEqual(ident.contract_hash,bound["contract"]["contract_hash"])

    def test_local_route_is_untouched(self):
        seen=[]
        adapter=KanbanRemoteSpawn(default_spawn=lambda task,ws,board=None: seen.append((task.id,ws,board)) or 7,routes={},supervisor=object())
        self.assertEqual(adapter(Task(),"/tmp/w",board="x"),7)
        self.assertEqual(seen,[("t1","/tmp/w","x")])


if __name__=="__main__": unittest.main()
