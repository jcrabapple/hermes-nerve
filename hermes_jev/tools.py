"""Hermes-visible tool handlers."""

from __future__ import annotations

import json
from typing import Any

from .engine import DecisionEngine

_engine_factory = DecisionEngine


def _engine() -> DecisionEngine:
    return _engine_factory()


def jev_decide(args: dict, **kwargs) -> str:
    try:
        result = _engine().decide(
            state=args.get("state"),
            instructions=str(args.get("instructions") or "").strip(),
            choices=list(args.get("choices") or []),
            criteria=args.get("criteria") if isinstance(args.get("criteria"), dict) else None,
            contract=str(args.get("contract") or "decision/v1"),
        )
        return json.dumps({"ok": True, **result.as_dict()}, sort_keys=True)
    except Exception as exc:  # handlers must return errors, not raise through Hermes
        return json.dumps({"ok": False, "error": str(exc)})


def jev_rank(args: dict, **kwargs) -> str:
    try:
        items = args.get("items")
        if not isinstance(items, dict) or len(items) < 2:
            raise ValueError("items must be an object with at least two candidates")
        result = _engine().rank(
            state=args.get("state"),
            instructions=str(args.get("instructions") or "").strip(),
            items=items,
            contract=str(args.get("contract") or "rank/v1"),
        )
        return json.dumps({"ok": True, **result}, sort_keys=True)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)})


def jev_verify(args: dict, **kwargs) -> str:
    try:
        result = _engine().verify(
            state=args.get("state"),
            instructions=str(args.get("instructions") or "").strip(),
            contract=str(args.get("contract") or "verify/v1"),
        )
        return json.dumps({"ok": True, **result.as_dict()}, sort_keys=True)
    except Exception as exc:
        return json.dumps({"ok": False, "error": str(exc)})
