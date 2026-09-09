#!/usr/bin/env bash
# The one C0 gate command (R11 step 1), run from the repository root.
set -o pipefail
TAG=c060_p0_20260909_5
SESSION=runs/campaign_v060/sessions/$TAG
PYTHONPATH=runs/section8_v0.5.0_20260907T0628Z/src \
  .mamba/envs/su2zx/bin/python -m pytest runs/campaign_v060/tests/gate_C0 \
  -q -p no:cacheprovider --junitxml="$SESSION/gate_C0.xml" 2>&1 | tee "$SESSION/gate_C0.log"
echo "pytest exit ${PIPESTATUS[0]}" | tee -a "$SESSION/gate_C0.log"
