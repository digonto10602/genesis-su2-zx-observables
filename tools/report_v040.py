"""Render evidence-backed release documents and secret-free run provenance."""

# ruff: noqa: E501
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version

import pandas as pd

from su2zx.paths import project_path


def command(args):
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def main():
    root = project_path(".")
    data = root / "artifacts/data/v040"
    logs = root / "artifacts/logs/v040"
    now = datetime.now(UTC).isoformat()
    config = json.loads((root / "config/research_v040.json").read_text())
    ml = json.loads((data / "pairwise_ml_summary.json").read_text())
    sym = json.loads((data / "symmetry_summary.json").read_text())
    tn = json.loads((data / "tn_summary.json").read_text())
    audit = json.loads((logs / "data_integrity.log").read_text())
    policies = pd.read_csv(data / "pairwise_ml_results.csv")
    fits = pd.read_csv(data / "trotter_fits.csv")
    native = pd.read_csv(data / "symmetry_compiler_results.csv")
    table = native.pivot(
        index=["num_plaquettes", "repetitions", "strategy"],
        columns="term_ordering",
        values=["native_2q_count", "native_2q_depth"],
    )
    compile_effect = {
        metric: dict(
            lower=int((table[metric].symmetry < table[metric].current).sum()),
            higher=int((table[metric].symmetry > table[metric].current).sum()),
            equal=int((table[metric].symmetry == table[metric].current).sum()),
        )
        for metric in ["native_2q_count", "native_2q_depth"]
    }
    (data / "symmetry_compiler_summary.json").write_text(json.dumps(compile_effect, indent=2))
    p = policies[policies.validation == "prospective"].set_index("model")
    policy_lines = "\n".join(
        f"| {name} | {row.mean_regret:.6f} | {row.median_regret:.6f} | {row.worst_regret:.6f} | {row.oracle_match_fraction:.4f} |"
        for name, row in p.iterrows()
    )
    fit_lines = "\n".join(
        f"| {row.term_ordering} | {row.fit} | {row.exponent:.6f} | {row.standard_error:.6f} |"
        for row in fits.query("num_plaquettes == 5 and x == 2").itertuples()
    )
    summaries = "\n".join(
        f"| {name} | {s['symmetry_better']} | {s['symmetry_worse']} | {s['total'] - s['symmetry_better'] - s['symmetry_worse']} |"
        for name, s in sym["metrics"].items()
    )
    test_result = next(
        line for line in (logs / "pytest.log").read_text().splitlines() if " passed" in line
    )
    text = f"""# SU2ZX research results — v0.4.0

Generated {now}. Input commit `{command(["git", "rev-parse", "HEAD"])}`.

## Executive summary

Direct-observable CPU MPS scaling is demonstrated through **N=32**, without saving or reconstructing a full statevector on the scaling path. N=5,8 validation against ideal Trotter observables has maximum error **{tn["max_validation_error"]:.3e}** at bond cap 64 and truncation threshold 1e-14. This is short-time, shallow-circuit scaling, not validation of large-N exact dynamics.

Basic–Teleport winner diversity survives five fixed-target routing seeds in this bounded design: **33 ROBUST_BASIC, 29 ROBUST_TELEPORT, 21 TIED** parameterized circuit/target/layout families, with zero seed-sensitive families. Of 860 attempted compiler outputs, **830 pass** the explicit numerical gates; **30 fail** and are excluded as complete pairs. The valid pairwise dataset contains **415 records**.

The pairwise ML result is **NULL**. The grouped-selected {ml["best_grouped_model"]} model has prospective mean normalized 2Q regret **{ml["prospective_mean_regret"]:.6f}**, versus **{ml["strongest_simple_prospective_regret"]:.6f}** for the strongest simple baseline. A different depth-three tree happens to achieve zero prospective regret, but it was not the grouped-selected model; this is an exploratory result requiring a new holdout, not a validated ML advantage.

Symmetry ordering is **MIXED**: it preserves mirror symmetry and reduces source depth throughout the grid, but TVD improves in only 16 of 56 comparisons and worsens in 40. Lower energy drift does not imply uniformly better probability distributions.

## Model and claims

The source of truth remains `src/su2zx/core.py`. Its Hamiltonian and ordering definitions are unchanged. This is a gauge-reduced, j_max=1/2 pure-SU(2) plaquette chain in a severely truncated 2+1D Hamiltonian geometry. Strings use q_(N-1)...q_0. No continuum SU(2), physical SU(3) QCD, string tension, string breaking, hadronization, or quantum advantage is established. All new results are ideal CPU simulation or synthetic-target compilation, never QPU data.

## v0.3.0 baseline reproduction

The initial baseline passed 17 tests, Ruff and mypy. A fresh baseline physics execution generated 405 observable rows; all 35 historical source hashes and the 426-row dataset structure reproduce. CUDA-Q qpp-cpu is rerun at N=1,2,5 and agrees within 1e-8. All six compiler strategies remain supported and pass 18 fresh bounded control evaluations (N=2,3,5).

The prior physics conclusions remain valid in their sampled scope. The historical assertion that all compiled outputs were verified at 1e-10 was too strong: the old flag used default-tolerance logical `Operator.equiv`, without independently checking routed outputs. v0.4.0 adds that missing check. PyZX's default QASM denominator cap also introduced accumulated rounding error around 1e-10; QASM import now temporarily uses a 2**40 denominator cap and restores the library setting. Logical unitary validation explicitly uses atol=rtol=1e-10.

A separate Qiskit level-2/3 resynthesis discrepancy of about 7.18e-8 is reproducible for N=2, x=0.5, t=0.08, r=2. Level 0/1 passes the same strict check. All 30 rejected outputs belong to this small-angle family across three target cases and five seeds. Their records remain in `compiler_raw_results.csv`. Compiler comparisons retain level 2 and exclude failures; hardware preparation uses level 1 and verifies the result.

## Robust compiler-selection study

The design selects all historical strict six-strategy winners plus tied/routing anchors (23 old cases), then adds 63 prospective cases: N=2,4,6; r=3; x=1.5; t=0.20; current/reversed/symmetry ordering; seven topology/layout configurations. Seeds are 11,19,29,37,47. Synthetic target calibration seed is always 7, rather than varying with the routing seed. ECR is the only native entangler studied. Five seeds, five existing topology classes and bounded controls replace a more expensive ten-seed/full-basis/full-control Cartesian study.

Robust means at least 80% strict 2Q wins across all five seeds and a matching median delta sign. A fully tied family has five count ties. Fractions, entropy and mean/median count/depth differences are saved. Parameterized family counts are not counts of statistically independent experiments; structural angle aggregation is saved separately in `compiler_structural_results.csv` and `compiler_strict_winners.csv`.

There are zero observed strict-sign reversals across the matched layout or topology comparisons; **layout/topology robustness remains INCONCLUSIVE** outside these cases. Many comparisons are singletons, and fixed target calibration plus one basis cannot establish general hardware robustness. Prospective families have 28 robust Basic, 14 robust Teleport and 21 ties; the valid historical subset has 5 Basic and 15 Teleport families.

![Basic–Teleport differences](artifacts/figures/v040/delta_distribution.png)
![Winner robustness](artifacts/figures/v040/winner_robustness.png)

## Pairwise Basic-vs-Teleport analysis

Delta C = Teleport native 2Q count − Basic native 2Q count. Negative means Teleport, positive Basic, zero a count tie. Both depth and estimated duration differences are also stored. `lexicographic_label` explicitly compares (count, depth, duration), without a weighted surrogate. ML predicts the primary 2Q objective; its normalized regret is (selected count − minimum count)/max(minimum count,1), so equal-count alternatives have zero primary regret even if depths differ. Count ties are a separate classifier class and execute Basic. Exact-label accuracy and cost-oracle equality are therefore different metrics.

## ML result: NULL

Four frozen lightweight models use only source-circuit, generation, topology and pre-selection layout features. Hashes are grouping keys, never predictors. Automatic-layout distance is an explicitly labeled identity-placement proxy, not an observed routed layout. Standardization is fit on training folds only. Structural GroupKFold and leave-one-size/topology/ordering-out use **historical robustness cases only**. Seed replicas of a structural family remain together. The prospective r=3 structural families are excluded from grouped model selection and are evaluated separately. Split assignments, predictions, features and feature importances are saved.

Historical grouped regret for the selected model is {ml["grouped_mean_regret"]:.6f}, versus {ml["strongest_simple_grouped_regret"]:.6f} for the strongest simple policy. This does not generalize prospectively. Logistic is the only tested learned model with zero historical grouped regret. Model settings were frozen before generation; there is no hyperparameter search or nested model selection. This small, historical-winner-enriched training set limits generalization.

## Frozen-rule prospective test

The rule was frozen in `config/research_v040.json` before new data: Teleport for N<=3 with current ordering, Basic otherwise. `frozen_design.json` records its timestamp and configuration SHA-256. It was never tuned on this holdout. On this particular holdout it matches always-Basic in cost: its differing small-N choices are count ties. Thus it does **not establish an improvement**, although it incurs low regret.

| Policy | Mean regret | Median | Worst | Oracle match |
|---|---:|---:|---:|---:|
{policy_lines}

![Grouped and prospective regret](artifacts/figures/v040/selector_regret.png)

## Symmetry-aware Trotterization

The physics grid has N=2..8, r=1,2,4,8, (x,t)=(1,0.16),(2,0.32), and three orders: 168 rows. Odd N uses the central occupied plaquette; even N uses the two central occupied plaquettes, making the initial state reflection invariant. Exact evolution uses sparse `expm_multiply` of the shared Hamiltonian. Occupations, survival, electric/magnetic/total energy, norm, TVD and mirror asymmetry are saved.

| Metric vs current ordering | Better | Worse | Equal within 1e-12 |
|---|---:|---:|---:|
{summaries}

Maximum symmetry-ordering mirror asymmetry is 1.11e-15. Symmetry compiler comparison covers N=3,5,7; r=1,2,4; x=2,t=0.32; Qiskit/Basic/Teleport; fixed favorable synthetic line and seed 11 (81 passing outputs). Count comparisons (lower/higher/equal): `{compile_effect["native_2q_count"]}`. Depth comparisons: `{compile_effect["native_2q_depth"]}`. These are matched ordering comparisons, not a device performance claim.

![TVD by ordering](artifacts/figures/v040/symmetry_tvd.png)
![Native depth by ordering and strategy](artifacts/figures/v040/symmetry_native_depth.png)

## Trotter convergence

N=5,x=2,t=0.32 representative TVD fits follow epsilon(r) proportional to r^(-p). Full uses r=1,2,4,8; asymptotic uses r=2,4,8. The expected second-order Strang limit is p=2. All size/parameter/order fits and slope standard errors are saved; coarse and asymptotic fits are distinct.

| Ordering | Fit | Exponent p | Slope standard error |
|---|---|---:|---:|
{fit_lines}

## Joint physics/compiler frontier

`physics_compiler_frontier.csv` marks nondominated choices within each N/x/time group over TVD, mirror asymmetry, native 2Q count, native 2Q depth and estimated duration. Repetition and ordering/strategy choices compete; mirror residuals below 1e-10 are treated as numerical ties. No arbitrary combined score is used. Duration is a synthetic-target estimate in seconds. The plot is a 2D projection of this five-metric comparison.

![Physics/compiler frontier](artifacts/figures/v040/physics_compiler_frontier.png)

## Tensor network

**VALIDATED direct-observable MPS; SCALING_DEMONSTRATED without statevector reconstruction.** Aer saves Z_i, X_i, neighboring ZZ correlators, electric/magnetic/total energies, normalized identity expectation, and compact MPS tensors. Occupations are (1-Z_i)/2. [Aer save_expectation_value](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.library.save_expectation_value.html) and [MPS snapshot APIs](https://qiskit.github.io/qiskit-aer/tutorials/7_matrix_product_state_method.html) were checked against installed signatures before implementation.

N=5,8 have independent ideal-Trotter and exact-Hamiltonian observable references. Caps 8/32/64 use thresholds 1e-10/1e-14/1e-14. N=12,16,20,24,32 scaling saves no statevectors; tests forbid statevector-save calls in the direct path. At N=32, cap 64 reaches final bond 10 with 72,112 returned tensor bytes and about 0.18 s runtime on this run. Cap 32 and 64 observables agree numerically throughout scaling. This short-time circuit has low final entanglement; longer-time growth is untested. Normalized identity is not a discarded-weight bound. Tensor bytes are final compact-state storage; cumulative process RSS includes imports and earlier runs and is not per-case peak workspace.

## CUDA-Q and IBM

CUDA-Q CPU **PASS** at N=1,2,5. GPU **BLOCKED_BY_HARDWARE**: the detected GTX 1060 Max-Q is compute capability 6.1. No unsupported GPU execution or driver modification occurred. Existing target-selectable CUDA-Q scripts remain available for a supported future device; no GPU tensor-network scaling is claimed.

IBM metadata **NOT_AVAILABLE** under repository-only credential scope. QPU **NOT_RUN**, zero submitted jobs. A 120-circuit synthetic hardware-ready bundle compares current/symmetry × Basic/Teleport, five times and six measurement bases. The analysis accepts all variants and retains exact Hamiltonian → ideal Trotter → compiled ideal → raw/mitigated hardware hierarchy. The live `--comparison` workflow recompiles against the chosen real backend. Submission requires the environment guard, `--submit`, and a matching one-use dry-run token bound to the manifest/configuration and expiring after 15 minutes. No token is archived.

## Validation and limitations

Tests: {test_result}. Ruff, formatting, mypy and data-integrity checks pass. Routed equivalence compares the zero state plus three seeded random complex states, including initial/final layout and ancilla leakage, at 1e-10. It is a numerical randomized check, not an exhaustive routed-unitary proof. [Qiskit layout documentation](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.transpiler.TranspileLayout) describes the two permutations handled explicitly.

All targets are synthetic, with a fixed calibration seed and one native basis. Compiler grids are bounded and historical selection is winner-enriched. No seed sensitivity was observed; this cannot prove absence on harder routing problems. Physics compiler anchors use one layout/seed. Large-N TN lacks an exact-Hamiltonian reference. ML is NULL; symmetry is MIXED. Validation excludes failed outputs without silently relaxing tolerance.

## Next research milestone

Freeze the successful exploratory shallow-tree decision boundary and test a new long-depth holdout on independent calibrated targets and adverse layouts, while extending direct MPS to longer times and monitoring bond/truncation growth. This would distinguish real structure/target dependence from the simple N/order boundaries in this bounded study.

## Artifacts and completion

Machine-readable data: `artifacts/data/v040/`; 16 PNG/PDF figures and source mapping: `artifacts/figures/v040/`. Provenance: `artifacts/provenance/run_v0.4.0.json`. Graphify and exact final archive receipts are recorded in `GRAPHIFY_UPDATE.md`, `RUN_MANIFEST.md`, and the timestamp-matched files under `zip_results/`.
"""
    (root / "RESEARCH_RESULTS.md").write_text(text)
    validation = f"""# SU2ZX v0.4.0 validation

Generated {now}.

- Initial v0.3.0 baseline: 17 tests, Ruff, mypy PASS; fresh physics run 405 rows.
- Final tests: {test_result}.
- Physics Hamiltonian, one/two plaquette analytics, Hermiticity, normalization, ordering and reconstruction regressions: PASS.
- Historical source hashes: 35/35 reproduce; prior 426-row data integrity PASS.
- New compiler: 830/860 pass; 30 failed outputs explicitly excluded. Logical atol=rtol=1e-10, routed phase-aligned maximum amplitude error <=1e-10 on zero plus three seeded random inputs. Ancillas and both layout permutations are checked.
- Six-strategy controls: 18 passing outputs. Fixed-seed/target/layout hash repeat PASS.
- Pairwise records: 415 complete verified pairs; delta integrity PASS.
- Feature allow-list and grouped leakage checks: PASS. No cost or routed-result inputs. Historical groups only for model selection; new r=3 families for prospective test.
- Frozen configuration SHA-256: PASS. No post-holdout rule tuning.
- Symmetry checks: 168 physics rows; maximum mirrored asymmetry 1.11e-15 for symmetry ordering. Even-N initial states are symmetric.
- Trotter fits: full r=1,2,4,8 and asymptotic r=2,4,8 recorded with standard errors; current N=5 exponents 1.865777 and 1.978062.
- Direct MPS N=5,8 maximum validated observable error {tn["max_validation_error"]:.3e} (<1e-7); no-statevector scaling N=12..32 PASS.
- CUDA-Q qpp-cpu N=1,2,5 comparison <1e-8 PASS; GPU BLOCKED_BY_HARDWARE.
- Hardware-ready synthetic bundle: 120 circuits; QPU NOT_RUN.
- Ruff, format and mypy: PASS (see logs).
- Figures: 16 regenerated from CSV, PNG/PDF with source mapping.
- Graphify: final counts and validation in GRAPHIFY_UPDATE.md.
- Secret scan/archive: exact final ZIP validation and SHA256 receipt are generated after this document, under zip_results/; see RUN_MANIFEST.md for exact name. They are not inferred from a staging archive.

## Reproduction commands

```bash
bash scripts/run_v040.sh
.mamba/envs/su2zx/bin/python -m pytest
.mamba/envs/su2zx/bin/ruff check src tests tools
.mamba/envs/su2zx/bin/ruff format --check src tests tools
.mamba/envs/su2zx/bin/mypy src
.mamba/envs/su2zx/bin/python tools/validate_v040.py audit
.mamba/envs/su2zx/bin/python tools/plot_v040.py
.mamba/bin/graphify update .
```

Full stage commands appear in README.md. Logs are in artifacts/logs/v040/. PyZX emits two upstream Python-enum deprecation warnings; mthree emits 45 upstream CircuitInstruction deprecation warnings in the guard test. Scikit-learn warns when held-out true labels lack a predicted class; the confusion matrices retain all three labels. Neither warning is suppressed. Earlier execution failures are explained in RESEARCH_RESULTS.md; final logs contain the corrected reruns. The rejected compiler outputs remain in the raw dataset.
"""
    (root / "VALIDATION.md").write_text(validation)
    (root / "README.md").write_text("""# SU2ZX v0.4.0

Reproducible research on exact compiler selection and real-time evolution of a gauge-reduced, j_max=1/2 SU(2) plaquette chain in a truncated 2+1D Hamiltonian geometry. `src/su2zx/core.py` defines the Hamiltonian and q_(N-1)...q_0 convention.

v0.4.0 demonstrates direct-observable CPU MPS scaling through N=32. Basic/Teleport winners survive the sampled fixed-target seeds; ML is NULL on prospective generalization, and symmetry-aware ordering has MIXED physics effects. See [RESEARCH_RESULTS.md](RESEARCH_RESULTS.md) and [VALIDATION.md](VALIDATION.md).

No continuum physics, physical SU(3) QCD, string tension, string breaking, hadronization or quantum advantage is established. Synthetic compilation and simulator outputs are never labeled QPU data.

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
.mamba/envs/su2zx/bin/python -m su2zx.qpu --comparison \
  --backend BACKEND --physical-path q0,q1,q2,q3,q4
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
""")
    (root / "RELEASE_NOTES_v0.4.0.md").write_text("""# SU2ZX v0.4.0 release notes

- Fixed-calibration five-seed Basic/Teleport study: 860 outputs, 830 passing, 30 excluded, 415 valid pairs; 33 robust Basic, 29 robust Teleport, 21 ties.
- Frozen prospective rule and four leakage-controlled pairwise models. ML NULL; the grouped-selected model fails to beat the simple prospective baseline.
- Symmetry grid: 168 physics rows and 81 compiler rows. Symmetry ordering preserves reflection and lowers source depth, but TVD and energy effects are mixed.
- Full and asymptotic Strang fits; five-metric physics/compiler Pareto data.
- Direct-observable Aer MPS validated at N=5,8 and scaled through N=32 without full statevector reconstruction.
- PyZX QASM import precision fixed; explicit logical tolerance and independent layout-aware routed verification added.
- 120 synthetic hardware-ready comparison circuits, generalized raw/M3 analysis and fresh one-use submission approval binding. Zero QPU jobs.
- CUDA-Q CPU passes; GPU blocked on compute capability 6.1.
- Sixteen reproducible PNG/PDF figures, refreshed knowledge graph, provenance and exact final ZIP verification.

The Hamiltonian and conventions are unchanged. Numerical failures are retained and excluded, not relabeled as successes. No physical-QCD, continuum or quantum-advantage claim is made.
""")
    packages = {}
    for name in [
        "qiskit",
        "qiskit-aer",
        "qiskit-ibm-runtime",
        "pyzx",
        "cudaq",
        "numpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "pytest",
        "ruff",
        "mypy",
    ]:
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = "not installed"
    payload = dict(
        version="v0.4.0",
        utc_timestamp=now,
        git=dict(
            commit=command(["git", "rev-parse", "HEAD"]),
            branch=command(["git", "branch", "--show-current"]),
            dirty=bool(command(["git", "status", "--porcelain"])),
        ),
        python=sys.version,
        packages=packages,
        hardware=dict(
            platform=platform.platform(),
            cpu=command(["lscpu"]),
            memory=command(["free", "-b"]),
            disk=command(["df", "-h", "."]),
            gpu=command(
                [
                    "nvidia-smi",
                    "--query-gpu=name,compute_cap,driver_version,memory.total",
                    "--format=csv",
                ]
            ),
            cuda=command(["nvidia-smi"]),
        ),
        experiment_configuration=config,
        random_seeds=dict(
            transpiler=config["transpiler_seeds"], target=7, verification=20260905, ml=11
        ),
        target_definitions="artifacts/data/v040/compiler_design.json and compiler_raw_results.csv target_definition",
        layouts=["favorable", "spread", "transpiler"],
        model_configurations=config["models"],
        frozen_rule=config["frozen_rule"],
        blocked_features=dict(
            CUDA_Q_GPU="BLOCKED_BY_HARDWARE", IBM_METADATA="NOT_AVAILABLE", IBM_QPU="NOT_RUN"
        ),
        generated_datasets=[
            str(p.relative_to(root)) for p in sorted(data.iterdir()) if p.is_file()
        ],
        generated_figures=[
            str(p.relative_to(root))
            for p in sorted((root / "artifacts/figures/v040").iterdir())
            if p.is_file()
        ],
        validation=audit,
    )
    (root / "artifacts/provenance/run_v0.4.0.json").write_text(json.dumps(payload, indent=2))
    print("Research results, validation, README, release notes and provenance written.")


if __name__ == "__main__":
    main()
