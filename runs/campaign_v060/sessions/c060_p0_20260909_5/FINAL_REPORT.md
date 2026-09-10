# Final report — session `c060_p0_20260909_5`

**Gate C0: PARTIAL.** Written 2026-09-10 (REPORT lane). This document supersedes
`SESSION_SUMMARY.md`, which was written before the 128-shot V10 run and is out of date on
every V10 number.

**All noisy data in this report is EMULATED** (`AerSimulator.from_backend(FakeTorino)`).
No hardware job has ever been submitted; `CAMPAIGN_STATE.json` records
`hardware.mode = "disabled"`, `hardware.backend = null`, `hardware.job_ids = []`.

Every number below is followed by the file it was read from. Paths are relative to the
repository root `SU2ZX/`; unqualified filenames are inside this session directory
`runs/campaign_v060/sessions/c060_p0_20260909_5/`.

---

## 1. Bottom line

Gate C0 is **PARTIAL**, and stays partial. `CAMPAIGN_STATE.json` records
`gates.C0.status = "partial"` at `2026-09-10T15:26:42Z` with two failed items, and
`gates.C1.status = "pass"` from the earlier session (C1 remains **unamended** —
prompt v0.6.4 §0). C2 is **not started**; only preparation evidence exists.

| C0 row | Verdict | Evidence |
|---|---|---|
| V1 — restored evidence and conditioned slopes | **met** | `slope-conditioning.json`; `gate_C0.xml`; `GATE_LEDGER.jsonl` line 8 |
| V11 — estimator, four R9 rows at 1e-10 against an in-test oracle | **met** | `gate_C0.xml`; `GATE_LEDGER.jsonl` line 10 |
| V11 — ODR closure | **deferred** to Phase 5 (V12), not a C0 failure | `GATE_LEDGER.jsonl` line 11 |
| Tier 2 — j_max = 1 kernel dimension and sector histogram | **met** | `gate_C0.xml`; `GATE_LEDGER.jsonl` line 12 |
| V10 — distinctness at r = 0 | **met** (5 of 5 required) | `twin_variance.json`; `GATE_LEDGER.jsonl` line 15 |
| V10 — distinctness at r = 1 | **met** (5 of 5 required) | `twin_variance.json`; `GATE_LEDGER.jsonl` line 15 |
| V10 — negative control (equal seeds → 1 dictionary) | **met** | `twin_variance.json` (`negative_control`) |
| V10 — variance band at r = 0 | **NOT met**: `dC` ratio 0.2381, outside the [0.5, 2.0] band | `v10-128shots.log`; `gate_C0_V10_128shots.xml` |
| V10 — variance band at r = 1 | **NOT met as run**; R21 of prompt v0.6.4 directs it be recorded *not evaluable at this shot count*. It is here recorded as a measured failure (`P_BBbar` ratio 2.603) at 2.6 kept shots per repeat, and **not** as a pass. | `v10-128shots.log`; `gate_C0_V10_128shots.xml` |
| Repository cleanliness (git status empty after the gate commit) | **met** at commit `d683118` | `GATE_LEDGER.jsonl` line 14; `git-status-final.txt` |

Two gate runs exist and they are different runs. Do not conflate them:

- `gate_C0.xml` — 8 tests, **0 failures**, 122.306 s, timestamp `2026-09-09T17:19:29`.
  It covers V1, the four V11 estimator rows and the j_max = 1 counts. It contains **no**
  twin-variance test.
- `gate_C0_V10_128shots.xml` — 9 tests, **2 failures**, 0 skips, 5260.106 s, timestamp
  `2026-09-09T17:27:43`. This is the V10 file, and the two failures are the two
  variance-band tests. `v10-128shots.log` is its console output.

C0 therefore cannot close until the r = 0 `dC` finding is resolved and the r = 1 row is
either measured at an affordable-but-meaningful shot count or formally recorded under
R21 as not evaluable.

---

## 2. The defect: v0.5.0 twin repeats were one shot stream, offset by one draw

The v0.5.0 twin seeded its five repeats `seed + k` inside `run_counts`
(`runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py`). Aer seeds shot *i* of a
sampled-noise run with `seed_simulator + i`, so a run at seed *s+1* replays shots
1…N−1 of the run at seed *s*.

Measured on the production path — `AerSimulator.from_backend(FakeTorino)`, 12 qubits,
1,024 shots — **before any code was changed** (`seed-mechanism.json`, 35.1 s):

| seed pair | same-index matches | shift matches | shots |
|---|---:|---:|---:|
| 500 → 501 | 0 | 1,023 | 1,024 |
| 501 → 502 | 0 | 1,023 | 1,024 |
| 2142847655 → 3468886739 (spawned) | 0 | **1** | 1,024 |
| 3468886739 → 2616834282 (spawned) | 0 | **1** | 1,024 |

