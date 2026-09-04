# SU2ZX v0.3.0

SU2ZX is a reproducible CPU research package for exact, backend-aware compilation of real-time circuits from a gauge-reduced SU(2), `j_max=1/2` plaquette-chain Hamiltonian. The current milestone tests whether the best exact Qiskit/PyZX rewrite depends on both logical circuit structure and synthetic hardware topology.

The principal result is non-degenerate compiler winner diversity: Basic and phase-teleport strategies each achieve multiple strict native two-qubit wins across structurally distinct circuit/target cases. A random-forest cost selector is scientifically meaningful enough to evaluate, but its v0.3.0 result is `NULL` because it does not beat always-Basic in structural-family holdout. See [RESEARCH_RESULTS.md](RESEARCH_RESULTS.md) for exact values and limitations.

## Scientific scope

The model is a pure SU(2), severely truncated, one-plaquette-wide open spatial chain in a small 2+1D Hamiltonian geometry. Each qubit is a retained gauge-invariant plaquette-loop degree of freedom. Qiskit strings and bitstrings use `q_(N-1)...q_0`.

This package does not model physical SU(3) QCD or establish continuum physics, string tension, string breaking, hadronization, or quantum advantage. `src/su2zx/core.py` is the single Hamiltonian and convention source of truth.

## Installation

Run from a directory whose basename is `SU2ZX`:

```bash
bash scripts/bootstrap_env.sh
```

The bootstrap reuses the single repository-local Mamba environment under `.mamba/`. It does not modify global Python or system configuration.

## Reproduce the run

```bash
bash scripts/run_all.sh
```

Individual stages are:

```bash
.mamba/envs/su2zx/bin/python -m pytest
.mamba/envs/su2zx/bin/ruff check src tests tools
.mamba/envs/su2zx/bin/mypy src

.mamba/envs/su2zx/bin/python -m su2zx.study \
  --config config/research.json --output artifacts
.mamba/envs/su2zx/bin/python -m su2zx.compiler_study \
  --config config/research.json --output artifacts
.mamba/envs/su2zx/bin/python -m su2zx.tn_study --output artifacts
.mamba/envs/su2zx/bin/python -m su2zx.report \
  --config config/research.json --output artifacts
```

The compiler stage regenerates the structural hashes, exact-equivalence records, target/layout metrics, winner table, three-seed sensitivity table, grouped ML assignments, selector metrics, and compiler figures. The study stage regenerates exact/Strang observables, the fitted convergence order, the symmetry-aware comparison, and physics figures.

## CUDA-Q CPU and optional GPU

```bash
.mamba/envs/su2zx/bin/python tools/cudaq_reference.py \
  --target qpp-cpu --plaquettes 5 --time 0.32
```

GPU execution must be capability-probed first. The current GTX 1060 Max-Q path is recorded as `BLOCKED_BY_HARDWARE`; do not force unsupported CUDA-Q targets or modify drivers. The reference program accepts supported CUDA-Q targets on a future compatible system without changing the physics implementation.

## IBM hardware preparation

The IBM path defaults to a dry run and never treats simulator output as QPU data:

```bash
.mamba/envs/su2zx/bin/python -m su2zx.qpu \
  --backend BACKEND --physical-path q0,q1,q2,q3,q4
```

Submission requires all three independent guards: `ALLOW_IBM_QPU_SUBMISSION=1`, `--submit`, and the exact fresh confirmation token printed by that dry run. v0.3.0 submitted no QPU job.

## Outputs

- `artifacts/data/`: CSV/JSON physics, compiler, ML, seed, and tensor-network data.
- `artifacts/figures/`: matching PNG/PDF publication figures.
- `artifacts/logs/`: test, lint, type-check, and execution logs.
- `artifacts/provenance/run_v0.3.0.json`: machine and run provenance.
- `graphify-out/`: refreshed code/document knowledge graph.
- `zip_results/`: timestamped, validated run archives and SHA-256 files.

Validation commands and tolerances are recorded in [VALIDATION.md](VALIDATION.md).
