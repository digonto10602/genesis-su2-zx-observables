Plan follows. Two findings shape it: the foundation package (v0.4.0) already implements nearly every phase of this prompt, so the run is a gated re-execution against the frozen spec with a handful of reconciliations, not a rebuild. Three conflicts between the prompt and the actual repository state are flagged as explicit stop conditions rather than silently resolved.

---

# Plan: one-month SU(2)-ZX program, gated dry-run execution

Run directory: `runs/2026-09-07-dryrun-one-month/`. Baseline snapshot: commit `eee1e16`, working tree dirty (21 paths, all preserved and off-limits). Selected specification: `prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT.md` sections 2 onward as reproduced in the brief. Routing: the approved override (Codex BUILD, execute_code and at most two NVIDIA workers TEST-BENCH, Opus 5 REVIEW and intermediate PHYSICS, Fable 5.1 plan, physics doubt and final sign-off, Claude only via `claude -p`). This document is the plan; nothing is executed by it.

## 1. Goals

1. **Verified physics.** Reproduce the frozen j_max=1/2 SU(2) plaquette-chain Hamiltonian, one- and two-plaquette analytics, exact and Strang dynamics for N=5, x=2, |00100>, and the six-basis reconstruction, each with a deterministic tolerance and a Claude verdict on the same snapshot.
2. **Frozen compiler grid.** Produce the 240-record dataset on the five-qubit linear ECR target (x in {0.5,1,2,4}, t in {0.04,0.08,0.16,0.24,0.32}, r in {1,2,4}, four exact candidates), every candidate exactly equivalence-checked, with the full-reduce routing penalty explained.
3. **Auditable selector.** Train and evaluate the random-forest selector under grouped (x,r) cross-validation against the fixed baselines and oracle. Report NULL honestly if a fixed strategy ties or wins. Prior evidence (v0.3.0 and v0.4.0) says NULL is the likely outcome.
4. **Accelerator and tensor-network status.** CUDA-Q CPU cross-checks at N=1,2,5; separate-process Aer MPS sweep at chi in {32,64,128,256} for N in {5,10,20,40}; GPU routes recorded as BLOCKED with evidence, never PASS.
5. **QPU readiness without submission.** Dry-run-ready code path exercised on a synthetic target and labeled as such; status `NOT RUN - AUTHORIZATION/CREDENTIALS REQUIRED`.
6. **Report and packaging.** Regenerated `RESEARCH_RESULTS.md`, all required non-conditional plots, quality gates of prompt section 15, publication readiness under a new deterministic repository name. Actual publication is out of scope for this dry run and is additionally blocked by the conflicts in section 7.

Non-goals, restated from AGENTS.md: no continuum, SU(3), string tension, string breaking, hadronization or quantum-advantage claims; no simulator output labeled as hardware.

## 2. Reuse inventory and reconciliation items

Existing package coverage, checked against the current tree:

| Prompt phase | Existing implementation | Reconciliation needed |
|---|---|---|
| A correctness (11 tests) | `tests/test_core.py` covers all 11 | Add the N=2 reduction identity and reflection-commutator checks listed in section 3. No change to `core.py` physics. |
| B observables | `su2zx.study` | Output to a fresh directory; frozen config with 81-point grid, r in {1,2,4,8}. |
| C six-basis reconstruction | `core.measurement_family`, `reconstruct_energy`, `project_to_probability_simplex` | None. |
| D compiler grid | `compiler_study.compile_candidate`, `generic_ecr_backend` (five-node linear ECR), `optimize_with_pyzx` | The existing design is N=2..6 and six strategies with a lexicographic cost. Add a frozen-grid generator (N=5 only, 60 sources times 4 strategies = 240) and the prompt's cost proxy C = N2q + 0.02 D2q + 20 sum(-log(1-e)). `config/research.json` sets optimization level 2; the frozen config for this run must set 3. |
| E selector | `GroupKFold`, regret and oracle functions in `compiler_study` | Group key must be the (x,r) family (12 groups). Add cost-weight sensitivity sweep over the 0.02 and 20 weights. |
| F CUDA-Q and MPS | `tools/cudaq_reference.py`, `tn_study`, `scaling_study tn` | Existing bond ladder is 4..32 and in-process. Add a process-per-(N,chi) driver for chi in {32,64,128,256}, N in {5,10,20,40}, with RSS guard. |
| G QPU | `su2zx.qpu` with env-var, `--submit`, fresh-token guard | None. Exercise dry run only. |
| Plots and report | `tools/plot_v040.py`, `su2zx.report` | Extend for the frozen-grid figures; write to fresh figure directory. |
| Publication | `tools/archive_v040.py`, gh workflow | Preferred name already taken by the v0.4.0 publication; see section 7. |

