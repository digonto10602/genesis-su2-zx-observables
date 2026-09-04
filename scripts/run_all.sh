#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd -P)"
if [[ "$(basename "$ROOT")" != "SU2ZX" ]]; then
  echo "Run from a directory named SU2ZX; current root is: $ROOT" >&2
  exit 2
fi

mkdir -p "$ROOT/.work/tmp" "$ROOT/artifacts/logs"
export TMPDIR="$ROOT/.work/tmp"
export MPLCONFIGDIR="$ROOT/.work/matplotlib"
export XDG_CACHE_HOME="$ROOT/.work/cache"

if [[ -f "$ROOT/.work/python_path" ]]; then
  IFS= read -r PYTHON < "$ROOT/.work/python_path"
elif [[ -x "$ROOT/.mamba/envs/su2zx/bin/python" ]]; then
  PYTHON="$ROOT/.mamba/envs/su2zx/bin/python"
else
  PYTHON="$(command -v python)"
fi

"$PYTHON" -m pytest 2>&1 | tee "$ROOT/artifacts/logs/pytest.log"
"$PYTHON" -m ruff check src tests tools 2>&1 | tee "$ROOT/artifacts/logs/ruff.log"
"$PYTHON" -m mypy src 2>&1 | tee "$ROOT/artifacts/logs/mypy.log"
"$PYTHON" -m su2zx.study --config config/research.json --output artifacts \
  2>&1 | tee "$ROOT/artifacts/logs/study.log"
"$PYTHON" -m su2zx.compiler_study --config config/research.json --output artifacts \
  2>&1 | tee "$ROOT/artifacts/logs/compiler.log"
"$PYTHON" -m su2zx.tn_study --output artifacts \
  2>&1 | tee "$ROOT/artifacts/logs/tensor_network_cpu.log"

if "$PYTHON" -c 'import cudaq' >/dev/null 2>&1; then
  for N in 1 2 5; do
    "$PYTHON" tools/cudaq_reference.py --target qpp-cpu --plaquettes "$N" --time 0.32 \
      > "$ROOT/artifacts/cudaq_reference_N${N}.json" \
      2>> "$ROOT/artifacts/logs/cudaq.log"
  done
fi

# The detected GTX 1060 Max-Q is compute capability 6.1. Current CUDA-Q and
# cuQuantum GPU backends require 7.5+, so GPU/TN execution is intentionally
# blocked rather than attempted on an unsupported architecture.
SU2ZX_GPU_RECORD="$(nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap \
  --format=csv,noheader 2>/dev/null | head -n 1 || true)"
export SU2ZX_GPU_RECORD
"$PYTHON" - <<'PY'
import json
import os
from importlib.metadata import version
from pathlib import Path

root = Path.cwd().resolve()
references = []
for n in (1, 2, 5):
    path = root / "artifacts" / f"cudaq_reference_N{n}.json"
    if path.exists():
        references.append(json.loads(path.read_text(encoding="utf-8")))
cpu_pass = len(references) == 3 and all(
    item["absolute_energy_error"] < 1e-8
    and item["probability_tvd_to_qiskit"] < 1e-8
    and item["state_norm_error"] < 1e-8
    for item in references
)
tn_summary_path = root / "artifacts" / "data" / "tensor_network_summary.json"
tn_summary = (
    json.loads(tn_summary_path.read_text(encoding="utf-8"))
    if tn_summary_path.exists()
    else {}
)
record = os.environ.get("SU2ZX_GPU_RECORD", "")
parts = [part.strip() for part in record.split(",")]
gpu = {
    "name": parts[0] if len(parts) > 0 else "not detected",
    "vram": parts[1] if len(parts) > 1 else "unknown",
    "driver": parts[2] if len(parts) > 2 else "unknown",
    "compute_capability": parts[3] if len(parts) > 3 else "unknown",
}
payload = {
    "cudaq_version": version("cudaq"),
    "cudaq_cpu_status": "LOCAL CPU PASS" if cpu_pass else "BLOCKED",
    "cudaq_cpu_references": references,
    "tensor_network_cpu_status": tn_summary.get("status", "NOT RUN"),
    "cudaq_gpu_status": "BLOCKED_BY_HARDWARE",
    "tensornet_mps_gpu_status": "BLOCKED_BY_HARDWARE",
    "direct_cutensornet_status": "BLOCKED_BY_HARDWARE",
    "minimum_compute_capability": "7.5",
    "requirement_url": "https://nvidia.github.io/cuda-quantum/latest/using/install/local_installation.html",
    "gpu": gpu,
}
destination = root / "artifacts" / "data" / "accelerator_status.json"
destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
PY

if [[ -f "$ROOT/artifacts/qpu/ibm_su2_run.json" ]]; then
  "$PYTHON" -m su2zx.qpu_analysis "$ROOT/artifacts/qpu/ibm_su2_run.json" \
    --output artifacts 2>&1 | tee "$ROOT/artifacts/logs/qpu_analysis.log"
fi

"$PYTHON" -m su2zx.report --config config/research.json --output artifacts \
  2>&1 | tee "$ROOT/artifacts/logs/report.log"

echo "Completed. Read RESEARCH_RESULTS.md"
