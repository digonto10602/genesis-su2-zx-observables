# SU2ZX v0.3.0 run manifest

- Archive timestamp: 2026-09-04T22:22:59Z
- Input Git commit: `fdf631acfeb351dd400ef79c3b63235a1758eeb1`
- Branch: `main`
- Physics validation: PASS
- Regression tests: PASS, 17 tests
- Ruff: PASS
- Mypy: PASS
- Compiler verification: PASS, 426/426 primary and 54/54 seed records
- Winner diversity: PASS
- ML selector: NULL
- Symmetry-aware ordering: POSITIVE for the sampled trajectory
- CPU tensor network: PASS for validated N=5,8; N=12 exploratory
- CUDA-Q CPU: PASS
- CUDA-Q GPU: BLOCKED_BY_HARDWARE
- Tensor-network GPU: BLOCKED_BY_HARDWARE
- IBM QPU: NOT_RUN
- Graphify: PASS, 408 nodes / 678 relationships

## Included material

The archive includes the root reports and metadata (`README.md`, `AGENTS.md`, `RESEARCH_RESULTS.md`, `VALIDATION.md`, `GRAPHIFY_UPDATE.md`, these release notes and manifest, citation/license, `.graphifyignore`, and `pyproject.toml`); `config/`, `src/`, `tests/`, `scripts/`, and relevant `tools/`; all v0.3.0 `artifacts/data/`, `artifacts/figures/`, `artifacts/provenance/`, and validation/research logs; current CUDA-Q CPU reference JSON; the v0.3.0 prompt and references; and the refreshed `graphify-out/GRAPH_REPORT.md`, `graph.json`, and `graph.html`.

It excludes `.git/`, `.mamba/`, `.work/`, caches, bytecode, package metadata caches, credentials/provider configuration, prior archives, and `zip_results/` itself.

## Major experiments

1. Exact/Strang physics observables and second-order convergence fit.
2. Reflection-paired symmetry-aware Strang ordering.
3. Six-strategy exact compiler benchmark over structural, topology, and layout diversity.
4. Three-seed routing sensitivity.
5. Leakage-controlled grouped ML strategy selection and fixed/rule/oracle baselines.
6. Qiskit Aer CPU MPS validation and bounded N=12 exploration.
7. CUDA-Q qpp-cpu cross-validation and hardware capability gating.
8. Guarded IBM hardware-ready workflow without QPU submission.

## Known limitations

Compiler targets are synthetic rather than named calibration snapshots; only three strict Basic wins were found; ML does not outperform always-Basic; N=12 MPS has no dense exact-Hamiltonian comparison; CUDA-Q GPU is unsupported on the local device; and IBM hardware was not run.
