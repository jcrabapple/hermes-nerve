#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "benchmarks" / "dev6_event_delivery" / "fixture"

proc = subprocess.run(
    [sys.executable, "-m", "pytest", "tests", "-q"],
    cwd=FIXTURE,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
out = proc.stdout
m = re.search(r"(\d+) failed, (\d+) passed", out)
if proc.returncode == 0 or not m:
    print(out)
    raise SystemExit("benchmark baseline no longer fails in the expected measurable way")
failed, passed = map(int, m.groups())
if (failed, passed) != (8, 5):
    print(out)
    raise SystemExit(f"benchmark drift: expected 8 failed / 5 passed, got {failed} failed / {passed} passed")
print(f"PASS dev6 benchmark baseline failed={failed} passed={passed}")