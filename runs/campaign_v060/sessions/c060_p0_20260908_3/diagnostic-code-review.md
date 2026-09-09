I read the six files and nothing else. No edits were made. Below is the review; everything is labelled **implemented** (what the code does now) or **proposal** (my suggested minimum change, not applied).

---

# C0 independent code review — v0.6.2 repair scope

No verdict on C0 is given or implied. Section A is what I can prove by reading the files. Section B is behaviour I cannot confirm without running code or reading files outside my allowed list. Section C is specification conflicts that need a Fable or human ruling before any code is written.

---

## A. Confirmed static defects

### A1. Test writes evidence into a *previous* session's directory, from a cwd-relative path
**Implemented:** `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:27-29` writes `runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json`. The session tag for this repair session is `c060_p0_<YYYYMMDD>_3` (prompt line 57). So the gate run overwrites the previous session's committed evidence file, and R11's manifest (prompt line 46) would then hash a file living under a foreign session tag.

Two further problems in the same three lines: the path is relative to the process cwd, not anchored to the repo, so the same test silently writes to a different place (or raises `FileNotFoundError`) when pytest runs from anywhere but the repo root; and the write happens *inside* the `for r in (0, 1)` loop at line 20, before the assert at line 30, so a failure at r = 0 leaves a `twin_variance.json` containing only the `"0"` key — while the §3 acceptance row requires "both r keys present" (prompt line 75).

**Proposal (minimum):** derive the output path from `Path(__file__).resolve().parents[2] / "sessions" / SESSION_TAG`, take `SESSION_TAG` from an environment variable with no default (fail loudly if unset), and write once after both r values are collected, in a `try/finally` so a failed assertion still emits the partial record under this session's tag.
**Required test:** a unit test that sets the tag env var to a temp value and asserts the file appears under that tag and nowhere else; plus a check that the file contains both `"0"` and `"1"` keys after a failing run.

### A2. Evidence file does not contain the evidence the gate row requires
**Implemented:** `test_twin_variance.py:23-26` records only `distinct_dictionaries` and `repeat_sizes`. The §3 rows demand, from `twin_variance.json`, the per-observable `two_sigma/2`, the predicted SE, the ratio, the seeds actually used, and the list of structurally empty channels (prompt lines 75-76, and R8 (b)-(d) at line 33). The bootstrap result computed at line 31 is asserted on and then discarded.

**Proposal:** serialise, per r: the seed list returned by the fixed `run_counts`, distinct count, key counts, per-observable mean, `two_sigma`, `two_sigma/2`, `Var_s`, `N̄_kept`, predicted SE, ratio, and an `empty_channels` list.
**Required test:** schema assertion over the written JSON (all keys present for both r), so the gate cannot be reached with an under-populated evidence file.

### A3. The negative control is a tautology, not a run
**Implemented:** `test_twin_variance.py:35` builds `[repeats[0][0]] * 5` — the same dict object five times — and asserts the set has one element. This is true by construction of Python set semantics; it never touches `run_counts`, never exercises seeding, and cannot fail. R8 (e) (prompt line 33) explicitly requires "a *run*, not a list comprehension": five repeats with all five run-time seeds forced equal, and the test must fail on that input.

**Proposal:** add a control that calls the production code path with the seed derivation forced to a constant, asserts exactly one distinct dictionary, and asserts that the *distinctness assertion itself* rejects that input (e.g. wrap the distinctness check in a helper and assert it raises on the control counts).
**Required test:** the control run itself, plus a meta-assertion that the helper raises. Note the mechanical obstacle in **C1** — after the R7 fix there is no public way to force equal seeds.

### A4. `assert any(two_sigma > 0)` is a weaker check than R8, and `assert all(v == v)` is a NaN check in disguise
**Implemented:** `test_twin_variance.py:32` accepts the whole variance row if a *single* observable has nonzero 2σ; R8 (b) requires every `Var_s > 0` observable to land in `[0.5, 2] × 0.894·√(Var_s/(5·N̄_kept))`. Line 33's `all(value == value ...)` is a NaN test written obscurely; the same idiom appears at `test_v1_regression.py:27`. Neither states its intent.

**Proposal:** replace line 32 with the R8 (b) ratio loop over observables with nonzero multinomial variance, collecting `Var_s == 0` observables into an explicitly reported "structurally empty" list rather than skipping them silently; replace the NaN idioms with `math.isnan(...)` assertions and a comment.
**Required test:** a synthetic-counts unit test of the ratio helper with a hand-computed `Var_s` and a known SE, asserting the helper both passes in-band and fails out-of-band.