Ponytail budget for BUILD: at most one new Python module (`src/su2zx/onemonth.py`: frozen-grid generator, C-cost, MPS process driver, report assembly), one new test file (`tests/test_onemonth.py`), one shell entry (`scripts/run_onemonth.sh`), one frozen config (`config/research_onemonth.json`, SHA256 recorded in provenance). Everything else is a call into existing functions. Generated outputs go under `artifacts/{data,figures,logs}/onemonth/` and `artifacts/provenance/onemonth.json`. Nothing under `runs/section8_v0.5.0_*` is read for physics or modified.

Frozen conventions carried into every gate packet: H_tilde = 2H/g^2, x = 2/g^4, j_max = 1/2, Qiskit order q4 q3 q2 q1 q0, initial state index 4, Strang splitting with the package's default term ordering ("current"), 2+1D spatial plaquette chain. The physics functions in `src/su2zx/core.py` (`plaquette_chain_terms`, `hamiltonian`, `pauli_rotation`, `strang_evolution`, `reconstruct_energy`) are frozen. Any diff touching them is an automatic Fable escalation.

## 3. Exact physics acceptance checks

All checks are deterministic, computed by gate scripts, and written as criterion rows (target, measured, pass) to `gates/GATE_G<n>.json`. Tolerances are absolute unless stated.

**A. Hamiltonian construction (gate G1)**

| # | Check | Criterion |
|---|---|---|
| A1 | One-plaquette matrix at x=1 equals [[0,-2],[-2,3]] | max elementwise error <= 1e-12 |
| A2 | Eigenvalues at x=1 | {-1, 4}, each within 1e-12 |
| A3 | Ground state parallel to (2,1) | overlap with (2,1)/sqrt(5) has modulus 1 within 1e-12 |
| A4 | P1(t) from \|0> versus analytic 4x^2/(4x^2+9/4) sin^2(t sqrt(4x^2+9/4)) at x=1 and x=2 on 81 points over one full period | max error <= 1e-12 |
| A5 | Two-plaquette matrix at x=1 in \|q1 q0> order equals the 4x4 in the spec | max elementwise error <= 1e-12 |
| A6 | Two-plaquette ground energy | \|E0 + 1.789221846776\| <= 1e-12 (the reference is quoted to 12 decimals; a miss below 5e-13 is a spec-precision issue and goes to Fable, not to BUILD) |
| A7 | General chain at N=2 reproduces H_tilde_2 term by term | simplified Pauli coefficient difference <= 1e-14 |
| A8 | Term count for N=5 | exactly 26 Pauli terms: 10 electric (I, Z0, Z4, Z1, Z2, Z3, four ZZ) and 16 magnetic (2 per end, 4 per interior site) |
| A9 | Hermiticity for N=1,2,5 | max \|H - H^dagger\| <= 1e-12 |
| A10 | Reflection symmetry | \|\|[H_5, R]\|\|_max <= 1e-12 where R maps q_p to q_{4-p} |
| A11 | Initial energy of \|00100> at x=2 | \|<H> - 3\| <= 1e-12 |
| A12 | Bit order | statevector index 4 has amplitude 1; n_2(0)=1 and n_{p != 2}(0)=0 within 1e-12 |
| A13 | Manual Pauli rotation vs matrix exponential for each term shape Z, ZZ, X, ZX, ZZX | max unitary error <= 1e-12 |

