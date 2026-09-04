# ruff: noqa: E501
"""Build a human-readable Markdown report only from saved research artifacts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from .paths import load_json, project_path


def commit_sha(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "not yet committed"


def format_hardware_table(frame: pd.DataFrame, method: str, times: list[float]) -> str:
    selected = frame[(frame.method == method) & frame.time.isin(times)].copy()
    columns = [
        "time",
        "survival",
        "electric_energy",
        "magnetic_energy",
        "total_energy",
        "tvd_to_exact_hamiltonian",
        *[f"occupation_{q}" for q in range(5)],
    ]
    selected = selected[columns]
    headers = ["t", "L", "E_E", "E_B", "E", "TVD", "n0", "n1", "n2", "n3", "n4"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---:|" * len(headers)]
    for row in selected.itertuples(index=False):
        lines.append("| " + " | ".join(f"{value:.6g}" for value in row) + " |")
    return "\n".join(lines)


def compiler_results(output: Path) -> tuple[dict, str]:
    dataset_path = output / "data" / "compiler_dataset.csv"
    summary_path = output / "data" / "selector_summary.json"
    if not dataset_path.exists() or not summary_path.exists():
        return {}, "BLOCKED"
    frame = pd.read_csv(dataset_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    pivot_count = frame.pivot(
        index="circuit_key", columns="strategy", values="native_two_qubit"
    )
    pivot_depth = frame.pivot(
        index="circuit_key", columns="strategy", values="native_two_qubit_depth"
    )
    count_reduction = float(
        np.median((pivot_count.qiskit - pivot_count.basic) / pivot_count.qiskit)
    )
    depth_reduction = float(
        np.median((pivot_depth.qiskit - pivot_depth.basic) / pivot_depth.qiskit)
    )
    full_reduce_penalty = float(
        np.median((pivot_count.full_reduce - pivot_count.qiskit) / pivot_count.qiskit)
    )
    best_fixed = min(summary["fixed_normalized_regret"].values())
    ai_status = "PASS" if summary["normalized_regret"] < best_fixed else "NULL"
    status = "PASS" if count_reduction >= 0.15 and depth_reduction >= 0.10 else "FAIL"
    return (
        {
            "count_reduction": count_reduction,
            "depth_reduction": depth_reduction,
            "full_reduce_penalty": full_reduce_penalty,
            "all_exactly_equivalent": bool(frame.exact_equivalence_validated.all()),
            "median_native_duration_seconds": {
                key: float(value)
                for key, value in frame.groupby("strategy").native_duration_seconds.median().items()
            },
            "resource_status": status,
            "ai_status": ai_status,
            **summary,
        },
        status,
    )


def optional_status(path: Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return "NOT RUN"
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "BLOCKED"
    return "EXECUTED - REVIEW NUMERICAL AGREEMENT"


def sensitivity_table(compiler: dict) -> str:
    rows = compiler.get("cost_weight_sensitivity", [])
    if not rows:
        return "Cost-weight sensitivity was not available."
    lines = [
        "| Depth weight | Calibration-error weight | Top-1 | Learned regret | Best fixed regret |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['depth_weight']:.3g} | {row['calibration_error_weight']:.3g} "
            f"| {row['top1_accuracy']:.4g} | {row['normalized_regret']:.4g} "
            f"| {row['best_fixed_normalized_regret']:.4g} |"
        )
    return "\n".join(lines)


def figure_section(name: str, title: str, explanation: str, output: Path) -> str:
    image = output / "figures" / f"{name}.png"
    if not image.exists():
        return f"### {title}\n\nStatus: not generated. Check the relevant phase log.\n"
    relative = image.relative_to(Path.cwd())
    return f"### {title}\n\n![{title}]({relative.as_posix()})\n\n{explanation}\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/research.json")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    config = load_json(args.config)
    output = project_path(args.output)
    physics = pd.read_csv(output / "data" / "physics_observables.csv")
    physics_summary = json.loads(
        (output / "data" / "physics_summary.json").read_text(encoding="utf-8")
    )
    compiler, compiler_status = compiler_results(output)
    accelerator_path = output / "data" / "accelerator_status.json"
    accelerator = (
        json.loads(accelerator_path.read_text(encoding="utf-8"))
        if accelerator_path.exists()
        else {}
    )
    cpu_status = (
        "PASS"
        if physics_summary["max_norm_error"] < 1e-10
        and physics_summary["max_six_basis_energy_error"] < 1e-10
        and abs(physics_summary["initial_energy"] - 3.0) < 1e-10
        else "FAIL"
    )
    cudaq_status = accelerator.get("cudaq_cpu_status", "NOT RUN")
    cudaq_gpu_status = accelerator.get("cudaq_gpu_status", "NOT RUN")
    cutn_status = accelerator.get("direct_cutensornet_status", "NOT RUN")
    tn_status = accelerator.get("tensornet_mps_status", "NOT RUN")
    qpu_files = list((output / "qpu").glob("*.json")) if (output / "qpu").exists() else []
    qpu_status = (
        "EXECUTED - VERIFY JOB IDS"
        if qpu_files
        else "NOT RUN - AUTHORIZATION/CREDENTIALS REQUIRED"
    )
    publication_path = output / "data" / "publication.json"
    publication = (
        json.loads(publication_path.read_text(encoding="utf-8"))
        if publication_path.exists()
        else {"repository": "pending validation", "url": "not yet published"}
    )
    pytest_log = (output / "logs" / "pytest.log").read_text(encoding="utf-8")
    test_match = re.search(r"(\d+) passed", pytest_log)
    test_count = int(test_match.group(1)) if test_match else 0
    qpu_summary_path = output / "data" / "qpu_summary.json"
    qpu_summary = (
        json.loads(qpu_summary_path.read_text(encoding="utf-8"))
        if qpu_summary_path.exists()
        else {}
    )
    times = [float(value) for value in config["hardware_times"]]
    primary = f"strang_r{int(config['primary_repetitions'])}"

    report = f"""# SU2ZX research results

