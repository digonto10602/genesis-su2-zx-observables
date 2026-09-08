# Validated Phase 0 plan with blocking-policy precedence

Fable planning and amendment both exited 0. Amendment supersedes original decisions. Higher-priority blocking policy overrides amendment permission to continue dependent BUILD after V1 PARTIAL: only independent stale-test repair and read-only diagnostics proceed; other Phase 0 lanes remain blocked pending V1 resolution. No threshold change authorized. The quasi-weight inequality in the amendment applies only to nonnegative weights, not arbitrary signed distributions; no V11 implementation is accepted under that ambiguity.

The read is complete. The proposal that blocked the earlier attempt is present, so this is not BLOCKED. Here is the Phase 0 plan.

## 1. Verdict, source resolution, and decisions

**Not blocked.** The Nine-Month Plan Section 8 is in the repository (`.work/c060_nine_month_plan.txt`, lines 571 to 713) and its objective is superseded by the campaign anyway, so Phase 0 needs it only as the wording source for the G4 closure row. C0 will end **partial by construction** because the user-preserved dirty paths keep `git status` non-empty. Every other C0 criterion can be met this session.

**Inherited references resolved by named topic** (the v0.6.0 prompt cites v0.5.0 section numbers that do not exist in `prompts/v0.5.0.md`):

| v0.6.0 reference | Actual source used |
|---|---|
| "§5 lanes, review, independence" | v0.5.0 §2 roles, §3 lanes and iteration loop, §0.2 non-negotiables |
| "§7 ledger row format, only gatekeeper writes pass" | v0.5.0 §0.2 "gates are scripts" plus Appendix D gate JSON schema and `run/GATES.md` |
| "§9.1 HARDWARE_MODE", "§9.3–9.5" | v0.5.0 §7 hardware policy, Phase 6 and 7 texts |
| "§10.4–10.5 re-plan, resume, watchdog" | v0.5.0 §1.2 heartbeat, §1.4 extension, §4.2 escalation. No resume or watchdog section exists. Supervised bounded subprocesses only, as the takeover requires. |
| "§13 D1–D2, D6–D11" | v0.5.0 §4.3 and §4.4 plus `run/DECISIONS.md` D1 to D5. D6 to D11 do not exist and are logged as absent. |
| "Appendix A templates", "Appendix C conventions" | v0.5.0 Appendix B and `src/su2qc/conventions.py` |
| `tests/gate_G1..G3` | `gates/gate_G1.py`, `gate_G2.py`, `gate_G3.py` plus `tests/test_route_spinnet.py`, `test_route_gausskernel.py`, `test_dynamics.py`, `test_l12.py` in the run directory |
| `GATE_LEDGER.jsonl`, `strang_table.md`, `resource_table.md`, `00_conventions.md` | `run/GATES.md` plus `gates/GATE_G*.json`; `circuits/resources_logical.md` plus `trotter_scaling.json`; `compile/resources_routed.md`; `conventions.py` |

**Physics and scope decisions (mine, final for this phase):**

