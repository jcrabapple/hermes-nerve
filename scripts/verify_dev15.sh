#!/usr/bin/env bash
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

python3 -m compileall -q .
python3 scripts/verify_release.py
python3 scripts/verify_dev6_benchmark.py

# The project has historically shown intermittent pytest shutdown hangs when
# third-party pytest plugins autoload. Dev15 verification disables unrelated
# external pytest plugins and runs the complete in-repo suite in one clean pass.
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q

printf 'DEV15_VERIFY=PASS\n'
