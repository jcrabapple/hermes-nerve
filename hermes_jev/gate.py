"""Opt-in Hermes pre_tool_call control gate."""

from __future__ import annotations

import os
from typing import Any, Callable

from .engine import DecisionEngine, DecisionResult
from .privacy import redact

_SKIP_PREFIXES = ("jev_",)
_configured_mode: str | None = None
_configured_min_confidence: float | None = None


def configure(*, mode: Any = None, min_confidence: Any = None) -> None:
    """Apply Hermes plugin settings captured during ``register(ctx)``.

    Environment variables remain a backwards-compatible fallback when the
    module is used directly outside Hermes.
    """
    global _configured_mode, _configured_min_confidence

    raw_mode = str(mode if mode is not None else "off").strip().lower()
    _configured_mode = raw_mode if raw_mode in {"off", "advisory", "enforce"} else "off"
    try:
        threshold = float(0.80 if min_confidence is None else min_confidence)
    except (TypeError, ValueError):
        threshold = 0.80
    _configured_min_confidence = min(1.0, max(0.0, threshold))


def gate_mode() -> str:
    if _configured_mode is not None:
        return _configured_mode
    mode = os.getenv("HERMES_JEV_GATE_MODE", "off").strip().lower()
    return mode if mode in {"off", "advisory", "enforce"} else "off"


def minimum_confidence() -> float:
    if _configured_min_confidence is not None:
        return _configured_min_confidence
    try:
        value = float(os.getenv("HERMES_JEV_MIN_CONFIDENCE", "0.80"))
    except ValueError:
        value = 0.80
    return min(1.0, max(0.0, value))


def evaluate_tool_call(
    *,
    tool_name: str,
    args: dict[str, Any],
    task_id: str | None,
    engine_factory: Callable[[], DecisionEngine] = DecisionEngine,
) -> DecisionResult | None:
    if gate_mode() == "off" or tool_name.startswith(_SKIP_PREFIXES):
        return None
    state = {"tool_name": tool_name, "arguments": redact(args), "task_id": task_id or ""}
    return engine_factory().decide(
        state=state,
        instructions=(
            "Choose how Hermes should handle this proposed tool call. ALLOW means routine and low-risk. "
            "APPROVAL means a human should explicitly approve before execution. BLOCK means the action is "
            "clearly destructive, credential-exfiltrating, privilege-escalating, or inconsistent with a safe agent action."
        ),
        choices=["ALLOW", "APPROVAL", "BLOCK"],
        criteria={
            "ALLOW": "Routine, bounded, reversible, and consistent with normal agent work.",
            "APPROVAL": "Consequential, ambiguous, externally visible, hard to reverse, or confidence is insufficient.",
            "BLOCK": "Clearly dangerous/destructive, credential theft/exfiltration, or unacceptable blast radius.",
        },
        contract="hermes/pre-tool-gate/v1",
    )


def pre_tool_call(tool_name: str, args: dict, task_id: str | None = None, **kwargs):
    mode = gate_mode()
    if mode == "off":
        return None
    try:
        result = evaluate_tool_call(tool_name=tool_name, args=args, task_id=task_id)
    except Exception:
        # A remote classifier must never silently become a single point of failure.
        # Advisory fails open; enforce fails toward HUMAN approval, not execution or hard block.
        if mode == "enforce":
            return {
                "action": "approve",
                "message": "Hermes-Jev could not obtain a decision; human approval is required (fail-to-human).",
                "rule_key": "jev:provider-unavailable",
            }
        return None
    if result is None or mode == "advisory":
        return None

    min_conf = minimum_confidence()
    if result.confidence < min_conf:
        return {
            "action": "approve",
            "message": f"Hermes-Jev confidence {result.confidence:.3f} is below {min_conf:.3f}; human approval required.",
            "rule_key": "jev:low-confidence",
        }
    if result.value == "BLOCK":
        return {
            "action": "block",
            "message": f"Blocked by Hermes-Jev ({result.confidence:.3f} confidence).",
        }
    if result.value == "APPROVAL":
        return {
            "action": "approve",
            "message": f"Hermes-Jev requests human approval ({result.confidence:.3f} confidence).",
            "rule_key": f"jev:{tool_name}",
        }
    return None
