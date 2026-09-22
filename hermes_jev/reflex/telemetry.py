"""Privacy-minimized paired Jev/Laya shadow telemetry."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..jsonl import append_jsonl, read_jsonl
from ..paths import report_home


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def default_path() -> Path:
    return report_home() / "reflex" / "shadow.jsonl"


def answer_summary(answers: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for qid, raw in (answers or {}).items():
        if not isinstance(raw, dict):
            continue
        qtype = str(raw.get("type") or "")
        if qtype == "choice":
            value = raw.get("choice")
        elif qtype == "score":
            value = raw.get("score")
        elif qtype == "noul":
            value = raw.get("noul")
        else:
            value = raw.get("value")
        out[str(qid)] = {
            "type": qtype,
            "value": value,
            "confidence": raw.get("confidence"),
            "probabilities": raw.get("probabilities") if isinstance(raw.get("probabilities"), dict) else None,
        }
    return out


def append_shadow_record(
    *,
    path: Path | None,
    state: Any,
    questions: dict[str, Any],
    primary: Any,
    shadow: Any | None = None,
    shadow_error: str = "",
) -> None:
    primary_answers = answer_summary(getattr(primary, "answers", {}) or {})
    shadow_answers = answer_summary(getattr(shadow, "answers", {}) or {}) if shadow is not None else {}
    compared = sorted(set(primary_answers) | set(shadow_answers))
    agreements: dict[str, bool] = {}
    for qid in compared:
        if qid in primary_answers and qid in shadow_answers:
            agreements[qid] = primary_answers[qid].get("value") == shadow_answers[qid].get("value")
    append_jsonl(
        path or default_path(),
        {
            "schema": "hermes-reflex-shadow/v1",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "state_sha256": _canonical_hash(state),
            "questions_sha256": _canonical_hash(questions),
            "question_ids": sorted(str(k) for k in questions),
            "primary": {
                "provider": str(getattr(primary, "provider", "") or ""),
                "model": str(getattr(primary, "model", "") or ""),
                "transport": str(getattr(primary, "transport", "") or ""),
                "latency_ms": float(getattr(primary, "latency_ms", 0.0) or 0.0),
                "answers": primary_answers,
            },
            "shadow": {
                "provider": str(getattr(shadow, "provider", "") or "") if shadow is not None else "",
                "model": str(getattr(shadow, "model", "") or "") if shadow is not None else "",
                "transport": str(getattr(shadow, "transport", "") or "") if shadow is not None else "",
                "latency_ms": float(getattr(shadow, "latency_ms", 0.0) or 0.0) if shadow is not None else 0.0,
                "answers": shadow_answers,
                "error": str(shadow_error or ""),
            },
            "agreements": agreements,
        },
    )


def report(path: Path | None = None, *, recent_limit: int = 5) -> dict[str, Any]:
    selected = path or default_path()
    rows = read_jsonl(selected)
    paired = 0
    agreed = 0
    disagreed = 0
    shadow_errors = 0
    per_question: dict[str, dict[str, int]] = {}
    for row in rows:
        shadow = row.get("shadow") if isinstance(row.get("shadow"), dict) else {}
        if shadow.get("error"):
            shadow_errors += 1
        agreements = row.get("agreements") if isinstance(row.get("agreements"), dict) else {}
        for qid, value in agreements.items():
            paired += 1
            bucket = per_question.setdefault(str(qid), {"paired": 0, "agree": 0, "disagree": 0})
            bucket["paired"] += 1
            if bool(value):
                agreed += 1
                bucket["agree"] += 1
            else:
                disagreed += 1
                bucket["disagree"] += 1
    return {
        "path": str(selected),
        "records": len(rows),
        "paired_answers": paired,
        "agreements": agreed,
        "disagreements": disagreed,
        "agreement_rate": round(agreed / paired, 6) if paired else None,
        "shadow_errors": shadow_errors,
        "per_question": per_question,
        "recent": rows[-max(0, int(recent_limit)) :] if recent_limit else [],
    }
