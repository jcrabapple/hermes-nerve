from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hermes_nerve.work import hooks, runtime
from hermes_nerve.work.models import CompletionVerdict, RunIdentity
from hermes_nerve.work.supervisor import CardSupervisor


class Accept:
    value = "ACCEPT"
    confidence = 1.0
    receipt_id = "local"


class Dev15ControllerCompletionTests(unittest.TestCase):
    def setUp(self):
        runtime.set_tool_dispatcher(None)
        runtime.set_supervisor_for_tests(None, enabled_value=False)
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        runtime.configure(enabled=True, mode="advisory", store_path=str(root / "work.db"))
        self.sup = CardSupervisor(store_path=root / "work.db", mode="advisory")
        bound = self.sup.bind_contract(
            task_id="t",
            goal="finish safely",
            criteria=[{"id": "DOD-01", "description": "task is complete", "estimated_tokens": 1000}],
            reserve_tokens=1000,
            preflight_result=Accept(),
        )
        self.ident = RunIdentity("t", 1, bound["contract"]["contract_hash"], "claim", "worker")
        self.sup.bind_run(self.ident)
        runtime.set_supervisor_for_tests(self.sup, enabled_value=True)
        self.verdict = CompletionVerdict(
            allow=True,
            value="PASS",
            confidence=1.0,
            reason="verified",
            receipt_id="deterministic",
        )
        self.env = {
            "HERMES_KANBAN_TASK": "t",
            "HERMES_KANBAN_TASK_ID": "t",
            "HERMES_KANBAN_RUN_ID": "1",
            "HERMES_KANBAN_CLAIM_LOCK": "claim",
            "HERMES_KANBAN_WORKER_ID": "worker",
            "HERMES_NERVE_DOD_HASH": self.ident.contract_hash,
        }

    def tearDown(self):
        runtime.set_tool_dispatcher(None)
        runtime.set_supervisor_for_tests(None, enabled_value=False)
        self.tmp.cleanup()

    def _state(self):
        control = self.sup.control_for_run(self.ident) or {}
        return (control.get("payload") or {}).get("lifecycle_state")

    def test_pre_verify_controller_completes_even_when_worker_is_child_fenced(self):
        calls = []
        runtime.set_tool_dispatcher(lambda name, args: calls.append((name, args)) or {"ok": True, "status": "done"})
        env = dict(self.env)
        env["HERMES_DELEGATED_CHILD_CONTEXT"] = "1"
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, env, clear=False):
            response = hooks.pre_verify(task_id="t", session_id="s", final_response="done")
        self.assertIsNone(response)
        self.assertEqual([name for name, _ in calls], ["kanban_complete"])
        self.assertEqual(self._state(), "COMPLETED")

    def test_transient_native_failures_retry_inside_controller_without_model_continue(self):
        calls = []
        results = iter([
            {"ok": False, "error": "temporary lock"},
            {"ok": False, "error": "temporary lock"},
            {"ok": True, "status": "done"},
        ])
        runtime.set_tool_dispatcher(lambda name, args: calls.append((name, args)) or next(results))
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, self.env, clear=False):
            response = hooks.pre_verify(task_id="t", session_id="s", final_response="done")
        self.assertIsNone(response)
        self.assertEqual(len(calls), 3)
        self.assertEqual(self._state(), "COMPLETED")

    def test_persistent_native_failure_defers_to_session_end_not_worker_loop(self):
        failures = []
        runtime.set_tool_dispatcher(lambda name, args: failures.append((name, args)) or {"ok": False, "error": "locked"})
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, self.env, clear=False):
            response = hooks.pre_verify(task_id="t", session_id="s", final_response="done")
        self.assertIsNone(response)
        self.assertEqual(len(failures), 3)
        self.assertEqual(self._state(), "COMPLETION_RETRY")

        retries = []
        runtime.set_tool_dispatcher(lambda name, args: retries.append((name, args)) or {"ok": True, "status": "done"})
        with patch.dict(os.environ, self.env, clear=False):
            hooks.on_session_end(task_id="t", session_id="s")
        self.assertEqual(len(retries), 1)
        self.assertEqual(self._state(), "COMPLETED")

    def test_pair3_cli_completion_attempt_is_converted_to_controller_completion(self):
        calls = []
        runtime.set_tool_dispatcher(lambda name, args: calls.append((name, args)) or {"ok": True, "status": "done"})
        env = dict(self.env)
        env["HERMES_DELEGATED_CHILD_CONTEXT"] = "1"
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, env, clear=False):
            response = hooks.pre_tool_call(
                "terminal",
                {"command": "hermes kanban --board example complete t --summary done"},
                task_id="t",
                session_id="s",
            )
        self.assertEqual(response.get("action"), "block")
        self.assertEqual(response.get("rule_key"), "jev:work-controller-completion")
        self.assertIn("controller completed", response.get("message", ""))
        self.assertEqual([name for name, _ in calls], ["kanban_complete"])
        self.assertEqual(self._state(), "COMPLETED")

    def test_direct_worker_kanban_complete_is_controller_owned(self):
        calls = []
        runtime.set_tool_dispatcher(lambda name, args: calls.append((name, args)) or {"ok": True, "status": "done"})
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, self.env, clear=False):
            response = hooks.pre_tool_call("kanban_complete", {"summary": "done"}, task_id="t", session_id="s")
        self.assertEqual(response.get("action"), "block")
        self.assertEqual(response.get("rule_key"), "jev:work-controller-completion")
        self.assertEqual([name for name, _ in calls], ["kanban_complete"])
        self.assertEqual(self._state(), "COMPLETED")


    def test_controller_dispatch_reentry_is_not_blocked_as_worker_completion(self):
        calls = []
        def dispatcher(name, args):
            # Simulate Hermes dispatch_tool re-entering the plugin pre-tool hooks.
            directive = hooks.pre_tool_call(name, args, task_id="t", session_id="s")
            self.assertIsNone(directive)
            calls.append((name, args))
            return {"ok": True, "status": "done"}
        runtime.set_tool_dispatcher(dispatcher)
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, self.env, clear=False):
            response = hooks.pre_verify(task_id="t", session_id="s", final_response="done")
        self.assertIsNone(response)
        self.assertEqual([name for name, _ in calls], ["kanban_complete"])
        self.assertEqual(self._state(), "COMPLETED")

    def test_worker_calls_after_verified_are_audited(self):
        runtime.set_tool_dispatcher(lambda name, args: {"ok": False, "error": "locked"})
        with patch.object(self.sup, "verify_completion", return_value=self.verdict), patch.dict(os.environ, self.env, clear=False):
            hooks.pre_verify(task_id="t", session_id="s", final_response="done")
            self.assertEqual(self._state(), "COMPLETION_RETRY")
            hooks.post_api_request(task_id="t", session_id="s", api_request_id="after-pass", usage={"input_tokens": 1})
        with sqlite3.connect(str(self.sup.store.path)) as con:
            count = con.execute(
                "SELECT COUNT(*) FROM supervision_diagnostics WHERE task_id='t' AND run_id=1 AND kind='completion_worker_call_after_verified'"
            ).fetchone()[0]
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
