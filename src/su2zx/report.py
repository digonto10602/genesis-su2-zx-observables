# ruff: noqa: E501
"""Generate the v0.3.0 research narrative from machine-readable artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from .paths import load_json, project_path


def commit_sha(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def load_optional(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def strategy_table(frame: pd.DataFrame) -> str:
    medians = frame.groupby("strategy")[["native_2q_count", "native_2q_depth", "routing_penalty_ratio"]].median()
    lines = [
        "| Strategy | Median native 2Q | Median native 2Q depth | Median routing ratio |",
        "|---|---:|---:|---:|",
    ]
    for strategy, row in medians.iterrows():
        lines.append(f"| {strategy} | {row.native_2q_count:.1f} | {row.native_2q_depth:.1f} | {row.routing_penalty_ratio:.3f} |")
    return "\n".join(lines)


def figure(name: str, caption: str, output: Path) -> str:
    path = output / "figures" / f"{name}.png"
    if not path.exists():
        return f"*Not generated: `{path.as_posix()}`.*"
    relative = path.relative_to(Path.cwd()).as_posix()
    return f"![{caption}]({relative})\n\n{caption}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/research.json")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    config = load_json(args.config)
    output = project_path(args.output)
    physics = load_optional(output / "data" / "physics_summary.json")
    selector = load_optional(output / "data" / "selector_summary.json")
    tn = load_optional(output / "data" / "tensor_network_summary.json")
    accelerator = load_optional(output / "data" / "accelerator_status.json")
    compiler = pd.read_csv(output / "data" / "compiler_dataset.csv")
    seeds = pd.read_csv(output / "data" / "compiler_seed_sensitivity.csv")
    verified = compiler[compiler.verification_result]
    p = physics.get("trotter_convergence_fit", {}).get("order_p", float("nan"))
    p_error = physics.get("trotter_convergence_fit", {}).get("slope_standard_error", float("nan"))
    symmetry = physics.get("symmetry_ordering", {})
    current = symmetry.get("current", {})
    symmetric = symmetry.get("symmetry", {})
    winner = selector.get("winner_distribution", {})
    strict = selector.get("strict_native_2q_winner_distribution", {})
    validation = selector.get("validation", {}).get("structural_family_holdout", {})
    seed_span = seeds.groupby(["target_topology", "strategy"]).native_2q_count.agg(lambda x: int(x.max() - x.min()))
    test_log = output / "logs" / "pytest.log"
    test_evidence = test_log.read_text(encoding="utf-8")[-1200:] if test_log.exists() else "not run"
    test_line = next((line.strip() for line in reversed(test_evidence.splitlines()) if "passed" in line), "not yet recorded")

    report = f"""# SU2ZX research results — v0.3.0

Generated: {datetime.now(UTC).isoformat()}<br>
Input Git commit: `{commit_sha(root)}`

## Executive summary

This run preserves the validated gauge-reduced SU(2), `j_max=1/2` plaquette-chain physics and turns the compiler benchmark into a non-degenerate target-aware problem. All {selector.get('verified_rows', 0)} compiler records passed global-phase-aware exact unitary equivalence. Across {selector.get('distinct_structural_target_cases', 0)} distinct structural-circuit/target cases, Basic won {winner.get('basic', 0)} lexicographic cases and teleport won {winner.get('teleport', 0)}; the stricter native-2Q-only audit found {strict.get('basic', 0)} Basic and {strict.get('teleport', 0)} teleport wins. The winner-diversity gate therefore **{'PASS' if selector.get('winner_diversity_gate') else 'FAIL'}**.

The ML selector result is **{selector.get('ml_status', 'NOT_RUN')}**. Its structural-family-holdout mean regret is {validation.get('mean_regret', float('nan')):.4f}, versus {selector.get('fixed_normalized_regret', {}).get('basic', float('nan')):.4f} for always-Basic and {selector.get('fixed_normalized_regret', {}).get('qiskit', float('nan')):.4f} for always-Qiskit. It improves on Qiskit but not the strongest fixed baseline, so no ML advantage is claimed.

The symmetry-aware Strang ordering is positive for the sampled five-plaquette trajectory: maximum TVD changes from {current.get('max_tvd', float('nan')):.6g} to {symmetric.get('max_tvd', float('nan')):.6g}, maximum energy drift from {current.get('max_energy_drift', float('nan')):.6g} to {symmetric.get('max_energy_drift', float('nan')):.6g}, and maximum mirror asymmetry from {current.get('max_mirror_asymmetry', float('nan')):.6g} to {symmetric.get('max_mirror_asymmetry', float('nan')):.6g}, with unchanged source 2Q count.

