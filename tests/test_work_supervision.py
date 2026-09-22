from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

from hermes_jev.work.models import RunIdentity, WorkEvent
from hermes_jev.work.store import SupervisionStore
from hermes_jev.work.supervisor import CardSupervisor


@dataclass
class FakeResult:
    value: str
    confidence: float = 0.95
    probabilities: dict | None = None
    receipt_id: str = "fake-receipt"

    def __post_init__(self):
        if self.probabilities is None:
            self.probabilities = {self.value: self.confidence}


class FakeEngine:
    def __init__(self, decisions=None, verifies=None):
        self.decisions = list(decisions or [FakeResult("ACCEPT")])
        self.verifies = list(verifies or [FakeResult("PASS")])

    def decide(self, **kwargs):
        choices = list(kwargs.get("choices") or [])
        if self.decisions:
            return self.decisions.pop(0)
        if "ACCEPT" in choices:
            return FakeResult("ACCEPT")
        return FakeResult("CONTINUE", probabilities={"CONTINUE": .9, "WATCH": .1})

    def verify(self, **kwargs):
        return self.verifies.pop(0) if self.verifies else FakeResult("PASS")


class WorkSupervisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "supervision.sqlite3"

    def tearDown(self):
        self.tmp.cleanup()

    def supervisor(self, engine: FakeEngine | None = None, mode: str = "shadow") -> CardSupervisor:
        eng = engine or FakeEngine()
        return CardSupervisor(store_path=self.db, engine_factory=lambda: eng, mode=mode)

    def criteria(self):
        return [
            {"id": "c1", "description": "implementation exists", "estimated_tokens": 1000, "weight": 2},
            {"id": "c2", "description": "tests pass", "estimated_tokens": 500, "depends_on": ["c1"]},
        ]

    def bind(self, sup: CardSupervisor):
        out = sup.bind_contract(task_id="t1", goal="ship feature", criteria=self.criteria(), reserve_tokens=500)
        self.assertTrue(out["accepted"])
        return out

    def identity(self, contract_hash: str, run_id: int = 7, claim: str = "claim-a"):
        return RunIdentity("t1", run_id, contract_hash, claim, "worker-a")

    def test_store_has_no_canonical_status_or_queue(self):
        store = SupervisionStore(self.db)
        tables = store.raw_table_names()
        self.assertNotIn("tasks", tables)
        self.assertNotIn("task_queue", tables)
        with store.read() as con:
            columns = []
            for table in tables:
                if table.startswith("sqlite_"):
                    continue
                columns.extend(str(r[1]) for r in con.execute(f"PRAGMA table_info({table})"))
        self.assertNotIn("task_status", columns)
        self.assertNotIn("retry_count", columns)

    def test_locked_contract_is_immutable_and_amendment_versions(self):
        sup = self.supervisor()
        first = self.bind(sup)["contract"]
        with self.assertRaises(ValueError):
            sup.bind_contract(task_id="t1", goal="ship feature", criteria=self.criteria())
        amended = self.criteria() + [{"id": "c3", "description": "docs", "estimated_tokens": 200}]
        out = sup.bind_contract(task_id="t1", goal="ship feature", criteria=amended, reserve_tokens=500, amend=True)
        self.assertTrue(out["accepted"])
        self.assertEqual(out["contract"]["version"], 2)
        self.assertEqual(out["contract"]["supersedes_hash"], first["contract_hash"])
        self.assertNotEqual(out["contract"]["contract_hash"], first["contract_hash"])
        old = sup.store.contract_row(first["contract_hash"])
        self.assertIsNotNone(old)

    def test_claim_is_not_verification_and_frontier_is_deterministic(self):
        sup = self.supervisor()
        contract = self.bind(sup)["contract"]
        ident = self.identity(contract["contract_hash"])
        sup.bind_run(ident)
        p = sup.record_event(ident, WorkEvent("e1", "CRITERION_CLAIMED_PASS", "c1"))
        self.assertEqual(p.verified_percent, 0.0)
        self.assertEqual(p.frontier, ("c1",))
        self.assertEqual(next(c for c in p.criteria if c.criterion_id == "c1").state, "CLAIMED_PASS")

    def test_stale_run_is_auditable_but_cannot_change_live_projection(self):
        sup = self.supervisor()
        contract = self.bind(sup)["contract"]
        current = self.identity(contract["contract_hash"], run_id=8, claim="new")
        stale = self.identity(contract["contract_hash"], run_id=7, claim="old")
        sup.bind_run(current)
        sup.record_event(stale, WorkEvent("stale-event", "CRITERION_CLAIMED_PASS", "c1"))
        p = sup.projection("t1")
        self.assertEqual(next(c for c in p.criteria if c.criterion_id == "c1").state, "UNKNOWN")
        rows = sup.store.events("t1", include_stale=True)
        self.assertEqual(rows[-1]["stale"], 1)

    def test_observed_evidence_then_jev_pass_creates_verified_progress(self):
        engine = FakeEngine(verifies=[FakeResult("PASS")])
        sup = self.supervisor(engine)
        contract = self.bind(sup)["contract"]
        ident = self.identity(contract["contract_hash"])
        sup.bind_run(ident)
        sup.record_event(ident, WorkEvent("e1", "CRITERION_CLAIMED_PASS", "c1"))
        sup.observe_evidence(ident, value={"pytest": "1 passed"}, criterion_id="c1", tool_name="terminal")
        out = sup.verify_criterion(ident, "c1")
        self.assertEqual(out["state"], "VERIFIED_PASS")
        p = sup.projection("t1")
        self.assertGreater(p.verified_percent, 0)
        self.assertEqual(p.frontier, ("c2",))

    def test_completion_requires_all_required_verified_then_terminal_pass(self):
        engine = FakeEngine(verifies=[FakeResult("PASS"), FakeResult("PASS"), FakeResult("PASS")])
        sup = self.supervisor(engine)
        contract = self.bind(sup)["contract"]
        ident = self.identity(contract["contract_hash"])
        sup.bind_run(ident)
        self.assertFalse(sup.verify_completion(ident).allow)
        for cid in ("c1", "c2"):
            sup.observe_evidence(ident, value={"criterion": cid, "test": "pass"}, criterion_id=cid)
            self.assertEqual(sup.verify_criterion(ident, cid)["state"], "VERIFIED_PASS")
        verdict = sup.verify_completion(ident, {"summary": "done"})
        self.assertTrue(verdict.allow)
        self.assertEqual(verdict.value, "PASS")

    def test_budget_checkpoint_fires_once_and_worker_cannot_change_allocation(self):
        sup = self.supervisor()
        contract = self.bind(sup)["contract"]
        ident = self.identity(contract["contract_hash"])
        sup.bind_run(ident)
        self.assertEqual(contract["allocated_tokens"], 2000)
        one = sup.record_usage(ident, consumed_tokens=800, source="provider_usage")
        self.assertEqual(one["newly_crossed"], [0.4])
        two = sup.record_usage(ident, consumed_tokens=850, source="provider_usage")
        self.assertEqual(two["newly_crossed"], [])
        self.assertEqual(two["budget"]["allocated_tokens"], 2000)

    def test_shadow_replan_never_sets_control(self):
        engine = FakeEngine(decisions=[FakeResult("ACCEPT"), FakeResult("REPLAN", probabilities={"REPLAN": .93, "CONTINUE": .04, "WATCH": .03})])
        sup = self.supervisor(engine, mode="shadow")
        contract = self.bind(sup)["contract"]
        ident = self.identity(contract["contract_hash"])
        sup.bind_run(ident)
        assessment = sup.assess_trajectory(ident, trigger="test_failure", failures=["pytest failed"])
        self.assertEqual(assessment.control, "REPLAN")
        self.assertIsNone(sup.control_for_run(ident))


if __name__ == "__main__":
    unittest.main()