**B. Dynamics (gate G2)**

| # | Check | Criterion |
|---|---|---|
| B1 | Norm of exact and Trotter states, all 81 times, r in {1,2,4,8} | norm error <= 1e-12 |
| B2 | Exact energy conservation | \|E(t) - 3\| <= 1e-10 for all t |
| B3 | Exact mirror symmetry | n_p(t) = n_{4-p}(t) within 1e-12; A_mir(exact) <= 1e-12 |
| B4 | Second-order Trotter convergence | state 2-norm error at t=0.32 strictly decreasing over r=1,2,4,8; least-squares slope on r=2,4,8 within [1.8, 2.2]; TVD slope over r=1..8 also recorded (prior value 1.87) |
| B5 | Trotter TVD ordering | at every hardware time t>0, TVD(r=8) < TVD(4) < TVD(2) < TVD(1) |
| B6 | Six-basis reconstruction, noiseless | \|E_direct - E_recon\| <= 1e-10 for E_E, E_B, E at the five hardware times, both exact and r=2 states. The physics justification to be stated in the report: every magnetic term contains exactly one X, so the six bases Z, X0..X4 diagonalize every term. |
| B7 | Simplex projection | output nonnegative, sums to 1 within 1e-12, idempotent on valid distributions, and matches a hand-computed projection on a 3-outcome case |
| B8 | Recorded, not pass/fail | Trotter r=2 energy drift (prior max 0.575) and A_mir(Trotter, prior max 1.15e-3). Both must appear with a physical explanation (Strang error and non-symmetric term ordering) in the report. |

**C. Compilation (gate G3)**

| # | Check | Criterion |
|---|---|---|
| C1 | Logical equivalence of every PyZX candidate, N<=5 | global-phase-aligned max \|U_cand - U_src\| <= 1e-10 on the full 32x32 unitary |
| C2 | Routed equivalence on the 5-qubit linear ECR target | same 1e-10 after applying the final layout permutation; no ancillas |
| C3 | Record count | exactly 240 rows, 60 distinct (x,t,r) sources times 4 strategies, each with source and native gate totals, 2q count, depth, 2q depth, duration, compile time, SWAP overhead, calibration proxy |
| C4 | Inequivalent candidates | rejected, counted, kept visible in raw data, excluded from selector training |
| C5 | Routing failure mode | full-reduce native 2q count exceeds its own logical count in the majority of cases and exceeds Qiskit L3 native count in the majority; the report explains nonlocal interactions created by extraction |
| C6 | Preregistered resource gate | median over 60 sources of native 2q reduction of the best exact PyZX candidate versus Qiskit L3 >= 15% and native 2q-depth reduction >= 10%; otherwise resource hypothesis FAIL, reported as such |

**D. Selector (gate G4)**: grouped cross-validation by complete (x,r) families only; no random split of time rows (deterministic leakage check: no group appears in both folds). Report top-1 accuracy, normalized regret, always-Qiskit, always-Basic, always-teleport, always-full-reduce, oracle, and cost-weight sensitivity over at least three weight settings. AI-success claim only if selector regret is strictly below every fixed baseline; otherwise NULL.

**E. Accelerators (gate G5)**: CUDA-Q qpp-cpu energy, survival, TVD and state error versus Qiskit at N=1,2,5 <= 1e-8. MPS: every primary observable (five n_p, E, L, A_mir) changes by less than 1e-3 under the final feasible doubling, else NOT CONVERGED for that N. Dense agreement <= 1e-8 at N=5 and N=10 (the only sizes with a dense reference). GPU routes: status BLOCKED with detected compute capability 6.1 versus documented minimum 7.5, reusing `artifacts/data/accelerator_status.json` evidence refreshed by a new probe log.

