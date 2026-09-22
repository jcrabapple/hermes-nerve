from __future__ import annotations

import os
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from hermes_nerve import context, ledger
from hermes_nerve.context_engine import NerveContextEngine


def long_messages(count: int) -> list[dict]:
    messages: list[dict] = []
    for i in range(count):
        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": [{
                "id": f"c{i}",
                "type": "function",
                "function": {"name": "terminal", "arguments": '{"command":"git status --short"}'},
            }],
        })
        messages.append({
            "role": "tool",
            "tool_call_id": f"c{i}",
            "content": (f"tool output {i} " * 50),
        })
    messages.append({"role": "user", "content": "continue"})
    return messages


class Patch0212Tests(unittest.TestCase):
    def test_engine_bounds_49_and_851_candidates_to_48(self):
        for count in (49, 60, 851):
            e = NerveContextEngine(mode="apply", protect_first_n=0, protect_last_n=1, fallback_builtin=False)
            seen: list[int] = []
            original = context.curate_context

            def fake(**kwargs):
                seen.append(len(kwargs["items"]))
                return {
                    "decisions": [
                        {"id": item["id"], "action": "ANCHOR"}
                        for item in kwargs["items"]
                    ],
                    "curated_items": [
                        {"id": item["id"], "content": f"[JEV_CONTEXT_ANCHOR id={item['id']}]"}
                        for item in kwargs["items"]
                    ],
                    "stats": {},
                }

            context.curate_context = fake
            try:
                out = e.compress(long_messages(count))
            finally:
                context.curate_context = original

            self.assertEqual(seen, [48])
            self.assertEqual(e.get_status()["context_selection"]["selected_items"], 48)
            self.assertEqual(e.get_status()["context_selection"]["deferred_items"], count - 48)
            self.assertEqual(sum(
                1 for msg in out if isinstance(msg, dict)
                and msg.get("role") == "tool"
                and str(msg.get("content", "")).startswith("[JEV_CONTEXT_ANCHOR")
            ), 48)

    def test_exact_48_is_not_truncated(self):
        e = NerveContextEngine(mode="apply", protect_first_n=0, protect_last_n=1, fallback_builtin=False)
        seen: list[int] = []
        original = context.curate_context
        context.curate_context = lambda **kwargs: (
            seen.append(len(kwargs["items"])) or
            {"decisions": [], "curated_items": [], "stats": {}}
        )
        try:
            e.compress(long_messages(48))
        finally:
            context.curate_context = original
        self.assertEqual(seen, [48])
        self.assertEqual(e.get_status()["context_selection"]["deferred_items"], 0)

    def test_curation_failure_falls_back_and_never_raises(self):
        class Fallback:
            def compress(self, messages, **kwargs):
                return [messages[0], {"role": "assistant", "content": "fallback"}]

        e = NerveContextEngine(mode="apply", protect_first_n=0, protect_last_n=1, fallback_builtin=True)
        e._fallback = Fallback()
        original = context.curate_context

        def boom(**kwargs):
            raise ValueError("synthetic curation failure")

        context.curate_context = boom
        try:
            out = e.compress(long_messages(1))
        finally:
            context.curate_context = original

        self.assertEqual(out[-1]["content"], "fallback")
        status = e.get_status()
        self.assertEqual(status["fail_open"]["curation_fail_open_count"], 1)
        self.assertEqual(status["fail_open"]["last_failure_stage"], "jev-curation")

    def test_curation_and_fallback_failure_returns_original_messages(self):
        class BadFallback:
            def compress(self, *args, **kwargs):
                raise RuntimeError("fallback exploded")

        messages = long_messages(1)
        e = NerveContextEngine(mode="apply", protect_first_n=0, protect_last_n=1, fallback_builtin=True)
        e._fallback = BadFallback()
        original = context.curate_context
        context.curate_context = lambda **kwargs: (_ for _ in ()).throw(ValueError("curation exploded"))
        try:
            out = e.compress(messages)
        finally:
            context.curate_context = original
        self.assertIs(out, messages)
        status = e.get_status()
        self.assertEqual(status["fail_open"]["curation_fail_open_count"], 1)
        self.assertEqual(status["fail_open"]["fallback_fail_open_count"], 1)
        self.assertEqual(status["fail_open"]["last_failure_stage"], "fallback")

    def test_existing_anchor_is_not_recurated_or_nested(self):
        e = NerveContextEngine(mode="apply", protect_first_n=0, protect_last_n=1, fallback_builtin=False)
        original = context.curate_context
        batches: list[list[str]] = []

        def fake(**kwargs):
            batches.append([item["content"] for item in kwargs["items"]])
            return {
                "decisions": [{"id": item["id"], "action": "DROP"} for item in kwargs["items"]],
                "curated_items": [],
                "stats": {},
            }

        context.curate_context = fake
        try:
            first = e.compress(long_messages(2))
            second = e.compress(first)
        finally:
            context.curate_context = original

        self.assertEqual(len(batches), 1)
        self.assertEqual(len(batches[0]), 2)
        # The second pass has no raw candidate left: both tool results are anchors,
        # so curate_context must not be called again.
        anchors = [
            str(msg.get("content", ""))
            for msg in second if isinstance(msg, dict) and msg.get("role") == "tool"
        ]
        self.assertTrue(all(value.count("JEV_CONTEXT_ANCHOR") == 1 for value in anchors))

    def test_unrecoverable_evidence_consumes_no_jev_candidate_capacity(self):
        class ForbiddenFallback:
            def compress(self, *args, **kwargs):
                raise AssertionError("unrecoverable evidence must not reach generic fallback")

        e = NerveContextEngine(mode="apply", protect_first_n=0, protect_last_n=1, fallback_builtin=True)
        e._fallback = ForbiddenFallback()
        messages = [
            {"role": "assistant", "content": "", "tool_calls": [{
                "id": "c1", "type": "function",
                "function": {"name": "terminal", "arguments": '{"command":"rm -rf /tmp/nope"}'},
            }]},
            {"role": "tool", "tool_call_id": "c1", "content": "one-shot unrecoverable output"},
            {"role": "user", "content": "continue"},
        ]
        calls = 0
        original = context.curate_context

        def fake(**kwargs):
            nonlocal calls
            calls += 1
            return {"decisions": [], "curated_items": [], "stats": {}}

        context.curate_context = fake
        try:
            out = e.compress(messages)
        finally:
            context.curate_context = original

        self.assertIs(out, messages)
        self.assertEqual(calls, 0)
        self.assertEqual(e.get_status()["context_selection"]["skipped_unrecoverable_items"], 1)

    def test_shadow_proposals_do_not_count_as_applied_compaction(self):
        class FakeEngine:
            def assess(self, **kwargs):
                answers = {}
                for slot in range(4):
                    answers[f"needed_{slot}"] = {"noul": 0.0}
                    answers[f"exact_{slot}"] = {"noul": 0.0}
                    answers[f"superseded_{slot}"] = {"noul": 1.0}
                    answers[f"conflict_{slot}"] = {"noul": 0.0}
                return {"answers": answers, "latency_ms": 0, "usage": {}}

        with tempfile.TemporaryDirectory() as td:
            with mock.patch.dict(os.environ, {
                "HERMES_NERVE_CONTEXT_LEDGER": str(Path(td) / "ledger.jsonl"),
            }, clear=False):
                ledger.configure(enabled=True, detail="sanitized")
                context.curate_context(
                    goal="test",
                    items=[{
                        "id": "shadow-only", "kind": "tool_result",
                        "content": "x" * 1000, "recoverable": True, "metadata": {},
                    }],
                    preserve_tail=0, mode="shadow", engine_factory=FakeEngine,
                )
                report = ledger.report()
                self.assertEqual(report["shadow_plans"], 1)
                self.assertEqual(report["compacted_unique_evidence"], 0)
        ledger.configure(enabled=False, detail="sanitized")

    def test_shadow_failure_is_observable_and_fail_open(self):
        e = NerveContextEngine(
            mode="shadow", protect_first_n=0, protect_last_n=1,
            fallback_builtin=False, shadow_trigger_percent=0.2,
        )
        e.context_length = 1000
        e.last_prompt_tokens = 900
        original = context.curate_context
        context.curate_context = lambda **kwargs: (_ for _ in ()).throw(RuntimeError("shadow failure"))
        try:
            self.assertIsNone(e.on_turn_complete(long_messages(60)))
        finally:
            context.curate_context = original
        status = e.get_status()
        self.assertEqual(status["shadow"]["curation_attempts"], 1)
        self.assertEqual(status["shadow"]["curation_failures"], 1)
        self.assertEqual(status["context_selection"]["selected_items"], 48)
        self.assertEqual(status["context_selection"]["deferred_items"], 12)

    def test_public_48_item_curation_fanout_is_at_most_12_requests(self):
        class FakeEngine:
            calls = 0

            def assess(self, **kwargs):
                FakeEngine.calls += 1
                answers = {}
                for slot in range(4):
                    answers[f"needed_{slot}"] = {"noul": 0.5}
                    answers[f"exact_{slot}"] = {"noul": 0.5}
                    answers[f"superseded_{slot}"] = {"noul": 0.5}
                    answers[f"conflict_{slot}"] = {"noul": 0.5}
                return {
                    "answers": answers, "latency_ms": 0, "usage": {},
                    "request_id": "", "model": "fake", "provider": "fake",
                }

        items = [
            {
                "id": f"e{i}", "kind": "tool_result", "content": f"data {i}",
                "recoverable": True, "metadata": {},
            }
            for i in range(48)
        ]
        context.curate_context(
            goal="test", items=items, preserve_tail=0,
            mode="shadow", engine_factory=FakeEngine,
        )
        self.assertEqual(FakeEngine.calls, 12)


if __name__ == "__main__":
    unittest.main()
