from __future__ import annotations

import json
import os
import tempfile
import threading
import unittest
from pathlib import Path

from hermes_jev.engine import DecisionEngine
from hermes_jev.receipts import report as receipt_report
from hermes_jev.reflex import config as reflex_config
from hermes_jev.reflex.laya import LayaClient, LayaError
from hermes_jev.reflex.laya_service import Handler, LayaServer
from hermes_jev.reflex.shadow import ShadowProvider
from hermes_jev.reflex.telemetry import report as shadow_report


class FakeAgent:
    def __init__(self):
        self.calls = []

    def system_one(self, state, questions):
        self.calls.append((state, questions))
        answers = {}
        for qid, q in questions.items():
            if q.get("type") == "choice":
                labels = list(q.get("criteria") or {})
                answers[qid] = {
                    "type": "choice",
                    "choice": labels[0],
                    "probabilities": {label: (0.9 if i == 0 else 0.1 / max(1, len(labels)-1)) for i, label in enumerate(labels)},
                    "confidence": 0.9,
                }
            elif q.get("type") == "score":
                answers[qid] = {"type": "score", "score": 1.25, "probabilities": {"0": 0.2, "1": 0.8}, "confidence": 0.8}
            else:
                answers[qid] = {"type": "noul", "noul": 0.75, "confidence": 0.75}
        return {"model": "ignored-agent-label", "answers": answers, "usage": {"input_tokens": 19, "output_tokens": 0}}


class StaticProvider:
    def __init__(self, choice="WATCH", *, provider="TypeSafe", transport="openrouter-decisions", live=True):
        self.choice = choice
        self.provider = provider
        self.transport = transport
        self.live = live

    def system_one(self, *, state, questions, model=None):
        labels = list(questions["decision"]["criteria"])
        choice = self.choice if self.choice in labels else labels[0]
        answer = {
            "type": "choice",
            "choice": choice,
            "probabilities": {x: (0.9 if x == choice else 0.1 / max(1, len(labels)-1)) for x in labels},
            "confidence": 0.9,
        }
        return type("R", (), {
            "model": model or "model",
            "answers": {"decision": answer},
            "usage": {"input_tokens": 10, "output_tokens": 0},
            "latency_ms": 1.0,
            "request_id": "req-primary" if self.live else "laya-local",
            "provider": self.provider,
            "transport": self.transport,
            "live_provider_call": self.live,
        })()