**F. QPU (gate G6)**: dry run prints backend label, path, shots, circuit count, mitigation overhead and total shots; circuit count 68 (60 physics: 2 variants x 5 times x 6 bases, plus 8 M3 calibration) and 278,528 requested shots; guard test proves no submission without env var, `--submit` and fresh token; status NOT RUN.

## 4. Lane assignments

| Lane | Model | Owns | Never does |
|---|---|---|---|
| BUILD | Codex main (`gpt-6-astra`, fallback `gpt-5.6-sol`; NVIDIA fallback only on Codex exhaustion) | `src/su2zx/onemonth.py`, `tests/test_onemonth.py`, `scripts/run_onemonth.sh`, `config/research_onemonth.json`, minimal extensions to `compiler_study.py`, `report.py`, `tools/plot_v040.py`; gate scripts `runs/.../gates/gate_G*.py` | Edit `core.py` physics functions, gate tolerances after a FAIL, anything under `runs/section8_*`, the 21 dirty paths |
| TEST-BENCH | `execute_code` (no LLM) for pytest, the 240-compile grid, the 16 MPS processes, plotting, report generation, secret scan, row-count and JSON audits; at most 2 NVIDIA workers (`deepseek-ai/deepseek-v4-flash-0731`) only for reasoning-assisted test triage with complete context and absolute paths | `runs/.../bench/*.json`, `artifacts/logs/onemonth/*` | Physics judgment, editing gate scripts, more than 2 concurrent workers, retry storms on 429 |
| REVIEW | Opus 5 via `claude -p`, background, one job per gate diff | `runs/.../review-<n>.md` | Edits; substitution by NIM |
| PHYSICS | Opus 5 for gates G0..G8; Fable 5.1 for escalations and final sign-off | `runs/.../gate-<n>.md`, `final-signoff.md` | Waiving deterministic evidence; passing on opinion |

Builder and reviewer are always different models. Gate scripts are plain Python that re-read artifacts and exit nonzero on any failed criterion.

## 5. Gate schedule

Sequence: BUILD, TEST-BENCH, background REVIEW, PHYSICS gate, then the next dependent step. A gate is PASS only when its script exits 0, its JSON has every criterion row measured, and the Opus verdict file's first line is exactly PASS on the same frozen snapshot (recorded diff hash). Two attempts per gate, then Fable escalation; maximum three escalations per gate, six per run. Failed gates block dependents; independent lanes may continue.