Read this literally: consecutive seeds agree on 1,023 of 1,024 shots once one stream is
shifted by a single draw, and on none of them at the same index. Two "independent
repeats" shared 1,023 of their 1,024 shots. Seeds spawned from a numpy `SeedSequence`
show the residual coincidence level of unrelated streams, 1 of 1,024.

**Consequence: every v0.5.0 twin sigma is void as an independent-repeat uncertainty.**
A bootstrap over R repeats estimates the spread of R independent sample means; here the
R samples overlap in N−1 of N shots, so the estimated spread measures the effect of
swapping one shot, not the sampling error of a repeat. It is not merely biased low by a
known factor — it is not an estimate of the intended quantity at all. This is recorded
as discrepancy **D-E** in
`runs/section8_v0.5.0_20260907T0628Z/physics/DISCREPANCIES.md` (lines 67-81) and in
`runs/section8_v0.5.0_20260907T0628Z/run/DECISIONS.md`. No v0.5.0 twin number was ever
gated, so no earlier gate verdict moves.

The same defect was searched for in the archived, published v0.4.0 package and is **not
present**: its only Aer call is `simulator.run(saved, shots=1, seed_simulator=11)` at
`src/su2zx/scaling_study.py:76`, a single shot at a fixed seed; the other Aer users pass
no `seed_simulator` at all, and the one repetition loop
(`src/su2zx/core.py:195`) is a ZX-rewrite count, not a sampler
(`v040-seed-pattern-finding.md`). Nothing in the v0.4.0 errata is amended.

Two further defects were found and ruled on in the same lane:

- The old `run_counts` mutated the caller's simulator through
  `sim.set_options(seed_simulator=...)`, overwriting a caller seed of 101 with 500.
- `channel_closure_residual` could not see an unphysical key at all (§3).

---

## 3. The repair, and the evidence that each change works

All edits are in `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py`.

**(a) Spawned seeds (ruling R7, `plan.md`).** `spawn_seeds(seed, n)` returns
`numpy.random.SeedSequence(seed).spawn(n)` children reduced to 31-bit non-negative ints,
and `run_counts` passes them **only** through `sim.run(..., seed_simulator=seeds[k])`.
The `sim.set_options` mutation is gone, so the caller's backend is untouched. The
function signature is unchanged, so `run_g4.py` needs no edit, and the seeds actually
used are exposed through the module-level `LAST_SEEDS` and `run_counts_meta()`.
Derivation is deterministic: the same `seed` and `n` always give the same list.

Evidence that it works, on the production path:

- Mechanism: spawned pairs give 1 shift match of 1,024 against 1,023 for `seed + k`
  (`seed-mechanism.json`).
- Pre-fix control, an untouched sandbox copy of the v0.5.0 package on the production
  twin at r = 0, 4,000 shots × 5 repeats: **4 distinct dictionaries of 5**, all five
  repeats carrying exactly 83 keys, 40.8 s (`v10-prefix-baseline.json`). The pre-fix
  code fails R8(a). Its r = 1 leg was never measured and the file says so, with the
  reason; the claim does not rest on it.
- Post-fix: **5 distinct of 5 at both r** (§4), with the seeds recorded
  (`twin_variance.json`).
- Negative control, which is a *real run* and not a simulation of one: all five run-time
  `seed_simulator` values forced equal to `2142847655` gives **1 distinct dictionary**,
  all five repeats at 84 keys (`twin_variance.json`, `negative_control`). The distinctness
  test therefore has demonstrated power to detect the failure mode it is guarding.

**(b) `physical_yield` on empty input (ruling in `plan.md`).** It returns `0.0` rather
than raising `ZeroDivisionError`, matching `postselect`, which returns `({}, 0.0)` on the
same input. The two functions may not disagree on the same degenerate input.

**(c) The closure-residual ruling (`ruling-R9-closure-residual.md`).** R9 requires
`channel_closure_residual` to return the correct nonzero residual on an input built to
violate the identity through an unphysical key that `l12.decode` rejects. Two prior
sessions recorded this as unsatisfiable, correctly: both sides of the identity ranged
only over decodable keys, so an undecodable key perturbed neither. Measured on the row-1
synthetic input with an unphysical key of weight 0.37, the residual was
`-1.1102230246251565e-16` **with and without the key, bit for bit**.

The ruling adds exactly one term to the right-hand side, the weight of keys that fail to
decode:

    residual = sum(four channel totals)
             - [ W(N = 4) + W(N != 4 and some |q_v| = 2) + W(undecodable) ]

implemented as `undecodable_weight(kept)` in `twin.py`. Checked consequences:

- On any contract-satisfying input (`kept` is by contract the output of `postselect`,
  which admits only physical codes) every key decodes, the new term is identically zero,
  and the residual is bit-for-bit unchanged. **No gated number, channel definition,
  threshold or observable moves.**
- On the violating input the residual becomes `-0.37`, whose magnitude is exactly the
  injected weight — what R9 demands.
- A decodable codeword that falls in no channel (an `N != 4` codeword with no `|q_v| = 2`)
  stays outside both sides, as it must; folding it in would break the identity on honest
  input.
