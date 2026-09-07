# Effective configuration (G0)
RUNID=20260907T0628Z
SU2ZX_TARGET_HOURS=12  SU2ZX_HARD_STOP_HOURS=16
SU2ZX_HW=0 (default; no credentials configured -> TWIN MODE)
SU2ZX_BACKEND=unset -> FakeTorino (Heron-class, CZ native, 133q)
SU2ZX_HW_BUDGET_SEC=600  SU2ZX_HW_MAX_SHOTS_PER_JOB=8192
SU2ZX_HW_OVERRIDE_G1=0
SU2ZX_MAX_CONCURRENT_AGENTS=3
SU2ZX_ESCALATION_MODEL=claude-fable-5-1 (via Hermes delegate_task)
SU2ZX_NOTIFY=0
Python: .mamba/envs/su2zx/bin/python 3.11.16
qiskit 2.5.2 / aer 0.17.2 / runtime 0.49.0 / pyzx 0.10.6 / scipy 1.17.1 / numpy 2.4.6 / mthree 3.0.0
CUDA-Q: NOT AVAILABLE  cuTensorNet: NOT AVAILABLE (Aer matrix_product_state used for TN cross-check)