1. **Stale test.** The failing call `build_hamiltonian(1.0, 0.0, 1.0)` is replaced by `kernel_dimension(1.0) == 152` plus orthonormality of the route 2 kernel projector at j_max = 1. That restores exactly the legacy scope of decision D1 and claims no j_max = 1 Hamiltonian validation from route 2. The sector counts (3, 36, 74, 36, 3) go into a **new** C0 test, evaluated from route 2 kernel labels and from route 1's 152-state basis, after Opus derives them independently from the transfer matrix T(x) with entries 1+x² on the diagonal and x on the off-diagonals. I checked the totals: Tr T(1)⁴ = 152 and the x⁰ and x⁸ coefficients are 3. If measured differs from derived, the test is not edited; the row fails and goes to DISCREPANCIES.
2. **Twin variance.** The test asserts three things: the five count dictionaries are pairwise distinct, the empirical standard deviation of a density and of P_S3 across repeats is within a factor 2 of √(p(1−p)/N_kept), and a repeat with the same seeds reproduces the same dictionaries. Run at r = 0 and r = 1 per rule D-C0. The fix, whatever the cause, is to drop the construction-time seed and set the simulator seed per repeat explicitly through the simulator's options before each run. The pre-fix code is already isolated in `.work/c060_p0_legacy_baseline/`, so "would have failed on the old code" is checked there without any git operation.
3. **G4 closure.** No `GATE_G4.json` is written: the gate script cannot run because `compile/twin_check.json` was never produced (the twin was killed at r = 1, see the run log), and a hand-written gate JSON would be fabrication. Instead an append-only decision D6 goes into the run's `run/DECISIONS.md` in the literal form `G4: REDUCED (campaign v0.6.0)` with the numbers 2,156 logical per step, 3,976 routed per step, 12,142 routed at r = 3, gap 8.6×, and evidence paths, plus one row in `run/GATES.md` and one INFO row in the new campaign ledger.
4. **`pyzx_basic_TP` is retired**, not fixed. Its pre-route step equivalence is 1.0e+00 in the routed table, meaning the pass produced an orthogonal state, and it is also more expensive than the Qiskit route. Ledger row `retired` with that reason.
5. **Replicate skeleton** is written as `runs/campaign_v060/replicate.py`, not as a repo-level `src/su2qc/` package. Creating a second `su2qc` namespace beside the run-local one is the duplicate backend the takeover forbids. The module name `su2qc.replicate` is assigned in Phase 2 when the reusable package is created. The skeleton implements the manifest hashing and the V1 comparison, which V14 needs anyway.
6. **V11 scope.** The existing estimator is post-selection plus decoded observables plus bootstrap in `twin.py`. No readout mitigation or ODR code exists. V11 in Phase 0 tests what exists on synthetic quasi-distributions with negative entries, channel closure, and a matched-subtraction helper added to the same module. The "after ODR" clause gets its own row `deferred to Phase 5` rather than a silent pass.
7. **Thresholds before C1.** A draft `GATE_THRESHOLDS.yaml` with the Section 5 table verbatim and a `status: draft` header is written now so C0 tests read thresholds from the file. Its hash stays null in the campaign state until C1 freezes it. C1 may not loosen any value.
8. **Dirty work.** Nothing outside the explicit path lists below is staged or discarded. The cleanliness criterion is evaluated honestly and fails.

## 2. Acceptance criteria and lanes

**Boot checks** (OPS, no LLM): prompt hash equals the recorded 50c60ff…; interpreter and package versions match ENV.md; `l12` encodes the stretched string (0, ½, ½, ½), (1, 1, 0, 2) to codeword 3793; conventions file hash fb3b7525… recorded into `hashes.conventions`; `RESUME_LOCK` and `TIME_LEDGER.md` created.

**V1 regression** (TEST-BENCH, fresh copy of the run directory under `.work/`, gate scripts write into the copy, never the run directory):

| Item | Must hold | Historical value |
|---|---|---|
| Legacy suite | 4 tracked test files all pass; `test_synth_l12.py` reported separately as Phase-4 informational | 44 passed, 1 failed |
| G1 | dims 82 and 152 both routes; sectors 2, 20, 38, 20, 2; [H,N] and Hermiticity ≤ 1e−13; spectra ≤ 1e−12; time series ≤ 1e−10; Gauss commutators ≤ 1e−12; degeneracies 16, 16, 18, 16, 16; frozen matter ≤ 1e−8 per D3; magnetic-off ≤ 1e−10 | PASS |
| G2 | expm vs Krylov ≤ 1e−9; energy and N drift ≤ 1e−10; window g² = 4, m = 0.75, δt = 0.8333, r_max = 3 with drop 0.99348, pair weight 0.81933, Strang error 0.019065 | PASS |
| G3 | block unitary deviation ≤ 1e−12; leakage 0; noiseless leakage ≤ 1e−14; slopes −2.0980 and −2.1495 | PASS with S8/C7 excluded by D4 |
| Value stability | every numeric criterion within 1e−12 absolute of the committed JSON at eee1e16, read with `git show`; timestamps and the pytest timing string excluded; `trotter_scaling.json` compared to HEAD and the divergent working-tree copy reported | |

**V10**: distinct dictionaries, σ within 2× multinomial, seeded reproducibility, at r = 0 and r = 1; the same test run on the pre-fix copy must fail on at least one assertion.

**V11**: on synthetic quasi-distributions including negative weights, observables equal the closed-form answers to 1e−10; P_S3 + P_meson + P_BB̄ + P_other equals the post-selected N = 4 weight to 1e−10; ΔO(t) = O(t) − O(0) on synthetic pairs to 1e−10; yield equals the known physical fraction.

**Tier 2 rows** each `done`, `retired`, or `deferred` with reason: ruff and mypy on the run-local package (safe autofixes only, then V1 rerun on the post-fix snapshot; per-line ignores with a reason; box 45 minutes); stale test; sector-count test; `pyzx_basic_TP` retired; replicate skeleton; V11 test; G4 closure rows.