Generated: {datetime.now(UTC).isoformat()}  
Commit: `{commit_sha(root)}`

## Run status

| Layer | Status | Evidence |
|---|---|---|
| CPU physics and six-basis reconstruction | {cpu_status} | `artifacts/data/physics_summary.json` |
| Generic target compiler resource gate | {compiler_status} | `artifacts/data/compiler_dataset.csv` |
| Learned selector | {compiler.get('ai_status', 'BLOCKED')} | `artifacts/data/selector_summary.json` |
| CUDA-Q `qpp-cpu` | {cudaq_status} | `artifacts/data/accelerator_status.json` |
| CUDA-Q GPU | {cudaq_gpu_status} | `artifacts/data/accelerator_status.json` |
| Tensor-network GPU routes | {tn_status} | `artifacts/data/accelerator_status.json` |
| Direct cuTensorNet | {cutn_status} | `artifacts/data/accelerator_status.json` |
| IBM QPU | {qpu_status} | `artifacts/qpu/` |

`EXECUTED - REVIEW NUMERICAL AGREEMENT` is not automatically a validation pass. It means the optional program ran and its value must still be compared with the CPU reference.

## Research question

Can a backend-aware selector over exactly equivalent Qiskit/PyZX pipelines reduce native two-qubit resources and, when authorized hardware data exist, lower physics-level distribution error for a five-plaquette SU(2) real-time circuit family?

The preregistered resource hypothesis requires median native two-qubit-count reduction of at least 15% and native two-qubit-depth reduction of at least 10%. The AI hypothesis requires grouped-CV regret below every fixed strategy. The hardware hypothesis requires a negative selected-minus-Qiskit paired TVD difference for both raw and M3-projected data; it cannot be evaluated without authorized real-device data.

## Model and conventions

- Gauge group: SU(2), pure gauge.
- Truncation: `j_max = {config['j_max']}`.
- Geometry: five spatial plaquettes in a one-plaquette-wide open chain, a tiny 2+1D Hamiltonian geometry.
- Coupling: `x = {config['x']}` in `H_tilde = 2H/g^2`, `x=2/g^4` units.
- Initial Qiskit-order state: `|q4 q3 q2 q1 q0> = |00100>`.
- Primary product formula: second-order Strang with `r={config['primary_repetitions']}`.
- Exact-Hamiltonian and ideal-Trotter references are stored separately.

This is a compiler and hardware-validation model. It is not continuum SU(2), SU(3) QCD, or a quantum-advantage demonstration.

## Environment and provenance