class LayaDev15BTests(unittest.TestCase):
    def setUp(self):
        self._old_home = os.environ.get("HERMES_HOME")
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["HERMES_HOME"] = self.tmp.name
        reflex_config.configure(backend="jev")

    def tearDown(self):
        reflex_config.configure(backend="jev")
        if self._old_home is None:
            os.environ.pop("HERMES_HOME", None)
        else:
            os.environ["HERMES_HOME"] = self._old_home
        self.tmp.cleanup()

    def _start_server(self, token="secret-token"):
        agent = FakeAgent()
        server = LayaServer(("127.0.0.1", 0), Handler, agent=agent, model_name="convaiinnovations/laya-typed-decisions", token=token)
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        thread.start()
        return agent, server, thread

    def test_real_http_sidecar_round_trip_with_fixed_model_and_auth(self):
        agent, server, _ = self._start_server()
        try:
            base = f"http://127.0.0.1:{server.server_address[1]}"
            client = LayaClient(base_url=base, token="secret-token", model="convaiinnovations/laya-typed-decisions")
            response = client.system_one(
                state={"goal": "stay on task"},
                questions={
                    "trajectory": {
                        "type": "choice",
                        "instructions": "What should the supervisor do?",
                        "criteria": {"WATCH": "continue", "REPLAN": "change plan"},
                    }
                },
            )
            self.assertEqual(response.provider, "Laya")
            self.assertEqual(response.transport, "laya-local-http")
            self.assertFalse(response.live_provider_call)
            self.assertEqual(response.model, "convaiinnovations/laya-typed-decisions")
            self.assertEqual(response.answers["trajectory"]["choice"], "WATCH")
            self.assertEqual(len(agent.calls), 1)
        finally:
            server.shutdown()
            server.server_close()

    def test_client_rejects_unexpected_sidecar_model(self):
        def transport(url, headers, body, timeout):
            raw = json.dumps({
                "model": "different-checkpoint",
                "answers": {"q": {"type": "noul", "noul": 0.5, "confidence": 0.5}},
                "usage": {},
            }).encode()
            return 200, raw, {}
        client = LayaClient(model="convaiinnovations/laya-typed-decisions", transport=transport)
        with self.assertRaises(LayaError):
            client.system_one(state="x", questions={"q": {"type": "noul", "instructions": "yes?"}})

    def test_sidecar_rejects_wrong_token(self):
        _, server, _ = self._start_server()
        try:
            base = f"http://127.0.0.1:{server.server_address[1]}"
            client = LayaClient(base_url=base, token="wrong")
            with self.assertRaises(LayaError):
                client.system_one(state="x", questions={"q": {"type": "noul", "instructions": "yes?"}})
        finally:
            server.shutdown()
            server.server_close()

    def test_client_rejects_plaintext_non_loopback(self):
        with self.assertRaises(LayaError):
            LayaClient(base_url="http://192.0.2.5:8765")

    def test_laya_decision_receipt_is_local_only_not_provider_call(self):
        def transport(url, headers, body, timeout):
            payload = json.loads(body)
            labels = list(payload["questions"]["decision"]["criteria"])
            raw = json.dumps({
                "id": "laya-test",
                "model": "convaiinnovations/laya-typed-decisions",
                "provider": "Laya",
                "transport": "laya-local-http",
                "answers": {
                    "decision": {
                        "type": "choice",
                        "choice": labels[0],
                        "probabilities": {labels[0]: 0.91, labels[1]: 0.09},
                        "confidence": 0.91,
                    }
                },
                "usage": {"input_tokens": 22, "output_tokens": 0},
            }).encode()
            return 200, raw, {}

        result = DecisionEngine(provider=LayaClient(transport=transport)).decide(
            state={"x": 1},
            instructions="Choose",
            choices=["WATCH", "REPLAN"],
            contract="dev15b/laya-local/v1",
        )
        payload = result.as_dict()
        self.assertEqual(payload["provider"], "Laya")
        self.assertEqual(payload["provenance_status"], "LOCAL_ONLY")
        self.assertFalse(payload["execution"]["live_provider_call"])
        self.assertEqual(receipt_report(recent_limit=0)["provider_calls"], 0)

    def test_default_decision_engine_uses_configured_laya_factory_end_to_end(self):
        agent, server, _ = self._start_server(token="")
        old = {k: os.environ.pop(k, None) for k in ("OPENROUTER_API_KEY", "TYPESAFE_API_KEY", "OPENCODE_API_KEY")}
        try:
            base = f"http://127.0.0.1:{server.server_address[1]}"
            reflex_config.configure(
                backend="laya",
                laya_base_url=base,
                laya_model="convaiinnovations/laya-typed-decisions",
                laya_token="",
            )
            result = DecisionEngine().decide(
                state={"failure": "same test failed twice"},
                instructions="Choose trajectory",
                choices=["WATCH", "REPLAN"],
                contract="dev15b/factory/v1",
            )
            self.assertEqual(result.provider, "Laya")
            self.assertEqual(result.value, "WATCH")
            self.assertFalse(result.live_provider_call)
            self.assertEqual(result.provenance_status, "LOCAL_ONLY")
            self.assertEqual(len(agent.calls), 1)
        finally:
            server.shutdown()
            server.server_close()
            for k, v in old.items():
                if v is not None:
                    os.environ[k] = v

    def test_laya_backend_does_not_require_jev_credentials(self):
        old = {k: os.environ.pop(k, None) for k in ("OPENROUTER_API_KEY", "TYPESAFE_API_KEY", "OPENCODE_API_KEY")}
        try:
            reflex_config.configure(backend="laya", laya_base_url="http://127.0.0.1:8765")
            provider = reflex_config.get_provider()
            self.assertIsInstance(provider, LayaClient)
        finally:
            for k, v in old.items():
                if v is not None:
                    os.environ[k] = v

    def test_shadow_returns_primary_and_logs_pair(self):
        path = Path(self.tmp.name) / "paired.jsonl"
        primary = StaticProvider("WATCH")
        shadow = StaticProvider("REPLAN", provider="Laya", transport="laya-local-http", live=False)
        provider = ShadowProvider(primary, shadow, path=path, asynchronous=False)
        response = provider.system_one(
            state={"goal": "x"},
            questions={"decision": {"type": "choice", "instructions": "x", "criteria": {"WATCH": "w", "REPLAN": "r"}}},
        )
        self.assertEqual(response.answers["decision"]["choice"], "WATCH")
        report = shadow_report(path, recent_limit=1)
        self.assertEqual(report["records"], 1)
        self.assertEqual(report["paired_answers"], 1)
        self.assertEqual(report["disagreements"], 1)
        self.assertEqual(report["shadow_errors"], 0)

    def test_shadow_failure_is_fail_open(self):
        class Broken:
            def system_one(self, **kwargs):
                raise RuntimeError("offline")

        path = Path(self.tmp.name) / "failopen.jsonl"
        provider = ShadowProvider(StaticProvider("WATCH"), Broken(), path=path, asynchronous=False)
        response = provider.system_one(
            state="x",
            questions={"decision": {"type": "choice", "instructions": "x", "criteria": {"WATCH": "w", "REPLAN": "r"}}},
        )
        self.assertEqual(response.answers["decision"]["choice"], "WATCH")
        report = shadow_report(path, recent_limit=1)
        self.assertEqual(report["shadow_errors"], 1)

    def test_config_report_redacts_sidecar_token(self):
        reflex_config.configure(backend="laya", laya_token="super-secret")
        report = reflex_config.report(recent_limit=0)
        self.assertNotIn("laya_token", report["settings"])
        self.assertTrue(report["settings"]["laya_token_configured"])
        self.assertNotIn("super-secret", json.dumps(report))


if __name__ == "__main__":
    unittest.main()
