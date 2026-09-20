#!/usr/bin/env python3
"""Live synthetic regression suite for Hermes-Jev through the selected Jev provider.

Supports HERMES_JEV_PROVIDER=openrouter, typesafe, or opencode. No local project data is sent. The script exercises
all public decision modes plus the advisory-gate classifier and prints a compact
cost/latency summary.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hermes_jev import gate, ledger
from hermes_jev.client import PROVIDER_API_KEY_ENV
from hermes_jev.context import curate_context
from hermes_jev.engine import DecisionEngine


def _cost(result: dict) -> float | None:
    usage = result.get("usage")
    if not isinstance(usage, dict) or "cost" not in usage or usage.get("cost") in {None, ""}:
        return None
    try:
        return float(usage["cost"])
    except (TypeError, ValueError):
        return None


def main() -> int:
    provider = os.getenv("HERMES_JEV_PROVIDER", "openrouter").strip().lower() or "openrouter"
    required = PROVIDER_API_KEY_ENV.get(provider)
    if required is None:
        print("HERMES_JEV_PROVIDER must be openrouter, typesafe, or opencode.", file=sys.stderr)
        return 2
    if not os.getenv(required, "").strip():
        print(f"{required} is not set; live suite skipped.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as td:
        os.environ["HERMES_JEV_RECEIPTS"] = str(Path(td) / "receipts.jsonl")
        os.environ["HERMES_JEV_CONTEXT_LEDGER"] = str(Path(td) / "context-ledger.jsonl")
        ledger.configure(enabled=True, detail="sanitized")
        e = DecisionEngine()
        outputs: dict[str, dict] = {}

        outputs["decide"] = e.decide(
            state={"task": "CUDA benchmark", "cpu": {"gpu": False}, "gpu": {"gpu": True}},
            instructions="Choose the worker that satisfies the CUDA requirement.",
            choices=["cpu", "gpu", "ask_human"],
            criteria={"cpu": "No GPU", "gpu": "NVIDIA GPU available", "ask_human": "State is insufficient"},
            contract="live-suite/decide-v1",
        ).as_dict()

        outputs["rank"] = e.rank(
            state={"task": "Compile a large CUDA project", "priority": "speed"},
            instructions="Rank the candidates for this workload, preferring capability and lower expected completion time.",
            items={
                "cpu-small": "8 CPU cores, no GPU",
                "gpu-local": "RTX 4060, local network",
                "gpu-cloud": "A10 GPU, higher startup latency",
            },
            contract="live-suite/rank-v1",
        )

        outputs["verify"] = e.verify(
            state={"goal": "Run unit tests", "exit_code": 0, "tests": {"passed": 42, "failed": 0}, "working_tree_clean": True},
            instructions="PASS only if the supplied evidence demonstrates the unit-test goal completed successfully.",
            contract="live-suite/verify-v1",
        ).as_dict()

        outputs["assess"] = e.assess(
            state={"message": "Production checkout has failed for every customer for 20 minutes."},
            questions={
                "urgent": {
                    "type": "noul",
                    "instructions": "Does this require urgent response?",
                    "criteria": {"true": "Active material customer impact", "false": "No immediate customer impact"},
                },
                "owner": {
                    "type": "choice",
                    "instructions": "Which team should own first response?",
                    "criteria": {"payments": "Checkout/payment failures", "sales": "Sales inquiry", "docs": "Documentation issue"},
                },
                "severity": {
                    "type": "score",
                    "instructions": "Score operational severity.",
                    "criteria": ["low", "medium", "high", "critical"],
                },
            },
            contract="live-suite/assess-v1",
        )

        outputs["context_curate"] = curate_context(
            goal="Debug the renderer test while preserving the exact failure and user constraints.",
            items=[
                {"id": "constraint", "kind": "user_text", "content": "Do not edit generated files."},
                {"id": "old-read", "kind": "tool_result", "content": "Earlier source listing: alpha beta gamma " * 30, "recoverable": True},
                {"id": "failure", "kind": "tool_result", "content": "AssertionError: expected 4 nodes, got 3 at tests/test_renderer.py:88", "recoverable": False},
                {"id": "status", "kind": "tool_result", "content": "git status --short returned clean", "recoverable": True},
                {"id": "recent", "kind": "observation", "content": "The current branch is fix/renderer-cardinality."},
            ],
            preserve_tail=1,
            mode="shadow",
            contract="live-suite/context-curation-v2",
        )

        gate.configure(mode="advisory", min_confidence=0.80)
        gate_result = gate.evaluate_tool_call(
            tool_name="terminal",
            args={"command": "git status --short"},
            task_id="live-suite",
        )
        outputs["advisory_gate"] = gate_result.as_dict() if gate_result else {"skipped": True}

        cost_observations = [_cost(v) for v in outputs.values() if isinstance(v, dict) and isinstance(v.get("usage"), dict)]
        reported_costs = [value for value in cost_observations if value is not None]
        missing_cost_cases = len(cost_observations) - len(reported_costs)
        latencies = [float(v.get("latency_ms") or 0.0) for v in outputs.values() if isinstance(v, dict)]
        summary = {
            "ok": True,
            "cases": outputs,
            "total_cost": None if missing_cost_cases else round(sum(reported_costs), 8),
            "provider_reported_cost": round(sum(reported_costs), 8),
            "provider_cost_reported_cases": len(reported_costs),
            "provider_cost_missing_cases": missing_cost_cases,
            "total_latency_ms": round(sum(latencies), 3),
            "receipt_count": len(Path(os.environ["HERMES_JEV_RECEIPTS"]).read_text().splitlines()),
            "context_ledger": ledger.report(),
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
