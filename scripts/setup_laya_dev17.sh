#!/usr/bin/env bash
set -euo pipefail

VENV="${LAYA_VENV:-$HOME/.venvs/hermes-reflex-laya}"
MODEL="${HERMES_REFLEX_LAYA_MODEL:-convaiinnovations/laya-typed-decisions}"
PORT="${HERMES_REFLEX_LAYA_PORT:-8765}"
DEVICE="${HERMES_REFLEX_LAYA_DEVICE:-cuda}"
PYTHON_SPEC="${LAYA_PYTHON_SPEC:-3.12}"
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
UV="${UV_BIN:-}"

have_working_venv() {
  local py="${PYTHON:-python3}" probe
  probe=$(mktemp -d)
  if "$py" -m venv "$probe" >/dev/null 2>&1 && [ -x "$probe/bin/python" ]; then
    rm -rf -- "$probe"
    printf '%s\n' "$py"
    return 0
  fi
  rm -rf -- "$probe"
  return 1
}

ensure_uv() {
  if [ -n "$UV" ] && [ -x "$UV" ]; then return 0; fi
  for candidate in "$HOME/.local/bin/uv" "$(command -v uv 2>/dev/null || true)"; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then UV="$candidate"; return 0; fi
  done
  echo "ERROR: Python venv support is unavailable and uv was not found." >&2
  echo "Install uv using your platform/package-manager workflow, or set UV_BIN to a trusted uv executable." >&2
  echo "Refusing to download and execute a remote installer automatically." >&2
  exit 20
}

rm -rf -- "$VENV"
if SYSTEM_PYTHON=$(have_working_venv); then
  "$SYSTEM_PYTHON" -m venv "$VENV"
  "$VENV/bin/python" -m pip install --upgrade pip
  "$VENV/bin/pip" install 'laya==0.3.3'
  INSTALLER="venv:$SYSTEM_PYTHON"
else
  ensure_uv
  "$UV" python install "$PYTHON_SPEC"
  "$UV" venv --python "$PYTHON_SPEC" "$VENV"
  "$UV" pip install --python "$VENV/bin/python" 'laya==0.3.3'
  INSTALLER="uv:$PYTHON_SPEC"
fi

"$VENV/bin/python" - <<'PY'
import laya, sys
print(f"LAYA_IMPORT=PASS python={sys.version.split()[0]} module={laya.__file__}")
PY

echo "LAYA_SETUP=PASS venv=$VENV model=$MODEL installer=$INSTALLER"
echo "Start with:"
echo "  cd '$ROOT'"
echo "  USE_TF=0 '$VENV/bin/python' -m hermes_jev.reflex.laya_service --device '$DEVICE' --host 127.0.0.1 --port '$PORT' --model '$MODEL'"
echo "Then smoke with:"
echo "  HERMES_REFLEX_LAYA_BASE_URL=http://127.0.0.1:$PORT python3 scripts/check_laya_sidecar.py"
