#!/usr/bin/env bash
set -euo pipefail

VENV="${OPENJEV_VENV:-$HOME/.venvs/hermes-reflex-openjev}"
MODEL_DIR="${OPENJEV_MODEL_DIR:-$HOME/models/openjev}"
VLLM_PORT="${OPENJEV_VLLM_PORT:-8000}"
SHIM_PORT="${OPENJEV_SHIM_PORT:-3000}"
PYTHON_SPEC="${OPENJEV_PYTHON_SPEC:-3.12}"
UV="${UV_BIN:-}"

find_nvidia_smi() {
  for candidate in "$(command -v nvidia-smi 2>/dev/null || true)" /usr/lib/wsl/lib/nvidia-smi /mnt/c/Windows/System32/nvidia-smi.exe; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then printf '%s\n' "$candidate"; return 0; fi
  done
  return 1
}

SMI="$(find_nvidia_smi || true)"
if [ -z "$SMI" ]; then
  if [ "${OPENJEV_ALLOW_NO_GPU_PROBE:-0}" != 1 ]; then
    echo "OPENJEV_SETUP=BLOCKED_NO_GPU_PROBE"
    echo "No NVIDIA GPU probe was found. Refusing to download the 27B model blindly."
    echo "Set OPENJEV_ALLOW_NO_GPU_PROBE=1 only on a GPU host you have verified separately."
    exit 29
  fi
else
  VRAM="$($SMI --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | sort -nr | head -1 | tr -d ' ')"
  echo "nvidia_smi=$SMI"
  echo "largest_gpu_vram_mib=${VRAM:-0}"
  if [ "${VRAM:-0}" -lt 30000 ] && [ "${OPENJEV_ALLOW_UNDERSIZED_GPU:-0}" != 1 ]; then
    echo "OPENJEV_SETUP=BLOCKED_GPU"
    echo "OpenJev's published FP8 checkpoint is about 29 GB and the primary measured recipe uses one 80 GB H100."
    echo "Use a >=30 GB GPU host (80 GB recommended for the published recipe), or set OPENJEV_ALLOW_UNDERSIZED_GPU=1 only for an experimental unsupported attempt."
    exit 30
  fi
fi

have_working_venv() {
  local py="${PYTHON:-python3}" probe
  probe=$(mktemp -d)
  if "$py" -m venv "$probe" >/dev/null 2>&1 && [ -x "$probe/bin/python" ]; then
    rm -rf -- "$probe"; printf '%s\n' "$py"; return 0
  fi
  rm -rf -- "$probe"; return 1
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
  "$VENV/bin/pip" install 'vllm==0.29.0' 'openai==3.16.2' 'httpx==0.28.1' 'huggingface_hub>=1,<2'
else
  ensure_uv
  "$UV" python install "$PYTHON_SPEC"
  "$UV" venv --python "$PYTHON_SPEC" "$VENV"
  "$UV" pip install --python "$VENV/bin/python" 'vllm==0.29.0' 'openai==3.16.2' 'httpx==0.28.1' 'huggingface_hub>=1,<2'
fi

mkdir -p "$MODEL_DIR"
"$VENV/bin/hf" download openjev/openjev --local-dir "$MODEL_DIR"

cat > "$MODEL_DIR/start-hermes-openjev.sh" <<EOF2
#!/usr/bin/env bash
set -euo pipefail
HERE=\$(CDPATH= cd -- "\$(dirname -- "\$0")" && pwd)
"$VENV/bin/vllm" serve "\$HERE" --host 127.0.0.1 --served-model-name qwen --port $VLLM_PORT \\
  --enable-prefix-caching --max-model-len 16384 --gpu-memory-utilization 0.90 \\
  --limit-mm-per-prompt '{"image":1}' --trust-remote-code --max-num-seqs 256 \\
  --max-logprobs 64 --gdn-prefill-backend triton --quantization fp8 &
VLLM_PID=\$!
trap 'kill \$VLLM_PID 2>/dev/null || true' EXIT INT TERM
ready=0
for _ in \$(seq 1 180); do
  if curl -fsS http://127.0.0.1:$VLLM_PORT/v1/models >/dev/null 2>&1; then ready=1; break; fi
  sleep 2
done
if [ "\$ready" != 1 ]; then echo "ERROR: vLLM did not become ready" >&2; exit 40; fi
VLLM=http://localhost:$VLLM_PORT/v1 TOKENIZER="\$HERE" READOUT_T=0.85 READOUT_NOUL_T=1.829074 READOUT_NOUL_BIAS=0 \\
READOUT_TARGETED=1 READOUT_INSTR_STYLE=pyrepr SHIM_STAGGER=1 \\
"$VENV/bin/python" "\$HERE/helper/shim.py" --host 127.0.0.1 --port $SHIM_PORT
EOF2
chmod +x "$MODEL_DIR/start-hermes-openjev.sh"
echo "OPENJEV_SETUP=PASS model_dir=$MODEL_DIR"
echo "Start: $MODEL_DIR/start-hermes-openjev.sh"
echo "Smoke from the Hermes host through a local tunnel: HERMES_REFLEX_OPENJEV_BASE_URL=http://127.0.0.1:$SHIM_PORT python3 scripts/check_openjev_sidecar.py"