**Lanes and ownership** (disjoint files, Codex concurrency 3, at most two NVIDIA test workers):

| Lane | Owner | Owns | Box |
|---|---|---|---|
| R0 repair | Codex | `tests/test_route_gausskernel.py` in the run dir | 20 min build, 2 h total cap |
| T-bench | execute_code, ≤ 2 NVIDIA workers | sandbox copies, junit XML, hash manifests | continuous |
| P0 physics | Opus 5 | `sessions/…/predictions_C0.md`: sector counts at j_max = 1 by generating function, multinomial σ expectations, D-C0 case | before A0a/A0d run |
| A0a twin | Codex | `src/su2qc/twin/twin.py`, `tests/gate_C0/test_twin_variance.py` | 45 min |
| A0b lint | Codex | run-local `ham/`, `dynamics/`, `encodings/`, `circuits/`, `compile/` only | 45 min |
| A0c estimator | Codex, after A0a lands | matched-subtraction helper in `twin.py`, `tests/gate_C0/test_estimator.py` | 40 min |
| A0d counts + V1 wrapper | Codex | `tests/gate_C0/test_jmax1_counts.py`, `tests/gate_C0/test_v1_regression.py`, `replicate.py`, draft thresholds | 45 min |
| REVIEW | Opus 5 | `reviews/c0_<file>_<n>.md`, blocking vs advisory, checks the pre-fix failure of the twin test | per lane |
| OPS scribe | orchestrator | ledger rows, D6 append, `GATES.md` row, `PHYSICS_STATUS.md` hourly, `TIME_LEDGER.md` | continuous |
| Sign-off | Fable 5.1, one call | `sessions/…/signoff_C0.md` on the snapshot manifest hash | end |

## 3. Schedule, gate, stop conditions, integration

| Clock from T0 | Step |
|---|---|
| 0:00–0:20 | Boot checks, draft thresholds, ledger initialised, P0 predictions dispatched |
| 0:20–1:00 | R0 repair, then full legacy suite plus G1–G3 in a fresh sandbox. No BUILD lane starts before V1 is green, per Section 7 step 2. |
| 1:00–2:15 | Wave 1: A0a, A0b, A0d in parallel; reviews start as each returns |
| 2:15–3:00 | Wave 2: A0c, lint on `twin/` and `compile/`, V1 rerun on the post-lint snapshot |
| 3:00–3:40 | Gate: one command `pytest runs/campaign_v060/tests/gate_C0 --junitxml`, evidence manifest hashed, ledger rows written by the gatekeeper only |
| 3:40–4:00 | Scoped commits, Fable sign-off on the manifest hash, `SESSION_SUMMARY.md`, state update, `RESUME_LOCK` removed |
| Latest 5:00 | Gate with whatever is done; remaining items continue next session. Hard cutoff 12 h. |

**Gate C0 row logic.** V1, V10, V11 rows pass only on deterministic evidence plus the Fable sign-off on the same manifest hash. The cleanliness criterion fails. Result: `C0: partial` with the failing criterion named, phase stays 0, `next_action` set to: "User resolves the listed dirty paths; then rerun `tests/gate_C0` and the V1 sandbox on a fresh copy and re-gate C0 to phase 1."

**Stop conditions.** Repair not green at 2 h: stop, summary first line is the failure, nothing else runs. Sector counts differ from Opus's derivation: row fails, no test edit, C0 partial, Phase 2 V3 blocked. V10 still zero-variance at r = 1 after the fix: row fails, Phase 5 twin work blocked. Any lane needing access outside the repository, hardware, or push: that lane stops. Fable sign-off unavailable: gate recorded as `partial: awaiting sign-off`, no substitute. Lint box expires: row `partial` with counts, V1 must still be green on the final snapshot.

**Commits, all by explicit path list, never by `git add -A`:**

| Commit | Contents |
|---|---|
| `campaign: commit phase-4 artifacts from v0.5.0` | the 16 untracked paths under the run directory, after Opus review |
| `campaign: C0 partial <one line>` | `runs/campaign_v060/` tree, the two `docs/refs` files, the v0.6.0 prompt, the stale-test fix, the twin fix, new tests, the D6 and GATES.md appends |

