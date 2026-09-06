#!/usr/bin/env bash
set -euo pipefail
ROOT="$(pwd -P)"
[[ "$(basename "$ROOT")" == SU2ZX ]] || exit 2
mkdir -p .work/tmp .work/matplotlib .work/cache artifacts/logs/v040
export TMPDIR="$ROOT/.work/tmp" MPLCONFIGDIR="$ROOT/.work/matplotlib"
export XDG_CACHE_HOME="$ROOT/.work/cache" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
PYTHON="$ROOT/.mamba/envs/su2zx/bin/python"
"$PYTHON" -m pytest
"$PYTHON" -m su2zx.robust_study
"$PYTHON" -m su2zx.scaling_study physics
"$PYTHON" -m su2zx.scaling_study tn
"$PYTHON" tools/validate_v040.py controls
"$PYTHON" tools/validate_v040.py hardware
for n in 1 2 5; do
  "$PYTHON" tools/cudaq_reference.py --target qpp-cpu --plaquettes "$n" \
    > "artifacts/data/v040/cudaq_N${n}.json"
done
"$PYTHON" tools/plot_v040.py
"$PYTHON" tools/validate_v040.py audit
"$PYTHON" -m pytest
"$PYTHON" -m ruff check src tests tools
"$PYTHON" -m ruff format --check src tests tools
"$PYTHON" -m mypy src
