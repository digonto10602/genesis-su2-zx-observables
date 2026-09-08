# SU2ZX status report — 2026-09-07

Repository: `SU2ZX` (v0.4.0 package plus the v0.5.0 "Section 8" run).
Git HEAD at report time: `eee1e162a0b28b4c8f6f8f917454e795efbea606`
("v0.5.0 run: G2 and G3 PASS", 2026-09-07 10:08 -0600). Working tree: nine
untracked paths (the Phase-4 work listed in §3.4) plus an edited
`.graphifyignore`. Nothing was committed by this report.

Every number below traces to a file in the repository; the path is given
next to it. No hardware (QPU) job has ever been submitted by this project.

---

## 1 Executive summary

| Area | State |
|---|---|
| v0.4.0 package (`src/su2zx`) | Complete, published, archived. 26/26 tests pass today. Graph refreshed. |
| v0.5.0 run, gates G0–G3 | PASS (G1 after one escalation; G3 on the L12 encoding only). Run tests today: 58/59 pass; the one failure is a stale test that contradicts decision D1 (§4.1). |
| v0.5.0 run, gate G4 (compile + twin) | IN PROGRESS. Routing done for three pipelines; twin simulation running; `GATE_G4.json` not yet written. Routed circuits are ~16× over the 2q-gate budget. |
| v0.5.0 gates G5–G9 | NOT STARTED (prereg, dry run, pilot/full run, analysis, packaging). |
| Graphify | Root graph 796→1459 nodes / 1258→2196 edges; run graph 820→830 nodes / 1087→1105 edges. Both validated (§6). |
| Reports | `runs/section8_v0.5.0_20260907T0628Z/reports/REPORT.md` and `SUMMARY.md` are STALE (written before G2/G3 passed). This file supersedes them for status purposes. |

The scientific core of v0.5.0 is established: the 82-state SU(2)-with-matter
single-plaquette Hamiltonian, built by two independent routes, agrees to
machine precision and is exactly gauge invariant. Exact dynamics, the
operating window, and a leak-free exact L12 circuit family exist. The
blocking problem for the rest of the plan is circuit cost: even after
structured synthesis, one Strang step needs about 3,976 native CZ after
routing on FakeTorino, against a budget of about 250.

---

## 2 Codebase layout and status

### 2.1 v0.4.0 package (repository root)

- `src/su2zx/`: `core.py` (Hamiltonian, conventions, Strang circuits, exact
  reference), `compiler_study.py`, `robust_study.py`, `scaling_study.py`,
  `tn_study.py`, `study.py`, `qpu.py`, `qpu_analysis.py`, `report.py`, `paths.py`.
- `tests/`: six files, 26 tests (rerun today: all pass, see §4.1).
- `tools/`: validation, plotting, provenance, archive, graph refresh helpers.
- Results: `RESEARCH_RESULTS.md`, `VALIDATION.md`, `RUN_MANIFEST.md`,
  `docs/V040_COMPLETION_AUDIT.md`, `docs/CODE_LOGIC_AND_TESTS.md`,
  `docs/CODE_FUNCTION_INVENTORY.md`. Data/figures/logs under `artifacts/`.
- Last archive: `zip_results/SU2ZX_v0.4.0_20260906T223709Z.zip` (225 files,
  SHA256 in the sidecar). Published to `digonto10602/genesis-su2-zx-observables`.
- Headline v0.4.0 conclusions (unchanged): direct-observable MPS scaling to
  N=32; Basic/Teleport compiler winners robust across five seeds; ML selector
  NULL; symmetry-aware ordering MIXED; CUDA-Q CPU PASS, GPU blocked by hardware;
  zero QPU jobs.

### 2.2 v0.5.0 run directory (`runs/section8_v0.5.0_20260907T0628Z/`)

Started 2026-09-07 06:28 UTC from `prompts/v0.5.0.md` (SU(2) with dynamical
matter on one plaquette, twin mode, FakeTorino target). All new code lives in
`src/su2qc/` (3,658 lines including tests):

