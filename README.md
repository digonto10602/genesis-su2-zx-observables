# SU2ZX v0.4.0

Reproducible research on exact compiler selection and real-time evolution of a gauge-reduced, j_max=1/2 SU(2) plaquette chain in a truncated 2+1D Hamiltonian geometry. `src/su2zx/core.py` defines the Hamiltonian and q_(N-1)...q_0 convention.

v0.4.0 demonstrates direct-observable CPU MPS scaling through N=32. Basic/Teleport winners survive the sampled fixed-target seeds; ML is NULL on prospective generalization, and symmetry-aware ordering has MIXED physics effects. See [RESEARCH_RESULTS.md](RESEARCH_RESULTS.md) and [VALIDATION.md](VALIDATION.md).

No continuum physics, physical SU(3) QCD, string tension, string breaking, hadronization or quantum advantage is established. Synthetic compilation and simulator outputs are never labeled QPU data.

The [completion audit](docs/V040_COMPLETION_AUDIT.md) maps the v0.4.0 prompt to evidence.
The [code logic and test report](docs/CODE_LOGIC_AND_TESTS.md) explains the complete
workflow, benchmarks, test coverage and limitations; the
[function inventory](docs/CODE_FUNCTION_INVENTORY.md) lists actual callables and assertions.

## Setup and reproduction

Run from the SU2ZX repository root. All working files remain inside it.

```bash
bash scripts/bootstrap_env.sh
bash scripts/run_v040.sh
```

Use the existing single `.mamba/` installation; the interpreter is `.mamba/envs/su2zx/bin/python`. `scripts/run_all.sh` retains the historical v0.3.0 reproduction pipeline and overwrites legacy reports; use run_v040.sh for the current milestone.

## Individual stages

```bash
export TMPDIR="$PWD/.work/tmp" MPLCONFIGDIR="$PWD/.work/matplotlib"
export XDG_CACHE_HOME="$PWD/.work/cache" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
.mamba/envs/su2zx/bin/python -m pytest
# Historical physics / six-strategy benchmark (use separate output for preservation):
.mamba/envs/su2zx/bin/python -m su2zx.study --config config/research.json --output .work/baseline
.mamba/envs/su2zx/bin/python -m su2zx.compiler_study --config config/research.json --output .work/baseline
# Fixed-target robustness, paired data, grouped ML and frozen-rule prospective test:
.mamba/envs/su2zx/bin/python -m su2zx.robust_study
# Re-analyze saved data without recompilation:
.mamba/envs/su2zx/bin/python -m su2zx.robust_study --stage analyze
# Symmetry physics/compiler grid, full/asymptotic fits and Pareto table:
.mamba/envs/su2zx/bin/python -m su2zx.scaling_study physics
# Direct-observable MPS validation then bounded no-statevector scaling:
.mamba/envs/su2zx/bin/python -m su2zx.scaling_study tn
.mamba/envs/su2zx/bin/python tools/validate_v040.py controls
.mamba/envs/su2zx/bin/python tools/validate_v040.py hardware
.mamba/envs/su2zx/bin/python tools/cudaq_reference.py --target qpp-cpu --plaquettes 5
.mamba/envs/su2zx/bin/python tools/plot_v040.py
.mamba/envs/su2zx/bin/python tools/validate_v040.py audit
.mamba/envs/su2zx/bin/python tools/report_v040.py
```

The frozen design is `config/research_v040.json`, checked against `artifacts/data/v040/frozen_design.json`. Preserve these for reproduction; a new research design needs a new timestamped freeze and a fresh holdout. Five routing seeds reuse calibration seed 7. All primary comparisons exclude any pair with a failed output. Randomized routed equivalence is explicitly distinguished from exact logical unitary validation.

## IBM and optional GPU

```bash
.mamba/envs/su2zx/bin/python -m su2zx.qpu --comparison   --backend BACKEND --physical-path q0,q1,q2,q3,q4
.mamba/envs/su2zx/bin/python -m su2zx.qpu_analysis artifacts/qpu/ibm_su2_run.json
```

The IBM command defaults to a dry run. Live submission requires ALLOW_IBM_QPU_SUBMISSION=1, --submit and the exact fresh --confirm token. Approval is one use, configuration/manifest bound, and expires after 15 minutes. The four-way current/symmetry × Basic/Teleport workflow measures occupations, survival, energy, mirror asymmetry and TVD, with raw/M3 analysis and separate exact/Trotter references. The saved QPY bundle uses a synthetic target; regenerate on the chosen real backend. This release submitted zero QPU jobs.

CUDA-Q CPU works. The detected GTX 1060 Max-Q (compute capability 6.1) blocks GPU execution. Existing CUDA-Q scripts accept supported targets on a future compatible GPU; do not alter drivers or force unsupported targets.

## Outputs, Graphify and archives

Data, figures/source mappings, logs and provenance live under artifacts/. Historical v0.3.0 outputs remain preserved alongside v040/. Sixteen current figures have both PNG and PDF outputs.

```bash
.mamba/bin/graphify query "direct MPS robustness pairwise selector symmetry"
.mamba/bin/graphify update .
# After final reports and Graphify validation:
.mamba/envs/su2zx/bin/python tools/archive_v040.py
```

The archive helper requires a passing Graphify validation record, scans the curated file set for secrets, creates a new UTC timestamped ZIP in zip_results/, tests that exact ZIP, verifies its expected contents and writes SHA256 plus an integrity receipt. It excludes environments, caches, credentials and prior archives. Never overwrite prior archives. Archive details are in RUN_MANIFEST.md and GRAPHIFY_UPDATE.md.