- The alternative of *raising* on an undecodable key was rejected: it turns a measurement
  into a validator and changes the behaviour of callers that legitimately hand in
  unfiltered counts.

The test that carried this row had been written as a strict `xfail` with this reason so
it would fail loudly rather than rot; with the ruling applied the `xfail` is removed and
the row is asserted outright. It now passes:
`test_row2_violating_input_must_give_the_correct_nonzero_residual`, 0.001 s, in
`gate_C0.xml`, alongside `test_row2_closure_identity_from_the_oracle_and_zero_residual`
which confirms the residual on physical input did not move.

**(d) V1, for completeness.** The rerun reproduced the committed error arrays bit for
bit: `max_error_array_delta = 0.0` and `refit_abs_delta = 0.0` for all three observables,
slopes `Psurv -2.0979681962024204`, `E2 -2.1494619561018267`, `state -2.0070143886994325`,
all inside the band `[-2.3, -1.7]` (`slope-conditioning.json`). The ledger row records the
honest caveat: because the propagated bound is exactly zero, the slope assertion is
`0 <= 0` and **the conditioning bound was not exercised by this run**; the binding check
is the 1e-12 primary-array comparison (`GATE_LEDGER.jsonl` line 8).

---

## 4. V10 at 128 shots — measured results

Run: `gate_C0_V10_128shots.xml` / `v10-128shots.log`, 9 tests, 7 passed, 2 failed,
5260.106 s wall. Evidence file: `twin_variance.json`. Both r use the production twin
`twin.twin_backend(seed=101) = AerSimulator.from_backend(FakeTorino)`, 5 repeats,
bootstrap `n_boot = 2000`, `seed = 77`, deficit factor 0.894, acceptance band
`[0.5, 2.0]` (a factor of two either way).

The r = 1 shot count is **128, not R8's 1,024**. Prompt v0.6.4 R21 records this as a
deliberate reduction made by the campaign authority on 2026-09-09 on the cost evidence of
§6. It is a recorded reduction of an acceptance number, never R8 having been met.

| quantity | r = 0 | r = 1 |
|---|---|---|
| shots × repeats | 4,000 × 5 | 128 × 5 |
| base seed | 500 | 510 |
| run-time seeds (spawned) | 2142847655, 1321403091, 469350634, 512696676, 752330546 | 1006018469, 62393738, 794117780, 708276999, 580686603 |
| **distinct dictionaries** | **5 of 5 — met** | **5 of 5 — met** |
| raw keys per repeat | 84, 81, 83, 78, 80 | 127, 127, 122, 127, 126 |
| kept shots per repeat | 2550, 2544, 2618, 2567, 2488 | 4, 0, 4, 1, 4 |
| **N_kept_mean** | **2553.4** | **2.6** |
| **post-selection yield** | **0.63835** | **0.0203125** |
| observables with `Var_s > 0` (checked) | 13 | 11 |
| structurally empty (`Var_s = 0`, skipped, never counted as determinism) | `P_other`, `P_short` | `P_meson`, `P_short`, `P_stretched`, `P_surv` |
| **variance band** | **FAIL — 1 of 13 outside** | **FAIL — 1 of 11 outside** |
| failing observable | `dC` | `P_BBbar` |
| measured half-sigma (`two_sigma/2`) | 6.61723e-05 | 0.17197 |
| predicted SE `0.894·sqrt(Var_s/(5·N_kept_mean))` | 0.000277875 | 0.0660713 |
| **ratio** | **0.2381** (band floor 0.5) | **2.603** (band ceiling 2.0) |
| `Var_s` of the failing observable | 0.00123343 | 0.0710059 |
| negative control | 1 distinct dictionary of 5 equal-seed repeats — met | (control run at r = 0) |
| D-C0 case recorded | A | A |

Full ratio spread at r = 0, for context (`twin_variance.json`): `dC` 0.2381,
`n_v1` 0.5833, `E2_l2` 0.6358, `E2_l1` 0.7201, `n_v4` 0.8535, `n_v2` 0.8720,
`E2_l4` 0.9923, `E2_l3` 0.9967, `P_meson` 0.9967, `n_v3` 1.0978,
`P_stretched` = `P_surv` 1.1768, `P_BBbar` 1.2050. Twelve of thirteen are inside the
band; only `dC` is outside, and it is outside on the **low** side.

At r = 1 (`twin_variance.json`): `P_other` 0.6704, `E2_l4` 0.8080, `n_v4` 0.8666,
`E2_l2` 1.0605, `n_v2` 1.2651, `E2_l3` 1.4724, `E2_l1` 1.5260, `dC` 1.4604, `n_v3` 1.4129,
`n_v1` 1.6086, `P_BBbar` 2.6028. Ten of eleven inside; only `P_BBbar` outside, on the
**high** side.

Stated plainly: **the two variance tests failed, and this report does not describe either
as a pass.** The distinctness sub-row, the negative control and the structurally-empty
bookkeeping all passed at both r.