| Gate | Depends on | Deterministic evidence (script exit 0 plus JSON) | Opus reviewer pass criteria | Estimated compute |
|---|---|---|---|---|
| G0 preflight | none | `artifacts/logs/onemonth/environment.md` and probe log; imports and smoke calls for every required package; interpreter path exists; baseline commit and dirty-path inventory recorded; `gh auth status` and `gh api user` read-only outputs logged (login must be `digonto10602`); quotas recorded or UNKNOWN; frozen config SHA256 | Environment matches the machine actually probed (not the RTX 3070 the prompt assumes); dirty-path inventory complete; no writes outside owned paths | minutes |
| G1 correctness | G0 | checks A1..A13; full `tests/` suite exit 0 with JUnit XML; ruff and mypy exit 0 on changed files | Each criterion row has target and measured; conventions consistent with spec section 3; no edit to frozen `core.py` functions in the diff | under 1 min |
| G2 dynamics and reconstruction | G1 | checks B1..B8; CSV row counts (81 times x required columns; 32 probabilities x 5 hardware times for r=2); JSON valid, all values finite | Observable definitions match the spec; B8 quantities explained, not hidden; separation of Trotter error from any later device error stated | minutes |
| G3 compiler grid | G1 | checks C1..C6; 240 rows; rejected-candidate count; routing-penalty table | Equivalence is exact unitary, not sampling; optimization level 3 recorded; the full-reduce failure mode is demonstrated with numbers; resource-gate verdict is stated whichever way it falls | 15 to 40 min |
| G4 selector | G3 | group-leakage check PASS; metrics table; sensitivity table; verdict SUCCESS or NULL | No random time-row splits; baselines computed on the same cases; NULL is not softened | under 5 min |
| G5 accelerators and MPS | G2 | CUDA-Q CPU table; 16 MPS process records with runtime, peak RSS, doubling deltas; GPU BLOCKED record with capability evidence | No GPU claim without a smoke-test log; convergence stated per N; dense agreement only where a dense reference exists | 10 to 60 min |
| G6 QPU readiness | G2, G3 | dry-run transcript on synthetic target; guard test exit 0; status NOT RUN | Synthetic label present on every artifact; no token or credential in any file | minutes |
| G7 plots, report, quality gates | G2..G6 | nine non-conditional figures in PNG and PDF with source mapping; conditional hardware figures absent with explanation; `RESEARCH_RESULTS.md` regenerated from files with all 16 required sections; link and figure existence audit; secret scan exit 0; full-suite and lint reruns; provenance JSON | Every plot paragraph has the five required elements; calculated results separated from expectations; success-gate table entries each cite a path; claim boundaries of AGENTS.md present | minutes |
| G8 publication readiness | G7 | staged file list limited to run-owned and intended paths; secret scan on staged content; `git diff --check`; chosen repository name computed deterministically and its non-existence verified read-only | See section 7. In this dry run G8 ends at readiness; no remote is created | minutes |
| Final | G0..G8 verdicts | `final-input.md` with whole-run diff including untracked owned files, gate ledger, evidence paths, open issues | Fable: gauge conventions, Hamiltonian, Trotter and ZX equivalence, every criterion; PASS, FAIL or DEFERRED | one call |

Wall-clock: total compute under two hours; the run is dominated by model latency and packet preparation. Protocol clock still applies when executed: 12 h target, no new escalation after T+14 h, freeze at T+15 h, stop at T+16 h. No overnight launch: the approved durable runner does not exist, so execution must be interactive.

## 6. Stop and block conditions

1. **Physics FAIL** on any A or B criterion after two BUILD attempts: escalate to Fable; no dependent gate proceeds.
2. **Any diff to frozen `core.py` physics functions**: block until Fable reviews it, regardless of test results.
3. **Deterministic and Claude disagreement** on any gate: Fable escalation; the gate stays FAIL meanwhile.
4. **Inequivalent candidate**: reject and count; not a stop, but a candidate family that is inequivalent for every source blocks G4 for that strategy.
5. **Claude unavailable**: REVIEW and PHYSICS defer; only independent BUILD and TEST-BENCH work continues; no gate is accepted. **Fable unavailable**: final sign-off DEFERRED, never substituted.
6. **Memory guard**: any MPS process exceeding 10 GiB RSS is killed by the driver and its (N, chi) recorded as SKIPPED UNSAFE; the sweep continues with smaller sizes.
7. **Workspace boundary**: any command targeting a path outside ROOT, or any write to the 21 preserved dirty paths or `runs/section8_*`, is a hard stop.
8. **QPU**: no submission under any circumstance in this run; the guard test is itself a gate criterion.
9. **Escalation caps**: three per gate, six per run; a seventh need means the run ends PARTIAL.

## 7. Conflicts requiring a user decision before G8 (not resolvable by the plan)