| Module | Purpose | Lines |
|---|---|---:|
| `conventions.py` | Frozen geometry, signs, JW order, Hamiltonian normalization | 100 |
| `ham/route_spinnet.py` | Route 1: dressed-vertex spin-network construction | 775 |
| `ham/route_gausskernel.py` | Route 2: redundant KS space + Gauss-kernel projection | 487 |
| `ham/compare.py`, `ham/limits.py` | Cross-route comparison; limit tests | 242 |
| `dynamics/engine.py`, `scan.py`, `run_g2.py` | Exact evolution, mass scan, window selection | 481 |
| `encodings/l12.py` | 12-qubit encoding, 82 physical codes, leakage flags | 69 |
| `circuits/strang_l12.py`, `export_l12.py` | Exact block unitaries, Strang step, QPY/QASM export | 293 |
| `circuits/synth_l12.py` | Structured synthesis (Gray-path MCRX, Givens 3×3, phase polynomial D) | 307 |
| `compile/route.py`, `run_g4.py` | Routing to FakeTorino, PyZX passes, routed equivalence, twin driver | 278 |
| `twin/twin.py` | Aer noise twin, post-selection, observables, bootstrap | 116 |

Ledgers: `run/{GATES,DECISIONS,HEARTBEAT,TASKBOARD,PLAN,MODELS,INVENTORY,CONFIG_ENV}.md`.
Gate scripts and JSON: `gates/`. Physics artifacts: `physics/`. Tables and
figures: `analysis/`. Escalation record: `solutions/0.5.0.md` (repo root).

---

## 3 v0.5.0 gate ledger

| Gate | Status | Attempts | Finished (UTC) | Evidence |
|---|---|---:|---|---|
| G0 bootstrap | PASS | 1 | 06:30 | `gates/GATE_G0.json` (14/14) |
| G1 Hamiltonian by two routes | PASS | 3 (1 escalation) | 09:11 | `gates/GATE_G1.json` (17/17), `physics/signoff_G1.md` |
| G2 exact dynamics and window | PASS | 1 | 16:07 | `gates/GATE_G2.json` (20/20), `physics/signoff_G2.md` |
| G3 encodings and circuits | PASS (L12 only) | 1 | 16:07 | `gates/GATE_G3.json` (16/18; S8, C7 not built, decision D4) |
| G4 compile, twin, Plan-B decision | IN PROGRESS | – | – | `logs/cmd/run_g4.log`; `gates/gate_G4.py` written, no JSON yet |
| G5 prereg and rehearsal | NOT STARTED | – | – | `prereg/` empty |
| G6 dry run | NOT STARTED | – | – | `hardware/` empty |
| G7 pilot and full run | NOT STARTED | – | – | 0 QPU seconds |
| G8 analysis and ablations | NOT STARTED | – | – | – |
| G9 report, replication, packaging | PARTIAL | – | – | stale `reports/REPORT.md`; this report; zip in §7 |

### 3.1 G1: verified Hamiltonian

| Criterion | Target | Measured |
|---|---|---|
| dim at j_max=½ (route 1 / route 2) | 82 | 82 / 82 |
| dim at j_max=1 (route 1 / route 2 kernel) | 152 | 152 / 152 |
| Number sectors N=0,2,4,6,8 | 2,20,38,20,2 | exact, both routes |
| Hermiticity, [H,N] | ≤1e-13 | 0.0, 0.0 |
| Cross-route spectra, 6 coupling points | ≤1e-12 | 2.7e-15 |
| Stretched-string time series, t∈[0,10] | ≤1e-10 | 1.6e-15 |
| Gauss commutators, route 2, every term | ≤1e-12 | 0.0 |
| Pure-electric degeneracies | 16,16,18,16,16 | exact |
| Frozen-matter block vs monograph H̃₁ | ≤1e-8 (D3) | 3.0e-9 |
| Magnetic-off spectra | ≤1e-10 | 1.3e-15 |

The escalation (`solutions/0.5.0.md`) diagnosed that route 1 omitted
dressed-vertex recoupling factors. The fix was implemented by the orchestrator
after a delegated builder failed; independence therefore holds at the level of
construction method, not authorship (recorded in the run report and review).
A factor-2 magnetic normalization difference against `src/su2zx/core.py` is
documented in `physics/conventions_reconciliation.md` (map monograph results
via x_eff = x/2; no code change).

### 3.2 G2: exact dynamics and operating window