---

## 5. Analysis of the two failures

> Everything in this section is **analysis by the report author**, not measurement.
> Nothing here is evidence, and nothing here changes a verdict. Where a cause is
> proposed, the measurement that would confirm or refute it is named.

### 5.1 r = 1: no variance statement is possible at 2.6 kept shots

The r = 1 row has `N_kept_mean = 2.6` at a yield of 2.03%, from kept counts
`[4, 0, 4, 1, 4]` — **13 kept shots in total across all five repeats**
(`twin_variance.json`). My view is that the correct description of this row is *not
evaluable*, and that its numerical "failure" carries no information about the twin:

1. **The pooled sample that defines the prediction is 13 shots.** `Var_s` is formed from
   the pooled kept counts (`test_twin_variance.py`, `_multinomial_variance`). A
   13-observation estimate of a per-shot variance has an enormous relative uncertainty of
   its own; the denominator of the ratio is not a reliable prediction, so a ratio of 2.6
   is not evidence of an excess.
2. **One repeat kept zero shots, and the code treats that as a measurement of zero, not
   as missing data.** `twin.observables({})` has `tot = 0`, never enters its loop, and
   returns every channel probability as `0.0` and `dC = e2.sum() - 2.25 = -2.25`
   (`twin.py`, `observables`). `twin.bootstrap` then resamples these five per-repeat
   vectors with replacement (`twin.py`, `bootstrap`). So repeat 2 enters the bootstrap as
   a hard `P_BBbar = 0` and `dC = -2.25`. Arithmetically consistent with the reported
   values: `P_BBbar` mean 0.75 over five repeats and `dC` mean −1.1625 are both what you
   get when one of five entries is the empty-repeat sentinel. An empty repeat inflates
   between-repeat spread by construction, which is the direction of the `P_BBbar` failure
   (ratio 2.603, high side). **This is a defect in how an empty repeat is handled, and it
   is worth fixing whatever else is decided**, because the sentinel is silently
   indistinguishable from a genuine measurement of zero.
3. Even if (2) were fixed, four surviving repeats of ~3 kept shots each cannot support a
   nonparametric bootstrap. A bootstrap over five values estimates a standard deviation
   with roughly 35% relative uncertainty even under ideal conditions, before the
   discreteness of 3-shot means is considered.

**Recommendation:** record the r = 1 variance sub-row as *not evaluable at this shot
count*, with the kept counts and the yield attached, exactly as R21 of prompt v0.6.4
directs — never as a pass, and equally never as a failure of the twin. Separately, change
`observables`/`bootstrap` so an empty repeat is excluded from the bootstrap sample with a
recorded count of excluded repeats, rather than contributing sentinel values; and rerun.
The shot count that would make the row evaluable follows directly from the measured
yield: at 2.03% one needs roughly 5,000 shots per repeat for ~100 kept shots, i.e. about
50× the present cost — see §6.

### 5.2 r = 0: `dC` fluctuates four times less than the multinomial prediction

This is the substantive open finding. It is **not** a small-sample artefact in the usual
sense: 2,553.4 kept shots per repeat, 12,767 kept shots pooled, yield 63.8%.

**What `dC` is.** In `twin.py`, `observables` accumulates `w = n/tot` times per-codeword
values, and

    e2  += w * [casimir(j_1), ..., casimir(j_4)]      # -> E2_l1..E2_l4
    dC   = float(e2.sum() - 2.25)

So `dC` is *the sum of the four link Casimirs, minus a constant*. It is a derived
quantity: a linear combination of four other reported observables. That is the first
place to look, and it makes the failure structurally interesting rather than random.

**The arithmetic that frames the puzzle** (all from `twin_variance.json`, r = 0):

- Per-shot variances of the parts: `E2_l1` 0.00044024, `E2_l2` 0.00070406,
  `E2_l3` 4.4055e-05, `E2_l4` 4.4055e-05. Their **sum is 0.0012324**.
- Per-shot variance of the whole: `Var_s(dC) = 0.0012334`.

The two agree to 1.0e-06, i.e. the pooled per-shot covariances between link Casimirs are
essentially zero — `Var_s(dC)` behaves as if the four links were independent. Also note
the constant −2.25 offset cancels in a variance, as `physics-check-variance.md` states,
and the near-equality above is consistent with that: the offset is not the problem.

- Measured spreads across repeats: `two_sigma(dC) = 1.3234e-04`, whereas
  `two_sigma(E2_l1) = 2.3909e-04` and `two_sigma(E2_l2) = 2.6695e-04`.

**The repeat-to-repeat spread of the sum is smaller than the spread of either of its two
largest terms.** Per shot the terms look uncorrelated; per repeat-mean they evidently
cancel. Any explanation must reconcile those two statements.

Candidate explanations, none of which the present data can single out:

