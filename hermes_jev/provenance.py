"""Canonical execution provenance attached to every Hermes-Jev result."""

from __future__ import annotations

from typing import Any

VERSION = "0.1.5.5"


def execution_provenance(*, live_provider_call: bool, transport: str = "openrouter-decisions") -> dict[str, Any]:
    return {
        "engine": "hermes-jev",
        "version": VERSION,
        "transport": transport,
        "live_provider_call": bool(live_provider_call),
    }


def attach(payload: dict[str, Any], *, live_provider_call: bool, transport: str = "openrouter-decisions") -> dict[str, Any]:
    out = dict(payload)
    out.setdefault("execution", execution_provenance(live_provider_call=live_provider_call, transport=transport))
    return out
