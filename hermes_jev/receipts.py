"""Decision receipts: JSONL, privacy-minimized by default."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .privacy import canonical_hash

_configured_detail: str | None = None


def configure(*, detail: Any = None) -> None:
    """Apply the Hermes plugin ``receipt_detail`` setting."""
    global _configured_detail
    value = str(detail if detail is not None else "hash").strip().lower()
    _configured_detail = value if value in {"hash", "sanitized"} else "hash"


def receipt_detail() -> str:
    if _configured_detail is not None:
        return _configured_detail
    value = os.getenv("HERMES_JEV_RECEIPT_DETAIL", "hash").strip().lower()
    return value if value in {"hash", "sanitized"} else "hash"


def receipt_path() -> Path:
    explicit = os.getenv("HERMES_JEV_RECEIPTS")
    if explicit:
        return Path(explicit).expanduser()
    home = Path(os.getenv("HERMES_HOME") or Path.home() / ".hermes")
    return home / "jev" / "receipts.jsonl"


def write_receipt(*, contract: str, state: Any, result: dict[str, Any], model: str, latency_ms: float) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema": "hermes-jev-receipt/v1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "contract": contract,
        "state_sha256": canonical_hash(state),
        "model": model,
        "latency_ms": round(latency_ms, 3),
        "result": result,
    }
    if receipt_detail() == "sanitized":
        record["state"] = state
    path = receipt_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False, default=str) + "\n")
    return record
