import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hermes_jev import client, engine, gate, ledger, receipts, tools
from hermes_jev.context_engine import JevContextEngine


class FakeProvider:
    def __init__(self, choice="ALLOW", confidence=0.9):
        self.choice = choice
        self.confidence = confidence

    def system_one(self, *, state, questions, model=None):
        name = next(iter(questions))
        criteria = questions[name].get("criteria") or {}
        labels = list(criteria) or ["ALLOW", "BLOCK"]
        choice = self.choice if self.choice in labels else labels[0]
        probs = {label: (self.confidence if label == choice else 0.0) for label in labels}
        return client.JevResponse(
            model="jev-test",
            answers={name: {"type": "choice", "choice": choice, "confidence": self.confidence, "probabilities": probs}},
            usage={"input_tokens": 10, "output_tokens": 2, "cost": 0.00001},
            latency_ms=12.5,
            request_id="req-test",
            provider="TypeSafe",
        )


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        client._configured_provider = None
        client._configured_base_url = None
        client._configured_model = None
        client._configured_typesafe_model = None
        client._configured_timeout = None
        gate.configure(mode="off", min_confidence=0.8, scope="selective")
        ledger.configure(enabled=True, detail="sanitized")

    def test_openrouter_wire(self):
        captured = {}
        def transport(url, headers, body, timeout):
            captured.update(url=url, headers=headers, body=json.loads(body))
            return 200, json.dumps({
                "id": "gen-dec-1", "provider": "TypeSafe", "model": "typesafe/jev-1.13-20260917",
                "usage": {}, "answers": {"q": {"type": "choice", "choice": "A", "confidence": 1.0, "probabilities": {"A": 1.0, "B": 0.0}}},
            }).encode()
        c = client.JevClient(provider="openrouter", api_key="k", transport=transport)
        r = c.system_one(state={}, questions={"q": {"type": "choice", "criteria": {"A": None, "B": None}}})
        self.assertEqual(captured["url"], "https://openrouter.ai/api/alpha/decisions")
        self.assertEqual(r.transport, "openrouter-decisions")
        self.assertEqual(r.request_id, "gen-dec-1")

    def test_typesafe_direct_wire_and_request_id(self):
        captured = {}
        def transport(url, headers, body, timeout):
            captured.update(url=url, headers=headers, body=json.loads(body))
            return 200, json.dumps({
                "model": "jev-latest", "usage": {},
                "answers": {"q": {"type": "choice", "choice": "B", "confidence": 0.9, "probabilities": {"A": 0.1, "B": 0.9}}},
            }).encode(), {"x-typesafe-request-id": "req-direct"}
        c = client.JevClient(provider="typesafe", api_key="k", transport=transport)
        r = c.system_one(state={}, questions={"q": {"type": "choice", "criteria": {"A": None, "B": None}}})
        self.assertEqual(captured["url"], "https://api.typesafe.ai/v1/systemone")
        self.assertEqual(r.transport, "typesafe-system-one")
        self.assertEqual(r.request_id, "req-direct")

    def test_selected_provider_requires_only_selected_key(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "or"}, clear=True):
            self.assertEqual(client.JevClient(provider="openrouter").api_key, "or")
            with self.assertRaisesRegex(client.JevError, "TYPESAFE_API_KEY"):
                client.JevClient(provider="typesafe")
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "ts"}, clear=True):
            self.assertEqual(client.JevClient(provider="typesafe").api_key, "ts")

    def test_decision_provenance(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_RECEIPTS": str(Path(td) / "r.jsonl")}, clear=False):
            result = engine.DecisionEngine(FakeProvider()).decide(state={}, instructions="choose", choices=["ALLOW", "BLOCK"])
            self.assertTrue(result.as_dict()["execution"]["live_provider_call"])
            self.assertEqual(result.as_dict()["execution"]["transport"], "openrouter-decisions")

    def test_selective_gate_bypasses_read_only_tool(self):
        gate.configure(mode="advisory", min_confidence=0.8, scope="selective")
        self.assertEqual(gate.bypass_reason("tool_search", {"query": "x"}), "read-only-tool")
        self.assertEqual(gate.bypass_reason("terminal", {"command": "git status --short"}), "read-only-terminal")

    def test_selective_gate_does_not_bypass_mutating_or_ambiguous_shell(self):
        gate.configure(mode="advisory", min_confidence=0.8, scope="selective")
        for command in ("git push origin main", "date --set now", "PATH=/tmp ls", "rg --pre cat x", "cat x > y", "ls | head"):
            self.assertIsNone(gate.bypass_reason("terminal", {"command": command}), command)

    def test_gate_scope_all_disables_read_only_bypass(self):
        gate.configure(mode="advisory", min_confidence=0.8, scope="all")
        self.assertIsNone(gate.bypass_reason("tool_search", {}))

    def test_gate_stats_track_avoided_provider_calls(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_GATE_EVENTS": str(Path(td) / "gate.jsonl")}, clear=False):
            gate.configure(mode="advisory", min_confidence=0.8, scope="selective")
            gate.pre_tool_call("tool_search", {"query": "x"})
            report = gate.report()
            self.assertEqual(report["bypassed"], 1)
            self.assertEqual(report["provider_calls"], 0)
            self.assertEqual(report["estimated_provider_calls_avoided"], 1)

    def test_ledger_records_and_rehydrates_sanitized_evidence(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_CONTEXT_LEDGER": str(Path(td) / "ledger.jsonl")}, clear=False):
            ledger.configure(enabled=True, detail="sanitized")
            ledger.record_evidence(evidence_id="e1", content="Bearer abcdefghijklmnop", kind="tool_result", recoverable=True)
            restored = ledger.rehydrate("e1")
            self.assertIn("[REDACTED]", restored["content"])
            self.assertNotIn("abcdefghijklmnop", restored["content"])

    def test_hash_ledger_refuses_fake_rehydration(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_CONTEXT_LEDGER": str(Path(td) / "ledger.jsonl")}, clear=False):
            ledger.configure(enabled=True, detail="hash")
            ledger.record_evidence(evidence_id="e1", content="exact", kind="tool_result", recoverable=True)
            with self.assertRaises(ValueError):
                ledger.rehydrate("e1")

    def test_stats_tool_is_local_and_combines_sections(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {
            "HERMES_JEV_RECEIPTS": str(Path(td) / "receipts.jsonl"),
            "HERMES_JEV_CONTEXT_LEDGER": str(Path(td) / "ledger.jsonl"),
            "HERMES_JEV_GATE_EVENTS": str(Path(td) / "gate.jsonl"),
        }, clear=False):
            ledger.configure(enabled=True, detail="sanitized")
            ledger.record_evidence(evidence_id="e1", content="status", kind="tool_result", recoverable=True)
            gate.configure(mode="advisory", min_confidence=0.8, scope="selective")
            gate.pre_tool_call("tool_search", {})
            payload = json.loads(tools.jev_stats({"recent_limit": 2}))
            self.assertTrue(payload["ok"])
            self.assertIn("receipts", payload)
            self.assertIn("gate", payload)
            self.assertIn("context", payload)
            self.assertFalse(payload["execution"]["live_provider_call"])

    def test_context_engine_shadow_keeps_builtin_fallback_active(self):
        class Fallback:
            def compress(self, messages, **kwargs):
                return [messages[0], {"role": "assistant", "content": "fallback"}]
        e = JevContextEngine(mode="shadow", threshold_percent=0.5, fallback_builtin=True)
        e.context_length = 1000
        e.threshold_tokens = 500
        e.last_prompt_tokens = 900
        e._fallback = Fallback()
        self.assertTrue(e.should_compress())
        self.assertEqual(e.compress([{"role": "user", "content": "x"}], current_tokens=900)[-1]["content"], "fallback")


if __name__ == "__main__":
    unittest.main()
