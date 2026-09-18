#!/usr/bin/env python3
"""Print combined Hermes-Jev decision + context telemetry for the active/inferred profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hermes_jev import ledger, receipts, nervous
from hermes_jev.paths import default_hermes_root, report_home


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", help="Named Hermes profile, e.g. muna")
    parser.add_argument("--recent", type=int, default=8, help="Recent receipts to include (0-50)")
    args = parser.parse_args()
    home = default_hermes_root() / "profiles" / args.profile if args.profile else report_home(ROOT)
    payload = {
        "resolved_hermes_home": str(home),
        "receipts": receipts.report(home / "jev" / "receipts.jsonl", recent_limit=args.recent),
        "context": ledger.report(home / "jev" / "context-ledger.jsonl"),
        "nervous": nervous.report(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