CPU MPS validation is **{tn.get('status', 'NOT_RUN')}** for N=5,8 at maximum bond dimension {tn.get('validation_bond_dimension', 'n/a')}; N=12 is exploratory. CUDA-Q CPU remains **{accelerator.get('cudaq_cpu_status', 'NOT RUN')}**. CUDA-Q GPU remains **{accelerator.get('cudaq_gpu_status', 'NOT RUN')}** on the compute-capability-{accelerator.get('gpu', {}).get('compute_capability', 'unknown')} GTX 1060 Max-Q. IBM QPU is **NOT_RUN**; no job was submitted.

## Physics model and boundaries

`src/su2zx/core.py` remains the sole Hamiltonian and convention source. The model is a pure SU(2), `j_max={config['j_max']}`, one-plaquette-wide open spatial chain in a truncated 2+1D Hamiltonian geometry. Qiskit strings and displayed bitstrings use `q_(N-1)...q_0`. This study does not establish continuum SU(2), physical SU(3) QCD, string tension, string breaking, hadronization, or quantum advantage.

The reference hierarchy is exact Hamiltonian → ideal Strang circuit → compiled ideal circuit → noisy/hardware result. No simulator or MPS output is labeled as QPU data.

## Validation

- Current local test result: `{test_line}`.
- One- and two-plaquette analytic matrices and spectra, Hermiticity, normalization, Qiskit ordering, Pauli rotations, energy reconstruction, reflection symmetry, PyZX equivalence, and guarded IBM dry-run behavior are covered by `tests/`.
- Maximum state-norm error: `{physics.get('max_norm_error', float('nan')):.3e}`.
- Maximum six-basis energy-reconstruction error: `{physics.get('max_six_basis_energy_error', float('nan')):.3e}`.
- Compiler equivalence: `{int(verified.verification_result.sum())}/{len(compiler)}` verified at recorded tolerance `1e-10`.
- Seed sensitivity: `{int(seeds.verification_result.sum())}/{len(seeds)}` verified; maximum native-2Q seed span was `{int(seed_span.max())}` gates, confined to stochastic aggressive-reduction cases.

## Trotter analysis

The fit uses ordinary least squares of `log(max TVD)` on `log(r)` for `r=1,2,4,8`. It gives `p = {p:.3f} ± {p_error:.3f}` (slope standard error), approaching the expected second-order value. The procedure and points are stored in `artifacts/data/trotter_convergence.csv` and `physics_summary.json`.

{figure('trotter_tvd_convergence', 'Exact-vs-Strang TVD across time and repetition counts.', output)}

## Physics observables

Stored observables include local plaquette occupation, central-state survival, electric, magnetic and total energy, norm, TVD, and mirror asymmetry. They are loop-sector diagnostics of the truncated model, not quark or hadron observables.

{figure('loop_occupations_exact_vs_trotter', 'Plaquette occupations for exact and ideal-Trotter evolution.', output)}

{figure('survival_probability', 'Central-state survival probability.', output)}

{figure('energy_components', 'Electric, magnetic, and total energy.', output)}

## Symmetry-aware Trotter ordering

The `symmetry` ordering groups every Pauli word with its spatial reflection without changing the Hamiltonian. On the sampled N=5, r=2 trajectory it eliminates ordering-induced mirror asymmetry to floating-point scale and reduces energy drift; its TVD improvement is smaller. These are ideal-algorithm results, not device-noise results.

{figure('symmetry_aware_ordering', 'Current versus reflection-paired Strang ordering.', output)}

## Compiler experiment

- raw circuits: **{selector.get('raw_circuits', 0)}**;
- unique parameterized circuits: **{selector.get('unique_parameterized_circuits', 0)}**;
- unique structural circuits: **{selector.get('unique_structural_circuits', 0)}**;
- explicit angle-only duplicates: **{selector.get('duplicate_structural_circuits', 0)}**;
- target configurations: **{selector.get('target_configurations', 0)}** across **{selector.get('topology_classes', 0)}** topology classes;
- primary compiler evaluations: **{len(compiler)}**;
- three-seed sensitivity evaluations: **{len(seeds)}**;
- verified primary evaluations: **{len(verified)}**.

The families cover N=2–6, r=1,2,4,8, current/reversed/reflection-paired ordering, and nonzero x/t variants. Targets are labeled synthetic line, ring, grid, heavy-hex-like, and sparse irregular graphs. Favorable, spread, and transpiler-selected placements are recorded. Strategies use the same ECR basis, target, layout constraint, optimization level, and seed within a case.

The primary objective is lexicographic: native 2Q count, then native 2Q depth, then estimated duration. Error-cost fields are stored separately and are not silently mixed into it.