**(K1) The rare-event structure of the variance, combined with only five repeats.**
`E2_l1` has mean 5.896e-04 but `Var_s` 4.4024e-04. A two-valued observable with values
{0, 0.75} reproduces that with an occupancy near 7.8e-04, i.e. roughly **two kept shots
per repeat** carry the entire `E2_l1` variance. `E2_l2`'s variance is likewise carried by
a rare deviation from 0.75. So the prediction for `dC` is dominated by codeword classes
seen a handful of times per repeat, and its measured spread is a five-point bootstrap over
those handfuls. That estimator is lumpy and heavy-tailed regardless of the 2,553 shots in
the sample; a ratio of 0.238 could be a downward excursion of the *estimator*, not of the
physics. Supporting circumstantial pattern: the four lowest ratios at r = 0 —
`dC` 0.2381, `n_v1` 0.5833, `E2_l2` 0.6358, `E2_l1` 0.7201 — are exactly the
rare-event-dominated quantities, while the well-occupied channels sit at 1.10-1.21.
*Distinguishing measurement:* rerun r = 0 with R = 20-50 repeats at the same 4,000 shots
(cheap: 5 repeats cost 20.1 s per `twin-row-calibrated.log`). If K1 is the cause the
ratio regresses toward 1 and the spread of ratios across observables collapses.

**(K2) A genuine per-repeat anticorrelation that the pooled `Var_s` cannot see.** If the
dominant noise process moves excitation between links — raising one link's Casimir while
lowering another's within the same repeat — then the repeat-mean of the *sum* is
stabilised while each term fluctuates. The pooled second-moment calculation would miss
this if the codewords that raise `E2_l1` and those that lower `E2_l2` are different
codewords whose *counts* covary negatively across repeats (a between-repeat covariance,
which the pooled p_k formula does not model at all). Physically this is what a
Gauss-law-respecting or total-flux-conserving error channel would look like.
*Distinguishing measurement:* store the per-repeat observable vectors (they are computed
inside `twin.bootstrap` and then discarded) and compute the 4×4 empirical covariance of
the per-repeat means of `E2_l1..E2_l4`. K2 predicts a clearly negative off-diagonal
between `E2_l1` and `E2_l2`; K1 predicts no stable sign. This costs no new circuit
execution beyond one rerun and should be the first thing done.

**(K3) Pooling inflation of the prediction.** `Var_s` is computed from counts pooled
across the five repeats. If the kept-codeword composition drifts between repeats, the
pooled distribution is a mixture and its variance exceeds the average within-repeat
variance, so `predicted_se` is biased *high* and every ratio is biased *low*. That the
r = 0 ratios have median below 1 (seven of thirteen at or below 0.90) is weakly
consistent with this. *Distinguishing measurement:* compute `Var_s` separately per repeat
and compare the mean of those with the pooled `Var_s`. If pooling inflation is material,
the per-repeat values are systematically smaller, and the correct prediction uses the
within-repeat variance.

**(K4) Sub-multinomial sampling by Aer.** The prediction assumes shots are i.i.d. draws
from a fixed codeword distribution. If Aer's noise sampling is in any way stratified or
otherwise correlated across shots within a run, rare-class counts would be less dispersed
than binomial and every ratio would be depressed — but this would depress *all* rare-class
observables together, and `P_meson` (a rare class, mean 7.86e-05) sits at 0.9967, which
argues against a universal sub-multinomial effect. *Distinguishing measurement:* a
batch-means test inside a single repeat — split one repeat's shots into sub-blocks and
compare the between-block variance with the multinomial prediction on the same data. This
needs the per-shot memory (`memory=True`) rather than aggregated counts.

**(K5) A degeneracy specific to `dC` in the post-selected sector.** Post-selection admits
only physical codes, and it is possible that within the admitted set the total Casimir
takes very few distinct values while the individual link Casimirs vary, so the true
per-shot variance of `dC` is much smaller than the sum of its parts. The pooled arithmetic
above (`Var_s(dC)` ≈ sum of parts) argues **against** this, but the check is worth making
explicitly rather than inferring it from a coincidence of two numbers. *Distinguishing
measurement:* enumerate the kept codewords in the pooled sample, tabulate the distinct
values of `sum_l casimir(j_l)` with their weights, and report the exact discrete
distribution of `dC`. This is a pure post-processing step on data already in hand.

**What I am not saying.** I do not claim the twin is wrong, and I do not claim the test is
wrong. The acceptance criterion itself was checked independently before the gate and
found to be the correct multinomial prediction with the factor-two band applied to every
observable with nonzero prediction (`physics-check-variance.md`). The finding is that one
derived observable's measured spread is 4.2× below its prediction on a large sample, and
that the ordering of the candidates above cannot be settled from the artefacts this
session produced. **The single cheapest step that would discriminate among K1, K2, K3 and
K5 is to persist the per-repeat observable vectors and the per-repeat `Var_s`, which the
current code computes and throws away.** I recommend that change before any further
r = 0 spending.

---

## 6. The cost finding

