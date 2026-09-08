# SU2ZX · GI-Cost Campaign · v0.6.1 session prompt — close C0, preregister, extend the reference (Phases 0 → 2)

**Hermes prompt v0.6.1 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.1.md`**
**Amends `prompts/gi_cost_campaign_v.0.6.0.md` (hereafter "v0.6.0"). v0.6.0 remains the campaign document: hypotheses, endpoints E1–E5, the claim table, the validation ladder V1–V14, the phase table, the thresholds, the decision rules, the deliverables tree and the summary format are all unchanged and are not repeated here. This file adds the human rulings the last session was waiting for, fixes three defects found in v0.6.0, and sets the scope of this session. Where this file and v0.6.0 disagree, this file wins; where both are silent, v0.5.0 mechanics apply as resolved in Section 1.**

**Launch (human, one line, from the SU2ZX repository root):** `hermes` then
`@prompts/gi_cost_campaign_v.0.6.1.md  Run phase 0 to C0, then continue. T0 is now.`
Everything below is addressed to you, the Hermes orchestrator session.

---

## 0. State as found, and the rulings that unblock it

The last session (`runs/campaign_v060/sessions/c060_p0_20260907/`) established: the legacy suite is 45/45 green after a test-only repair of `tests/test_route_gausskernel.py` (`kernel_dimension(1.0) == 152` plus projector orthonormality, no j_max = 1 Hamiltonian claim from route B); G1 17/17, G2 20/20 and G3 PASS in a sandbox copy; the Fable plan and its amendment (`plan.md`) are the Phase 0 plan. The session then stopped with `phase = 0`, `gates = {}`, C0 not passed, because four things needed a human. Those rulings follow. They are final for this campaign; apply them, log the ruling number in the ledger row, and do not re-plan them.

**R1 · V1 value-stability wording (replaces the 1e-12 slope criterion).** Every *primary* numeric quantity in the committed gate evidence at `eee1e162` (dimensions, sector counts, spectra, aligned matrix elements, time series, Trotter error arrays, energies, leakage probabilities, window numbers) must agree with the sandbox rerun to 1e-12 absolute. A *derived* quantity obtained by a fit — the three Trotter log-slopes in `circuits/trotter_scaling.json` — is compared at **10 × its first-order propagated conditioning bound** computed from the primary deltas by the method already recorded in `slope-conditioning.json` (centered log-r weights over r = 8…128, Σw² = 4.80), and must in addition lie inside the G3 band [−2.3, −1.7]. The bound and the measured delta are written next to every slope, every time. `GATE_THRESHOLDS.yaml` records this as `V1.primary_abs: 1.0e-12` and `V1.slope_rule: propagated_bound_x10`. Reason for the record: a 1e-12 slope stability would require the r = 128 error (3.7e-7, itself a difference of O(1) probabilities) to be stable to 1.3e-18, below double-precision epsilon; the criterion was ill-posed for a log-slope, not tight. This is the only threshold change of the campaign and it is a wording repair, not a loosening of any physics tolerance.

**R2 · Dirty working tree (the cleanliness criterion).** Dispositions by path, in this order, before the regression step:

1. `runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json` and the three modified figures under `analysis/figures/`: **the committed HEAD versions are the evidence of record** (they are what G3 signed off). Copy the working-tree versions, with SHA-256 and a copy of `slope-conditioning.json`, into `runs/campaign_v060/00_repair/v050_working_tree_divergent/` with a one-paragraph `README.md` stating the cause (log-fit conditioning, primary arrays agree to ≤ 5.4e-15), then `git checkout -- <those four paths>`. Nothing is deleted.
2. The untracked v0.5.0 Phase-4 paths under the run directory (16 paths: `synth_l12.py`, `test_synth_l12.py`, `compile/`, `twin/`, `gate_G4.py`, `resources_synth.md`, `resources_routed.*`, `layout.json`, `run_g4.log`, `synth_l12.*.md`, `exact_at_window.csv`, `compile/__init__.py`, `twin/__init__.py`): commit after an Opus read-through, message `campaign: commit phase-4 artifacts from v0.5.0`.
3. `STATUS_REPORT_20260907.md`, `.graphifyignore`, `GRAPHIFY_UPDATE.md`, `artifacts/logs/v050/`, `docs/refs/` (three files incl. the Nine-Month Plan PDF), `prompts/gi_cost_campaign_v.0.6.0.md` and this file: commit, message `repo: status report, graphify refresh, campaign references (2026-09-07)`.
4. `runs/2026-09-07-dryrun-one-month/` and `runs/_reference/`: run the repository's secret scan (`tools/` provenance/secret patterns plus: `sk-`, `hf_`, `ghp_`, `ibm`/`qiskit` token shapes, `Bearer`, `.env` contents, private-key headers) on every file. Files that pass: commit, message `ops: hermes run records 2026-09-07`. A file that fails is moved, not deleted, to `.work/quarantine/<same relative path>` and listed in the session summary. Check that `verified-config-redacted.yaml` is actually redacted before committing it.
5. After steps 1–4, `git status` must be empty except the campaign tree, which is committed at the gate. Commits are by explicit path list, never `git add -A`.

**R3 · V11 scope at C0.** The "channel closure re-reported after ODR" clause of V11 is moved to Phase 5 (it becomes a sub-row of V12, evaluated on the real estimator code path when readout mitigation and ODR exist). V11 at C0 consists of the four executable rows: synthetic quasi-distribution observables with negative entries (1e-10), channel closure identities as corrected in Section 2.2 below, matched subtraction ΔO(t) = O(t) − O(0) (1e-10), and yield. With that, V11 can PASS at C0; a `deferred to Phase 5` row is written for the ODR clause.

**R4 · The Fable amendment's rulings are adopted as written** (`plan.md`, "Superseding Fable amendment", items 2–5): the twin-seed conditional no-change path with the negative control; the bootstrap-SE (not per-repeat SD) variance criterion with multinomial variance; `pyzx_basic_TP` retired with the wording "pre-route equivalence error 1.0e+00 fails the ≥ 1 − 1e-10 hardware-eligibility requirement; root cause not diagnosed; no orthogonality claim"; the replicate skeleton at run-local `src/su2qc/replicate.py` (the module name `su2qc.replicate` is thereby satisfied; the repo-level package move is a Phase 2 deliverable, see Section 4).

**R5 · Coupling point P-A is the v0.5.0 window, not the v0.6.0 §2.2 ratio.** `physics/window.json` fixes g² = 4, m = 0.75, δt = 0.8333, r_max = 3, and `conventions.py` fixes the coefficients (g²/2, m, 1/2, 1/(2g²)) of (Σ E², staggered mass, hopping, −Tr(U□ + U□†)). In code units P-A is therefore **(cE, cM, cH, cB) = (2, 0.75, 0.5, 0.125)**, i.e. electric : hopping : magnetic = **1 : 0.25 : 0.0625** with μ = m/g_E = 3/8 and **g_E ≡ g²/2 = 2**, not the "1 : 0.5 : 0.25, our g_E = 1" printed in v0.6.0 §2.2 (that row corresponds to g² = 2, a point where no G2 visibility criterion or Trotter admissibility was ever established). Consequences: (i) time points are multiples of the frozen δt: **t = r·δt with r ∈ {1, 2}, t ∈ {0.8333, 1.6667}** in code units (τ = t·g_E ∈ {1.667, 3.333}), and t = 2.5 (r = 3) only if Phase 4 shows r = 2 → 3 admissible; the v0.6.0 "t ∈ {0.75, 1.5}/g_E" is void. (ii) P-S keeps the same electric scale so both points share g_E = 2: **(cE, cM, cH, cB) = (2, 0.75, 0.04, 0.04)**, ratio 1 : 0.02 : 0.02, μ = 3/8, Sufian time points τ ∈ {5, 12.5} → **t ∈ {2.5, 6.25}** in code units. (iii) The tree-level resonance check 2m = ¾ g_E reads 1.5 = 0.75 · 2, consistent with `tree_level_resonance(4) = 0.75`. The Phase 2 physics auditor (C2) recomputes this mapping from `conventions.py` and `window.json` alone; if the auditor's arithmetic differs from the numbers above, **`window.json` and `conventions.py` are the authority**, the corrected numbers go into the preregistration with a note, and the ledger records `R5 corrected`. The one-parameter wrapper `H(gE, mu, jmax)` of v0.6.0 §2.2 is defined with g_E = g²/2 so that `H(2, 3/8, 1/2)` reproduces the v0.5.0 Hamiltonian bit-for-bit (V2 checks this at 1e-12).

**R6 · Session scope.** `CONFIG.resolved.yaml`: `AUTOPILOT: true`, `STOP_AT: C2`, `SESSION_HARD_HOURS: 12`, `HARDWARE_MODE: disabled` (no IBM credentials are configured on this machine; Phase 6 stays twin-only until a human configures them — state this in the preregistration's hardware slot rather than leaving it blank). Run Phase 0 to gate C0, then Phase 1 to C1, then Phase 2 to C2, inside one session while the cutoff allows; gate whatever phase is open when the cutoff arrives as `partial` with artifacts and `next_action` set. Phase 0 and Phase 1 need **no** Fable planning call (the existing `plan.md` plus this file is the plan); Phase 2 gets exactly one, bounded at 600 s, retried at most once on an empty result, then the Section 4 plan is used as written. Fable sign-off: one call per gate, on the evidence manifest hash. Model routing as before: Codex for builds, Opus 5 for reviews and physics audit, NVIDIA workers (≤ 2) for test benches. Quota at the last check: Fable week 46 % used (resets Sep 12, 3 am Denver); Codex weekly 40 % left (resets Sep 11); re-check at boot and record in `ENV.md`. **Do not update, install or reconfigure any CLI or tool** (the last session accidentally accepted a Codex CLI update at a `/status` prompt; answer such prompts with an explicit "no"). Supervised bounded subprocesses only; no watchdog claim; no push; no hardware.

---

## 1. Reference resolution (adopt verbatim; do not re-derive)

v0.6.0 cites v0.5.0 section numbers that do not exist in `prompts/v0.5.0.md`. The last session resolved them; this table is now normative.

| v0.6.0 says | Use |
|---|---|
| "§5 lanes, review, independence" | v0.5.0 §2 roles, §3 lanes and iteration loop, §0.2 non-negotiables |
| "§7 ledger row format; only the gatekeeper writes pass" | v0.5.0 §0.2 "gates are scripts", Appendix D gate-JSON schema, `run/GATES.md`; campaign ledger `runs/campaign_v060/GATE_LEDGER.jsonl` (create at boot; one JSON object per line: `{gate, item, value, threshold, source, pass, utc, evidence, rule}`) |
| "§9.1 HARDWARE_MODE; §9.3–9.5" | v0.5.0 §7 hardware policy and Phase 6–7 texts |
| "§10.4–10.5 re-plan, resume, watchdog" | v0.5.0 §1.2 heartbeat, §1.4 extension, §4.2 escalation; no resume/watchdog section exists — bounded supervised subprocesses |
| "§13 D1–D2, D6–D11" | v0.5.0 §4.3–4.4 and `run/DECISIONS.md` D1–D5; D6 is the G4 closure row written this session; D7–D11 do not exist and are logged as absent |
| "Appendix A templates; Appendix C conventions" | v0.5.0 Appendix B; `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py` (hash fb3b7525…, record it in `hashes.conventions`) |
| `tests/gate_G1..G3` | `gates/gate_G{1,2,3}.py` plus `tests/test_route_spinnet.py`, `test_route_gausskernel.py`, `test_dynamics.py`, `test_l12.py` in the run directory (`test_synth_l12.py` reported separately, informational) |
| `GATE_LEDGER.jsonl`, `strang_table.md`, `resource_table.md`, `00_conventions.md` (v0.5.0 artifacts) | `run/GATES.md` + `gates/GATE_G*.json`; `circuits/resources_logical.md` + `trotter_scaling.json`; `compile/resources_routed.md`; `conventions.py` (copy it to `runs/campaign_v060/00_conventions.md` with a header, extended in Phase 2) |
| route A / route B | route 1 = `ham/route_spinnet.py` (dressed-vertex spin network); route 2 = `ham/route_gausskernel.py` (redundant KS space projected onto the Gauss kernel) |
| the "82-state package" | the run-local package `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/` (3,658 lines). There is **no** repo-level `src/su2qc/`; do not create a second `su2qc` namespace before the Phase 2 package move (Section 4) |

Sandbox rule (from the last session, now standing): every gate script and every legacy test runs on a fresh copy of the run directory under `.work/`; no Phase 0–2 process writes any historical JSON, figure or table in `runs/section8_v0.5.0_20260907T0628Z/`. Campaign tests import the run-local package through one path constant in `runs/campaign_v060/tests/conftest.py`.

---

## 2. Phase 0 · finish and gate C0 (target 3 h; box 5 h)

### 2.1 Order of work

1. **Boot (≤ 20 min).** T0, session tag `c060_p0_<YYYYMMDD>_2`. Read `CAMPAIGN_STATE.json` (phase 0). Verify the prompt hash of v0.6.0 (50c60ff…) and record this file's hash as `hashes.prompt_v061`. Live import probe (Python 3.11.16, NumPy 2.4.6, SciPy 1.17.1, Qiskit 2.5.2, Aer 0.17.2). Codeword check: `l12` encodes the stretched string ((0, ½, ½, ½), (1, 1, 0, 2)) to 3793. Quota check, `ENV.md`, `TIME_LEDGER.md`, `RESUME_LOCK`. Write the draft `GATE_THRESHOLDS.yaml` (v0.6.0 §5 verbatim plus the R1 lines; header `status: draft`).
2. **R2 dispositions** (steps 1–4 of R2) — before regression, so the sandbox compares against a tree that equals HEAD plus the campaign files.
3. **Regression (rule 12)** on a fresh sandbox copy: legacy 4-file suite (expect 45/45), G1, G2, G3 scripts, value-stability comparison against `git show eee1e162:<path>` blobs under the R1 rule. Write V1 rows. A red result here is a repair session (2 h box) and nothing else starts.
4. **P0 physics predictions (Opus, before A0a/A0d run)** → `sessions/<tag>/predictions_C0.md`: the j_max = 1 sector counts (3, 36, 74, 36, 3; total 152) derived independently by generating function / transfer matrix; the bootstrap-SE expectations for V10 per the amendment §3 (SE = √(Var_s/(R·N̄_kept)), multinomial Var_s, R = 5); which D-C0 case applies at r = 0.
5. **Wave 1 (parallel, disjoint files):** A0a twin variance (V10) per amendment §3 — pre-fix run first at r = 0 and r = 1; "override harmless" recorded if distinct and within 2× SE; negative control with all five run-time seeds forced equal must fail; only on identical dictionaries locate the cause and fix. A0d: `tests/gate_C0/test_jmax1_counts.py` (route 1 basis and route 2 kernel labels versus P0's derivation; a mismatch fails the row and is not edited away), `tests/gate_C0/test_v1_regression.py` (the R1 wrapper), `src/su2qc/replicate.py` skeleton (manifest hashing + V1 comparison). A0b lint: ruff and mypy on the run-local package, safe autofixes only, per-line ignores with a reason, 45-minute box, then V1 rerun on the post-lint snapshot.
6. **Wave 2:** A0c estimator (V11) per Section 2.2 — additive helpers in `twin.py`, legacy `observables()` output unchanged and regression-checked; `tests/gate_C0/test_estimator.py`. G4 closure: append D6 to the run's `run/DECISIONS.md` in the literal form `G4: REDUCED (campaign v0.6.0) — 2,156 logical 2q per step (D=16, h0–h3 248/248/239/241, B=174), 3,976 routed per step, 12,142 routed at r=3, gap 8.6× logical against 250; no GATE_G4.json because compile/twin_check.json was never produced (twin killed at r=1); evidence: compile/resources_routed.md, circuits/resources_synth.md, logs/cmd/run_g4.log`; one row in `run/GATES.md`; one INFO row in the campaign ledger. `pyzx_basic_TP` retired (R4 wording). Reviews (Opus) per lane, blocking versus advisory.
7. **Gate C0.** One command: `pytest runs/campaign_v060/tests/gate_C0 --junitxml=sessions/<tag>/gate_C0.xml`. Evidence manifest hashed; ledger rows written by the gatekeeper only; Fable sign-off on the manifest hash → `sessions/<tag>/signoff_C0.md`. `CAMPAIGN_STATE.json` → `phase: 1`, `gates.C0 = pass` (or `partial` with the failing criterion named). Commit `campaign: C0 <pass|partial> <one line>`. Continue to Phase 1 (R6).

### 2.2 V11 identities (corrected; from the actual `twin.py`)

`P_surv` is the full q = (1, −1, 0, 0) occupation sector; `P_stretched` (S3, j = (0, ½, ½, ½)) and `P_short` (j = (½, 0, 0, 0)) are strict subchannels of it. Branch order: any |q_v| = 2 → BB̄; q = (1, −1, 0, 0) → surv; all |q_v| = 1 → meson; Σn = 4 → other; anything else uncounted. With N_VAC = (0, 2, 0, 2), `P_BBbar` can include N ≠ 4 codewords. The test asserts, to 1e-10 on synthetic inputs including negative quasi-weights: `P_surv + P_meson + P_BBbar + P_other = W_kept(N=4) + W_kept(N≠4 ∧ ∃v |q_v|=2)`; `P_stretched + P_short ≤ P_surv` with the remainder equal to the label-computed weight of the other j-configurations in that sector; ΔO(t) on synthetic pairs; yield equals the known physical fraction. If the campaign wants "channels sum to post-selected N = 4 weight", that is an *additive* estimator helper (N = 4 filter on BB̄ plus an explicit `P_Nviol` channel) in lane A0c, never a change to legacy output.

### 2.3 C0 exit (unchanged from v0.6.0 except as ruled)

V1 (R1 rule) pass; V10 pass (either "override harmless + negative control" or "fixed + pre-fix failure"); V11 four rows pass, ODR row `deferred to Phase 5`; Tier 2 rows each `done` / `retired` / `deferred` with reason (lint, stale test, sector-count test, `pyzx_basic_TP`, replicate skeleton, estimator test, G4 closure); `git status` empty; sign-off present. Any criterion not met → `C0: partial`, phase stays 0, `next_action` names it, and the session still proceeds to write the Phase 1 documents (they do not depend on C0) but does **not** start Phase 2 builds.

---

## 3. Phase 1 · preregister (target 2 h)

As v0.6.0 Phase 1, with these contents made explicit in `PREREGISTRATION.md`:

- Section 1 of v0.6.0 verbatim (hypotheses, E1–E5, claim table → `CLAIM_TABLE.md`).
- **Coupling points per R5**, four coefficients written out in code units and in electric units, with the g_E = g²/2 = 2 identification, the time points t = r·δt, and the P-S time points t ∈ {2.5, 6.25}; the `H(coeffs=(cE, cM, cH, cB), jmax, geometry, static_charges)` API and its one-parameter wrapper.
- v0.6.0 §2.5 matched-experiment rules; the KR search budget (rule 11); the GI synthesis-sprint box (4 h); mitigation arms M0–M2; shot policy; the prespecified defect classes (v0.5.0 Phase 5 list plus "KR K-scan changes after a Hamiltonian fix → rerun V8, new C3 row").
- The R1 V1 wording, the R3 V11 deferral, the R4 twin-seed ruling, the D6 G4 closure — each with a one-line reason.
- Hardware slot: `HARDWARE_MODE: disabled — no IBM credentials configured on the Hermes machine as of <date>; Phases 5–6 run on the calibration-derived twin until a human configures credentials and flips the mode; the D7/rule-10 submission blockers then apply unchanged.` Empty slots for backend, qubit path, δ_dev table, hashes (filled at C5).
- `GATE_THRESHOLDS.yaml` header `status: frozen`, SHA-256 into `hashes.thresholds`; preregistration SHA-256 into `hashes.preregistration`; `00_conventions.md` hash into `hashes.conventions`.
- `docs/refs/README.md` listing the three reference documents (v0.5.0 review, Sufian overlap, Nine-Month Plan PDF — note that pages 19–20 of the PDF needed OCR and the extracted text is not represented as complete) and the Sufian numbers of v0.6.0 Appendix A.
- Campaign todo list: one item per phase and per V-item.

**C1 exit:** the three hashes present; claim table present; nothing else. Commit `campaign: C1 pass`. Continue to Phase 2.

---

## 4. Phase 2 · reference extension, V2–V7 (target 8 h; gate partial at the cutoff)

One Fable planning call (R6), then the lanes of v0.6.0 Phase 2 (A2a–A2e, C2 auditor). Additions and priorities:

**Package move (first, 45-minute box, one Codex lane, Opus review).** Create the repo-level `src/su2qc/` by *moving* (git mv) the run-local package, leaving a thin re-export shim at the old path so the v0.5.0 gate scripts and tests keep running unchanged; rerun the legacy suite and G1–G3 on a fresh sandbox after the move (V1 under R1). Only after that is green may A2a/A2b extend the Hamiltonian builders. If the move is not green inside the box, revert it (git checkout of the moved paths), row `deferred`, and extend the run-local package in place; the campaign does not stall on packaging.

**Priority order if time runs short** (never loosen a threshold; gate C2 partial with whatever is done):
1. **V2** four-coefficient H by both routes at P-A and P-S (spectra, aligned matrix elements 1e-12; S3 observables over [0, 20] 1e-10); the wrapper reproduces the v0.5.0 H at g² = 4, m = 0.75 to 1e-12.
2. **V3** route 2 (Gauss-kernel) j_max = 1 Hamiltonian: the 9-state link needs a 4-qubit register (codes 9–15 unphysical) or a direct 9-level sparse register; D1 estimated the redundant space at ≈ 9.8 M — build the kernel projector sparsely, sector by sector, or by the vertex-singlet product structure the last review noted; route 1 already supports j_max = 1. Agreement 1e-12; counts 152 / (3, 36, 74, 36, 3).
3. **V5** static-charge bridge counts on route 2: one plaquette with charges at v0 and v2 → 112 / (2, 27, 54, 27, 2); 2×3 with charges at the far corners → 2,417 / (4, 119, 597, 977, 597, 119, 4). Counts are convention-independent; the C2 auditor derives them independently by generating function.
4. **V7 counts** 1,727 at 2×3, j_max = ½, by both routes and by a third method (spin-network enumeration).
5. **V4** truncation table: j_max = 1 versus ½ at t ∈ {0.8333, 1.6667} (P-A) and t ∈ {2.5, 6.25} (P-S), every primary observable, one plaquette.
6. **V7 dynamics**: 2×3 stretched string defined in `00_conventions.md` (quark on an even corner, antiquark hole on the adjacent odd vertex, flux along the five-link path); expm/Krylov in the N = 6 sector at both points; P_BB̄/P_meson versus t; K_min(t) curves for 10⁻³ accuracy.
7. **V6** bridge dynamics on STATIC-112 and STATIC-2417 at P-S from the Sufian strings (v0.6.0 Appendix A); pass / near / fail, never blocking (D-C7).
8. **D-C8**: the W̄ estimator (review N6), 1 h box, else `retired` with reason.

**Physics guardrails for this phase.** j_max = 1 at 2×3 is out of scope (D-C2). Route 2 at 2×3 without static charges is 7 links × 5 states × 4⁶ = 320,000 raw states at j_max = ½ — build the kernel sparsely and never densify a 320,000² matrix. The 2×3 count 1,727 and the plaquette count 82 are prior facts from the Nine-Month Plan's spin-network count; a mismatch in either route is a route bug until three methods agree. Every table carries the rule-13 columns (`point`, `model`, `arm`, `source`). No number from the Sufian report is ever reported as ours.

**C2 gate (gatekeeper; v0.6.0 §5 thresholds):** V2 both points; V3; V5 all four counts; V7 count by three methods and route agreement; V4 table; V6 recorded; V7 dynamics and K_min files present. Failure loop as v0.5.0 G1 (diagnosis child, route-owner fix, 45-minute box); route disagreement after the box → `C2: partial`, continue on the route that passes the counts, no hardware in Phase 6 until resolved (D7). Commit `campaign: C2 <pass|partial> <one line>`. **STOP here** (`STOP_AT: C2`): write `SESSION_SUMMARY.md`, update memory, remove `RESUME_LOCK`.

---

## 5. Stop conditions (this session)

- Regression not green within 2 h of T0 → repair session only; summary's first line is the failure.
- Any lane needing access outside the repository, a tool update, hardware, or a push → that lane stops and is rowed.
- Fable planning empty twice → use Section 4 as the plan and say so. Fable sign-off unavailable → gate `partial: awaiting sign-off`, no substitute model.
- Sector counts (V3, V5, V7) disagree with the independent derivation → row fails, no test edit, `DISCREPANCIES.md` entry, C2 partial.
- 12 h hard cutoff → gate the open phase partial; `next_action` verbatim; no early turn end before that.

---

## 6. Session summary (v0.6.0 §9 format, under one page) — additionally state

- Which rulings R1–R6 were applied and whether R5's arithmetic survived the auditor.
- The final `git log --oneline -8` and the list of quarantined files, if any.
- The three hashes, the new `src/su2qc/` layout (moved or deferred), and the exact command that reruns C0, C1 and C2 tests from a clean shell.
- Quotas at end of session.
- Anything a human must know before trusting a number — starting with the fact that no hardware job has ever been submitted by this project.

**Start now.** Record T0, apply R2, run the regression, close C0, preregister, extend the reference. The campaign is judged on E1–E5, on the honesty of the ledger, and on whether a physicist can rebuild every number from the tree.
