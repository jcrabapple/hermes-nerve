#!/usr/bin/env python3
"""Print profile-aware Nerve context shadow/rehydration telemetry as JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hermes_nerve import ledger
from hermes_nerve.paths import default_hermes_root, report_home


def _profile_home(name: str) -> Path:
    return default_hermes_root() / "profiles" / name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", help="Read one named Hermes profile, e.g. muna")
    parser.add_argument("--all-profiles", action="store_true", help="Report every discovered ledger under the Hermes root")
    args = parser.parse_args()

    if args.all_profiles:
        root = default_hermes_root()
        paths = [root / "jev" / "context-ledger.jsonl"]
        profiles = root / "profiles"
        if profiles.is_dir():
            paths.extend(sorted(profiles.glob("*/jev/context-ledger.jsonl")))
        reports = [ledger.report(path) for path in paths if path.exists()]
        print(json.dumps({"reports": reports, "count": len(reports)}, indent=2, sort_keys=True))
        return 0

    home = _profile_home(args.profile) if args.profile else report_home(ROOT)
    path = home / "jev" / "context-ledger.jsonl"
    payload = ledger.report(path)
    payload["resolved_hermes_home"] = str(home)
    payload["resolution"] = "explicit-profile" if args.profile else "environment-or-plugin-path"
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