The r = 1 circuit, transpiled for the production twin at `optimization_level=0` with
`seed_transpiler=101` (`tools/twin_row_calibrated.py`, `prepare`):

| quantity | value | source |
|---|---:|---|
| target qubits | 133 | `twin-row-calibrated.log` |
| total operations | **821,320** | `twin-row-calibrated.log` |
| depth | **506,888** | `twin-row-calibrated.log` |
| `cz` | 141,929 | run-lane gate-count breakdown (see caveat below) |
| `sx` | 352,800 | run-lane gate-count breakdown (see caveat below) |
| `rz` | 326,584 | run-lane gate-count breakdown (see caveat below) |
| r = 0 circuit, for scale | 7 ops, depth 1 | `twin-row-calibrated.log` |

**Caveat on the breakdown, stated because integrity requires it:** the three per-gate
counts were measured by the run lane and reported into this session, but **they are not
persisted in any file in this session directory** — the persisted figures are the total
(821,320) and the depth (506,888) in `twin-row-calibrated.log` and the total, depth and
per-shot cost quoted in the header of
`runs/campaign_v060/tests/gate_C0/test_twin_variance.py` (lines 54-58). The breakdown is
internally consistent with the persisted total: 141,929 + 352,800 + 326,584 = 821,313,
seven operations short of 821,320, and the r = 0 preparation circuit is exactly 7 ops of
other kinds. A future session should re-emit the breakdown into a JSON artefact rather
than relying on this paragraph.

**Per-shot cost and the R8 projection.** The figure of record is **15.6 s per shot**, from
the header of `runs/campaign_v060/tests/gate_C0/test_twin_variance.py` and restated in
prompt v0.6.4 §0, giving **about 22 hours** for R8's 1,024 shots × 5 repeats
(15.6 × 1024 × 5 / 3600 = 22.2 h) against the roughly ten minutes the ruling budgeted.