- Engine self-check: expm vs Krylov 2.3e-15; energy drift 4.4e-16; N drift 1.8e-15.
- Mass scan: 4 values of g² × 25 masses, 100 rows (`analysis/tables/exact_mass_scan.csv`).
- Window (`physics/window.json`): g²=4, m=0.75 (=3g²/16), δt=0.8333, r_max=3
  (t=2.5). Expected P_surv drop 0.993, pair weight 0.819, Strang error 0.019.
- Three discrepancies against the pre-registered predictions were adjudicated
  and signed off (`physics/DISCREPANCIES.md`, `physics/signoff_G2.md`):
  - D-A: the baryon–antibaryon channel dominates (max P_BB̄ 0.833 vs
    max P_meson 0.073); a one-plaquette geometric effect. Hypothesis wording
    must change to "BB̄-dominated channel split".
  - D-B: the time-averaged pair-weight estimator is flat in m and does not
    locate 3g²/16; the resonance is confirmed by exact level degeneracy instead.
  - D-C: truncation error j_max=1 vs ½ is 0.257 (>0.1). This is the leading
    systematic and must head the error budget.

### 3.3 G3: L12 encoding and exact circuits

- 82 physical codes; leakage flags verified on all 4,096 codes; stretched code 3793.
- Block unitaries exact on the physical subspace (dev 2.7e-14) with zero
  leakage; full Strang step matches the exact product; noiseless leakage
  probability 0.0.
- Trotter scaling at t=2.5, r∈{8,…,128}: slopes −2.10 (P_surv), −2.15 (E²),
  −2.01 (state) (`circuits/trotter_scaling.json`).
- Circuits exported for r=0..3 as QPY and OpenQASM 3 (`circuits/`, 146 MB;
  QPY files are git-ignored and excluded from the zip because of size).
- Generic synthesis cost: 45,875 CZ per Strang step (`circuits/resources_logical.md`).
- S8 and C7 encodings were not built (decision D4). The encoding-ablation
  secondary endpoint is therefore not available.

### 3.4 G4: compile and twin (in progress at report time)

Work done since the last commit (all untracked in git):

- `src/su2qc/circuits/synth_l12.py` + `tests/test_synth_l12.py`: structured
  synthesis. Exact to 1e-10 elementwise, leak-free. Cost per Strang step
  before routing: 15,360 two-qubit gates (`circuits/resources_synth.md`);
  the diagonal group D costs 16 and the plaquette group B 371, but each of the
  four hopping groups costs about 1,850 because multi-controlled rotations on
  6-qubit supports decompose expensively.
- `src/su2qc/compile/route.py`, `run_g4.py`, `src/su2qc/twin/twin.py`,
  `gates/gate_G4.py`: routing, PyZX comparison, routed equivalence, twin driver, gate.
- `run_g4.py` was started at 16:30 UTC and is still running (PID 1956816).
  Pipeline results so far (`logs/cmd/run_g4.log`):

| Pipeline | Step CZ | Step 2q depth | Full r=3 CZ | Full r=3 2q depth | Pre-route equivalence | Routed equivalence r=3 |
|---|---:|---:|---:|---:|---|---|
| Qiskit L3 | 3,976 | 3,300 | 12,142 | 9,695 | – | 3.5e-13 |
| PyZX basic (TP) | 4,603 | 3,990 | 13,914 | 12,042 | **0.996 (FAIL)** | not computed |
| PyZX full_reduce | 4,778 | 3,737 | 16,025 | 12,575 | 2.9e-13 | not computed |

Budget from the prompt: ≤250 CZ per step, ≤1,000 per circuit, 2q depth <200
(10 % slack). The best pipeline misses by factors of about 16, 12 and 48.
Qiskit L3 routed equivalence passes (3.5e-13 ≤ 1e-10). The PyZX basic pass
breaks equivalence (0.996), which is a defect in `route.pyzx_pass` for that
strategy, not a physics result; full_reduce is fine.

