#!/usr/bin/env python3
"""Opt-in live Jev smoke test through the selected Jev provider.

Supports HERMES_JEV_PROVIDER=openrouter, typesafe, or opencode. It sends only synthetic test state and prints the
returned decision metadata; it never reads local Hermes state or receipts.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hermes_jev.client import PROVIDER_API_KEY_ENV
from hermes_jev.engine import DecisionEngine


def main() -> int:
    provider = os.getenv("HERMES_JEV_PROVIDER", "openrouter").strip().lower() or "openrouter"
    required = PROVIDER_API_KEY_ENV.get(provider)
    if required is None:
        print("HERMES_JEV_PROVIDER must be openrouter, typesafe, or opencode.", file=sys.stderr)
        return 2
    if not os.getenv(required, "").strip():
        print(f"{required} is not set; live API smoke skipped.", file=sys.stderr)
        return 2

    result = DecisionEngine().decide(
        state={
            "task": "Choose the appropriate execution target for a synthetic CUDA workload.",
            "requires_cuda": True,
            "targets": {
                "cpu_host": {"gpu": False},
                "gpu_host": {"gpu": True},
            },
        },
        instructions="Choose the execution target that satisfies the stated hardware requirement.",
        choices=["cpu_host", "gpu_host", "ask_human"],
        criteria={
            "cpu_host": "Choose only if the workload does not require CUDA.",
            "gpu_host": "Choose when CUDA is required and this target provides a GPU.",
            "ask_human": "Choose if the state is insufficient or materially ambiguous.",
        },
        contract="live-smoke/v1",
    )
    print(json.dumps({"ok": True, **result.as_dict()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