An earlier, higher figure exists and must not be quietly dropped:
`twin-row-calibrated.json` records `seconds_per_shot = 27.502` and
`r8_projected_hours = 39.11`, measured at 17:01 from a **4-shot** calibration
(`tools/twin_row_calibrated.py`, `main`) while the machine was under contention — the
same contention that R20 of prompt v0.6.4 now forbids ("two noisy-twin simulations on one
twelve-core machine roughly halve each other's speed"). The two figures differ by 1.76×,
which is the size of the contention effect R20 describes. Treat 15.6 s/shot as the
uncontended cost and 27.5 s/shot as the cost under load; both are measured, neither is
discarded. Three r = 1 attempts were aborted, at 88, 44 and 28 minutes
(`SESSION_SUMMARY.md`); the partial log of one of them is kept as
`gate_C0-aborted-1024shots.log` (pytest exit 137, i.e. killed, after 7 dots).

**The structured-synthesis alternative.** The r = 1 cost above is for the **generic**
transpiler synthesis. The v0.5.0 run already recorded a structured synthesis of the same
step (Gray-path multi-controlled RX on minimal control sets, exact 3×3 Givens blocks,
phase-polynomial D) whose routed cost is far lower:
`runs/section8_v0.5.0_20260907T0628Z/compile/resources_routed.md` gives **4,025 routed CZ
at r = 1** for the chosen `qiskit_L3` pipeline, against 141,929 `cz` in the generically
synthesised circuit above — a factor of 35 on two-qubit gates. The corresponding total for
the structured r = 1 circuit is **39,996 operations**, i.e. 821,320 / 39,996 = **20.5×
fewer operations**, which would bring R8's 1,024-shot r = 1 row from ~22 hours to roughly
one hour. (The 39,996 figure comes from the same run-lane report as the gate breakdown and
is subject to the same caveat: it is corroborated by, but not identical to, the routed-CZ
figure in `resources_routed.md`.)

**This is not a free win and must not be treated as one.** The structured circuit is a
*different circuit*. Before any V10 number is produced on it, it must be shown equivalent
to the circuit the campaign's other numbers were produced on, to the campaign's own
equivalence standard. Such evidence already exists for the structured pipeline in the
v0.5.0 run — `resources_routed.json` records `routed_equiv_rmax = 3.506e-13` and per-r
equivalence `1.253e-13` at r = 1 for `qiskit_L3` — but that is equivalence of the routed
structured circuit against its own logical target, established in a different session for
a different purpose. Reusing it as the basis for a C0 twin row requires a fresh, in-session
equivalence check against the exact circuit V10 uses, recorded as its own gate row. Note
also `DECISIONS.md` D6: G4 is REDUCED, the best structured synthesis is 2,156 logical
two-qubit gates per step against a budget of 250, an 8.6× logical gap; the structured
route is cheaper, not compliant.

---

## 7. C2 preparation, and the far-corners ambiguity

**No C2 verdict is issued by this session.** What follows is classical enumeration
evidence so that C2 can later be decided on measured numbers. Three independent methods
were written for every count (`tools/gi_count.py`): **M1** an integer Clebsch-Gordan
singlet multiplicity at each vertex, **M2** the nullity of `sum_a (J^a_total)^2` on the
explicit tensor-product carrier space, **M3** a Haar character integral by Gauss-Legendre
quadrature. Total wall time 351.39 s (`c2_prep/C2_prep_summary.json`).

| Row | Campaign target | Measured | Agreement |
|---|---|---|---|
| V3, j_max = 1 plaquette | 152; sectors 3 / 36 / 74 / 36 / 3 | 152, same sectors | M1, M2, M3 **and both frozen routes** agree |
| V5, static bridge, 1×1 | 112; sectors 2 / 27 / 54 / 27 / 2 | 112, same sectors | three methods agree |
| V5, static bridge, 2×3 | 2,417; sectors 4 / 119 / 597 / 977 / 597 / 119 / 4 | 2,417, same sectors | three methods agree |
| V7, 2×3 ladder | 1,727 (total only) | 1,727; sectors 4 / 95 / 426 / 677 / 426 / 95 / 4 | three methods agree |

Sources: `c2_prep/V3_jmax1_counts.json`, `c2_prep/V5_static_bridge_counts.json`,
`c2_prep/V7_ladder_2x3_counts.json`. Rounding errors are 0.0 for M1 and M2 and at most
3.72e-10 for the Haar quadrature. The V3 row additionally records route A
(`route_spinnet`) and route B (`route_gausskernel`) both giving 152 with identical label
sets *and* identical label order, a Hamiltonian of shape (152, 152) with exactly zero
Hermiticity asymmetry, and a projector orthonormality deviation of **8.881784197001252e-16
against a threshold of 1e-12**.

**The far-corners ambiguity, resolved by enumeration rather than by reading.** The campaign
describes the two static charges as sitting at "the two far corners" of the ladder, which
is not a unique placement. Rather than choose the reading that fits the target, the lane
enumerated **all fifteen** placements of two static charges on the six-vertex 2×3 ladder
and reported every count (`c2_prep/V5_static_bridge_counts.json`, `placement_audit`):

| placement | vertices | count |
|---|---|---:|
| diagonally opposite corners | (0,0)-(2,1) | **2,417** |
| diagonally opposite corners | (2,0)-(0,1) | **2,417** |
| far corners, same row | (0,0)-(2,0), (0,1)-(2,1) | 2,418 |
| corners, same column | (0,0)-(0,1), (2,0)-(2,1) | 2,442 |
| adjacent / interior placements (the remaining nine) | — | 2,706 to 3,041 |

Only the two diagonally opposite pairs give 2,417. **"Far corners" means diagonally
opposite, and the enumeration says so independently of the prose.** The single-plaquette
case behaves identically: both diagonal pairs (v0-v2, v1-v3) give 112 and all four
adjacent pairs give 113.

**A caveat the eventual C2 gate must carry.** Neither frozen route implements a 2×3
geometry; both are hard-coded to the single plaquette
(`c2_prep/V7_ladder_2x3_counts.json`, `note_on_routes`). The 1,727 count is therefore
evidenced by the three independent methods only, not by route code. As a proxy, all three
methods and both routes were run on the single plaquette at j_max = 1/2 and all five give
**82**, matching the frozen `EXPECTED_DIM`. V7's route-agreement clause needs the route
extension that V2 and V7 call for, and that work has not been done.

C2 rows **V2** (the four-coefficient Hamiltonian signature at both coupling points, with
the v0.5.0 route-agreement test rerun against it), **V4** (the truncation table at the
frozen time points) and **V6** (the bridge dynamics scan, which the campaign records as
never blocking) are **untouched and not started**.

---

## 8. What is blocked, and why

**C6, C7 and C8 are BLOCKED on credentials, and that is a fact about this machine, not a
judgement about the physics.**

- C6 requires HARDWARE rows from a real device. `HARDWARE_MODE` is disabled and no IBM
  credentials are configured on this machine (`CAMPAIGN_STATE.json`:
  `hardware.mode = "disabled"`, `backend = null`, `job_ids = []`; prompt v0.6.4 R26).
- **No job has ever been submitted.** The list of job ids is empty and has always been
  empty.
- C7 and C8 consume C6's data and are blocked transitively.
- These are recorded as **BLOCKED: awaiting credentials and a human decision to submit** —
  never as "not yet run", and no emulated result may be presented in a C6, C7 or C8 row
  (R26). This campaign does not submit hardware jobs without an explicit human
  instruction.

Also blocked or deferred, for clarity:

- **V11 ODR closure** — deferred to Phase 5 as sub-row V12, because orthogonal distance
  regression closure needs the full error model, which does not exist before Phase 5
  (`c1-amendment-prepared.md`; `GATE_LEDGER.jsonl` line 11). Not a C0 failure.
- **V10 r = 1 variance** — blocked on cost as measured in §6, and on the statistical
  impossibility described in §5.1.
- **V7 route agreement** — blocked on a route that implements a 2×3 geometry (§7).
- **C5** is the last gate reachable without hardware, and R25 requires every number in it
  to stay labelled EMULATED. Producing C5 does not authorise submission.

---

## 9. Next actions

Taken from `prompts/gi_cost_campaign_v.0.6.4.md` §2 (order of work) and its rulings, with
this session's findings folded in where they change what must be done.

1. **Close or re-mark C0.**
   - Record the r = 1 variance sub-row as *not evaluable at this shot count* per R21, with
     the kept counts `[4, 0, 4, 1, 4]`, `N_kept_mean = 2.6` and yield 0.0203 attached.
     Never as a pass.
   - Resolve the r = 0 `dC` finding (ratio 0.2381). Before spending any more simulator
     time, persist the per-repeat observable vectors and the per-repeat `Var_s` that
     `twin.bootstrap` already computes and discards, then run the K2/K3/K5 discriminating
     checks of §5.2 on data already in hand. If the answer is still open, rerun r = 0 with
     R = 20-50 repeats at 4,000 shots (5 repeats cost 20.1 s).
   - Fix the empty-repeat sentinel in `observables`/`bootstrap` (§5.1) so a repeat that
     keeps zero shots is excluded with a recorded count rather than contributing
     `P = 0`, `dC = -2.25`.
   - C0 closes as **pass with a named, evidenced reduction** only if the distinctness
     sub-row holds and the r = 0 variance band is satisfied or its failure is explained
     and ruled on. Otherwise it stays partial. Do not upgrade it to close it.
2. **Apply R22, the C1 amendment, and commit `campaign: C1 amended`.** The text is already
   prepared in `c1-amendment-prepared.md`: inline the three verified SHA-256 values
   (`GATE_THRESHOLDS.yaml` `a7d1135ebd09c2a3…`, pre-amendment `PREREGISTRATION.md`
   `b587c4859c16ec44…`, `00_conventions.md` `d7de725c3895d5f5…`, plus
   `src/su2qc/conventions.py` `fb3b7525b1a1d69b…`); resolve the conventions-hash ambiguity
   under the labelled keys `conventions_md` and `conventions_py`; add the prespecified
   defect classes including "twin seed derivation changes → rerun V10, new C0 row"; add
   the one-line reasons to R1, R3 and R4; add R21's shot reduction as an amendment entry
   naming the cost evidence; re-hash; write `gates.C1 = pass (amended <utc>)` carrying
   both the old and the new preregistration hash.
3. **Open C2 (R23)** with the counting evidence of §7 wired into its rows: build **V2**
   (the `H(coeffs=(cE,cM,cH,cB), jmax, geometry, static_charges)` signature with the
   `H(gE, mu, jmax)` wrapper reproducing v0.5.0 at `gE = 2`, at both coupling points P-A
   and P-S, plus the v0.5.0 G1 route-agreement test rerun at 1e-12 route agreement and
   1e-10 observable time series), then **V4** (the truncation table j_max = 1 against
   j_max = 1/2 at the frozen time points, every primary observable), then **V6** (the
   bridge dynamics K-scan on the static-charge cases, recorded pass/near-pass/fail, never
   blocking). Either extend a route to the 2×3 geometry or record V7's route-agreement
   clause as **unmet with its reason**; the 1,727 count itself already stands by three
   methods.
4. **C3, then C4**, each on the full R20 cycle (plan → build → watch → report → hand on),
   and with R20's contention rule observed: no long verification while an authoritative
   gate run is in flight. C3 thresholds: infidelity ≤ 1e-3, observable error ≤ 1e-3,
   unused-codeword weight ≤ 1e-5, leakage ≤ 1e-12. C4 needs V9, the E1 resource frontier
   and E5 extensibility drafts with the NOISELESS accuracy columns filled, a synthesis
   sprint closed inside four hours with its number, and the decision row naming the GI
   hardware circuit's routed CZ and depth — for which §6's structured-synthesis figures
   are the starting point, once equivalence is proven in-session.
5. **C5 on EMULATED data**, with R25's labelling: V12 with E2 passing at two or more time
   points per arm, the E3 sign pattern per arm, δ_dev frozen, the preregistration hash,
   and the QPU estimate inside the cap with its approval file. Producing C5 does not
   authorise submission.
6. **Write C6, C7 and C8 as BLOCKED** per R26, each naming its exact missing precondition:
   IBM credentials and an explicit human decision to submit.

---

### Standing constraints observed by this session

No hardware submission. No git push. No threshold, band, Hamiltonian, Gauss-law
convention or observable definition was changed; the one acceptance number that moved is
R21's r = 1 shot count, changed by the campaign authority in writing with cost evidence
and recorded as a reduction. Historical evidence in the v0.5.0 run directory was read,
never overwritten — the D-E discrepancy and the D6/D-E decision appends are additions, not
replacements. The pre-fix control ran in an untouched sandbox copy of the v0.5.0 package.
All noisy data is EMULATED.