Twin progress at report time: routed equivalence for r=0..3 is 0, 1.3e-13,
2.4e-13, 3.5e-13 (all pass). The first twin point (r=0, t=0) gave
post-selection yield 0.690 and P_surv 0.946 against exact 1.000, reported as
outside 2σ. The printed 2σ was 0.000, which is implausible for five repeats of
4,000 shots; whether the five repeats received distinct simulator seeds in
`twin.run_counts` should be checked before any twin number is trusted.
At packaging time the twin was still simulating r=1 (about 35 minutes on that
point alone; r=2 and r=3 are two and three times deeper). The process was left
running. When it ends it writes `compile/twin_check.json` and
`analysis/tables/twin_timeseries.csv` and prints `done`; those two files are
therefore absent from the zip and must be read from the run directory.

Consequence: when `gate_G4.py` runs it will FAIL on the three budget criteria
regardless of the twin outcome, and `run/DECISIONS.md` has no G4 GO/REDUCED/
PLAN B entry yet. Either a REDUCED design (smaller r_max, cheaper hopping
synthesis) or PLAN B (monograph chain with static charges, prompt §4.4) must
be decided and recorded.

---

## 4 Tests performed

### 4.1 Rerun today (2026-09-07, this session)

| Suite | Command | Result | Log |
|---|---|---|---|
| Root v0.4.0 (`tests/`, 26 tests) | `.mamba/envs/su2zx/bin/python -m pytest tests` | 26 passed, 0 failed, exit 0 | `.work/tmp/root_pytest_20260907.log` (copied into the zip as `logs/root_pytest_20260907.log`) |
| Run directory (`runs/.../tests/`, 5 files, 59 tests) | `../../.mamba/envs/su2zx/bin/python -m pytest tests` | 58 passed, 1 failed in 522 s | `logs/run_pytest_20260907.log` in the zip |

The single failure is `test_route_gausskernel.py::test_kernel_dimensions_and_number_sectors`.
Its first half passes (82 states, sectors 2/20/38/20/2, orthonormal projector);
its second half calls route 2 at j_max=1, which raises `NotImplementedError` by
design after decision D1 (route 2 reports only the kernel dimension 152 at
j_max=1; `gate_G1.py` uses `kernel_dimension(1.0)` instead). The test predates
D1 and was never updated, so this is a stale test, not a physics regression.
It should be changed to assert `kernel_dimension(1.0) == 152`. All 17 `test_l12`
tests and all 13 `test_synth_l12` tests pass in this rerun.

### 4.2 Recorded by the run (historical, with evidence)

| Test file | Tests | Last recorded result |
|---|---:|---|
| `tests/test_route_spinnet.py` | 20 | 20 pass (review `reviews/p1_route_spinnet_1.md`, G1 gate) |
| `tests/test_route_gausskernel.py` | 3 | pass (G1 gate) |
| `tests/test_dynamics.py` | 5 | pass (G2 gate) |
| `tests/test_l12.py` | 17 | 17 passed in 212 s at the G3 gate (16:07 UTC). An earlier run at 15:54 UTC had 2 failures (`logs/cmd/test_l12.log`, Strang-step and Trotter tests) that were fixed before the gate. |
| `tests/test_synth_l12.py` | 13 (6 groups × 2 angles, Strang, resources) | builder reports green after tightening to the elementwise 1e-10 criterion (`logs/agents/synth_l12.out.md`) |

Gate scripts are deterministic Python (no LLM) and re-verify their criteria
from artifacts: `gates/gate_G{0,1,2,3,4}.py`.

### 4.3 Static checks

Ruff, mypy and formatting were run for v0.4.0 (`artifacts/logs/v040/`).
They have not been run on the v0.5.0 `src/su2qc` tree; `tests/test_l12.py`
uses an unregistered `unit` pytest mark and `strang_l12.py` uses the
deprecated `Diagonal` gate (warnings only).

---

## 5 What is still to be done

Ordered by dependency. Items 1–3 are needed before any twin or hardware claim.

1. **Finish G4.** Let `run_g4.py` complete (it writes `compile/resources_routed.{md,json}`,
   `compile/layout.json`, `compile/twin_check.json`,
   `analysis/tables/twin_timeseries.csv`), then run `gates/gate_G4.py`.
   Record the decision in `run/DECISIONS.md` as "G4: GO", "G4: REDUCED" or
   "G4: PLAN B". Given the numbers in §3.4 the honest outcomes are REDUCED or PLAN B.
