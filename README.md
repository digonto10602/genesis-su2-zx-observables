# SU2ZX observable-preserving compilation study

Reproducible CPU study of backend-aware ZX compilation for a minimally truncated,
open five-plaquette SU(2) Hamiltonian in a tiny 2+1D spatial geometry. A classical
selector chooses among exactly validated Qiskit/PyZX pipelines; quantum circuits
represent the real-time dynamics.

The complete numerical interpretation, status table, plots, and limitations are in
[RESEARCH_RESULTS.md](RESEARCH_RESULTS.md). The main local findings are:

- mandatory physics gates: 12 tests passed;
- six-basis energy reconstruction error: at most `1.257e-13`;
- compiler resource gate: PASS (`20.3%` median native two-qubit and `23.5%`
  two-qubit-depth reduction for PyZX Basic versus Qiskit L3);
- learned selector: NULL, because always-Basic ties its zero grouped-CV regret;
- CUDA-Q `qpp-cpu`: LOCAL CPU PASS for `N=1,2,5`;
- CUDA-Q/cuTensorNet GPU routes: BLOCKED because the local GTX 1060 Max-Q has
  compute capability 6.1, below the current 7.5 minimum;
- IBM QPU: NOT RUN because scoped credentials and explicit submission authorization
  were absent.

## Start

Run from a directory named `SU2ZX`:

Manual bootstrap and CPU run:

```bash
bash scripts/bootstrap_env.sh
bash scripts/run_all.sh
```

The bootstrap script reuses a complete active environment when possible. Otherwise it creates or reuses exactly one prefix at `.mamba/envs/su2zx`. Generated outputs go to `artifacts/`; the generated narrative is `RESEARCH_RESULTS.md`.

## Individual commands

```bash
# Unit tests
.mamba/envs/su2zx/bin/python -m pytest

# Exact/Trotter data and physics plots
.mamba/envs/su2zx/bin/python -m su2zx.study --config config/research.json --output artifacts

# Generic linear-ECR compiler dataset and learned selector
.mamba/envs/su2zx/bin/python -m su2zx.compiler_study --config config/research.json --output artifacts

# Regenerate the Markdown explanation from saved outputs
.mamba/envs/su2zx/bin/python -m su2zx.report --config config/research.json --output artifacts

# CUDA-Q CPU cross-check (GPU targets require compatible hardware)
.mamba/envs/su2zx/bin/python tools/cudaq_reference.py --target qpp-cpu --plaquettes 5 --time 0.32

# IBM circuits: dry run unless all explicit submission guards are supplied
.mamba/envs/su2zx/bin/python -m su2zx.qpu --backend BACKEND --physical-path q0,q1,q2,q3,q4
```

The generated datasets have 405 observable rows, 320 computational-basis
probability rows, five measurement-reconstruction rows, and 240 compiler records.
PNG and PDF figures are stored in `artifacts/figures/`; commands and failures are
preserved in `artifacts/logs/`.

## Scientific boundaries

The model is pure SU(2), `j_max=1/2`, and a tiny one-plaquette-wide spatial chain in 2+1D. It is a compiler/hardware benchmark. It does not determine continuum physics, SU(3) QCD, string tension, string breaking, or hadronization.

The package contains the analytic one/two-plaquette checks, general chain
Hamiltonian, exact and Strang evolution, six-basis energy reconstruction, exact
PyZX validation, target-aware compiler dataset, grouped selector evaluation,
plot/report generation, a guarded IBM Runtime path, and CUDA-Q/cuTensorNet
reference programs. Optional targets are never reported as successful unless they
actually execute.