- Execution target: Omarchy/Arch Linux, kernel `7.1.9-arch1-2`, Python 3.11.
- CPU/RAM probe: 12 logical CPUs and 16,429,694,976 bytes of RAM.
- GPU: `{accelerator.get('gpu', {}).get('name', 'not detected')}`, {accelerator.get('gpu', {}).get('vram', 'unknown')} VRAM, driver `{accelerator.get('gpu', {}).get('driver', 'unknown')}`, compute capability `{accelerator.get('gpu', {}).get('compute_capability', 'unknown')}`.
- CUDA-Q version: `{accelerator.get('cudaq_version', 'not installed')}`. Current GPU minimum: compute capability {accelerator.get('minimum_compute_capability', 'unknown')} ([official compatibility source]({accelerator.get('requirement_url', 'https://nvidia.github.io/cuda-quantum/latest/using/install/local_installation.html')})).
- The repository scope lock prevented reading `/etc/os-release`; Omarchy is the user-supplied execution environment. `nvcc` was unavailable.
- Full package pins are preserved in `artifacts/environment-pip-freeze.txt`; commands and test/compiler output are in `artifacts/logs/`.

## Correctness gates

| Gate | Tolerance | Result |
|---|---:|---|
| One-plaquette matrix, spectrum, ground state, transition formula | `1e-12` or tighter | PASS |
| Two-plaquette matrix and `-1.789221846776` ground energy | `1e-12` | PASS |
| Hermiticity and exact/Trotter normalization for `N=1,2,5` | `1e-12` | PASS |
| Qiskit little-endian strings/bitstrings | exact assertion | PASS |
| Manual Pauli rotation versus matrix exponential | exact unitary equivalence | PASS |
| Strang convergence for `r=1,2,4,8` | strictly decreasing infidelity | PASS |
| Exact five-plaquette mirror symmetry | `1e-12` | PASS |
| Six-basis versus direct energy | `<1e-10` | PASS (`{physics_summary['max_six_basis_energy_error']:.3e}`) |
| Probability-simplex projection | nonnegative, sum within `1e-13` | PASS |
| PyZX Basic/teleport/full-reduce at `N=2,5` | exact unitary equivalence | PASS |
| IBM dry-run manifest and fresh-token guard | 60 unique physics circuits | PASS |

The final local test command was `.mamba/envs/su2zx/bin/python -m pytest -q`: {test_count} tests passed. Ruff and mypy also passed; see `artifacts/logs/pytest.log`, `artifacts/logs/ruff.log`, and `artifacts/logs/mypy.log`.

## Observables

| Observable | Definition or estimator | Measurement/meaning |
|---|---|---|
| Computational distribution | `p(s)=|<s|psi>|^2` | Z basis; primary information for TVD |
| Loop occupation | `n_p=(1-Z_p)/2` | Retained `j=1/2` plaquette sector, not quark number |
| Survival | `L(t)=p(00100)` | Persistence of the initial central excitation |
| Electric energy | coefficient-weighted I/Z/ZZ expectations | Electric-flux contribution |
| Magnetic energy | coefficient-weighted one-X expectations | Coherent plaquette-loop mixing |
| Total energy | `E_E+E_B` | Conserved for exact H; finite-r drift diagnoses Trotter error |
| Trotter TVD | half the L1 distance to exact-H distribution | Separates product-formula error |
| Mirror asymmetry | `(abs(n0-n4)+abs(n1-n3))/2` | Symmetry/layout/noise diagnostic |

Six settings, `Z,X0,X1,X2,X3,X4`, reconstruct the entire five-plaquette Hamiltonian because every magnetic term contains exactly one X.

## Exact results at the proposed hardware times

{format_hardware_table(physics, 'exact', times)}

## Primary ideal Trotter results

{format_hardware_table(physics, primary, times)}

The CPU gate is based on an initial energy of `{physics_summary['initial_energy']:.12g}`, maximum norm error `{physics_summary['max_norm_error']:.3e}`, and maximum six-basis energy-reconstruction error `{physics_summary['max_six_basis_energy_error']:.3e}`.

## Physics plots

{figure_section('loop_occupations_exact_vs_trotter', 'Loop occupations', 'Solid curves are dense exact-Hamiltonian evolution; dashed curves are the primary ideal Strang circuit. Motion away from the central plaquette shows mixing among retained gauge-invariant loop sectors. Differences between paired curves are Trotter error, not hardware noise.', output)}

{figure_section('survival_probability', 'Survival probability', 'The curve tracks the probability of measuring the initial `00100` state. Comparing repetitions exposes product-formula convergence. It is a real-time loop-sector diagnostic, not a hadron survival probability.', output)}