1. **Repository name.** `genesis-su2-zx-observables` already holds the v0.4.0 publication, so the deterministic fallback name is `genesis-su2-zx-observables-20260907` (then `-2`, `-3`). The prompt's `gh repo create --source=. --remote=origin --push` cannot run because `origin` already exists and points at the v0.4.0 repository. Options: a second remote name, or a fresh clone-free export of tracked content. Both deviate from the literal prompt.
2. **Clean-status requirement versus preserved dirty tree.** Prompt section 16 requires clean local status before completion, but the brief requires preserving the 21 uncommitted paths, which include the unfinished v0.5.0 gate-G4 work. Checkpoint commits in this run must stage only run-owned paths, which leaves the tree dirty. Completion under the prompt's own rule is therefore impossible without the user either committing or approving an exception.
3. **Publishing scope.** Pushing this repository publishes the tracked v0.5.0 Section-8 run artifacts and the regenerated `RESEARCH_RESULTS.md`, which overwrites the published v0.4.0 report at the repository root. The plan preserves the old report as `docs/RESEARCH_RESULTS_v0.4.0.md` before regeneration, but the overwrite and the inclusion of in-progress v0.5.0 material need explicit approval.

The environment mismatch (prompt assumes Ubuntu with an RTX 3070; the machine is Arch-based with a GTX 1060 Max-Q at compute capability 6.1) is not a decision point: the prompt's own blocker clauses apply, GPU routes are BLOCKED with evidence, and CPU physics proceeds.

## 8. Token and call budget

Quotas are UNKNOWN until `/status` and `/usage` are read at G0 and stay UNKNOWN if unreadable. Budget is therefore expressed as hard call caps and packet-size limits. Estimates are estimates.

| Class | Model | Cap | Packet limit | Estimated tokens |
|---|---|---|---|---|
| Planning | Fable 5.1 | 1 (this document) | brief plus cited files | done |
| Physics escalation | Fable 5.1 | reserve 2, hard max 6 | gate JSON, failing criterion, minimal diff, under 30k input | up to 200k total |
| Final sign-off | Fable 5.1 | 1, capacity reserved at G0 before any optional Fable call | `final-input.md` under 60k input | about 80k |
| Intermediate gates | Opus 5 | 9 gates x 2 attempts max = 18 | gate packet under 40k; diff limited to owned files | about 500k |
| Background review | Opus 5 | 1 per gate with a code diff (G1, G3, G4, G5, G7), reruns only after a FAIL: max 10 | diff plus plan under 50k | about 300k |
| BUILD | Codex | 6 module tasks (config, onemonth module, tests, gate scripts, plot extension, report extension) plus fixes | full conventions and ownership in every task | Codex quota, weekly reset preferred |
| Reasoning-assisted test triage | NVIDIA workers | at most 2 concurrent, 40 RPM shared, only when a mechanical loop fails and the cause is not obvious from logs | complete context, absolute paths, timebox | small |
| Mechanical loops | none (execute_code) | pytest, lint, 240 compiles, 16 MPS processes, CUDA-Q CPU runs, plots, report generation, audits, secret scan, archive | n/a | zero LLM tokens |

Fable total stays under the 50% weekly Claude share; if the reserve for the final call cannot be established at G0, optional Fable calls are skipped and escalations block rather than spend the reserve. Compression under the auto provider consumes main-subscription quota and is counted at preflight; conventions and criteria live in this file and the gate JSONs, not in model context.

## 9. End-of-run deliverables

`runs/2026-09-07-dryrun-one-month/{run.log, gates/GATE_G0..G8.json, gate-<n>.md, review-<n>.md, final-input.md, final-signoff.md, bench/}`; `artifacts/{data,figures,logs}/onemonth/`; `artifacts/provenance/onemonth.json`; regenerated `RESEARCH_RESULTS.md` with the status table in the PASS / FAIL / NULL / BLOCKED / NOT RUN vocabulary; `PUBLISH_BLOCKER.md` if section 7 is unresolved. Final report format follows the run protocol: run identity and snapshots, criterion table, gate ledger with model per verdict, lane usage with actual providers or UNKNOWN, claim boundaries, open issues, and either the Fable sign-off path or DEFERRED with the exact pending decisions.
