"""Hermes-visible tool handlers."""

from __future__ import annotations

import json

from .context import curate_context
from .engine import DecisionEngine
from . import gate, ledger, lifecycle, receipts
from .provenance import execution_provenance

_engine_factory = DecisionEngine


def _engine() -> DecisionEngine:
    return _engine_factory()


def _ok(payload: dict) -> str:
    body = {"ok": True, **payload}
    body.setdefault("execution", execution_provenance(live_provider_call=bool(body.get("request_id") or body.get("requests"))))
    return json.dumps(body, sort_keys=True)


def _error(exc: Exception) -> str:
    return json.dumps({
        "ok": False,
        "error": str(exc),
        "execution": execution_provenance(live_provider_call=False),
    }, sort_keys=True)


def jev_decide(args: dict, **kwargs) -> str:
    try:
        result = _engine().decide(
            state=args.get("state"),
            instructions=str(args.get("instructions") or "").strip(),
            choices=list(args.get("choices") or []),
            criteria=args.get("criteria") if isinstance(args.get("criteria"), dict) else None,
            contract=str(args.get("contract") or "decision/v1"),
        )
        return _ok(result.as_dict())
    except Exception as exc:  # handlers must return errors, not raise through Hermes
        return _error(exc)


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
        return _ok(result)
    except Exception as exc:
        return _error(exc)


def jev_verify(args: dict, **kwargs) -> str:
    try:
        result = _engine().verify(
            state=args.get("state"),
            instructions=str(args.get("instructions") or "").strip(),
            contract=str(args.get("contract") or "verify/v1"),
        )
        lifecycle.record_verification(
            value=result.value, contract=result.contract, confidence=result.confidence, probabilities=result.probabilities
        )
        return _ok(result.as_dict())
    except Exception as exc:
        return _error(exc)


def jev_assess(args: dict, **kwargs) -> str:
    try:
        questions = args.get("questions")
        if not isinstance(questions, dict):
            raise ValueError("questions must be an object")
        result = _engine().assess(
            state=args.get("state"),
            questions=questions,
            contract=str(args.get("contract") or "assess/v1"),
        )
        return _ok(result)
    except Exception as exc:
        return _error(exc)


def jev_context_curate(args: dict, **kwargs) -> str:
    try:
        result = curate_context(
            goal=str(args.get("goal") or "").strip(),
            items=args.get("items"),
            preserve_tail=args.get("preserve_tail"),
            min_confidence=args.get("min_confidence"),
            preview_chars=args.get("preview_chars"),
            stub_chars=args.get("stub_chars"),
            anchor_chars=args.get("anchor_chars"),
            mode=args.get("mode"),
            policy=args.get("policy") if isinstance(args.get("policy"), dict) else None,
            contract=str(args.get("contract") or "context-curation/v2"),
        )
        return _ok(result)
    except Exception as exc:
        return _error(exc)


def jev_context_rehydrate(args: dict, **kwargs) -> str:
    try:
        result = ledger.rehydrate(str(args.get("evidence_id") or ""))
        return _ok({
            "contract": str(args.get("contract") or "context-rehydrate/v1"),
            "rehydrated": result,
            "ledger": ledger.stats(),
            "execution": execution_provenance(live_provider_call=False, transport="local-evidence-ledger"),
        })
    except Exception as exc:
        return _error(exc)


def jev_stats(args: dict, **kwargs) -> str:
    try:
        recent_limit = args.get("recent_limit", 8)
        try:
            recent_limit = max(0, min(50, int(recent_limit)))
        except (TypeError, ValueError):
            recent_limit = 8
        return _ok({
            "contract": "stats/v1",
            "receipts": receipts.report(recent_limit=recent_limit),
            "gate": gate.report(recent_limit=recent_limit),
            "context": ledger.report(),
            "execution": execution_provenance(live_provider_call=False, transport="local-telemetry"),
        })
    except Exception as exc:
        return _error(exc)