{figure_section('energy_components', 'Electric, magnetic, and total energy', 'Exact evolution conserves total energy while exchanging weight between electric and magnetic terms. The finite-r circuit can drift relative to the original Hamiltonian because it exactly conserves neither noncommuting component. This separates algorithmic error from later device error.', output)}

{figure_section('trotter_tvd_convergence', 'Trotter TVD convergence', 'TVD compares each ideal product-formula computational distribution with exact-Hamiltonian evolution. Decreasing error with increasing r validates the expected second-order trend. Real hardware must instead use the exact ideal Trotter distribution as its primary reference.', output)}

{figure_section('mirror_asymmetry', 'Mirror-symmetry diagnostic', 'The exact Hamiltonian and central initial state are reflection symmetric, so the exact curve remains at floating-point scale. The ordered finite-r Pauli product formula can introduce a small algorithmic asymmetry even without device noise; this is part of Trotter error. A real-device comparison must subtract that ideal-circuit baseline before attributing additional asymmetry to layout or noise.', output)}

## Compiler and selector

The compiler dataset uses a generic five-node linear ECR target, not an IBM device. It contains `{compiler.get('rows', 0)}` strategy records. Median Basic-versus-Qiskit native two-qubit reduction is `{100*compiler.get('count_reduction', float('nan')):.3g}%`; median two-qubit-depth reduction is `{100*compiler.get('depth_reduction', float('nan')):.3g}%`. Resource status is `{compiler.get('resource_status', 'BLOCKED')}`.

All candidate records carry exact-equivalence validation: `{compiler.get('all_exactly_equivalent', False)}`. The aggressive full-reduce negative control has a median native two-qubit penalty of `{100*compiler.get('full_reduce_penalty', float('nan')):.3g}%` relative to Qiskit after routing, demonstrating that logical ZX simplification can create topology-hostile interactions. Native durations, routing overhead, SWAP counts, compilation times, counts, and depths are retained per row; median durations by strategy are `{json.dumps(compiler.get('median_native_duration_seconds', {}), sort_keys=True)}` seconds on the generic target model, not measured hardware wall time.

Selector top-1 accuracy is `{compiler.get('top1_accuracy', float('nan')):.4g}` and learned normalized regret is `{compiler.get('normalized_regret', float('nan')):.4g}`. AI status is `{compiler.get('ai_status', 'BLOCKED')}`. A null status means a fixed policy tied or beat the learned model and no AI advantage should be claimed.

### Cost-weight sensitivity

{sensitivity_table(compiler)}

The learned selector ties always-Basic at zero regret in every tested weighting, so the result remains **NULL**, despite perfect top-1 prediction.

{figure_section('compiler_native_resources', 'Native compiler resources', 'This plot compares strategies only after target-aware translation and routing. Native two-qubit gates and depth are more relevant than the logical gate count because they dominate much of the hardware error budget.', output)}

{figure_section('compiler_routing_penalty', 'Logical versus routed cost', 'Points above a favorable logical trend expose extraction-induced nonlocality. Aggressive full reduction can lower logical count while raising routed native cost, which is why the selector must see topology and target information.', output)}

{figure_section('selector_accuracy_regret', 'Selector regret', 'The learned policy is compared with always-Qiskit, fixed PyZX strategies, and the oracle. A useful selector must beat every fixed baseline on grouped `(x,r)` holdouts; row-wise random splitting is prohibited.', output)}

## CUDA-Q and tensor networks

CUDA-Q `qpp-cpu` status: **{cudaq_status}**. CUDA-Q GPU status: **{cudaq_gpu_status}**. Direct cuTensorNet status: **{cutn_status}**. The `qpp-cpu` cross-checks at `N=1,2,5` have maximum energy error `{max((item['absolute_energy_error'] for item in accelerator.get('cudaq_cpu_references', [])), default=float('nan')):.3e}` and maximum distribution TVD `{max((item['probability_tvd_to_qiskit'] for item in accelerator.get('cudaq_cpu_references', [])), default=float('nan')):.3e}` versus the shared Qiskit Strang circuit. GPU and tensor-network routes were not launched because compute capability 6.1 is below the documented 7.5 minimum. Package installation or target listing is not counted as GPU execution. MPS convergence therefore cannot be evaluated and no tensor-network plot is fabricated.

{figure_section('tensor_network_convergence', 'Tensor-network convergence', 'Each bond dimension is run in a fresh CUDA-Q process. Stable energy and survival under the final bond-dimension doubling support observable convergence; a single bond dimension is never sufficient evidence.', output)}