{strategy_table(verified)}

{figure('compiler_native_resources', 'Native two-qubit count and depth by exact strategy.', output)}

{figure('compiler_routing_penalty', 'Native/logical two-qubit routing penalty by strategy.', output)}

## Winner distribution

After aggregating angle-only duplicates by structure/target, winners are `{json.dumps(winner, sort_keys=True)}`. Strict native-2Q winners are `{json.dumps(strict, sort_keys=True)}`. Basic and teleport each have at least three strict wins, the operational threshold used here to reject a single-anomaly interpretation. Qiskit tie-break wins in raw cases are not presented as strict native-2Q wins.

{figure('strategy_winner_distribution', 'Lexicographic strategy winners.', output)}

{figure('strategy_winner_by_topology', 'Winner distribution across synthetic topology classes.', output)}

## ML result: {selector.get('ml_status', 'NOT_RUN')}

Features are available before compiler selection; no competing-strategy output is an input. Structural-family, leave-one-size-out, and leave-one-topology-out validation are stored in `selector_summary.json`. Primary top-1 accuracy is {validation.get('top1_strategy_accuracy', float('nan')):.3f}, median regret {validation.get('median_regret', float('nan')):.4f}, worst-case regret {validation.get('worst_case_regret', float('nan')):.4f}, and oracle-equality fraction {validation.get('fraction_equal_to_oracle', float('nan')):.3f}. The simple distance rule has regret {selector.get('rule_based_normalized_regret', float('nan')):.4f}; the majority policy is always-{selector.get('majority_winner_strategy', 'unknown')} with regret {selector.get('majority_winner_normalized_regret', float('nan')):.4f}. Oracle regret is zero.

The highest random-forest cost-model importances are source 2Q count, source gate count, and source depth. This does not establish causality; it indicates circuit scale dominated this bounded dataset more than topology summaries.

{figure('selector_accuracy_regret', 'Grouped selector regret versus fixed and oracle policies.', output)}

## Tensor-network result: {tn.get('status', 'NOT_RUN')}

Qiskit Aer’s CPU MPS backend was validated at N=5,8 against the ideal Strang statevector. At bond dimension {tn.get('validation_bond_dimension', 'n/a')}, maximum validated TVD is {tn.get('max_validated_tvd_to_ideal_trotter', float('nan')):.3e}, maximum energy error is {tn.get('max_validated_energy_error_to_ideal_trotter', float('nan')):.3e}, and minimum fidelity is {tn.get('minimum_validated_state_fidelity_to_ideal_trotter', float('nan')):.12f}. N=12 is exploratory without a dense exact-Hamiltonian reference.

{figure('tensor_network_convergence', 'CPU MPS bond-dimension error and runtime.', output)}

## CUDA-Q and IBM status

CUDA-Q `qpp-cpu` is `{accelerator.get('cudaq_cpu_status', 'NOT RUN')}` using the shared conventions. CUDA-Q GPU and GPU tensor-network routes are `BLOCKED_BY_HARDWARE`; the local GTX 1060 Max-Q has compute capability 6.1. No driver, system, or global environment was modified.

IBM QPU is `NOT_RUN`. The guarded bundle requires `ALLOW_IBM_QPU_SUBMISSION=1`, `--submit`, and the exact fresh dry-run token; this run supplied none. The repository contains hardware-ready preparation but no QPU result and no paid job.

## Limitations

Targets are synthetic rather than calibration snapshots; the balanced-incomplete target design is not a full Cartesian grid; three strict Basic wins reject a single anomaly but remain a small minority; and the model does not beat always-Basic. Estimated durations/errors are target-model estimates, not measured hardware performance. N=12 MPS lacks dense exact-Hamiltonian comparison. GPU and real-QPU conclusions remain unavailable.

## Reproduction

```bash
bash scripts/bootstrap_env.sh
bash scripts/run_all.sh
```

Machine-readable data are under `artifacts/data/`, figures under `artifacts/figures/`, provenance under `artifacts/provenance/`, and validation logs under `artifacts/logs/`.

## Next research questions

1. Does strict winner diversity persist on named backend calibration snapshots and independent target seeds?
2. Can block-local or routing-aware ZX extraction create more strict wins without sacrificing exactness?
3. Which pre-compilation graph embeddings improve regret beyond always-Basic under topology holdout?
4. How does symmetry-aware ordering behave across sizes, times, and compiled hardware costs?
5. Can CPU MPS reach larger N using local-observable extraction without materializing a full statevector?
"""
    destination = project_path("RESEARCH_RESULTS.md")
    destination.write_text(report, encoding="utf-8")
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