### A5. The V10 test does not exercise the production twin
**Implemented:** `test_twin_variance.py:11` calls `twin.twin_backend(seed=101, compact=True)`. In `twin.py:33-37`, `compact=True` returns `AerSimulator(noise_model=noise)` — no `from_backend`, therefore no coupling map, no basis-gate set, and no `seed_simulator` at construction. Line 12 then transpiles against that unrouted simulator, so the ISA circuit under test is not the heavy-hex-routed circuit `run_g4.py` runs. R7 step 1 and R8 both require the production `AerSimulator.from_backend` path (prompt lines 26 and 33).

**Separate bug in the same call:** `twin_backend`'s `seed` parameter is used only on the non-compact branch (`twin.py:37`). `twin_backend(seed=101, compact=True)` silently drops the seed — the argument at `test_twin_variance.py:11` has no effect at all and is misleading to any reader auditing seeding.

**Proposal:** the V10 rows run on `twin_backend(seed=101)` (production path); keep the compact path only as a fast secondary record, clearly labelled as non-production in the JSON. Independently, either accept a seed on the compact branch (`AerSimulator(noise_model=noise, seed_simulator=seed)`) or make `compact=True` with an explicit `seed` a `TypeError` — silently ignoring it is the worst of the three.
**Required test:** assert `type(sim).__name__`/configuration shows a coupling map on the path used by the V10 rows; and a unit test that the seed passed to `twin_backend` is observable in the returned simulator's options (or that the call is rejected).

### A6. Consecutive-seed overlap is generated *inside* `run_counts`, so no wrapper change can remove it
**Implemented:** `twin.py:60-61` sets `seed_simulator=seed + k` for repeat index `k`, both via `set_options` and via the `run` kwarg. `test_twin_variance.py:14` passes one `seed=500` and the list `[measured] * 5`, so the five repeats are seeds 500…504 — exactly the adjacent-seed pattern the prompt diagnoses (prompt line 16).

The consequence matters for the repair order: any change confined to the test file (calling `run_counts` five times with well-separated seeds, say) would make the V10 test green while leaving the production defect intact, because `run_g4.py` still passes one base seed per time point. The fix must be in `run_counts`, and the V10 test must not be allowed to pass by re-parameterising the caller.

**Proposal:** as R7 states — derive per-repeat seeds from `SeedSequence(seed).spawn(len(isa_meas_list))`, pass only through `sim.run(..., seed_simulator=...)`, keep the signature.
**Required test:** an assertion that the seeds actually used are pairwise separated by more than `shots` (readable from the sidecar/`LAST_SEEDS`), so a future regression to `seed + k` fails the gate directly rather than only through a statistical symptom.

### A7. `run_counts` mutates the shared simulator and leaves it mutated
**Implemented:** `twin.py:59-60` calls `sim.set_options(seed_simulator=seed + k)` on the caller's simulator object. After the loop the simulator retains `seed_simulator = seed + N - 1`. Any later `sim.run(...)` in the same process that does not pass an explicit seed silently replays that last repeat. This is a real cross-test contamination channel: `test_twin_variance.py` and `test_twin_seed_reproducibility` construct fresh simulators, but nothing enforces that.

**Proposal:** delete the `set_options` mutation (R7 already calls for this); the `run` kwarg at line 61 is sufficient.
**Required test:** call `run_counts`, then assert the simulator's `seed_simulator` option is unchanged from its constructed value.

### A8. `run_counts` re-transpiles already-ISA circuits after measurement mapping
**Implemented:** `twin.py:58` transpiles each element of `isa_meas_list` again. `add_measurements` (`twin.py:44-51`) wired `c[i] = logical i` using `isa.layout.final_index_layout()` from the *caller's* transpile. If the second transpile alters the layout, the classical-bit mapping the docstring promises ("count strings read q11..q0", lines 5-8) no longer holds and `l12.decode` is applied to permuted strings. At `optimization_level=0` on an already-ISA circuit this is very likely a no-op, so I rate this latent rather than active — but it is an unguarded assumption sitting directly under the V10 and V11 numbers.

**Proposal:** drop the inner transpile (the argument is named `isa_meas_list`; it is already ISA), or assert `t.layout is None or t.layout.final_index_layout() == list(range(...))` before running.
**Required test:** for the production twin at r = 0 and r = 1, assert the inner transpile is layout-preserving (compare `final_index_layout()` before and after).

