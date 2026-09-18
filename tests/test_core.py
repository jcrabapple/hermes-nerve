import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hermes_jev import client, engine, gate, privacy, receipts, tools


class FakeProvider:
    def __init__(self, choice="ALLOW", confidence=0.93, probabilities=None):
        self.choice = choice
        self.confidence = confidence
        self.probabilities = probabilities or {"ALLOW": confidence, "APPROVAL": 0.05, "BLOCK": 0.02}

    def system_one(self, *, state, questions, model=None):
        return client.JevResponse(
            model="jev-test",
            answers={"decision": {"type": "choice", "choice": self.choice, "confidence": self.confidence, "probabilities": self.probabilities}},
            usage={"input_tokens": 10, "output_tokens": 0},
            latency_ms=12.5,
        )


class EngineTests(unittest.TestCase):
    def test_redacts_secrets_and_hashes_stably(self):
        value = {"api_key": "abc", "nested": {"token": "secret"}, "text": "Bearer abcdefghijklmnop"}
        safe = privacy.redact(value)
        self.assertEqual(safe["api_key"], "[REDACTED]")
        self.assertEqual(safe["nested"]["token"], "[REDACTED]")
        self.assertNotIn("abcdefghijklmnop", safe["text"])
        self.assertEqual(privacy.canonical_hash({"b": 2, "a": 1}), privacy.canonical_hash({"a": 1, "b": 2}))

    def test_client_wire_protocol(self):
        captured = {}
        def transport(url, headers, body, timeout):
            captured.update(url=url, headers=headers, body=json.loads(body), timeout=timeout)
            return 200, json.dumps({
                "model": "jev-test", "usage": {"input_tokens": 3, "output_tokens": 0},
                "answers": {"q": {"type": "choice", "choice": "A", "confidence": 0.9, "probabilities": {"A": 0.9, "B": 0.1}}},
            }).encode()
        c = client.JevClient(api_key="secret", transport=transport)
        response = c.system_one(state={"x": 1}, questions={"q": {"type": "choice", "criteria": {"A": None, "B": None}}})
        self.assertEqual(captured["url"], "https://api.typesafe.ai/v1/systemone")
        self.assertEqual(captured["headers"]["Authorization"], "Bearer secret")
        self.assertEqual(captured["body"]["model"], "jev-latest")
        self.assertEqual(response.answers["q"]["choice"], "A")

    def test_decision_receipt_omits_raw_state_by_default(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_RECEIPTS": str(Path(td) / "r.jsonl")}, clear=False):
            result = engine.DecisionEngine(FakeProvider()).decide(
                state={"secret": "raw-value", "task": "x"}, instructions="choose", choices=["ALLOW", "APPROVAL", "BLOCK"], contract="test/v1"
            )
            self.assertEqual(result.value, "ALLOW")
            record = json.loads((Path(td) / "r.jsonl").read_text())
            self.assertIn("state_sha256", record)
            self.assertNotIn("state", record)
            self.assertNotIn("raw-value", json.dumps(record))

    def test_rank_orders_probabilities(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_RECEIPTS": str(Path(td) / "r.jsonl")}, clear=False):
            provider = FakeProvider(choice="b", confidence=0.6, probabilities={"a": 0.3, "b": 0.6, "c": 0.1})
            result = engine.DecisionEngine(provider).rank(state={}, instructions="rank", items={"a": None, "b": None, "c": None})
            self.assertEqual([x["label"] for x in result["ranking"]], ["b", "a", "c"])

    def test_out_of_contract_choice_rejected(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_RECEIPTS": str(Path(td) / "r.jsonl")}, clear=False):
            with self.assertRaises(ValueError):
                engine.DecisionEngine(FakeProvider(choice="MAYBE", probabilities={"MAYBE": 1.0})).decide(
                    state={}, instructions="x", choices=["YES", "NO"]
                )


class GateTests(unittest.TestCase):
    def setUp(self):
        gate._configured_mode = None
        gate._configured_min_confidence = None

    def _factory(self, choice, confidence=0.95):
        class Factory:
            def __call__(self):
                return engine.DecisionEngine(FakeProvider(choice=choice, confidence=confidence, probabilities={choice: confidence}))
        return Factory()

    def test_gate_off_never_calls_provider(self):
        with patch.dict(os.environ, {"HERMES_JEV_GATE_MODE": "off"}, clear=False):
            self.assertIsNone(gate.evaluate_tool_call(tool_name="terminal", args={}, task_id="t", engine_factory=lambda: (_ for _ in ()).throw(AssertionError())))

    def test_enforce_block(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"HERMES_JEV_GATE_MODE": "enforce", "HERMES_JEV_RECEIPTS": str(Path(td) / "r.jsonl")}, clear=False):
            original = gate.evaluate_tool_call
            gate.evaluate_tool_call = lambda **kwargs: engine.DecisionResult("BLOCK", 0.95, {"BLOCK": 0.95}, "jev-test", 1.0, "x")
            try:
                # The block verdict is mocked, so the command content is irrelevant. Keep the
                # fixture non-destructive so Hermes' install-time scanner does not mistake a
                # rejection test vector for executable destructive behavior.
                decision = gate.pre_tool_call("terminal", {"command": "fixture-command"}, "t")
            finally:
                gate.evaluate_tool_call = original
            self.assertEqual(decision["action"], "block")

    def test_enforce_low_confidence_goes_to_human(self):
        with patch.dict(os.environ, {"HERMES_JEV_GATE_MODE": "enforce", "HERMES_JEV_MIN_CONFIDENCE": "0.80"}, clear=False):
            original = gate.evaluate_tool_call
            gate.evaluate_tool_call = lambda **kwargs: engine.DecisionResult("ALLOW", 0.51, {"ALLOW": 0.51}, "jev-test", 1.0, "x")
            try:
                decision = gate.pre_tool_call("terminal", {"command": "echo hi"}, "t")
            finally:
                gate.evaluate_tool_call = original
            self.assertEqual(decision["action"], "approve")

    def test_provider_failure_fails_to_human_in_enforce(self):
        with patch.dict(os.environ, {"HERMES_JEV_GATE_MODE": "enforce"}, clear=False):
            original = gate.evaluate_tool_call
            gate.evaluate_tool_call = lambda **kwargs: (_ for _ in ()).throw(RuntimeError("down"))
            try:
                decision = gate.pre_tool_call("terminal", {}, "t")
            finally:
                gate.evaluate_tool_call = original
            self.assertEqual(decision["action"], "approve")


class RegistrationTests(unittest.TestCase):
    def test_registers_three_tools_and_hook(self):
        import importlib.util
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location("hermes_jev_plugin", root / "__init__.py", submodule_search_locations=[str(root)])
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        class Ctx:
            def __init__(self): self.tools = []; self.hooks = []
            def get_config(self, key, default=None):
                return {
                    "gate_mode": "advisory",
                    "min_confidence": 0.91,
                    "receipt_detail": "sanitized",
                }.get(key, default)
            def register_tool(self, **kwargs): self.tools.append(kwargs)
            def register_hook(self, name, callback): self.hooks.append((name, callback))
        ctx = Ctx(); module.register(ctx)
        self.assertEqual({x["name"] for x in ctx.tools}, {"jev_decide", "jev_rank", "jev_verify"})
        self.assertEqual([x[0] for x in ctx.hooks], ["pre_tool_call"])
        self.assertTrue(callable(ctx.hooks[0][1]))
        self.assertEqual(module.gate.gate_mode(), "advisory")
        self.assertAlmostEqual(module.gate.minimum_confidence(), 0.91)
        self.assertEqual(module.receipts.receipt_detail(), "sanitized")


class LiveSmokeTests(unittest.TestCase):
    def test_live_smoke_requires_explicit_api_key(self):
        import importlib.util
        root = Path(__file__).resolve().parents[1]
        smoke_path = root / "scripts" / "live_api_smoke.py"
        spec = importlib.util.spec_from_file_location("hermes_jev_live_smoke", smoke_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(module.main(), 2)


if __name__ == "__main__":
    unittest.main()
