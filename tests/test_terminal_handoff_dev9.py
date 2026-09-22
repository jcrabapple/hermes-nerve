from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from hermes_nerve.work import hooks, runtime
from hermes_nerve.work.models import RunIdentity, utc_now
from hermes_nerve.work.supervisor import CardSupervisor


class Accept:
    value = "ACCEPT"
    confidence = 1.0
    receipt_id = "local"


class TrackingEngine:
    verify_calls = 0

    def verify(self, **kwargs):
        type(self).verify_calls += 1
        return SimpleNamespace(
            value="PASS",
            confidence=0.99,
            receipt_id=f"completion-{type(self).verify_calls}",
            usage={"input_tokens": 100, "output_tokens": 10, "total_tokens": 110},
        )


class Dev9TerminalHandoffTests(unittest.TestCase):
    def setUp(self):
        TrackingEngine.verify_calls = 0
        runtime.set_tool_dispatcher(None)

    def _supervisor(self, root: Path):
        runtime.configure(
            enabled=True,
            mode="advisory",
            store_path=str(root / "work.db"),
            provider_decisions_enabled=True,
        )
        sup = CardSupervisor(
            store_path=root / "work.db",
            engine_factory=TrackingEngine,
            mode="advisory",
            control_confidence=0.90,
        )
        bound = sup.bind_contract(
            task_id="t",
            goal="ship",
            criteria=[{
                "id": "DOD-SEM",
                "description": "The requested repair is independently verified.",
                "estimated_tokens": 60000,
            }],
            reserve_tokens=10000,
            preflight_result=Accept(),
        )
        ident = RunIdentity("t", 1, bound["contract"]["contract_hash"], "claim", "worker")
        sup.bind_run(ident)
        runtime.set_supervisor_for_tests(sup, enabled_value=True)
        return sup, ident

    @staticmethod
    def _env(ident: RunIdentity, *, child: bool = False):
        env = {
            "HERMES_KANBAN_TASK": ident.task_id,
            "HERMES_KANBAN_TASK_ID": ident.task_id,
            "HERMES_KANBAN_RUN_ID": str(ident.run_id),
            "HERMES_KANBAN_CLAIM_LOCK": ident.claim_identity,
            "HERMES_KANBAN_WORKER_ID": ident.worker_id or "worker",
            "HERMES_NERVE_DOD_HASH": ident.contract_hash,
        }
        if child:
            env["HERMES_DELEGATED_CHILD_CONTEXT"] = "/tmp/fenced-kanban-root"
        return env

    def _observe_semantic_evidence(self, sup: CardSupervisor, ident: RunIdentity):
        sup.observe_evidence(
            ident,
            value={"summary": "tests pass and requested behavior is present"},
            kind="tool_result",
            source="controller_observed",
            tool_name="terminal",
        )

    def test_child_pre_verify_never_spends_jev_or_controls_parent_completion(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)
            with patch.dict(os.environ, self._env(ident, child=True), clear=False):
                response = hooks.pre_verify(task_id="t", session_id="child", final_response="done")
            self.assertIsNone(response)
            self.assertEqual(TrackingEngine.verify_calls, 0)
            self.assertEqual(sup.store.supervisor_usage_total(ident), 0)
            self.assertEqual(sup.projection("t").criteria[0].state, "UNKNOWN")

    def test_child_session_end_never_audits_parent_completion(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)
            with patch.dict(os.environ, self._env(ident, child=True), clear=False):
                hooks.on_session_end(task_id="t", session_id="child")
            self.assertEqual(TrackingEngine.verify_calls, 0)
            self.assertEqual(sup.store.supervisor_usage_total(ident), 0)
            self.assertEqual(sup.projection("t").criteria[0].state, "UNKNOWN")

    def test_child_cannot_authorize_parent_kanban_complete(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            sup.mark_deterministic_verdict(
                ident,
                "DOD-SEM",
                passed=True,
                reason="deterministically proven",
            )
            with patch.dict(os.environ, self._env(ident, child=True), clear=False):
                response = hooks.pre_tool_call(
                    tool_name="kanban_complete",
                    args={"summary": "done"},
                    task_id="t",
                    session_id="child",
                )
            self.assertIsInstance(response, dict)
            self.assertEqual(response.get("action"), "block")
            self.assertEqual(response.get("rule_key"), "jev:work-completion-authority")
            self.assertEqual(TrackingEngine.verify_calls, 0)

    def test_fresh_completion_verdict_can_clear_stale_replan_control(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            sup.mark_deterministic_verdict(
                ident,
                "DOD-SEM",
                passed=True,
                reason="deterministically proven",
            )
            sup.store.set_control(
                ident,
                control="REPLAN",
                decision_id="older-replan",
                payload={"confidence": 0.99, "reason": "older trajectory state"},
                created_at=utc_now(),
            )
            self.assertIsNotNone(sup.control_for_run(ident))
            with patch.dict(os.environ, self._env(ident), clear=False):
                response = hooks.pre_tool_call(
                    tool_name="kanban_complete",
                    args={"summary": "done"},
                    task_id="t",
                    session_id="parent",
                )
            self.assertIsNone(response)
            self.assertEqual((sup.control_for_run(ident) or {}).get("control"), "COMPLETE_READY")
            self.assertEqual(TrackingEngine.verify_calls, 0)


    def test_passing_pre_verify_arms_terminal_only_handoff_without_reverify(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)
            with patch.dict(os.environ, self._env(ident), clear=False):
                response = hooks.pre_verify(task_id="t", session_id="parent", final_response="done")
                self.assertIsInstance(response, dict)
                self.assertEqual(response.get("action"), "continue")
                self.assertEqual(response.get("rule_key"), "jev:work-terminal-ready")
                self.assertIn("directly-listed kanban_complete", response.get("message", ""))
                self.assertEqual(TrackingEngine.verify_calls, 1)

                # Re-entering the finish boundary must not spend another Jev call.
                response2 = hooks.pre_verify(task_id="t", session_id="parent", final_response="done again")
                self.assertEqual(response2.get("rule_key"), "jev:work-terminal-ready")
                self.assertEqual(TrackingEngine.verify_calls, 1)

                # The exact dev9 failure path is fenced: no generic wrapper, tool
                # search, shell, or file-writing detour is allowed after PASS.
                for tool_name in ("tool_call", "tool_search", "terminal", "write_file"):
                    blocked = hooks.pre_tool_call(
                        tool_name=tool_name,
                        args={"command": "echo nope"} if tool_name == "terminal" else {},
                        task_id="t",
                        session_id="parent",
                    )
                    self.assertIsInstance(blocked, dict)
                    self.assertEqual(blocked.get("action"), "block")
                    self.assertEqual(blocked.get("rule_key"), "jev:work-terminal-ready")
                self.assertEqual(TrackingEngine.verify_calls, 1)

                # The directly-listed native terminal tool is the sole allowed exit.
                allowed = hooks.pre_tool_call(
                    tool_name="kanban_complete",
                    args={"summary": "done"},
                    task_id="t",
                    session_id="parent",
                )
                self.assertIsNone(allowed)
                self.assertEqual(TrackingEngine.verify_calls, 1)

    def test_dev11_pre_verify_pass_dispatches_native_completion_without_new_model_turn(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)
            dispatched = []

            def fake_dispatch(name, args):
                dispatched.append((name, args))
                return '{"ok":true,"task_id":"t","run_id":1}'

            runtime.set_tool_dispatcher(fake_dispatch)
            with patch.dict(os.environ, self._env(ident), clear=False):
                response = hooks.pre_verify(
                    task_id="t", session_id="parent",
                    final_response="DOD-SEM complete; python3 -m pytest tests/ -q; 1 passed",
                )
            self.assertIsNone(response)
            self.assertEqual(TrackingEngine.verify_calls, 1)
            self.assertEqual(len(dispatched), 1)
            self.assertEqual(dispatched[0][0], "kanban_complete")
            self.assertIn("summary", dispatched[0][1])
            self.assertEqual((sup.control_for_run(ident) or {}).get("control"), "COMPLETE_READY")
            with sup.store.read() as con:
                kinds = [r[0] for r in con.execute("SELECT kind FROM supervision_diagnostics WHERE task_id=?", ("t",))]
            self.assertIn("completion_native_dispatch", kinds)

    def test_dev12_native_success_suppresses_hermes_stop_nudge_without_extra_turn(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)

            def fake_dispatch(name, args):
                return {"ok": True, "task_id": "t", "run_id": 1}

            runtime.set_tool_dispatcher(fake_dispatch)
            env = self._env(ident)
            env["HERMES_KANBAN_STOP_NUDGE"] = "1"
            with patch.dict(os.environ, env, clear=False):
                response = hooks.pre_verify(
                    task_id="t", session_id="parent",
                    final_response="DOD-SEM complete; python3 -m pytest tests/ -q; 1 passed",
                )
                self.assertIsNone(response)
                self.assertEqual(os.environ.get("HERMES_KANBAN_STOP_NUDGE"), "0")
            with sup.store.read() as con:
                kinds = [r[0] for r in con.execute(
                    "SELECT kind FROM supervision_diagnostics WHERE task_id=?", ("t",)
                )]
            self.assertIn("completion_stop_nudge_suppressed", kinds)

    def test_dev12_native_failure_does_not_suppress_hermes_stop_nudge(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)

            def fake_dispatch(name, args):
                return {"ok": False, "error": "no"}

            runtime.set_tool_dispatcher(fake_dispatch)
            env = self._env(ident)
            env["HERMES_KANBAN_STOP_NUDGE"] = "1"
            with patch.dict(os.environ, env, clear=False):
                response = hooks.pre_verify(
                    task_id="t", session_id="parent", final_response="done"
                )
                # dev15: verified PASS never sends the model into another completion
                # turn. Controller-local retries fail closed into COMPLETION_RETRY.
                self.assertIsNone(response)
                self.assertEqual(os.environ.get("HERMES_KANBAN_STOP_NUDGE"), "1")
                control = sup.control_for_run(ident) or {}
                self.assertEqual((control.get("payload") or {}).get("lifecycle_state"), "COMPLETION_RETRY")

    def test_dev11_native_dispatch_result_parsing_fails_closed(self):
        self.assertEqual(hooks._native_dispatch_succeeded({"ok": True, "task_id": "t"})[0], True)
        self.assertEqual(hooks._native_dispatch_succeeded('{"ok":true,"task_id":"t"}')[0], True)
        self.assertEqual(hooks._native_dispatch_succeeded({"ok": False, "error": "no"})[0], False)
        self.assertEqual(hooks._native_dispatch_succeeded('{"error":"no"}')[0], False)
        self.assertEqual(hooks._native_dispatch_succeeded("ambiguous tool output")[0], False)
        self.assertEqual(hooks._native_dispatch_succeeded(None)[0], False)

    def test_dev11_blocks_generic_kanban_database_bypass_before_pass(self):
        with tempfile.TemporaryDirectory() as td:
            _, ident = self._supervisor(Path(td))
            with patch.dict(os.environ, self._env(ident), clear=False):
                cases = [
                    ("terminal", {"command": "hermes kanban complete t --summary done"}),
                    ("terminal", {"command": "sqlite3 ~/.hermes/kanban/boards/x/kanban.db \"UPDATE tasks SET status='done' WHERE id='t';\""}),
                    ("write_file", {"path": "_kanban_done.py", "content": "import sqlite3\n# kanban.db\nconn.execute(\"UPDATE tasks SET status='done'\")"}),
                ]
                for name, args in cases:
                    blocked = hooks.pre_tool_call(
                        tool_name=name, args=args, task_id="t", session_id="parent"
                    )
                    self.assertEqual(blocked.get("action"), "block")
                    self.assertEqual(blocked.get("rule_key"), "jev:work-kanban-authority")

    def test_dev11_session_end_does_not_reverify_terminal_ready_pass(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            sup.store.set_control(
                ident, control="COMPLETE_READY", decision_id="ready",
                payload={"reason": "verified", "confidence": 1.0, "receipt_id": "det"},
                created_at=utc_now(),
            )
            with patch.dict(os.environ, self._env(ident), clear=False):
                hooks.on_session_end(task_id="t", session_id="parent")
            self.assertEqual(TrackingEngine.verify_calls, 0)
            with sup.store.read() as con:
                kinds = [r[0] for r in con.execute("SELECT kind FROM supervision_diagnostics WHERE task_id=?", ("t",))]
            self.assertIn("completion_session_end_skipped", kinds)

    def test_terminal_ready_still_cannot_be_used_by_delegated_child(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            sup.store.set_control(
                ident,
                control="COMPLETE_READY",
                decision_id="ready",
                payload={"reason": "verified"},
                created_at=utc_now(),
            )
            with patch.dict(os.environ, self._env(ident, child=True), clear=False):
                response = hooks.pre_tool_call(
                    tool_name="kanban_complete",
                    args={"summary": "done"},
                    task_id="t",
                    session_id="child",
                )
            self.assertIsInstance(response, dict)
            self.assertEqual(response.get("action"), "block")
            self.assertEqual(response.get("rule_key"), "jev:work-completion-authority")
            self.assertEqual(TrackingEngine.verify_calls, 0)

    def test_terminal_ready_supersedes_stale_replan_and_stays_durable(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            self._observe_semantic_evidence(sup, ident)
            sup.store.set_control(
                ident,
                control="REPLAN",
                decision_id="stale-replan",
                payload={"confidence": 0.99},
                created_at=utc_now(),
            )
            with patch.dict(os.environ, self._env(ident), clear=False):
                response = hooks.pre_verify(task_id="t", session_id="parent", final_response="done")
            self.assertEqual(response.get("rule_key"), "jev:work-terminal-ready")
            control = sup.control_for_run(ident) or {}
            self.assertEqual(control.get("control"), "COMPLETE_READY")
            self.assertNotEqual(control.get("decision_id"), "stale-replan")
            self.assertEqual(TrackingEngine.verify_calls, 1)

    def test_active_control_still_blocks_ordinary_non_checkpoint_tools(self):
        with tempfile.TemporaryDirectory() as td:
            sup, ident = self._supervisor(Path(td))
            sup.store.set_control(
                ident,
                control="REPLAN",
                decision_id="replan",
                payload={"confidence": 0.99},
                created_at=utc_now(),
            )
            with patch.dict(os.environ, self._env(ident), clear=False):
                response = hooks.pre_tool_call(
                    tool_name="write_file",
                    args={"path": "x.py", "content": "x"},
                    task_id="t",
                    session_id="parent",
                )
            self.assertIsInstance(response, dict)
            self.assertEqual(response.get("action"), "block")
            self.assertEqual(response.get("rule_key"), "jev:work-control")


if __name__ == "__main__":
    unittest.main()