2. **Cut circuit cost or change scope.** Options, cheapest first:
   the hopping groups dominate (4 × ~1,850 2q gates). Candidates: relative-phase
   Toffoli decompositions for the multi-controlled rotations, exploiting that
   the 4 two-level and 2 three-level blocks per hopping group act on disjoint
   code pairs, or a smaller r_max / larger δt within the window constraints.
   If no route reaches roughly 250 CZ per step, take Plan B.
3. **Fix the PyZX basic pass** in `compile/route.py` (pre-route equivalence
   0.996) or drop it from the comparison with a note; the compiler comparison
   is a secondary endpoint and cannot use a non-equivalent circuit.
4. **G5.** `prereg/MEASUREMENT_PLAN.md`, signed `prereg/PREREG.md` with
   `config.lock.json` and its SHA256, mitigation arms A0/A1(/A2), end-to-end
   twin rehearsal with no manual steps, tensor-network cross-check (Aer MPS;
   CUDA-Q and cuTensorNet are NOT AVAILABLE on this machine).
5. **G6.** `hardware/DRYRUN.md`, ISA inspection, approval token; reuse the
   dry-run-first mechanism from `src/su2zx/qpu.py`. No credentials are
   configured, so this stays in twin mode.
6. **G7.** Pilot and full run on the twin (5 repeats × arms × settings),
   `hardware/jobs.jsonl`, raw counts under `hardware/raw/` with SHA256.
7. **G8.** `analysis/tables/primary_endpoint.csv`, error budget headed by the
   0.257 truncation term, ablations (arms, compiler pipelines; the encoding
   ablation needs S8/C7, which do not exist).
8. **G9.** Rewrite `reports/REPORT.md` and `SUMMARY.md` (currently stale),
   `reports/REPLICATION.md` with `python -m su2qc.replicate` (module not yet
   written), `LOGIC_FLOW.md` + `logic_flow.json`, `MANIFEST.json`, final zip
   under `results/` per prompt §9.
9. **Housekeeping.** Commit the Phase-4 files and the `.graphifyignore`
   change; update the stale j_max=1 assertion in `test_route_gausskernel.py`
   to use `kernel_dimension(1.0)`; verify distinct simulator seeds per repeat in
   `twin.run_counts`; register the `unit` pytest mark; replace the deprecated `Diagonal`
   gate; run Ruff/mypy on `src/su2qc`; bump `pyproject.toml`/`CITATION.cff`
   only when v0.5.0 is actually complete.

Claims that remain unsupported (and must stay so until G7/G8 pass): a 12-qubit
symmetry-verified evolution within hardware reach at the stated depth; the
channel split, string shortening and Casimir reduction on hardware; a
decomposed error budget; the compiler comparison as a secondary endpoint.
Never claimed by design: string tension, continuum limit, hadron
phenomenology, quantum advantage.

---

## 6 Graphify update (this session)

Command: `.mamba/bin/graphify update .` and
`.mamba/bin/graphify update runs/section8_v0.5.0_20260907T0628Z` (AST only, no LLM, no API cost).
Graphify 0.9.53. Previous curated graphs were backed up to `graphify-out/2026-09-07/`
in each location. `.graphifyignore` was extended to exclude the run's nested
`graphify-out/`, the multi-megabyte agent transcripts (`logs/agents/*.out.md`),
exported QPY/QASM circuits and the run's pytest cache, so the root graph does
not index them.

| Graph | Before | After | Validation |
|---|---|---|---|
| Root `graphify-out/graph.json` | 796 nodes / 1258 edges / 61 communities (built from commit dc0e3c9) | 1459 nodes / 2196 edges / 131 communities | unique ids, all endpoints exist, 0 duplicate edge pairs, 1 self-loop (heading node) |
| Run `graphify-out/graph.json` | 820 / 1087 / 57 | 830 / 1105 / 65 | unique ids, all endpoints exist, 0 duplicate pairs, 2 self-loops |

SHA256 of `graph.json`: root `c126c09a45074da0fc9aca3ff20791274e28e23b461544c08ca366f330e804a3`,
run `577e7274a6245048fc3a368ea3f4b363bc47fb88272cbf584b54989adfa1d97c`.

