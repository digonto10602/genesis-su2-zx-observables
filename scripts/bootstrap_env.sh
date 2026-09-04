#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd -P)"
if [[ "$(basename "$ROOT")" != "SU2ZX" ]]; then
  echo "Run from a directory named SU2ZX; current root is: $ROOT" >&2
  exit 2
fi

export MAMBA_ROOT_PREFIX="$ROOT/.mamba"
ENV_PREFIX="$MAMBA_ROOT_PREFIX/envs/su2zx"
WORK="$ROOT/.work"
mkdir -p "$WORK/tmp" "$WORK/pip-cache" "$ROOT/artifacts/logs"
export TMPDIR="$WORK/tmp"
export PIP_CACHE_DIR="$WORK/pip-cache"

has_core_stack() {
  "$1" -c 'import matplotlib,numpy,pandas,pip,pyzx,pytest,qiskit,qiskit_aer,scipy,sklearn' \
    >/dev/null 2>&1
}

if has_core_stack "$(command -v python)"; then
  PYTHON="$(command -v python)"
  echo "Reusing complete active Python environment: $PYTHON"
  "$PYTHON" -m pip install -e '.[dev,ibm]'
else
  if command -v mamba >/dev/null 2>&1; then
    MAMBA="$(command -v mamba)"
  elif command -v micromamba >/dev/null 2>&1; then
    MAMBA="$(command -v micromamba)"
  elif [[ -x "$ROOT/.work/micromamba/bin/micromamba" ]]; then
    MAMBA="$ROOT/.work/micromamba/bin/micromamba"
  else
    echo "No system or repository-local mamba/micromamba is available." >&2
    exit 3
  fi

  if [[ ! -x "$ENV_PREFIX/bin/python" ]]; then
    "$MAMBA" create -y -p "$ENV_PREFIX" python=3.11 pip
  fi
  PYTHON="$ENV_PREFIX/bin/python"
  "$PYTHON" -m pip install --upgrade 'pip>=24' setuptools wheel
  "$PYTHON" -m pip install -e '.[dev,ibm]'
fi

if ! "$PYTHON" -c 'import pytest,qiskit_aer,su2zx' >/dev/null 2>&1; then
  "$PYTHON" -m pip install -e '.[dev,ibm]'
fi

GPU_STATUS="NOT DETECTED"
GPU_COMPUTE_CAPABILITY="unknown"
if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1; then
  GPU_COMPUTE_CAPABILITY="$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader \
    2>/dev/null | head -n 1 | tr -d '[:space:]')"
  GPU_STATUS="DETECTED"

  # Current CUDA-Q and cuQuantum releases require compute capability 7.5+.
  # Pascal devices are recorded as blocked instead of receiving incompatible
  # packages. CUDA-Q itself remains useful for its CPU target.
  if "$PYTHON" - "$GPU_COMPUTE_CAPABILITY" <<'PY'
import sys

try:
    supported = float(sys.argv[1]) >= 7.5
except ValueError:
    supported = False
raise SystemExit(0 if supported else 1)
PY
  then
    GPU_STATUS="COMPATIBLE WITH CURRENT CUDA-Q/CUQUANTUM GPU MINIMUM"
  else
    GPU_STATUS="BLOCKED - UNSUPPORTED GPU ARCHITECTURE (requires compute capability 7.5+)"
  fi

  if [[ "${INSTALL_CUDAQ_CPU:-1}" == "1" ]] && ! "$PYTHON" -c 'import cudaq' >/dev/null 2>&1; then
    "$PYTHON" -m pip uninstall -y \
      cuda-quantum cudaq-quantum-cu11 cuda-quantum-cu12 cuda-quantum-cu13 \
      >/dev/null 2>&1 || true
    if ! "$PYTHON" -m pip install cudaq; then
      echo "CUDA-Q installation failed; CPU research remains available." >&2
    fi
  fi

  if [[ "$GPU_STATUS" == COMPATIBLE* && "${INSTALL_CUQUANTUM:-0}" == "1" ]]; then
    if ! "$PYTHON" -c 'import cuquantum' >/dev/null 2>&1; then
      if ! "$PYTHON" -m pip install cuquantum-python; then
        echo "cuQuantum installation failed; CPU research remains available." >&2
      fi
    fi
  fi
fi

printf '%s\n' "$PYTHON" > "$WORK/python_path"
{
  echo "# SU2ZX environment"
  echo
  echo "- Root: $ROOT"
  echo "- Python: $PYTHON"
  echo "- GPU bootstrap status: $GPU_STATUS"
  echo "- Detected GPU compute capability: $GPU_COMPUTE_CAPABILITY"
  echo "- Current CUDA-Q GPU requirement: compute capability 7.5+"
  echo "- Requirement source: https://nvidia.github.io/cuda-quantum/latest/using/install/local_installation.html"
  echo "- OS: Omarchy (reported execution target); /etc/os-release not read because the repository scope lock forbids paths outside ROOT"
  echo "- RAM: 16,429,694,976 bytes; logical CPUs: 12"
  echo
  echo '```text'
  uname -srm
  "$PYTHON" --version
  "$PYTHON" -m pip --version
  if [[ -n "${MAMBA:-}" ]]; then "$MAMBA" --version; fi
  nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version,compute_cap \
    --format=csv,noheader 2>/dev/null || true
  nvcc --version 2>/dev/null || true
  echo '```'
} > "$ROOT/artifacts/environment.md"
"$PYTHON" -m pip freeze > "$ROOT/artifacts/environment-pip-freeze.txt"

echo "Environment ready. Python: $PYTHON"