### A9. Closure identity: the two sides of `channel_closure_residual` use different membership rules
**Implemented:** in `twin.py`, the left-hand side sums `P_surv + P_meson + P_BBbar + P_other` from `channel_weights` (lines 133, 105-127), where the meson branch at line 123 tests only `all(abs(x) == 1 for x in q)` with **no** N = 4 condition, while `P_other` at line 125 does require `sum(ns) == 4`. The right-hand side at line 141 admits a key only if `sum(ns) == 4 or any(abs(x) == 2 for x in q)`.

So a decodable codeword with `all(abs(q_v)) == 1` and `sum(ns) != 4` (e.g. q = (1, 1, 1, −1)) enters the LHS as `P_meson` and is absent from the RHS: the residual is nonzero by construction. R9 row 1 (prompt line 37) asserts the opposite expectation — that an N ≠ 4 codeword with no |q_v| = 2 "must fall in no channel". The specification and the implementation disagree about the meson channel. Whether the meson channel should be restricted to the N = 4 sector is a physics question; see **C4**.

**Proposal (pending that ruling):** state the intended membership rule once, in one place, and derive both sides from it — a single classifier returning the channel label, with `channel_closure_residual` summing the same classifier's output on both sides. Do not patch one branch in isolation.
**Required test:** R9 row 2's violating input, constructed from a codeword in the disputed class, asserting the residual is the exact nonzero literal expected under the ruling.

### A10. Invalid keys are dropped from *both* sides, so the R9 "violating input" row cannot fail as specified
**Implemented:** `twin.py:110-111` and `twin.py:137-138` both `continue` when `l12.decode` returns `None`. An unphysical bitstring therefore contributes to neither side and cannot move the residual. R9 row 2 (prompt line 38) requires the residual to "return the correct nonzero residual on an input deliberately constructed to violate the identity through an unphysical key (which `decode` must reject)". Under the current silent-skip semantics, that row is unsatisfiable — an unphysical key is invisible, not a violation.

**Proposal:** decide the closure convention explicitly and encode it — either (a) unphysical weight is accumulated into an `unphysical` bucket that appears on the RHS, so its presence produces a nonzero residual; or (b) `channel_closure_residual` gains a strict mode that raises on undecodable keys. Silent `continue` in both places is the one option that makes the required test impossible. This is a semantics choice, not a bug fix — see **C4**.
**Required test:** the R9 row 2 input, asserting the exact residual (option a) or the exception (option b).

### A11. `test_estimator.py` does not implement R9
Comparing the file against R9 (prompt lines 35-42), row by row:

- **In-test oracle:** required "never by calling `twin.channel_weights` or `twin.channel_closure_residual` for the expected side". Lines 15-18 do compare against literals (`0.7`, `0.2`, `0.9`, `0.1`), which is fine; but lines 19 and 26 assert the residual is 0 using the implementation as its own oracle. More seriously, the *classification* the literals encode depends on `cv.N_VAC` (`twin.py:114`), which the test never restates or imports. A reader cannot check the expected channel assignment from the test alone, so it is not an independent oracle in the sense R9 requires.
- **Row 1 coverage:** required "at least eight codewords across all four channels" plus the two N ≠ 4 cases. Lines 9-12 supply three labels; `P_meson` and `P_other` are never populated and never asserted; no N ≠ 4 codewords appear.
- **Signed weights:** lines 23-26 subtract 0.8 from the first key. That key is in the stretched/surv branch, which sits on both sides of the closure identity, so the residual stays 0 for reasons unrelated to sign handling. The check has no discriminating power. R9 requires "at least two genuinely negative entries whose channel totals are still checked exactly" — no channel total is re-checked after the mutation.
- **Row 3 (remainder identity):** absent. Line 22 asserts `P_surv >= P_stretched + P_short`, an inequality that is trivially tight here (0.9 vs 0.9) and is not even generally valid once negative weights are admitted, which the same test deliberately introduces three lines later. R9 requires the **equality** `P_surv − P_stretched − P_short = 0` at 1e-10 on every synthetic input, the two-configuration derivation in the docstring, and an assertion that `l12` has exactly two physical codes with occupation (1, 1, 0, 2).
- **Row 4 (yield):** line 36 calls `twin.physical_yield(counts, physical_keys={"0000"})` — a caller-supplied key set, which R9 line 40 explicitly forbids; the yield must come from `twin.postselect`.
- **Fifth ledger row** `V11 ODR closure: deferred to Phase 5 (V12)` (prompt line 42): nothing in the file emits or marks it.

