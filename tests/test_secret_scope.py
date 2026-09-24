"""Regression tests for #18: provider keys must resolve through the Hermes secret scope.

Hermes keeps ~/.hermes/.env values in a per-profile secret scope, not os.environ, so a bare
os.getenv finds nothing in gateway turns and cron workers and the pre-tool gate never gets
a verdict.
"""
import os
import sys
import types
import unittest
from unittest.mock import patch

from hermes_nerve import client


class _Scope:
    """Stand-in for agent.secret_scope installed under sys.modules."""

    def __init__(self, values=None, error=None):
        self.values = values or {}
        self.error = error
        self.calls = []

    def module(self):
        mod = types.ModuleType("agent.secret_scope")

        def get_secret(name, default=""):
            self.calls.append(name)
            if self.error:
                raise self.error
            return self.values.get(name, default)

        mod.get_secret = get_secret
        pkg = types.ModuleType("agent")
        pkg.secret_scope = mod
        return {"agent": pkg, "agent.secret_scope": mod}


def _no_env():
    return {k: v for k, v in os.environ.items()
            if k not in {"OPENROUTER_API_KEY", "TYPESAFE_API_KEY", "OPENCODE_API_KEY"}}


class SecretScopeTests(unittest.TestCase):
    def test_key_found_in_hermes_scope_but_not_os_environ(self):
        scope = _Scope({"OPENROUTER_API_KEY": "sk-or-scope"})
        with patch.dict(os.environ, _no_env(), clear=True), patch.dict(sys.modules, scope.module()):
            c = client.JevClient(provider="openrouter")
        self.assertEqual(c.api_key, "sk-or-scope")
        self.assertIn("OPENROUTER_API_KEY", scope.calls)

    def test_each_provider_uses_scope(self):
        values = {"OPENROUTER_API_KEY": "a", "TYPESAFE_API_KEY": "b", "OPENCODE_API_KEY": "c"}
        with patch.dict(os.environ, _no_env(), clear=True), patch.dict(sys.modules, _Scope(values).module()):
            self.assertEqual(client.JevClient(provider="openrouter").api_key, "a")
            self.assertEqual(client.JevClient(provider="typesafe").api_key, "b")
            self.assertEqual(client.JevClient(provider="opencode").api_key, "c")

    def test_scope_failing_closed_means_no_key_not_env_fallback(self):
        # Multiplexed Hermes with no profile bound: get_secret raises. Must not borrow os.environ.
        scope = _Scope(error=RuntimeError("no secret scope bound"))
        env = dict(_no_env(), OPENROUTER_API_KEY="sk-other-profile")
        with patch.dict(os.environ, env, clear=True), patch.dict(sys.modules, scope.module()):
            with self.assertRaises(client.JevError):
                client.JevClient(provider="openrouter")

    def test_outside_hermes_falls_back_to_process_env(self):
        with patch.dict(os.environ, dict(_no_env(), OPENROUTER_API_KEY=" sk-env "), clear=True), \
                patch.dict(sys.modules, {"agent": None, "agent.secret_scope": None}):
            self.assertEqual(client.JevClient(provider="openrouter").api_key, "sk-env")

    def test_explicit_api_key_wins(self):
        with patch.dict(sys.modules, _Scope({"OPENROUTER_API_KEY": "scope"}).module()):
            self.assertEqual(client.JevClient(provider="openrouter", api_key="explicit").api_key, "explicit")


if __name__ == "__main__":
    unittest.main()
