# SU2ZX v0.3.0 validation

Validated locally on 2026-09-04 in the single repository-local environment `.mamba/envs/su2zx`.

## Commands and results

```text
.mamba/envs/su2zx/bin/python -m pytest
17 passed, 2 PyZX deprecation warnings

.mamba/envs/su2zx/bin/python -m ruff check src tests tools
All checks passed

.mamba/envs/su2zx/bin/python -m mypy src
Success: no issues found in 9 source files
```

The initial interrupted worktree baseline could not collect compiler/QPU tests because `src/su2zx/compiler_study.py` was absent; core and study tests still passed 11/11. The v0.3.0 implementation restored that required module as a new diverse compiler study and the complete final suite passes.

## Physics gates

| Gate | Tolerance/procedure | Result |
|---|---|---|
| Hamiltonian Hermiticity | `atol=1e-13`, N=1,2,5 | PASS |
| One-plaquette analytic matrix/spectrum/ground state | `atol<=1e-13` | PASS |
| One-plaquette transition probability | `atol=1e-12` | PASS |
| Two-plaquette analytic matrix and ground energy `-1.789221846776` | `atol=1e-12` | PASS |
| Exact and Strang state normalization | `atol=1e-12` | PASS |
| Qiskit Pauli/bit ordering | exact assertions in `q_(N-1)...q_0` | PASS |
| Pauli-rotation convention | global-phase-aware operator equivalence | PASS |
| Six-basis energy reconstruction | maximum error `1.257e-13` | PASS |
| Exact mirror symmetry | `atol=1e-12` | PASS |

Primary physics data contain 405 exact/Strang observable rows. The maximum norm error is `1.203e-13`.

## Trotter convergence

For N=5, x=2, t in `[0,0.32]`, the maximum TVD over nonzero sampled times is:

| r | max TVD |
|---:|---:|
| 1 | 0.1298423321 |
| 2 | 0.04256837745 |
| 4 | 0.01092096804 |
| 8 | 0.002742681177 |

Ordinary least squares of `log(max TVD)` on `log(r)` gives `p=1.8658` with slope standard error `0.06495`, consistent with approach to second-order Strang scaling over this finite grid.

## Symmetry-aware ordering

The reflection-paired ordering preserves exactly the same Hamiltonian terms. At N=5 and r=2 it changes maximum TVD from `0.0425684` to `0.0415574`, maximum energy drift from `0.575290` to `0.241868`, and maximum mirror asymmetry from `1.150e-3` to `3.331e-16`. Source gate count and native-independent source 2Q count remain unchanged. Result: `POSITIVE` for this sampled trajectory.

## Compiler exactness and dataset integrity

- Six pipelines: Qiskit, Basic, Basic with swaps, phase teleport, full reduce, and depth-oriented full-reduce extraction.
- Exactness: 426/426 primary records and 54/54 seed-sensitivity records passed `qiskit.quantum_info.Operator.equiv`, which is global-phase aware. Recorded tolerance: `1e-10`.
- Circuit counts: 35 parameterized, 30 structurally unique, 5 explicit angle-only duplicates.
- Target/layout cases: 35 target configurations across line, ring, grid, heavy-hex-like, and irregular synthetic topology classes; favorable, spread, and transpiler layouts are recorded.
- Structural/target cases after angle aggregation: 70.
- Primary objective: native 2Q count, then native 2Q depth, then estimated duration.
- Strict native-2Q winners: teleport 15, Basic 3. Winner-diversity gate: PASS under the stated minimum-three-independent-wins criterion.
- Aggressive strategies remain useful negative controls and show seed-dependent routed costs.
- Integrity command checked required finite numeric columns, all hash counts, verification flags, ML metadata, and CSV/JSON/plot presence: PASS. See `artifacts/logs/data_integrity.log`.

## ML leakage and validation

`ml_feature_definitions.json` contains only circuit-generation, source-circuit, topology, mapping, layout, and strategy identity features available before competing compilation. No native resource or winner column is an input. Leakage check: PASS.

Structural-family holdout gives top-1 accuracy `0.3239`, mean regret `0.06942`, median regret `0`, worst regret `0.51429`, and oracle-equality fraction `0.7042`. Always-Basic regret is `0.03561`, always-Qiskit `0.18541`, the simple rule `0.06664`, and oracle `0`. Result: `NULL` because the learned selector does not beat always-Basic. Leave-one-size-out and leave-one-topology-out results are stored in `selector_summary.json`.

## CPU tensor network

Qiskit Aer `matrix_product_state` ran on CPU for N=5,8,12 with maximum bond dimensions 4,8,16,32 and truncation tolerance `1e-14`. At bond 32 for validated N=5,8, maximum TVD to ideal Trotter is `9.599e-8`, maximum energy error `2.147e-9`, minimum fidelity `0.9999999999997504`, and norm error is below `1e-9`: PASS. N=12 is exploratory and is not claimed to have a dense exact-Hamiltonian reference.

## CUDA-Q and IBM

CUDA-Q 0.15.1 `qpp-cpu` was rerun for N=1,2,5 and agrees with the shared Qiskit Strang circuit within `1e-8`: PASS. The local GTX 1060 Max-Q has compute capability 6.1, so CUDA-Q GPU and GPU tensor-network paths are `BLOCKED_BY_HARDWARE`; no unsupported target was forced and no driver was modified.

IBM QPU is `NOT_RUN`. No submission flag, `--submit`, or exact fresh confirmation token was supplied. No simulator result is represented as QPU data.

## End-of-run integrity

- Graphify refresh: PASS, 408 nodes / 678 relationships with a clean extraction diagnostic.
- Archive integrity: PASS on the explicit candidate staging tree; final timestamped ZIP is re-tested below the same gate.
- Secret scan: pending final completion gate.