**Proposal:** rewrite as four test functions matching R9's four rows plus an explicitly `deferred`-marked ODR placeholder, with an in-test `classify(label)` function that restates the N_VAC-relative rule as literals.
**Required test:** the four rows themselves; additionally a guard asserting the test module never calls `twin.channel_weights`/`channel_closure_residual` to build an expected value (a review checklist item, or a small import-level assertion).

### A12. `physical_yield` divides by zero on empty counts, unlike `postselect`
**Implemented:** `twin.py:155` computes `sum(...) / total` with no guard; `postselect` at line 69 guards with `if tot else 0.0`. Two functions on the same page, opposite behaviour on the same degenerate input.

**Proposal:** mirror the `postselect` guard, or drop `physical_yield` entirely if R9 row 4 moves the yield to `postselect` (my preference — one code path).
**Required test:** empty-counts case asserting the defined return value.

### A13. `test_v1_regression.py` cites a prior session's conditioning file and can pass vacuously
**Implemented:** line 21-22 reads `sessions/c060_p0_20260907/slope-conditioning.json`. R10 (prompt line 44) requires this session's file, computed by the test itself: centered log-r weights over r = 8…128, Σw² = 4.80, first-order propagation against `git show HEAD`. The test computes nothing; it reads `propagated_abs_bound` from a file it did not produce and then checks the slope delta against it. The bound is unverified input, so the assertion at line 25 is circular.