**Left untouched for the user**, listed in the summary with a recommended disposition each: modified `trotter_scaling.json` and three figures in the run directory (working tree diverges from the committed evidence), `.graphifyignore`, `GRAPHIFY_UPDATE.md`, `STATUS_REPORT_20260907.md`, `artifacts/logs/v050/`, `runs/2026-09-07-dryrun-one-month/`, `runs/_reference/`.

**Integration path.** No package move, no new runner. Campaign tests import the run-local package through one path constant in a `conftest.py`, run legacy code in fresh `.work/` copies, and compare against `git show` blobs. Historical JSON, figures, and tables in the run directory are never written by any Phase 0 process.


# Superseding Fable amendment

Approval for the Python check was denied, so I did the propagation by hand from the printed arrays. Result is unambiguous; ruling follows.

# Phase 0 plan amendment (physics escalation, Fable 5.1)

**Verdict: AMEND, not BLOCKED.** V1 is not restorable to a literal PASS, but that does not trigger the regression-repair STOP, and the stale-test repair remains permitted. Details per issue.

## 1. Value stability of `trotter_scaling.json`: amplification is established, not plausible

The slope is `polyfit(log r, log err)` over r = 8…128. Centered log-r weights are ±1.386, ±0.693, 0 with Σw² = 4.80. The first-order slope change from a relative perturbation ε in the r = 128 error alone is 1.386·ε/4.80 = 0.289·ε.

| criterion | max abs Δ in err array | rel Δ at r = 128 | predicted slope Δ | measured slope Δ |
|---|---|---|---|---|
| Psurv | 6.3e-16 | 1.7e-9 | 4.9e-10 | 4.99e-10 |
| E2 | 5.4e-15 | 4.8e-9 | 1.39e-9 | 1.398e-9 |
| state | 2.4e-15 | 3.6e-11 | 1.04e-11 | 1.047e-11 |

Prediction matches measurement to two digits in all three. The primary quantities (the error arrays) agree to ≤ 5.4e-15, inside 1e-12. A slope stability of 1e-12 would require the r = 128 error (3.7e-7, itself a difference of O(1) probabilities) to be stable to 1.3e-18 absolute, below double-precision epsilon on O(1). No non-bitwise-identical rerun can meet it. The criterion is ill-posed for the log-slope, not merely tight.

Decisions:
- **Threshold is not waived.** V1 sub-rows: G1–G3 gate scripts PASS/FAIL as they report; every primary numeric value compared at 1e-12 (expected PASS); the three slopes compared at 1e-12 and recorded **FAIL, cause established: floating-point conditioning of the log-slope fit**, with the table above in the row. V1 overall = **PARTIAL**, never PASS, until the user amends the V1 wording (e.g. 1e-12 on primary values, slopes at the propagated bound). That is a prompt change only the user may make. C0 stays partial for this reason as well as cleanliness.
- **Does this force STOP?** No. The STOP condition is "regression repair not green in 2 h", where green means the legacy suite passes after the stale-test fix and G1–G3 gate scripts PASS in the sandbox. Those establish the legacy package behaves as before, which is the only thing the Phase 0 BUILD lanes depend on. BUILD lanes proceed. Anything in later phases that cites V1 PASS is blocked until the user rules.
- **Permitted bounded diagnostic** (TEST-BENCH, mechanical, read-only on both JSON versions): refit slopes from the committed `err_*` arrays with the same `polyfit` call and confirm reproduction of the committed slopes to 1e-14 (proves the fit is deterministic and the Δ is entirely input-borne); compute the propagated bound as above for the sandbox rerun vs HEAD and vs working tree; record all three. **Not permitted:** editing the fit or thresholds in `test_l12.py`, touching the working-tree JSON or figures, or substituting the committed values for the rerun.

## 2. V11 closure identity and status

The plan's identity is wrong. From `twin.py` `observables()`: `P_surv` is the full q = (1,−1,0,0) occupation sector; `P_stretched` (S3, j = (0,½,½,½)) and `P_short` (j = (½,0,0,0)) are strict subchannels of it, and other j-configurations in that sector are counted in `P_surv` only. Channels are normalized by kept weight, and the branch order is: any |q| = 2 → BB̄; q = (1,−1,0,0) → surv; all |q| = 1 → meson; Σn = 4 → other; anything else uncounted. With N_VAC = (0,2,0,2), surv and meson imply N = 4 but **P_BBbar can include N ≠ 4 codewords** (e.g. q = (2,0,0,0)), and kept weight with N ≠ 4 and no |q| = 2 falls in no channel.

