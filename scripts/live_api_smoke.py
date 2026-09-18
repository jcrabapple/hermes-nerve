#!/usr/bin/env python3
"""Opt-in live Jev smoke test through the selected provider.

Set HERMES_JEV_PROVIDER=openrouter (default) with OPENROUTER_API_KEY, or HERMES_JEV_PROVIDER=typesafe with TYPESAFE_API_KEY. It sends only synthetic test state and prints the
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

from hermes_jev.engine import DecisionEngine


def main() -> int:
    provider = os.getenv("HERMES_JEV_PROVIDER", "openrouter").strip().lower()
    key_name = "TYPESAFE_API_KEY" if provider in {"typesafe", "direct", "typesafe-direct"} else "OPENROUTER_API_KEY"
    if not os.getenv(key_name, "").strip():
        print(f"{key_name} is not set for HERMES_JEV_PROVIDER={provider}; live test skipped.", file=sys.stderr)
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