Second defect: if `conditioning` is an empty list, the loop at line 24 never executes and the test passes having asserted essentially nothing (only line 27's NaN check runs). A gate row must not be able to pass on an empty evidence file.

Third: line 24 assumes a JSON list. If the file is an object, `row` is a `str` and `row["observable"]` raises `TypeError` — I could not check the file's shape, as it is outside my read list.

**Proposal:** compute the weights, Σw², and the propagated bound inside the test from the final-snapshot G3 output; write `sessions/<this-tag>/slope-conditioning.json` as an *output*; assert `len(rows) == 3` before the loop; assert Σw² ≈ 4.80 as a self-check on the weight construction.
**Required test:** a unit test of the bound computation against a hand-worked two-point example, so the propagation formula itself is covered rather than trusted.

### A14. The HEAD-bytes comparison proves the file was not touched, not that it was regenerated
**Implemented:** lines 16-18 assert the working-tree bytes of `trotter_scaling.json` equal `git show HEAD:` bytes. This is a full-file self-comparison of a committed artifact against its own commit: it passes whenever nobody edited the file, and it says nothing about whether the V1 numbers were recomputed this session — which is precisely what R10 demands. It also inverts the failure mode: a legitimate in-place rerun makes the gate row fail, which pushes reruns toward isolated copies (correct per the campaign rule) but leaves the row with no positive evidence at all.

Additionally, `subprocess.check_output(["git", "show", ...])` at line 11 runs in the *process cwd*, not `_repo()`. Under the §2.6 gate command that happens to be the repo root, but §2.2 and R7 both mandate running the regression on a fresh sandbox copy (prompt lines 24, 58). If that sandbox is a plain directory copy rather than a git clone, this test errors out — so the mandated pre-fix regression cannot run the V1 row as written.

**Proposal:** pass `cwd=_repo()` to `check_output` and handle a non-repo sandbox explicitly (skip with a recorded reason, or resolve the reference snapshot by recorded SHA-256 rather than by `git show`). Replace the identity comparison with a recorded hash of the snapshot the slopes were computed *from*, plus this session's freshly written slope file.
**Required test:** run the V1 test in a non-git temp copy and assert it either skips with the documented reason or passes against the recorded hash — never errors.

### A15. Preregistration is stale relative to the rulings it is supposed to freeze
**Implemented, in `runs/campaign_v060/PREREGISTRATION.md`:**
- Line 1 titles the document "v0.6.1" while the governing prompt is v0.6.2.
- Line 6 lists R1–R6 only; R7–R12 are unrecorded.
- Lines 61-62 do **not** inline the thresholds and preregistration hashes; they defer to `CAMPAIGN_STATE.json`. That is circular — the state file's record of the preregistration hash is not verifiable from the preregistration. R12 (prompt line 50) requires inlining.
- Line 63 gives one unlabelled conventions hash (`fb3b7525…`); R12 requires both, labelled `conventions.py` and `00_conventions.md`, because the state file carries a different value (`d7de725c…`). The document as it stands cannot tell a reader which artifact `fb3b7525…` hashes.
- The prespecified defect classes R12 requires (v0.5.0 Phase 5 list, the KR K-scan class, and the new "twin seed derivation changes → rerun V10, new C0 row") are absent.
- Line 3 declares the document "frozen at C1", and there is no amendment-history section to carry the old and new hashes R12 asks for.
- Line 47 preregisters "bootstrap 1,000 resamples"; `test_twin_variance.py:31` uses `n_boot=250` and `twin.py:158` defaults to 400. Line 47 scopes 1,000 to hardware phases, so the twin-phase value is simply unpreregistered, and three different numbers are in play.

**Proposal:** amend as R12 directs, add an "Amendments" section recording (old hash → new hash, UTC, ruling), and state one `n_boot` for the C0 V10 rows.
**Required test:** a preregistration lint asserting the file contains a labelled hash line for each of thresholds / preregistration / `conventions.py` / `00_conventions.md`, a defect-class section, and that every ruling number cited in `CAMPAIGN_STATE.json` appears in line 6's list.

---

## B. Unmeasured hypotheses — not defects until measured

These follow from the prompt's §0 diagnosis and my reading, but I cannot confirm any of them from the six files.

- **B1. The Aer per-shot seeding mechanism** (prompt line 16) is a hypothesis about a third-party library. R7 step 1's shift test is correctly *directed*: if Aer seeds shot j with `seed_simulator + j`, then run 500's shot j+1 and run 501's shot j share a seed, which is exactly `mem_500[1:] == mem_501[:-1]`. But the converse leg of R7 — "if the shift test is false on both paths, the hypothesis is wrong" — is too strong. A simulator that advances one RNG stream across shots with a different per-shot derivation would still produce overlapping-but-not-shifted memories, and R7's fallback (multisets, prefixes, every-n-th) may not detect it. The `fail: cause not located` stop condition (prompt line 90) can therefore fire on a real, differently-shaped overlap.
- **B2. That `run_g4.py` uses `500 + 10·r`** (prompt line 16) — I did not read `run_g4.py`; it is outside my list. Every claim in this review about the production caller is conditional on that.
- **B3. That the 3-distinct-of-5 with equal key counts observation follows quantitatively** from Σ_k p_k² ≈ 0.5 (prompt line 16). Plausible, unverified; it is the physics content of the diagnosis and belongs to Fable.
- **B4. Statistical power of the R8 (b) band.** With 5 repeats, a bootstrap SE estimate has a relative spread of roughly 1/√(2(n−1)) ≈ 35%. A `[0.5, 2]` acceptance band applied to *every* `Var_s > 0` observable at *both* r values is a multiple-comparison surface, and a chance excursion is not negligible. §4's third stop condition (prompt line 91) converts any single excursion into "not fixed by re-seeding" and C0 partial. Whether that is the intended risk posture is a ruling, not a code question.
- **B5. Whether `q = (1, −1, 0, 0)` keys are inside the RHS set** at `twin.py:141` depends on `sum(cv.N_VAC)`. If it is not 4, `channel_closure_residual` is nonzero for *every* input containing survival weight. I could not read `conventions.py`. This should be checked first when acting on **A9**.

---

## C. Decisions requiring a Fable or human ruling — I am not resolving these

- **C1. R7 and R8 (e) conflict mechanically.** R7 (prompt line 31) fixes the seeds inside `run_counts` via `SeedSequence(seed).spawn(...)` and keeps the signature `run_counts(isa_meas_list, shots, seed, sim)`. R8 (e) (line 33) then requires a *run* "with all five run-time seeds forced equal". After the R7 fix there is no public route to force equal seeds — the derivation is internal and deterministic in `seed`. The control needs a sanctioned hook (an optional `seeds=` override, a monkeypatched spawn, or an injectable derivation function), and adding one is a design decision on the production module. Ruling needed on which hook is acceptable.
- **C2. Where the `run_counts` fix lands.** The gate command (prompt line 62) sets `PYTHONPATH=runs/section8_v0.5.0_20260907T0628Z/src`, so the gate imports the *historical v0.5.0* twin module as production code. R7 says to diagnose on a sandbox copy of the HEAD file, but does not say where the fix is committed. Editing a frozen v0.5.0 run directory collides with the standing "never overwrite historical results" rule, while v0.6.1 §4 defers the package move to Phase 2 (prompt line 64). Ruling needed: patch in place under v0.5.0, move the package before C0, or vendor a campaign-local copy.
- **C3. R12's appends to the frozen v0.5.0 run** (`physics/DISCREPANCIES.md`, `run/DECISIONS.md`, prompt line 51) modify a frozen artifact. Appending a discrepancy note is defensible and arguably required for honesty, but it changes those files' hashes. Ruling needed on whether frozen-run annotation is permitted and how the pre-append hashes are preserved.
- **C4. The meson-channel and invalid-key semantics** behind **A9** and **A10**. Should `P_meson` be restricted to the N = 4 sector? Should undecodable keys be silently dropped, bucketed, or rejected? Both are physics/convention calls that determine what the R9 rows are even asserting. I am not resolving either.
- **C5. Frozen R4 forbids the fix R7 mandates.** `PREREGISTRATION.md:56` reads: "R4: no change to twin seed unless pre-fix dictionaries are identical; negative control required." The observed pre-fix state is 3 distinct dictionaries of 5 — *not* identical — so the frozen preregistration's own condition for changing the seed derivation is not met, while R7 requires exactly that change. This must be resolved by an explicit, recorded amendment (old hash → new hash) before the fix is made, not silently by newest-file-wins. This is the single item I would put in front of Fable first.
- **C6. R12's self-hash is a fixed point.** Prompt line 50 requires `PREREGISTRATION.md` to inline "preregistration-of-record is the hash *after* this amendment". A full-file SHA-256 written into the file it hashes cannot be computed — inserting the digest changes the digest. The rule needs a defined convention: hash the file with the hash line excluded/normalised to a placeholder, hash a canonical subset, or record the digest only in `CAMPAIGN_STATE.json` and the ledger row (which is what line 62 does today). Ruling needed on which, since the C1-amended row's verifiability depends on it.
- **C7. R11's manifest interacts badly with tests that write.** `test_twin_variance.py` writes `twin_variance.json` on every gate run, and R11 step 3 hashes it, with any later write invalidating the manifest and restarting at step 3 (prompt line 46). Any re-run of the gate command after the manifest — including a re-run to satisfy a reviewer — forces a manifest restart. Step 6's provision for `SESSION_SUMMARY.md` also implies the manifest lists a file that does not yet exist when the manifest is written. Ruling needed on whether test-written evidence is manifested at its post-run hash with reruns forbidden, or excluded and cited by the ledger row instead.
- **C8. Cleanliness target names a file that is not the one present.** R12 (prompt line 49) directs moving `artifacts/SU2ZX_GI_cost_campaign_v060_last_run.zip` to `zip_results/`. The session-start `git status` shows a different untracked archive, `artifacts/SU2ZX_latest_update_723d083_complete.zip`, plus untracked `prompts/gi_cost_campaign_v.0.6.2.md` and `runs/campaign_v060/sessions/c060_p0_20260908_3/`. I did not list `artifacts/` (outside my read list), so I cannot say whether the R12-named file exists at all. Under the standing rule that unrelated dirty paths are preserved and the `git status` empty criterion is never waived, the cleanliness row's disposition is a human call, not something to be tidied automatically.

---

## Summary

Fifteen confirmed static defects, concentrated in three places: the V10 test does not run on the production twin, does not produce the evidence its gate row cites, writes into a prior session's directory, and its negative control cannot fail (**A1-A6**); the V11 test implements roughly one of R9's four rows and uses the implementation as its own oracle, over a closure function whose two sides use inconsistent membership rules and whose invalid-key handling makes the required violating-input row unsatisfiable (**A9-A12**); and the V1 test reads a prior session's bound instead of computing one, can pass vacuously on an empty file, and asserts a file-versus-HEAD identity that is evidence of nothing (**A13-A14**). Two production-code issues sit under all of it: the shared simulator is left mutated (**A7**), and `twin_backend` silently ignores `seed` on the compact path (**A5**).

The two items I would resolve before any code is written are **C5** — the frozen R4 forbids the seed change R7 orders, and that must be amended on the record first — and **C1**, because R8's negative control has no mechanical route to exist against R7's fix as specified.

No PASS verdict for C0 is offered; nothing in this review constitutes gate acceptance or physics sign-off.