Exact identities the test must assert (all to 1e-10 on synthetic inputs, including negative quasi-weights):
- `P_surv + P_meson + P_BBbar + P_other = W_kept(N=4) + W_kept(N≠4 ∧ ∃v |q_v|=2)`, both sides computed from decoded labels.
- `P_stretched + P_short ≤ P_surv`, and `P_surv − P_stretched − P_short` equals the label-computed weight of the remaining j-configurations in the (1,−1,0,0) sector.
- If the campaign wants the cleaner "channels sum to post-selected N = 4 weight", that requires an N = 4 filter on BB̄ and an explicit `P_Nviol` channel. That is an estimator change, not a test change: allowed only in lane A0c as an additive helper, with the legacy `observables()` output unchanged and regression-checked.

Status: no readout-mitigation step and no ODR exist in the estimator; the "re-reported after ODR" clause cannot be executed in Phase 0. **V11 = PARTIAL at C0** (rows: synthetic-quasi observables, closure, matched subtraction, yield; ODR-closure row `deferred to Phase 5, V11 rerun on real code path`). Not PASS. C0 cannot exit on V11 grounds either.

## 3. Seed override: conditional no-change path is mandatory

`twin_backend(seed=101)` sets a construction-time `seed_simulator`; `run_counts` passes `seed_simulator = seed + k` per run, and Aer run options override backend options. The per-run seed should already dominate. Amended lane A0a:
1. Run the V10 test on the pre-fix isolated copy first, at r = 0 and r = 1.
2. If five dictionaries are distinct and σ is within 2× → record **"override harmless: run-time seed_simulator = seed + k supersedes construction-time 101"**, no code change, V10 PASS on that evidence. Do not manufacture RED and do not alter the seed + k semantics.
3. Reviewer's "test would fail on old code" requirement is then satisfied by a **negative control**, not history: run the same test with all five run-time seeds forced equal and show it fails (proves detection power).
4. Only if step 1 shows identical dictionaries: locate the actual cause (e.g. run option ignored by this Aer version) and fix at that point; then step 3 becomes the pre-fix run.

Variance criterion, corrected: `bootstrap()` returns 2× the bootstrap standard error **of the mean over R = 5 repeats**, so the expectation is SE = √(Var_s / (R·N̄_kept)), not the per-repeat SD √(p(1−p)/N_kept). Using the per-repeat SD would be off by √5 ≈ 2.24 and fail the 2× window spuriously. Var_s is the multinomial variance of the observable over the pooled kept weights, Var_s = Σ_s w_s O(s)² − (Σ_s w_s O(s))², valid for densities taking values 0, 1, 2 and for E2 as well as for Bernoulli channels. Compare `two_sigma/2` to SE, factor 2 both sides. Note: with 5 repeats the sample SE has ~35% intrinsic scatter (χ²₄), so the seeded test is deterministic and a single-observable miss is recorded as a discrepancy with that probability, never fixed by re-seeding.

## 4. `pyzx_basic_TP`

`state_equivalence` returns 1 − |⟨a|b⟩|; the table prints 1.0e+00 with one significant digit, so all that is established is |overlap| < 0.05. Retire with reason: **"pre-route equivalence error 1.0e+00 fails the ≥ 1 − 1e-10 hardware-eligibility requirement; root cause not diagnosed (candidate: qasm round-trip qubit or phase convention); no orthogonality claim."** Remove the word "orthogonal" from the plan and the ledger row.

## 5. Replicate skeleton path

Prompt Section on code layout puts reusable code in a repo-level `src/su2qc/` package, which does not exist; the takeover forbids a second `su2qc` namespace. Ruling: write the skeleton as run-local `src/su2qc/replicate.py` inside the existing single package, alongside the `twin.py` edits already in scope. The module name `su2qc.replicate` is then literally satisfied. Ledger row `done (skeleton; repo-level package move deferred to Phase 2 with the rest of the package)`. A campaign-local `replicate.py` would have to be rowed `partial`, not done.

## Consolidated stop conditions and gate result

- STOP only if the legacy suite plus G1–G3 gate scripts are not green in the sandbox within 2 h.
- C0 result: **partial**, failing criteria named: repository cleanliness (user-preserved paths), V1 slope stability (threshold ill-posed, user ruling required), V11 ODR clause (deferred to Phase 5). Phase stays 0.
- Independent stale-test repair (kernel dimension 152 plus projector orthonormality, no j_max = 1 Hamiltonian claim) remains permitted and required.
- No historical JSON, figure, or table is written by any Phase 0 process. Final sign-off reserved for the snapshot manifest.
