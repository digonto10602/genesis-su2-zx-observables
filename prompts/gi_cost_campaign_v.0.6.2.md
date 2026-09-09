# SU2ZX · GI-Cost Campaign · v0.6.2 repair prompt — close C0 for real, amend C1, then Phase 2

**Hermes prompt v0.6.2 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.2.md`**
**Amends v0.6.1 (which amends v0.6.0). Both remain in force; this file adds rulings R7–R12 and a repair order for the items the C0 sign-off of session `c060_p0_20260908_2` marked blocking. Where files disagree, the newest wins. Nothing here loosens a threshold.**

**Launch (human, one line, from the SU2ZX repository root):** `hermes` then
`@prompts/gi_cost_campaign_v.0.6.2.md  Repair and re-gate C0, then continue. T0 is now.`
Everything below is addressed to you, the Hermes orchestrator session.

---

## 0. State as found (commit `723d083`) and what the evidence says

Recorded: **C0 partial, C1 pass, C2 not started.** Final fresh regression 45/45; G1 17/17, G2 20/20, G3 PASS (S8/C7 excluded by D4); the j_max = 1 sector test passed against the independent generating function 3 + 36x² + 74x⁴ + 36x⁶ + 3x⁸; R2 restorations and four scoped commits done; R5 mapping confirmed by the sign-off from `conventions.py` alone. The sign-off (`signoff_C0.md`) lists seven blocking fixes and the retry review (`review_C0_retry.md`) agrees. They are all addressed below. Read both files at boot; they are the review of record.

**The V10 failure is diagnosed here, and the diagnosis is a hypothesis you must confirm before fixing.** Evidence: `twin_variance.json` shows 5 repeats at r = 0 (compact twin, 1,024 shots, run-time seeds 500…504) giving **3 distinct dictionaries, every one with exactly 47 keys**; `twin-probe.log` shows another configuration giving 4 distinct of 5 with 24 keys each; the v0.5.0 twin printed **2σ = 0.000** at r = 0 for five repeats of 4,000 shots (status report §3.4). One shared RNG stream would give 1 distinct dictionary; five independent draws would give 5 with fluctuating key counts. Neither fits. What fits all three observations: **Aer seeds each shot with `seed_simulator + shot_index`** in its sampled-noise path, so a run at seed s + 1 replays shots 1…N of the run at seed s and adds one new shot. Adjacent dictionaries are then identical exactly when the dropped outcome equals the added one (probability Σ_k p_k², about 0.5 at r = 0 where one codeword dominates), which predicts about 1 + 4 × 0.5 = 3 distinct of 5, equal key counts, and a bootstrap σ ≈ 0 over five near-identical repeats. `run_counts` uses `seed + k`, and `run_g4.py` uses `500 + 10·r` across time points with 4,000 shots — so every v0.5.0 twin repeat overlapped its neighbours in 3,999 of 4,000 shots. The construction-time `seed_simulator = 101` is not the cause; the run-time seed does override it, as R4 anticipated.

Consequences if confirmed: (i) the fix is in the seed derivation, not in Aer options; (ii) every v0.5.0 twin σ (the r = 0 datum P_surv 0.946 ± 0.000) is void and must be so recorded; (iii) the E2 endpoint's σ_stat definition is unaffected (bootstrap over repetitions is right once the repetitions are independent).

---

## 1. Rulings (apply, log the number, do not re-plan)

**R7 · V10 diagnosis protocol and fix.** Before any code change, on a sandbox copy carrying the HEAD version of `twin.py` (`git show HEAD:runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py`), run the following and write `sessions/<tag>/v10_diagnosis.json`:

1. **Shift test (decisive).** For the r = 0 measured ISA circuit on the production twin `twin_backend(seed=101)` (the `AerSimulator.from_backend` path `run_g4.py` uses), run `sim.run(t, shots=S, seed_simulator=s, memory=True)` at s = 500 and s = 501 with S = 1,024 and compare per-shot memories: record whether `mem_500[1:] == mem_501[:-1]` (list equality, all S − 1 entries). Repeat on the compact twin. Record true/false per path.
2. **Equal-seed control.** Two runs at the same seed must return identical dictionaries (bit-identical `get_counts()`); record.
3. **Well-separated seeds.** Five runs at seeds spaced by more than S (for example 500, 500 + 10⁶, 500 + 2·10⁶, …) must give five distinct dictionaries; record the distinct count and key counts.
4. **Pre-fix V10 on the production path**, r = 0 (S = 4,000) and r = 1 (S = 1,024; the r = 1 twin is slow, see §2 timing), 5 repeats each with the HEAD seeding: record distinct counts, key counts, bootstrap two_sigma per observable.

If the shift test is **true** on the production path: the hypothesis is confirmed; fix `run_counts` so per-repeat seeds are derived from `numpy.random.SeedSequence(seed).spawn(len(isa_meas_list))`, each converted to a 31-bit int, passed only through `sim.run(..., seed_simulator=...)` (drop the `set_options` mutation), and returned alongside the counts in a sidecar `run_counts_meta(...)` or a module-level `LAST_SEEDS` so the ledger can record the seeds used; keep the signature `run_counts(isa_meas_list, shots, seed, sim)` so `run_g4.py` is unchanged. Post-fix: steps 1–4 again; the shift test must now be **false**, equal seeds still identical, five distinct at r = 0 and r = 1. If the shift test is **false** on both paths, the hypothesis is wrong: record the four measurements, then compare `mem_500` and `mem_501` for any other structural overlap (equal multisets, equal prefixes, equal every-n-th entry), report what is found, and stop the V10 lane with row `fail: cause not located` and the raw memories saved — do not change seeds blindly.

**R8 · V10 acceptance (replaces the `any(two_sigma > 0)` clause).** On the production twin, post-fix, r = 0 and r = 1, five repeats: (a) five distinct dictionaries; (b) for every observable whose multinomial variance Var_s (computed from the pooled kept counts, values o_k per codeword as `predictions_C0.md` §2.2) is nonzero, `two_sigma/2` lies within a factor 2 of 0.894 × √(Var_s/(5·N̄_kept)); (c) observables with Var_s = 0 are listed as structurally empty, never counted as failures or as evidence of determinism; (d) the D-C0 case letter from `predictions_C0.md` §3.4 is recorded with the mechanism; (e) the negative control is a *run*, not a list comprehension: five repeats with all five run-time seeds forced equal must produce one distinct dictionary and the test must fail on it. The pre-fix run of R7 step 4 is the "would have failed on the old code" evidence. Shots: r = 0 at 4,000; r = 1 at 1,024 with N̄_kept used as measured. Budget the r = 1 twin at ≈ 10 min per 5 × 1,024 shots (v0.5.0 measured 35 min for 5 × 4,000); pre-fix plus post-fix plus control is under an hour. Predictions in `predictions_C0.md` (P4–P6) are judged, not edited; a miss goes to `DISCREPANCIES.md`.

**R9 · V11 test as specified (replaces `test_estimator.py`).** Four rows, each 1e-10, each with an **independent oracle written inside the test** from the classification rule stated in v0.6.1 §2.2 (decode labels with `l12.decode`, then classify with the test's own function — never by calling `twin.channel_weights` or `twin.channel_closure_residual` for the expected side):

1. *Synthetic observables with negative quasi-weights.* At least eight codewords across all four channels plus at least one N ≠ 4 codeword with |q_v| = 2 and one N ≠ 4 codeword with no |q_v| = 2 (which must fall in no channel); weights include at least two genuinely negative entries whose channel totals are still checked exactly (a channel total may itself be negative). Closed-form expected values written as literals.
2. *Closure.* `P_surv + P_meson + P_BBbar + P_other = W_kept(N=4) + W_kept(N≠4 ∧ ∃v |q_v|=2)`, both sides from the test's oracle; `twin.channel_closure_residual` must return 0 to 1e-10 on the same input, and must return the correct nonzero residual on an input deliberately constructed to violate the identity through an unphysical key (which `decode` must reject).
3. *Remainder identity, stated correctly.* At j_max = ½ with n = (1, 1, 0, 2), Gauss's law at v3 and v4 forces j2 = j3 = j4 and at v1, v2 forces j1 to differ by ½, so the q = (1, −1, 0, 0) sector contains **exactly two** link configurations, (0, ½, ½, ½) and (½, 0, 0, 0). The test states this derivation in its docstring and asserts `P_surv − P_stretched − P_short = 0` to 1e-10 on every synthetic input — an equality, not an inequality — and additionally asserts that `l12` has exactly two physical codes with that occupation pattern. (At j_max = 1 there would be four; that is a Phase 2 note, not a C0 row.)
4. *Matched subtraction and yield.* ΔO on synthetic pairs; yield via `twin.postselect` on synthetic counts mixing physical and unphysical bitstrings with a known physical fraction — not via a caller-supplied key set.

The ledger carries a fifth row `V11 ODR closure: deferred to Phase 5 (V12)` with status `deferred`, not `fail`.

**R10 · V1 evidence must be this session's.** `test_v1_regression.py` recomputes the three slopes from the final-snapshot G3 output, computes the propagated bound itself (centered log-r weights over r = 8…128, Σw² = 4.80, first-order propagation of the primary error-array deltas against `git show HEAD`), writes `sessions/<tag>/slope-conditioning.json`, and asserts |Δslope| ≤ 10 × bound and the G3 band. The legacy-suite row cites `sessions/<tag>/final-regression.xml` produced on the snapshot that contains the fixed `twin.py`, `replicate.py` and the new tests — never a prior session's XML.

**R11 · Evidence chain order.** At the gate: (1) run the one gate command **with** `--junitxml=sessions/<tag>/gate_C0.xml` and tee the log; (2) gatekeeper writes `GATE_LEDGER.jsonl` rows and `CAMPAIGN_STATE.json`; (3) write `sessions/<tag>/evidence-manifest.json` (SHA-256 of every file the rows cite, plus the ledger, state, thresholds, preregistration, and the test files) and its `.sha256`; (4) Opus review of the manifest's files, bounded to the listed files and ≥ 40 turns (last session's review died at 15 turns and left an empty file — a review that cannot finish is rerun with a narrower file list, never recorded as done); (5) Fable sign-off naming the manifest hash; (6) after sign-off, only `SESSION_SUMMARY.md` and the commit are written, and the manifest lists them as post-sign-off. Any write to a manifested file after step 3 invalidates the manifest and restarts at step 3.

**R12 · Cleanliness, C1 amendment, and the v0.5.0 twin note.**
- `git status` at boot must show only this session's work. `artifacts/SU2ZX_GI_cost_campaign_v060_last_run.zip` is moved (not deleted) to `zip_results/`, which is where archives live; if it is not ignored there, add `zip_results/*.zip` to `.gitignore` with a commit. C0's final criterion is `git status` empty after the gate commit `campaign: C0 pass <one line>`.
- `PREREGISTRATION.md` is amended deliberately: inline the three SHA-256 values (thresholds, preregistration-of-record is the hash *after* this amendment, conventions); resolve the conventions-hash ambiguity — `CAMPAIGN_STATE.hashes.conventions` (d7de725c…) and the preregistration line (fb3b7525…) differ; record both, labelled `conventions.py` and `00_conventions.md`, and make the state file carry both keys; add the prespecified defect classes (v0.5.0 Phase 5 list plus "KR K-scan changes after a Hamiltonian fix → rerun V8, new C3 row" plus, new, "twin seed derivation changes → rerun V10, new C0 row"); add one-line reasons to R1/R3/R4. Re-hash, write `gates.C1 = pass (amended <utc>)` with the old and new hashes in the row, commit `campaign: C1 amended`.
- Append to the v0.5.0 run's `physics/DISCREPANCIES.md` and to D6 in `run/DECISIONS.md`: "D-E: v0.5.0 twin repeats were seeded `seed + k` and overlap in N − 1 of N shots under Aer's per-shot seeding; every v0.5.0 twin σ is void; no v0.5.0 twin number was ever gated. Mechanism evidence: `runs/campaign_v060/sessions/<tag>/v10_diagnosis.json`." Also grep `src/su2zx/` (v0.4.0) for the same consecutive-seed pattern used with Aer sampling; report in the summary; do not modify v0.4.0 (archived, published) — a finding there is a note for its errata, not a repair.

---

## 2. Order of work (target 5 h to the C0 gate; hard cutoff 12 h)

1. **Boot (≤ 20 min).** Session tag `c060_p0_<YYYYMMDD>_3`. Read `CAMPAIGN_STATE.json`, `signoff_C0.md`, `review_C0_retry.md`, `predictions_C0.md`. Hash checks; codeword 3793; quota check into `ENV.md` (no CLI updates, answer update prompts "no"); `TIME_LEDGER.md`, `RESUME_LOCK`. Apply the zip move of R12.
2. **Regression (rule 12)** on a fresh sandbox: legacy 4-file suite, G1–G3, `tests/gate_C0` as it stands (expect the V10 failure reproduced — record it, it is the pre-fix baseline).
3. **V10 diagnosis (R7 steps 1–4, pre-fix)** — TEST-BENCH lane, no code change, results into `v10_diagnosis.json`. Opus reads the JSON and rules "confirmed / not confirmed" in `sessions/<tag>/v10_ruling.md` before any edit to `twin.py`.
4. **Wave 1 (parallel, disjoint files):** A0a′ fix `run_counts` per R7 and rewrite `tests/gate_C0/test_twin_variance.py` per R8 (Codex; 60-minute box); A0c′ rewrite `tests/gate_C0/test_estimator.py` per R9 (Codex; 45-minute box); A0d′ rewrite `tests/gate_C0/test_v1_regression.py` per R10 (Codex; 30-minute box). Each lane gets an Opus review with a file list of at most six files and ≥ 40 turns; blocking versus advisory.
5. **Wave 2:** post-fix R7 steps 1–4 and the R8 runs on the production twin (r = 0, r = 1, negative control); V1 rerun on the final snapshot (legacy suite + G1–G3 + slope conditioning); the R12 DISCREPANCIES/D6 appends; the v0.4.0 seed-pattern grep.
6. **Gate C0 (R11).** Command: `PYTHONPATH=runs/section8_v0.5.0_20260907T0628Z/src .mamba/envs/su2zx/bin/python -m pytest runs/campaign_v060/tests/gate_C0 -q -p no:cacheprovider --junitxml=runs/campaign_v060/sessions/<tag>/gate_C0.xml`. Rows: V1 (R1/R10), V10 (R8, with seeds used, distinct counts, σ table, D-C0 case, control outcome), V11 four rows plus the `deferred` ODR row, Tier 2 (carry the existing ledger; lint/mypy findings stay deferred to Phase 2 as already rowed), cleanliness. Commit `campaign: C0 pass <one line>` (or `partial` naming the criterion), `CAMPAIGN_STATE.json` → phase 1.
7. **C1 amendment (R12)**, commit. Phase → 2.
8. **Phase 2** per v0.6.1 §4 unchanged (package move first, then V2 → V3 → V5 → V7 counts → V4 → V7 dynamics → V6 → D-C8), with one Fable planning call, **only if ≥ 6 h remain before the cutoff**; otherwise stop after C1 with `next_action: "Run phase 2 per v0.6.1 §4"`. Gate C2 partial at the cutoff if opened.

Timing note: the r = 1 production twin is the slow item (≈ 10 min per 5 × 1,024 shots). Run its pre-fix and post-fix instances detached with `wait_for_done.sh`, not in the foreground of a review.

---

## 3. Acceptance, row by row (what "pass" means this session)

| Row | Pass requires | Evidence file |
|---|---|---|
| V10 mechanism | shift test true pre-fix and false post-fix on the production path (or the not-confirmed branch of R7 fully recorded) | `v10_diagnosis.json`, `v10_ruling.md` |
| V10 distinctness | 5 of 5 at r = 0 and r = 1 post-fix; 1 of 5 under the equal-seed control; pre-fix 3–4 of 5 recorded | `twin_variance.json` (both r keys present) |
| V10 variance | `two_sigma/2` within [0.5, 2] × 0.894·√(Var_s/(5·N̄_kept)) on every Var_s > 0 observable at both r; empty channels listed | `twin_variance.json`, ledger row |
| V11 | four rows at 1e-10 with in-test oracles; the violating-input residual test; the two-configuration equality; `deferred` ODR row | `gate_C0.xml`, ledger |
| V1 | 45/45 on the final snapshot; G1 17/17, G2 20/20, G3 core PASS; slopes within 10× bound and band, bound computed this session | `final-regression.xml`, `final-G{1,2,3}.log`, `slope-conditioning.json` |
| Evidence chain | manifest written after ledger and state, before review and sign-off; hashes match on recheck; review and sign-off non-empty and on the manifest hash | `evidence-manifest.json(.sha256)`, `review_C0.md`, `signoff_C0.md` |
| Cleanliness | `git status` empty after the gate commit | `git-status-final.txt` |
| C1 amended | inline hashes, both conventions hashes, defect classes, reasons; old and new preregistration hash in the row | `PREREGISTRATION.md`, ledger |

No row may cite a prior session's artifact as its evidence. A row that cannot be met is `fail` or `deferred` with a reason; C0 is `pass` only when every row above is `pass` or (ODR only) `deferred`.

---

## 4. Stop conditions

- Regression not green (excluding the expected V10 pre-fix failure) within 2 h → repair session only.
- Shift test false on both twin paths and no structural overlap found → V10 `fail: cause not located`, C0 partial, no Phase 2; summary's first line says so, with the raw memories attached.
- Any post-fix variance ratio outside [0.5, 2] on an interior observable → not fixed by re-seeding; `DISCREPANCIES.md` entry, row fails, C0 partial.
- Review or sign-off unavailable → `partial: awaiting review/sign-off`; no substitute model; no phase advance.
- Cutoff → gate the open phase partial; `next_action` verbatim.

---

## 5. Session summary (v0.6.0 §9 format) — additionally state

- The V10 mechanism verdict in one sentence, with the shift-test truth values pre- and post-fix and the seeds used.
- The variance table: per observable, `two_sigma/2`, predicted SE, ratio, at r = 0 and r = 1.
- Which sign-off items 1–7 were closed and by which file.
- The v0.4.0 seed-pattern grep result (finding or none), not acted on.
- `git log --oneline -6`; the three hashes plus both conventions hashes; the exact commands that rerun C0 and (if reached) C2 from a clean shell.
- Anything a human must know before trusting a number — starting with: no hardware job has ever been submitted, and every v0.5.0 twin σ is void.

**Start now.** Diagnose before you fix, fix once, prove it on the production path, then gate. The campaign is judged on E1–E5, on the honesty of the ledger, and on whether a physicist can rebuild every number from the tree.