New branches now present in the root graph: `runs/src` (269 nodes),
`runs/physics` (188), `runs/tests` (61), `runs/reports` (19), `runs/gates` (18),
`runs/logs` prompts (17). Critical v0.5.0 callables confirmed as nodes in both
graphs: `synth_unitary`, `synth_strang_step`, `route`, `routed_equivalence`,
`twin_backend`, `postselect`, `bootstrap`, `build_hamiltonian`, `mass_scan`,
`select_window`, `encode`, `physical_codes`. Community labels were not
regenerated (needs an LLM backend); graphify renamed 7 root and 10 run
communities by their hub node. A validation record is stored at
`artifacts/logs/v050/graph_validation_20260907.json`.

---

## 7 Analysis package (zip)

Written to `zip_results/SU2ZX_v0.5.0_status_20260907T170902Z.zip`
(270 files, 3.0 MB, SHA256 `16cd8c43b31362a2c522a06016f4e90c8be6b0233bbe2dd2b73c6e14517d5471`,
`unzip -t` clean) with a `.sha256` sidecar and an `.integrity.json` receipt
(same convention as v0.4.0). The copy of this report inside the zip predates
this paragraph. Contents:

- `PACKAGE_INFO.md` (what is in the zip, commit, environment, how to reproduce,
  test outcomes) and `MANIFEST.json` (SHA256 and size of every file, prompt hash, git HEAD).
- This report; `GRAPHIFY_UPDATE.md`; root docs (`README.md`, `RESEARCH_RESULTS.md`,
  `VALIDATION.md`, `RUN_MANIFEST.md`, `AGENTS.md`, `CITATION.cff`, `LICENSE`,
  `pyproject.toml`, `docs/`, release notes); root `src/`, `tests/`, `tools/`,
  `scripts/`, `config/`, `prompts/`, `solutions/`.
- The complete v0.5.0 run directory except QPY/QASM circuit exports and caches:
  `run/`, `gates/`, `physics/`, `analysis/`, `circuits/*.md|json`, `compile/`
  (whatever exists at packaging time), `reports/`, `reviews/`, `env/`, `src/`,
  `tests/`, `logs/cmd/`, `logs/agents/` (prompts and outputs), `OUTPUT_CONTRACT.json`.
- Both graphify outputs (`graph.json`, `GRAPH_REPORT.md`, `graph.html`, `manifest.json`).
- v0.4.0 `artifacts/data`, `artifacts/provenance`, `artifacts/logs` (figures are
  omitted; they are in the v0.4.0 archive).
- Today's test logs and the graph validation record.

Excluded on purpose: `.mamba/`, `.work/`, `.git/`, caches, prior zips,
`artifacts/figures/`, 146 MB of exported circuits, any credentials (none exist
in the tree; a pattern scan for tokens is recorded in `PACKAGE_INFO.md`).

---

## 8 Reproduction

```bash
cd SU2ZX
export TMPDIR="$PWD/.work/tmp" MPLCONFIGDIR="$PWD/.work/matplotlib" XDG_CACHE_HOME="$PWD/.work/cache" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
.mamba/envs/su2zx/bin/python -m pytest tests                       # v0.4.0, 26 tests
cd runs/section8_v0.5.0_20260907T0628Z
../../.mamba/envs/su2zx/bin/python -m pytest tests                 # v0.5.0, ~10 min
G1_ATTEMPT=3 ../../.mamba/envs/su2zx/bin/python gates/gate_G1.py
../../.mamba/envs/su2zx/bin/python gates/gate_G2.py
../../.mamba/envs/su2zx/bin/python gates/gate_G3.py
../../.mamba/envs/su2zx/bin/python -u src/su2qc/compile/run_g4.py  # ~30 min+, then:
../../.mamba/envs/su2zx/bin/python gates/gate_G4.py
cd ../.. && .mamba/bin/graphify update . && .mamba/bin/graphify update runs/section8_v0.5.0_20260907T0628Z
```

Environment: Python 3.11.16; qiskit 2.5.2, qiskit-aer 0.17.2,
qiskit-ibm-runtime 0.49.0, pyzx 0.10.6, scipy 1.17.1, numpy 2.4.6, mthree 3.0.0
(`runs/section8_v0.5.0_20260907T0628Z/env/requirements.lock.txt`).