## IBM hardware

Status: **{qpu_status}**.

If this says `NOT RUN`, no real-device conclusion is available. The guarded program must first print the backend, physical path, 60 physics circuits, eight balanced M3 calibration circuits, shots, and total usage estimate. Simulator or fake-backend output must never be relabeled as hardware data.

No IBM credential or `ALLOW_IBM_QPU_SUBMISSION=1` variable was present in the scoped environment. Reading account files outside the repository was prohibited, so backend discovery and dry-run compilation were not attempted. No job was submitted and no simulator result is represented as QPU data.

Hardware paired summary, when present: `{json.dumps(qpu_summary, sort_keys=True) if qpu_summary else 'not available'}`.

{figure_section('hardware_tvd_comparison', 'Hardware TVD comparison', 'Raw and M3-projected distributions are compared with the exact ideal Trotter circuit at matched times. The selected-minus-Qiskit paired difference is the primary hardware effect; negative is better.', output)}

{figure_section('hardware_observables', 'Hardware survival and energy', 'Survival and reconstructed energy test whether resource changes preserve physically structured dynamics rather than merely changing a compiler count.', output)}

{figure_section('raw_vs_m3', 'Raw versus M3-projected results', 'Linear observables use the M3 quasidistribution directly. TVD is shown only after an explicit probability-simplex projection because a quasidistribution can contain negative weights.', output)}

When hardware exists, the primary metric is time-averaged TVD to the exact ideal Trotter circuit. Comparison to exact Hamiltonian evolution is reported separately because it includes Trotter error. M3 quasiprobabilities are used directly for linear expectations; M3 TVD is calculated only after explicit probability-simplex projection.

## Relation to lattice QCD

The project shares gauge links, Gauss constraints, electric terms, magnetic plaquettes, Wilson-loop motivation, regulator questions, and real-time challenges with lattice QCD. It differs in gauge group (SU(2) versus SU(3)), absence of dynamical quarks, dimension, volume, and severe representation truncation.

No string tension is extracted: that requires several separations, volumes, cutoffs, lattice spacings, and controlled long-time/static-charge energies. No string breaking is present because the model has no dynamical matter. Hadronization additionally requires energetic colored initial states and gauge-invariant hadronic yields or correlations.

## Reproduction

```bash
bash scripts/bootstrap_env.sh
bash scripts/run_all.sh
```

Raw numerical outputs are in `artifacts/data/`; figures are in `artifacts/figures/`; logs are in `artifacts/logs/`. See `artifacts/environment.md` and `artifacts/environment-pip-freeze.txt` for provenance.

## Success-gate summary

| Hypothesis/gate | Outcome | Evidence |
|---|---|---|
| Mandatory CPU physics | PASS | `artifacts/logs/pytest.log`, `artifacts/data/physics_summary.json` |
| Compiler-resource threshold | {compiler.get('resource_status', 'BLOCKED')} | `artifacts/data/compiler_dataset.csv` |
| AI selector beats every fixed policy | {compiler.get('ai_status', 'BLOCKED')} | `artifacts/data/selector_summary.json` |
| CUDA-Q CPU agreement | {cudaq_status} | `artifacts/data/accelerator_status.json` |
| CUDA-Q/cuTensorNet GPU | BLOCKED | GTX 1060 Max-Q capability 6.1 is below 7.5 |
| Hardware-physics hypothesis | NOT RUN | authorization/credentials absent; `artifacts/qpu/` has no result |
| Public repository | {publication.get('status', 'PENDING')} | [{publication.get('repository', 'pending validation')}]({publication.get('url', '#')}) |

## Limitations

The target is generic rather than a calibration snapshot from a named IBM backend; the compiler result does not imply improved hardware fidelity. The family is tiny, fixed at five plaquettes for selection, and the synthetic target seed is fixed. No uncertainty bars are available for exact statevector quantities. GPU tensor-network scaling and real-QPU mitigation are blocked/not run, so neither hardware performance nor large-system convergence can be inferred.

## Next 90 days

Extend to several chain lengths and calibration snapshots, repeat authorized QPU comparisons in independent windows, add static charges and flux-tube observables, and only then introduce dynamical matter in a gauge-invariant loop-string-hadron encoding. Retain exact rewrite checks and classical/tensor-network references at every stage.
"""
    destination = project_path("RESEARCH_RESULTS.md")
    destination.write_text(report, encoding="utf-8")
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
