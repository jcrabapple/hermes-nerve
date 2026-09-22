import json
import os
import unittest
from unittest.mock import patch

from hermes_nerve import client


class OpenCodeProviderTests(unittest.TestCase):
    def setUp(self):
        client._configured_provider = None
        client._configured_base_url = None
        client._configured_model = None
        client._configured_typesafe_model = None
        client._configured_opencode_model = None
        client._configured_timeout = None

    def test_opencode_wire_contract(self):
        captured = {}
        def transport(url, headers, body, timeout):
            captured.update(url=url, headers=headers, body=json.loads(body), timeout=timeout)
            return 200, json.dumps({
                "id": "zen-req-1", "provider": "TypeSafe", "model": "jev-1.13",
                "answers": {"q": {"type": "choice", "choice": "A", "confidence": 0.9, "probabilities": {"A": 0.9, "B": 0.1}}},
                "usage": {"input_tokens": 3, "output_tokens": 1, "cost": 0},
            }).encode(), {}
        c = client.JevClient(provider="opencode", api_key="zen-secret", transport=transport)
        r = c.system_one(state={"x": 1}, questions={"q": {"type": "choice", "criteria": {"A": None, "B": None}}})
        self.assertEqual(captured["url"], "https://opencode.ai/zen/v1/systemone")
        self.assertEqual(captured["headers"]["Authorization"], "Bearer zen-secret")
        self.assertEqual(captured["body"]["model"], "jev-1.13")
        self.assertEqual(r.transport, "opencode-zen-system-one")
        self.assertEqual(r.request_id, "zen-req-1")

    def test_selected_provider_only_requires_opencode_key(self):
        with patch.dict(os.environ, {"OPENCODE_API_KEY": "zen"}, clear=True):
            c = client.JevClient(provider="opencode")
            self.assertEqual(c.api_key, "zen")
            self.assertEqual(c.model, client.OPENCODE_MODEL)

    def test_other_provider_keys_do_not_satisfy_opencode(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "or", "TYPESAFE_API_KEY": "ts"}, clear=True):
            with self.assertRaisesRegex(client.JevError, "OPENCODE_API_KEY"):
                client.JevClient(provider="opencode")

    def test_paid_model_selection(self):
        client.configure(provider="opencode", opencode_model=client.OPENCODE_MODEL)
        with patch.dict(os.environ, {"OPENCODE_API_KEY": "zen"}, clear=True):
            self.assertEqual(client.JevClient().model, "jev-1.13")

    def test_free_model_is_rejected_for_hermes(self):
        with patch.dict(os.environ, {"OPENCODE_API_KEY": "zen"}, clear=True):
            with self.assertRaisesRegex(client.JevError, "supports only paid model 'jev-1.13'"):
                client.JevClient(provider="opencode", model="jev-1.13-free")

    def test_provider_credential_map_is_complete(self):
        self.assertEqual(client.PROVIDER_API_KEY_ENV, {
            "openrouter": "OPENROUTER_API_KEY",
            "typesafe": "TYPESAFE_API_KEY",
            "opencode": "OPENCODE_API_KEY",
        })
        self.assertEqual(set(client.SUPPORTED_PROVIDERS), set(client.PROVIDER_API_KEY_ENV))

    def test_existing_providers_remain_accepted(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "or", "TYPESAFE_API_KEY": "ts"}, clear=True):
            self.assertEqual(client.JevClient(provider="openrouter").provider_kind, "openrouter")
            self.assertEqual(client.JevClient(provider="typesafe").provider_kind, "typesafe")


if __name__ == "__main__":
    unittest.main()
