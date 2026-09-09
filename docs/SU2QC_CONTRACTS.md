# SU2QC_CONTRACTS — first draft (source-derived)

**Lane:** documentation-only (Opus PHYSICS-as-documentation lane of the accepted Fable plan). No code was edited, no `su2qc` module was imported or executed, and no tests were run to produce this draft. Every substantive statement below is derived from the numbered source supplied with the task, from the test files supplied with the task, or from the named historical JSON summaries. Test outputs referenced here are **historical**; they are not new gate passes.

**Campaign status (carried, unchanged by this document):** C0 **PARTIAL**; C1 **unamended**; C2 **NOT STARTED** (stored state may say BLOCKED — that stored value is superseded by NOT STARTED). No production repair has been made. All noisy-simulator results in the cited evidence are **EMULATED**. Every v0.5.0 twin sigma is **void as independent-repeat uncertainty**. All proposed repairs are **PROPOSED, NOT IMPLEMENTED**. No thresholds were changed. **No campaign physics sign-off is given or implied by this document.**

**Scope:** exactly the 43 public functions listed in the task. The AST scan reports no public classes in these modules, so there are no class entries. Imported external-library primitives (`numpy`, `scipy.sparse`, `scipy.linalg`, `hashlib`, `json`, `itertools`, `pathlib`) are not package-authored API and get no entries; locally imported `su2qc` callables are documented at their own definitions (e.g. `conventions.casimir` is documented once, not again at each import site).

**Enforcement vocabulary.** *Direct* = a supplied test calls the documented function and asserts on its result. *Indirect* = a supplied test asserts on a value that the function contributes to through another code path (this never pins the function's own contract beyond what the assertion literally states). *UNENFORCED* = no supplied test constrains the stated behaviour. **Missing input validation is never reported as a validated precondition**, and no test is described as enforcing more than its literal assertions.

## Front matter A — mandatory R15 correction (supersedes the prompt's meson paragraph)

Under the frozen conventions, occupation `n_v ∈ {0,1,2}` (`conventions.py:51`, `conventions.py:98-99`) and `N_VAC = (0,2,0,2)` (`conventions.py:53`). With `q_v = n_v − N_VAC[v]` (`conventions.py:55-57`), requiring `|q_v| = 1` at **every** vertex forces `n_1 = 1`, `n_2 = 1` (since `n_2 = 3` is outside the domain), `n_3 = 1`, `n_4 = 1`. Hence every state selected by the meson predicate has `n = (1,1,1,1)`, total `N = 4`, and `q = (1,−1,1,−1)` with `Σ_v q_v = 0`.

Therefore **the claimed non-`N=4` meson hazard and the associated `jmax=1` recurrence argument are false under these conventions and are explicitly superseded.** The incorrect original R15 paragraph is not reproduced here and is not to be quoted as true. Channels are preserved exactly as implemented (`route_gausskernel.py:457-462`, `route_spinnet.py:634-676`); no channel definition is amended by this document.

Two independent supports, kept distinct:

* **Structural argument (domain-level, exact):** the argument above rests only on `n_v ∈ {0,1,2}` and `N_VAC = (0,2,0,2)`. It holds for any `jmax` and any basis size.
* **Measured finite oracle (82 codes only):** `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` reports `physical_code_count: 82`, `vacuum_occupations: [0,2,0,2]`, and `non_N4_meson_codes: []`. This is a finite inspection of the 82-code `jmax=1/2` set, explicitly annotated `"Finite code inspection only; no channel-definition amendment or gate sign-off."` It corroborates but does not prove the structural claim, and it says nothing about `jmax=1`.

## Front matter B — closure relations as implemented

The only channel-closure content in the numbered source is the set of diagonal indicator definitions. Stated exactly:

```
q_v          = n_v - N_VAC[v]                       conventions.py:57
P_surv[i,i]  = 1 iff (q_1,q_2,q_3,q_4) == (1,-1,0,0)   route_gausskernel.py:457-458
P_meson[i,i] = 1 iff all_v |q_v| == 1                  route_gausskernel.py:459-460
P_BBbar[i,i] = 1 iff any_v |q_v| == 2                  route_gausskernel.py:461-462
```

with the same three predicates re-implemented in `route_spinnet.py:627-631`, `:660-663`, `:672-675`. These three indicators are pairwise disjoint (a `(1,−1,0,0)` charge vector has no `|q|=1` at v3/v4 and no `|q|=2` anywhere; `all |q|=1` excludes `any |q|=2`) but they are **not exhaustive**: no completeness identity, no residual, and no normalisation is computed anywhere in the numbered source. `route_spinnet.P_BBbar`'s docstring phrase "takes precedence" (`route_spinnet.py:668`) describes no implemented logic — there is no precedence branch in the code.

A separate, finer channel set (`P_stretched`, `P_short`, `P_surv`, `P_BBbar`) with an explicit closure residual exists in `su2qc.twin.twin` and is exercised by `runs/campaign_v060/tests/gate_C0/test_estimator.py:15-26`. That module's source is **not** in this bundle, so its closure equation is not quoted here and no claim is made about it beyond the literal test assertions.

**R9 (residual as an invalid-code detector) is UNSATISFIABLE AS WRITTEN.** `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` records `invalid_input: {code: 1, decode_is_none: true, residual: 0.0}`: an invalid code carrying nonzero weight is skipped by **both** sides of the residual, so the residual is identically zero whether or not such weight is present and cannot detect it. The R9 demand awaits a ruling; nothing in this document satisfies it.

## Front matter C — cross-cutting findings on functions outside the entry list

These are recorded because they bound how any listed function's outputs may be used downstream. They are **not** function entries.

* **`su2qc.twin.twin.run_counts` (measured backend/path).** Uses a fixed transpiler seed, **re-transpiles every circuit**, assigns per-circuit simulator seed `seed + k`, and mutates `sim.set_options`; the mutation **persists** after the call. Independence between the resulting "repeats" is **VIOLATED on the measured backend/path**: `runs/campaign_v060/sessions/c060_p0_20260908_3/seed-diagnosis.json` reports, for both the production and compact paths, `shift_equal: true` with `shift_matches: 1023` of `shots_shift: 1024` shots matching after a **one-shot shift**, versus `same_index_matches: 424` (production) and `414` (compact). `runs/campaign_v060/sessions/c060_p0_20260908_3/equal-seed-control.json` shows caller seed 101 overwritten to 500 (`simulator_seed_option_before: 101`, `simulator_seed_option_after: 500`), five runtime seeds all 500, `distinct: 1`. That control is scoped `"independent pre-fix r0 control; not the post-fix R8 r0/r1 controls"`. Both JSONs are `source: EMULATED`; `seed-diagnosis.json` carries `status: "partial: diagnostic process exited 124 at 2400-second cap during r1; no completed r1 counts"`. **Do not extrapolate this to every random generator or every backend** — the evidence covers the two paths named. The repair is **PROPOSED, NOT IMPLEMENTED**; campaign physics acceptance is **DEFERRED**. The current quota is **not** described as exhausted.
* **`su2qc.twin.twin.bootstrap`.** Resamples elements of `counts_list`; because those elements are correlated in the measured path above, the returned `2*s` is **not** valid independent-repeat uncertainty for them. Independence alone would also not suffice: ordinary bootstrap adequacy additionally requires representative replicates and sufficient sample size. `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:32-33` asserts only that some `two_sigma` value exceeds 0.0 and that means are not NaN; it asserts nothing about coverage or calibration. That test also writes `runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json` via a **CWD-relative** path (`test_twin_variance.py:27-29`).
* **`physical_yield` vs `postselect` on empty input.** Empty counts raise `ZeroDivisionError` in `physical_yield`, whereas `postselect` returns `({}, 0.0)` — an asymmetry recorded in `oracle-diagnostics.json` (`empty_physical_yield`, `empty_postselect`) and **UNENFORCED** by any supplied test. `test_estimator.py:36` covers only the non-empty case (`0.75`). The physical-yield denominator includes **all reported shots** and can be zero.
* **Caller preconditions, not guarantees.** Negative and unnormalised weights, and float-vs-int key typing, are accepted without validation throughout the estimator path. `test_estimator.py:23-26` demonstrates that a signed weight still yields residual 0.0; that is a demonstration of closure under signed input, not a validation of the input.
* **Encoding bit order.** `conventions.py:94` freezes `QISKIT_BIT_ORDER = "q_(N-1)...q_0"` for Qiskit strings and displayed bitstrings. `test_l12.py:28-29` pins `encode(STRETCHED) == 3793` and `decode(format(3793, "012b")) == STRETCHED`, i.e. a 12-character most-significant-first string; the state-preparation loop at `test_l12.py:45-47` uses `(c >> q) & 1` to drive qubit `q`, i.e. integer bit `q` ↔ qubit index `q`. Both conventions must be preserved by any consumer of the projector/observable entries below.

---

### su2qc.conventions.parity

**Signature** `parity(v: int) -> int`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:23-26`
**Inputs** `v` — used directly as an index into `VERTICES` (`conventions.py:20`). No range, type, or sign validation.
**Outputs** Python `int`, exactly `1` or `-1`: `1 if (x + y) % 2 == 0 else -1` where `(x, y) = VERTICES[v]`.
**Invariants**
1. `parity(0..3) == (+1, −1, +1, −1)`, materialised as the module constant `PARITY` (`conventions.py:28`). — **UNENFORCED** (no supplied test imports `conventions.parity` or asserts on `PARITY`).
2. Return is a signed unit, never 0. — **UNENFORCED**.

**Side effects** None. Module import evaluates `PARITY` once (`conventions.py:28`).
**Empty/degenerate and errors** `v ∈ {-4..-1}` is silently accepted via Python negative indexing and returns the parity of a different vertex; `|v| ≥ 4` raises `IndexError`; non-integer `v` raises `TypeError` from tuple indexing. None of these is a validated precondition.
**Enforcement** No direct coverage. Indirect only: `PARITY` enters the mass diagonal at `route_spinnet.py:324` and `route_gausskernel.py:320`, and the resulting `H` is asserted Hermitian (`tests/test_route_spinnet.py::TestHermiticity::test_H_hermitian`, line 59, assert line 63) and to commute with `N` (`test_route_spinnet.py::TestCommutator::test_H_commutes_with_N`, line 75, assert line 87). Neither assertion is sensitive to the sign pattern: any real diagonal satisfies both. The staggered sign convention is therefore **UNENFORCED**.

### su2qc.conventions.eta

**Signature** `eta(l: int) -> int`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:37-42`
**Inputs** `l` — index into `LINKS` (`conventions.py:34`). No validation.
**Outputs** `int`, `1` or `-1`. For direction `"x"` returns `1` unconditionally (`:40-41`); otherwise returns `1` if the **source** vertex has even `x`, else `-1` (`:42`).
**Invariants**
1. `eta(0..3) == (+1, −1, +1, +1)`, materialised as `ETA` (`conventions.py:44`); only `l2` (source `v2`, `x=1`) is negative. — **UNENFORCED**.
2. The staggered phase depends on the **source** vertex only, never the target. — **UNENFORCED**.

**Side effects** None; `ETA` computed at import (`:44`).
**Empty/degenerate and errors** Negative `l` wraps silently; `|l| ≥ 4` raises `IndexError`; the `"y"` branch is reached for any direction string that is not exactly `"x"`.
**Enforcement** No direct coverage. `ETA` multiplies each hopping block in `route_gausskernel._h_red` (`:416`) and `route_spinnet._hopping_matrix_element` (`:366`). Because **both routes import the same constant** from the same frozen module, any cross-route spectral agreement is *not* independent evidence for the sign pattern. **UNENFORCED**.

### su2qc.conventions.charge

**Signature** `charge(v: int, n: int) -> int`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:55-57`
**Inputs** `v` — index into `N_VAC` (`:53`), unvalidated. `n` — occupation; **not** checked against the documented domain `{0,1,2}` (`:51`).
**Outputs** `n - N_VAC[v]`. Returns `int` when `n` is `int`; a float `n` propagates to a float result (no coercion).
**Invariants**
1. `N_VAC = (0,2,0,2)`, so `charge` maps `{0,1,2}` to `{0,1,2}` at even vertices and `{−2,−1,0}` at odd vertices. — **UNENFORCED**.
2. Consequence used throughout the channel definitions: `|q_v| = 1` at every vertex ⇒ `n = (1,1,1,1)`, `N = 4`, `Σq = 0` (the R15 correction above). — Structurally exact; measured only over the finite 82-code set by `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` (`non_N4_meson_codes: []`). No supplied test asserts it.

**Side effects** None.
**Empty/degenerate and errors** `|v| ≥ 4` raises `IndexError`; out-of-domain `n` (e.g. `3`, `−1`) is accepted and produces an out-of-range charge silently.
**Enforcement** No direct coverage. Indirect: `compare._observables` calls it at `ham/compare.py:70` to build the survival mask, but `compare.py` is not imported by any supplied test. **UNENFORCED.**

### su2qc.conventions.casimir

**Signature** `casimir(j: float) -> float`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:67-69`
**Inputs** `j` — no check for non-negativity or half-integrality.
**Outputs** `j * (j + 1.0)`, always `float` (the `1.0` literal forces float promotion for integer `j`). `casimir(0.0) = 0.0`, `casimir(0.5) = 0.75`, `casimir(1.0) = 2.0`.
**Invariants**
1. `E_l² = j(j+1)` per link, matching the frozen model statement at `conventions.py:14`. — **UNENFORCED directly**; see Enforcement.
2. Monotone non-negative on `j ≥ 0`; negative `j ∈ (−1,0)` returns a negative value without error. — **UNENFORCED**.

**Side effects** None.
**Empty/degenerate and errors** Non-numeric `j` raises `TypeError`. A numpy scalar returns a numpy scalar, not a Python float.
**Enforcement** No supplied test calls `casimir`. **Indirect** coverage of the value `0.75` at `j=1/2` only: `test_route_spinnet.py::TestPureElectricDegeneracy::test_electric_degeneracies` (line 94) fixes `unit = 1e6/2.0*0.75` and asserts the degeneracy pattern `[16,16,18,16,16]` (line 102) and `rel <= 1e-8` (line 106); `test_route_gausskernel.py::test_pure_electric_clusters_and_stretched_label` (line 39) asserts the diagonal multiplicities `[16,16,18,16,16]` (line 43). Both reach `casimir` through the electric diagonal (`route_spinnet.py:319`, `route_gausskernel.py:316`, `:452`). Neither constrains `casimir` at `j=1.0`.

### su2qc.conventions.coupling_electric

**Signature** `coupling_electric(g2: float) -> float`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:77-79`
**Inputs** `g2`, unvalidated (negative and zero accepted).
**Outputs** `g2 / 2.0`, float.
**Invariants**
1. Coefficient of `Σ_l E_l²`, i.e. `H_E = (g²/2) Σ_l j_l(j_l+1)` per `conventions.py:9`. — **UNENFORCED directly**.
2. Only `route_gausskernel` consumes it (`:414`); `route_spinnet._electric_diag` hardcodes `g2 / 2.0` (`route_spinnet.py:319`) instead of importing it. The two routes therefore duplicate rather than share this constant. — **UNENFORCED**.

**Side effects** None.
**Empty/degenerate and errors** `g2 = 0.0` returns `0.0` without error.
**Enforcement** **Indirect** only, and only at `g2 = 1e6`: the `unit = g2/2*0.75` scaling used in `test_route_spinnet.py:98` and the cluster multiplicities asserted at `test_route_gausskernel.py:43` are consistent with the factor `1/2`, but no supplied test calls the function or varies `g2` against it.

### su2qc.conventions.coupling_magnetic

**Signature** `coupling_magnetic(g2: float) -> float`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:81-83`
**Inputs** `g2`, unvalidated.
**Outputs** `1.0 / (2.0 * g2)`, float. Sign convention per docstring and `conventions.py:12`: this is `c` in `H_B = −c · Tr(U_box + U_box†)`; the minus sign lives at the call site (`route_gausskernel.py:418`), not in this function.
**Invariants**
1. `H_B = −(1/(2g²)) Tr(U_box + U_box†)`. — **UNENFORCED**.
2. Consumed by `route_gausskernel._h_red` (`:418`) only. `route_spinnet.build_hamiltonian` hardcodes `-(1.0 / (2.0 * g2))` at `route_spinnet.py:515` rather than calling this function — a second duplication of a frozen constant. — **UNENFORCED**.

**Side effects** None.
**Empty/degenerate and errors** `g2 = 0.0` raises `ZeroDivisionError` (float division); `g2 < 0` silently flips the sign of the magnetic coupling.
**Enforcement** No supplied test calls it, and no supplied test pins any magnetic matrix element magnitude. **UNENFORCED.**

### su2qc.conventions.tree_level_resonance

**Signature** `tree_level_resonance(g2: float) -> float`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py:89-90` (no docstring; the physics rationale is the preceding comment at `:87-88` — removing one `j=1/2` link releases `(g²/2)(3/4)`, equal to the pair cost `2m` at `m* = 3g²/16`).
**Inputs** `g2`, unvalidated.
**Outputs** `3.0 * g2 / 16.0`, float. `tree_level_resonance(1.0) = 0.1875`.
**Invariants**
1. `m*(g²) = 3g²/16`, linear in `g2` through the origin. — **UNENFORCED**.

**Side effects** None.
**Empty/degenerate and errors** No error path.
**Enforcement** **UNENFORCED.** The value `0.1875` appears as a literal in `ham/compare.py:23` (`COUPLING_POINTS`), `compare.time_series_comparison`'s default (`:88`), and `test_route_spinnet.py:55,72` — in every case hardcoded, never obtained by calling this function. No test asserts consistency between the literal and the function.

### su2qc.ham.compare.spectra_comparison

**Signature** `spectra_comparison(jmax=0.5, points=COUPLING_POINTS)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py:45-60` (helpers `_get_routes` `:34-37`; defaults `COUPLING_POINTS` `:21-28`)
**Inputs** `jmax` — forwarded verbatim to both route builders. `points` — iterable of `(g2, m)` pairs; the default list has 6 entries and includes `m = 0.0` (`:22`). No validation of either argument.
**Outputs** `list[dict]`, one dict per point, in the order of `points`, each with keys `g2`, `m`, `max_rel_dev` (Python float), `dim1`, `dim2` (ints from `H.shape[0]`). A fresh list is built per call; nothing is cached here.
**Invariants**
1. `max_rel_dev = max|e1 − e2| / max(1.0, max|e1|)` over **sorted** eigenvalues from `scipy.linalg.eigh(..., eigvals_only=True)` (`:54-57`). The normalising scale uses route 1's spectrum only — the comparison is asymmetric. — **UNENFORCED**.
2. Comparison is basis-independent (sorted spectra), so it cannot detect a basis-ordering disagreement between routes. — **UNENFORCED**.
3. The function **returns** deviations and applies **no threshold and no assertion**; acceptance is entirely the caller's. — **UNENFORCED**.

**Side effects** Imports `route_spinnet` and `route_gausskernel` lazily on first call (`:35-36`). Through `route_gausskernel.build_hamiltonian` it populates the module-global caches `_CACHE` (`route_gausskernel.py:155-162`), `_TERMS_CACHE` and `U_CONVENTION` (`:349-350`, `:378-379`) — persistent process state, and the dominant cost of the first call. `H1`/`H2` are densified via `.toarray()` (`:52-53`), so peak memory is `O(dim²)` per point. No file writes.
**Empty/degenerate and errors** `points = []` returns `[]` (vacuous, no error). `jmax > 0.75` raises `NotImplementedError` from route 2 (`route_gausskernel.py:425-427`) before any comparison. If the two routes ever returned different dimensions, `e1 - e2` (`:57`) raises a numpy broadcast `ValueError` rather than reporting a mismatch. Route 1 raises `ValueError` for `jmax ∉ {0.5, 1.0}` (`route_spinnet.py:245`).
**Enforcement** **UNENFORCED.** No supplied test file imports `su2qc.ham.compare`. The cross-route agreement criterion described in the module docstring (`:1-7`) is therefore not covered by any test in this bundle; the only supplied cross-route assertions are on **dimensions and label counts**, not spectra (`test_route_gausskernel.py:17-26`; `runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py:36-40`).

### su2qc.ham.compare.time_series_comparison

**Signature** `time_series_comparison(g2=1.0, m=0.1875, jmax=0.5, times=TIMES)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py:88-106` (observable helper `_observables` `:63-85`; `STRETCHED` `:30`; `TIMES = np.linspace(0.0, 10.0, 21)` `:31`; `_norm_label` `:40-42`)
**Inputs** `g2`, `m`, `jmax` forwarded to both builders; `times` a sequence of length ≥ 2 (index `times[1]` is taken at `:74`).
**Outputs** Tuple `(dev, s1)`. `dev` is a Python float: the maximum over time steps of the absolute deviations of `P_surv`, all four `n_v`, and all four `E2_l` between routes (`:101-105`). `s1` is **route 1's** series only — a list of dicts `{"t": float, "P_surv": float, "n": list[4], "E2": list[4]}` (`:80-83`). Route 2's series is discarded.
**Invariants**
1. Initial state is the single basis vector matching `STRETCHED = ((0.0,0.5,0.5,0.5),(1,1,0,2),0)` after label normalisation that **drops the intertwiner tag** and coerces `j` to float / `n` to int (`_norm_label`, `:40-42`). — **UNENFORCED**.
2. Uniqueness of that label in each basis is checked by `assert len(i1) == 1 and len(i2) == 1` (`:98`) — an in-function assertion, removed under `python -O`.
3. Channel masks are computed from labels, not from route internals (`:70-73`), so the comparison is basis-order independent.
4. **Implicit assumption, not validated:** a single propagator `U = expm(-1j*H*dt)` with `dt = times[1] - times[0]` is reused for every step (`:74-75,84`). Non-uniform `times` silently produce wrong results, and `times[0] != 0.0` makes the reported `t` label (`:80`) inconsistent with the actual elapsed evolution `i*dt`. — **UNENFORCED**.
5. `series[i]` records the probabilities **before** applying the step at `:84`, so entry `i` is the state after exactly `i` propagator applications.

**Side effects** Same lazy imports and route-2 global cache population as `spectra_comparison`. Dense `expm` on an `82×82` matrix per route. No file writes.
**Empty/degenerate and errors** `len(times) < 2` raises `IndexError` at `:74`. Label absent or duplicated ⇒ `AssertionError` at `:98`. `jmax > 0.75` ⇒ `NotImplementedError` from route 2. `zip(s1, s2)` (`:102`) silently truncates to the shorter series if the two ever differed in length.
**Enforcement** **UNENFORCED** (no supplied test imports `compare`).

### su2qc.ham.limits.pure_electric_check

**Signature** `pure_electric_check(g2_big=1e6)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py:28-43`
**Inputs** `g2_big` — used both as the coupling and as the tolerance scale. `m` and `jmax` are **not** parameters: hardcoded `0.0` and `0.5` at `:32`.
**Outputs** `dict` with `"degeneracies"` (`list[int]` of length 5, counts for `k = 0..4`), `"rel_dev"` (Python float), `"ok"` (Python `bool`).
**Invariants**
1. `unit = g2_big/2 * 0.75` and `k = rint(eval/unit)`; degeneracies are counted only for `k ∈ 0..4` (`:36-37`), so eigenvalues outside that band are silently excluded from `got` while still contributing to `rel`.
2. `ok` requires **both** `got == [16,16,18,16,16]` and `rel <= 1e-8 * g2_big/1e6 * 100` (`:40`). At the default `g2_big=1e6` the effective relative tolerance is **1e-6**, not the `1e-8` the surrounding comments suggest; the tolerance scales **linearly with `g2_big`**, i.e. the check becomes looser at larger coupling. — **UNENFORCED**.
3. `ok` is coerced to Python `bool` (`:43`); `rel_dev` to Python `float`.

**Side effects** None inside the function. **Module import** has side effects: `sys.path` is mutated twice at `limits.py:20-25`, including a `parents[4].parent` walk to a presumed repo root — position-dependent on the file's location in the tree.
**Empty/degenerate and errors** `g2_big = 0.0` ⇒ `ZeroDivisionError` in `route_spinnet` at `:515` before this function's arithmetic. Dense `eigh` on `82×82` (`:33`).
**Enforcement** **UNENFORCED directly** — no supplied test imports `su2qc.ham.limits`. The near-identical copy `route_spinnet.pure_electric_check` (`:739-753`) *is* called directly by `test_route_spinnet.py::TestCorePhysics::test_pure_electric_check` (line 166, assert line 169). The degeneracy pattern itself is asserted independently at `test_route_spinnet.py:102` and `test_route_gausskernel.py:43`; those are assertions on separately recomputed values, not on this function's return.

### su2qc.ham.limits.frozen_matter_check

**Signature** `frozen_matter_check(tol=1e-9)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py:46-99`
**Inputs** `tol` — **the argument has no effect**: it is unconditionally overwritten at `:69` with `tol = 1e-8`. The returned `"tol"` field is therefore always `1e-8` regardless of the caller. `g2 = 1.3` and `m_big = 1e7` are hardcoded (`:67-68`).
**Outputs** `dict` with `"dev"` (float, max diagonal deviation), `"offdiag_times_g2"` (float, `Re(offd) * g2` — a **recorded** number, not a checked one), `"tol"` (always `1e-8`), `"ok"` (Python `bool`), `"note"` (fixed string).
**Invariants**
1. The 2×2 block is extracted by exact projection onto the two labels `((0,0,0,0),(0,2,0,2))` and `((.5,.5,.5,.5),(0,2,0,2))` (`:73-82`), then shifted so `block[0,0] = 0` (`:84`).
2. Expected electric splitting is `diag(0, 1.5*g2)` (`:87`); `dev` compares only the **diagonal** (`:94`).
3. `ok = (dev ≤ tol·max(1, 1.5g2)) and (|Im offd| ≤ 1e-12) and (Re offd < 0)` (`:96-97`). The off-diagonal **magnitude** is *not* compared to any monograph value — only reality and sign are checked; the normalisation ratio is deliberately recorded for the reconciliation document (`:89-93`, `:99`). Any claim that this function verifies the magnetic normalisation would overstate it. — **UNENFORCED**.
4. The extraction relies on large `m` suppressing matter excitations; the residual `O(h²/m)` (~2.5e-9 at `m=1e7` per `:69-70`) is absorbed by the relaxed tolerance, not measured separately.

**Side effects** None beyond the module-import `sys.path` mutation (`limits.py:20-25`). Dense `82×82` array (`:72`).
**Empty/degenerate and errors** `AssertionError` at `:80` if either of the two labels is missing or duplicated (removed under `python -O`). Basis construction cost at `m=1e7` is the full route-1 build.
**Enforcement** **UNENFORCED.** No supplied test imports `su2qc.ham.limits`.

### su2qc.ham.limits.magnetic_off_check

**Signature** `magnetic_off_check(tol=1e-10)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py:102-122`
**Inputs** `tol` — here genuinely used (`:122`). `g2 = 1.1`, `m = 0.3`, `jmax = 0.5` hardcoded (`:105-106`).
**Outputs** `dict` with `"dev"` (float), `"ok"` (bool), `"note"` (string naming which comparison source was used).
**Invariants**
1. `dev = max|e1 − e2| / max(1.0, max|e1|)` on sorted spectra (`:121`); `ok = dev <= tol` (`:122`).
2. The `"note"` field distinguishes the two possible comparators: `"independent limits_1d chain"` (`:115`) versus `"cross-route B-off comparison (limits_1d unavailable)"` (`:120`). **In the fallback branch the check is *not* independent** — it compares route 1 against route 2, both of which import the same frozen conventions. The docstring's "independent periodic 1D 4-site SU(2) chain" (`:103`) describes only the first branch. — **UNENFORCED**.
3. The `hasattr` guard at `:106-107` and the failure dict at `:109-110` are **unreachable for the current route 1**, which does define `build_hamiltonian_no_magnetic` (`route_spinnet.py:531`). — **UNENFORCED**.

**Side effects** None beyond module-import `sys.path` mutation. In the fallback branch, populates route-2 module globals `_CACHE`/`_TERMS_CACHE`/`U_CONVENTION`.
**Empty/degenerate and errors** Only `ImportError` is caught (`:116`); any other exception from `limits_1d.chain_spectrum` propagates. If `limits_1d` returns a spectrum of a different length, `e1 - e2` (`:121`) raises a numpy broadcast `ValueError` rather than reporting a mismatch.
**Enforcement** **UNENFORCED.** No supplied test imports `su2qc.ham.limits`; nothing in this bundle exercises `limits_1d` either.

### su2qc.ham.route_gausskernel.kernel_dimension

**Signature** `kernel_dimension(jmax)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:165-166`
**Inputs** `jmax` — coerced to `float` inside `_basis` (`:159`), so `kernel_dimension(1)` and `kernel_dimension(1.0)` hit the same cache entry.
**Outputs** `int` — `len(labels)` for the Gauss-law kernel at that truncation.
**Invariants**
1. `kernel_dimension(0.5) == 82`, `kernel_dimension(1.0) == 152`, matching `conventions.EXPECTED_DIM` (`conventions.py:72`). — `1.0` case: **DIRECT**, `tests/test_route_gausskernel.py::test_kernel_dimensions_and_number_sectors` (line 12), assert line 22. The `0.5` case is asserted through `build_hamiltonian`'s labels (line 17), not through this function.
2. **No validation of `jmax`.** `_spins` uses `int(2*jmax) + 1` (`:34`), so any `jmax ∈ [0.5, 1.0)` silently yields the `jmax=0.5` spin set and returns 82. — **UNENFORCED**.

**Side effects** First call for a given `jmax` runs `_physical_basis` (`:104-152`) and stores `(labels, P)` in the module-global `_CACHE` (`:155-162`). This is expensive (per-vertex singlet diagonalisations over the full `itertools.product` of spins × occupations) and the result persists for the process lifetime.
**Empty/degenerate and errors** Non-numeric `jmax` raises `TypeError` at `float(jmax)`.
**Enforcement** Direct at `jmax=1.0` only (line 22). The same test also asserts `P1` orthonormality to `1e-12` (line 26) and `len(labels1) == 152` (line 25), but those go through `_basis`, a private helper, not through `kernel_dimension`.

### su2qc.ham.route_gausskernel.gauss_commutator_norms

**Signature** `gauss_commutator_norms(jmax)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:390-407`
**Inputs** `jmax`, coerced to `float` (`:392`).
**Outputs** `dict[str, float]` with exactly the keys `"electric"`, `"mass"`, `"hop_0"`, `"hop_1"`, `"hop_2"`, `"hop_3"`, `"magnetic"` (`:395-397`). Each value is the max over `a ∈ 0..2` and `v ∈ 0..3` of the maximum absolute stored entry of `[G^a_v, op]`; a commutator with no stored nonzeros contributes `0.0` (`:404-405`).
**Invariants**
1. `"magnetic"` is evaluated on the **Hermitised** plaquette operator `trU + trU†` (`:397`), whereas the convention-selection routine `_select_convention` tests only `hops[0]` and the bare `trU` (`:364`). The returned dictionary is thus a broader diagnostic than the selection criterion. — **UNENFORCED** as a distinction.
2. The reported value is a max over **stored** entries (`c.data`), so exact numerical cancellation that leaves an explicit zero stored is counted as 0.0 — the metric is not an operator norm.
3. All seven groups vanish to `1e-12` at `jmax=0.5`. — **DIRECT**: `tests/test_route_gausskernel.py::test_hermiticity_and_gauss_diagnostics` (line 29), assert line 36 (`max(norms.values()) <= 1e-12`). Note the assertion is on the **max over values only**; it does not pin the key set, and it covers `jmax=0.5` only.

**Side effects** Calls `_terms(jmax)` (`:383-387`), which on a cache miss runs `_select_convention` — this populates the module globals `U_CONVENTION` and `_TERMS_CACHE` (`:378-379`) and contains its own `assert best is not None` (`:377`). Also rebuilds the full Gauss operators via `_gauss_ops(jmax)` on **every** call (`:394`) — no caching there. Memory is dominated by the redundant space (`dl⁴ × 256`).
**Empty/degenerate and errors** `AssertionError` from `_select_convention` (`:377`) if no `(conjL, conjR)` variant commutes with `G`. At `jmax=1.0` the redundant space is ~9.8M-dimensional per the module docstring (`:14-17`) — no guard prevents the attempt.
**Enforcement** Direct at `jmax=0.5` (line 36). `jmax=1.0` behaviour: **UNENFORCED**.

### su2qc.ham.route_gausskernel.build_hamiltonian

**Signature** `build_hamiltonian(g2, m, jmax)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:422-431` (redundant-space assembly `_h_red` `:412-419`)
**Inputs** `g2` (electric and magnetic coupling), `m` (mass), `jmax` coerced to float (`:423`). No validation of `g2` or `m`.
**Outputs** Three-tuple `(H, labels, P)`:
* `H` — `scipy.sparse.csr_matrix`, complex, shape `(D, D)` with `D = len(labels)`, explicitly symmetrised as `(H + H†)/2` to remove ~1e-17 asymmetry (`:430`).
* `labels` — the **cached list object** from `_CACHE` (`:428`, `:155-162`). It is **not copied**: callers mutating or sorting it corrupt the cache for every later call in the process. Order is the enumeration order of `_physical_basis` (`itertools.product` over spins, then over occupations, `:110-111`).
* `P` — the cached CSC isometry from the redundant space, likewise **aliased, not copied**.

Note the arity: route 1's `build_hamiltonian` returns a **2-tuple**, this one a **3-tuple**; callers in the bundle handle this with `out[0], out[1]` (`compare.py:93-94`) or `[:2]` slicing (`limits.py:32`).
**Invariants**
1. `D = 82` at `jmax=0.5`, with fermion-number sector counts `{0:2, 1:0, 2:20, 3:0, 4:38, 5:0, 6:20, 7:0, 8:2}` — **DIRECT**: `test_route_gausskernel.py::test_kernel_dimensions_and_number_sectors` (line 12), asserts lines 17-18.
2. `P† P = I` to `1e-12` — **DIRECT**, same test, line 19.
3. `H` Hermitian to `1e-13` at `(g2, m) = (0.73, 0.19)` — **DIRECT**: `test_hermiticity_and_gauss_diagnostics` (line 29), assert line 33. Note this is the *post*-symmetrisation matrix, so the assertion largely re-checks line `:430`.
4. Pure-electric diagonal clusters `[16,16,18,16,16]` at `g2 = 1e6, m = 0` — **DIRECT**: `test_pure_electric_clusters_and_stretched_label` (line 39), assert line 43. This asserts on `H.diagonal()`, i.e. the diagonal only, not the eigenvalues.
5. The stretched label `((0.0,0.5,0.5,0.5),(1,1,0,2),0)` appears exactly once in `labels` — **DIRECT**, same test, line 45.
6. `jmax > 0.75` raises `NotImplementedError` with the message naming `kernel_dimension(1.0) (=152)` (`:424-427`). — **UNENFORCED** (no supplied test asserts the raise). Values in `(0.5, 0.75]` do **not** raise and silently reuse the `jmax=0.5` spin set (`:34`).
7. `H` is the exact projection `P† H_red P` — no truncation or thresholding is applied beyond the symmetrisation.

**Side effects** Populates/uses `_CACHE`, `_TERMS_CACHE`, `U_CONVENTION` (module globals). First call for a truncation performs the numerical `U`-convention selection (`:353-380`). No file writes, no printing.
**Empty/degenerate and errors** `g2 = 0.0` ⇒ `ZeroDivisionError` via `coupling_magnetic` (`conventions.py:83`) at `:418`. `NotImplementedError` as in (6). Memory/time at `jmax=1.0` is the documented blocker (`:14-17`).
**Enforcement** Items 1-5 direct as cited; items 6-7 **UNENFORCED**. `runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py:35,39-40` exercises the `jmax=1` **kernel** via `route2._basis(1.0)`, not this function.

### su2qc.ham.route_gausskernel.build_hamiltonian_no_magnetic

**Signature** `build_hamiltonian_no_magnetic(g2, m, jmax)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:434-441`
**Inputs** As `build_hamiltonian`.
**Outputs** Same three-tuple shape `(H, labels, P)`, same cached-and-aliased `labels`/`P`, same `(H + H†)/2` symmetrisation (`:440`). `H` omits the magnetic term via `_h_red(..., magnetic=False)` (`:439`, `:417-418`).
**Invariants**
1. `H_no_mag = coupling_electric(g2)·electric + m·mass + Σ_l (1/2)·ETA[l]·hops[l]` exactly (`:414-416`) — i.e. `build_hamiltonian` minus `coupling_magnetic(g2)·(trU + trU†)`. — **UNENFORCED** (no supplied test compares the two).
2. `jmax > 0.75` raises `NotImplementedError("see build_hamiltonian")` (`:436-437`). — **UNENFORCED**.
3. Because the magnetic term is dropped, `g2 = 0.0` no longer divides by zero here — it yields a zero electric coefficient instead. This asymmetry with `build_hamiltonian` is unvalidated.

**Side effects** Same module-global cache population as `build_hamiltonian`.
**Empty/degenerate and errors** As above.
**Enforcement** **UNENFORCED.** No supplied test calls it. Its only in-bundle consumer is the fallback branch of `limits.magnetic_off_check` (`limits.py:118`), which is itself untested.

### su2qc.ham.route_gausskernel.get_state

**Signature** `get_state(label, basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:444-445`
**Inputs** `label` — a full label tuple; `basis_labels` — the list returned by `build_hamiltonian`.
**Outputs** `int` — the index of the **first** match, via `list.index`. Linear scan, `O(D)` per call.
**Invariants**
1. Matching is Python tuple equality, which uses `==` elementwise. Consequently an integer `0` compares equal to the stored float `0.0`, so mixed int/float `j` tuples **do** match; but an `int` vs `float` mismatch in the tag or a numpy scalar with different equality semantics is not specially handled. — **UNENFORCED**.
2. Returns the first index only; duplicate labels would be silently masked. The uniqueness of the stretched label is asserted separately at `test_route_gausskernel.py:45`, not by this function.

**Side effects** None.
**Empty/degenerate and errors** `ValueError: tuple is not in list` when the label is absent — **no** custom message, and no `None` sentinel. Empty `basis_labels` always raises.
**Enforcement** **Weak direct.** `tests/test_route_gausskernel.py::test_pure_electric_clusters_and_stretched_label` (line 39) asserts only `get_state(stretched, labels) >= 0` (line 46). Since `list.index` never returns a negative value, that assertion verifies only that no `ValueError` was raised; **it does not verify that the returned index addresses the correct row** of `H`. No supplied test checks the absent-label `ValueError`.

### su2qc.ham.route_gausskernel.E2_link

**Signature** `E2_link(l, basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:466-467` (builder `_obs` `:450-463`)
**Inputs** `l` — link index, **unvalidated**; `basis_labels` — label list.
**Outputs** A **freshly constructed** `scipy.sparse` CSR matrix (`format="csr"` at `:452`), diagonal, shape `(D, D)`, with entries `casimir(float(j_l))` per label. Real (float64) dtype — **not** complex, unlike `H`. Each call returns a new object; there is **no caching** at this layer.
**Invariants**
1. `E2_link` is diagonal in the label basis and its row order matches `basis_labels` exactly — so it is only valid against an `H` built from the *same* label list.
2. Entry values are `0.0` for `j=0`, `0.75` for `j=1/2`, `2.0` for `j=1` (`conventions.py:69`).
3. `l` is not range-checked: negative `l` wraps to another link, `|l| ≥ 4` raises `IndexError` from the list index at `:467`.

**Side effects** **Performance contract:** every call rebuilds *all six* observable groups — four `E`, four `n_v`, `N`, and three projectors (`_obs`, `:450-463`) — and discards five of them. Cost is `O(6·D)` construction per accessor call.
**Empty/degenerate and errors** `basis_labels = []` yields a `(0,0)` matrix without error. Malformed labels raise `IndexError`/`TypeError` from `x[0][l]`.
**Enforcement** **UNENFORCED.** No supplied test imports `E2_link`. The nearest coverage is `tests/test_dynamics.py::test_channel_masks_partition_N4_sector` (line 44) and `tests/test_l12.py::test_trotter_scaling` (line 100, via `_diagnostics`), which exercise a **different implementation** in `su2qc.dynamics.scan`.

### su2qc.ham.route_gausskernel.n_op

**Signature** `n_op(v, basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:470-471` (`_obs` `:454`)
**Inputs** `v` — vertex index, unvalidated; `basis_labels`.
**Outputs** New CSR diagonal matrix, entries `x[1][v]` taken **as stored integers** (`:454`) — so the dtype is integer, not float or complex. Contrast `route_spinnet.number_op`, which casts to `float` (`route_spinnet.py:590`) and produces a complex matrix. Mixing the two in one arithmetic expression will upcast silently.
**Invariants**
1. Diagonal, aligned to `basis_labels` order.
2. Values lie in `{0,1,2}` by construction of the basis (`conventions.py:51`), not by any check in this function.
3. `v` unvalidated: negative wraps, `|v| ≥ 4` ⇒ `IndexError`.

**Side effects** Rebuilds all six observable groups per call (see `E2_link`).
**Empty/degenerate and errors** Empty label list ⇒ `(0,0)` matrix.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_gausskernel.N_total

**Signature** `N_total(basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:474-475` (`_obs` `:455`)
**Inputs** `basis_labels`.
**Outputs** New sparse diagonal matrix `Σ_v n_v`, formed as `sum(nv[1:], nv[0])` (`:455`) — an accumulation of four CSR matrices; integer dtype.
**Invariants**
1. Diagonal with values in `{0,2,4,6,8}` for the physical basis (odd sectors are empty per `conventions.EXPECTED_SECTOR_DIMS`, `conventions.py:74`). The emptiness of odd sectors is a property of the basis, not of this function.
2. `[H, N] = 0`. — For route 2 this is **UNENFORCED**; the supplied commutator assertions are on route 1 with an inline-built `N` (`tests/test_route_spinnet.py::TestCommutator::test_H_commutes_with_N`, line 75, assert line 87), and `test_route_gausskernel.py:18` checks only the sector **counts**, not commutation.

**Side effects** Rebuilds all six observable groups per call.
**Empty/degenerate and errors** Empty label list ⇒ `(0,0)` matrix.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_gausskernel.P_surv

**Signature** `P_surv(basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:478-479` (`_obs` `:456-458`)
**Inputs** `basis_labels`.
**Outputs** New CSR diagonal indicator matrix; entry `1` iff `(q_1,q_2,q_3,q_4) == (1,−1,0,0)` with `q_v = n_v − N_VAC[v]` (`:456-458`); integer dtype.
**Invariants**
1. Projector: idempotent, Hermitian, 0/1 diagonal — by construction, **UNENFORCED**.
2. **Rank is 2 at `jmax=1/2`, not 1.** `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` lists `survival_occupation_codes` = code **2058** (links `[0.5,0,0,0]`, occupations `[1,1,0,2]`) and code **3793** (links `[0,0.5,0.5,0.5]`, occupations `[1,1,0,2]`): **two distinct physical codewords sharing one occupation pattern**, differing only in link spins. The survival projector combines both. Do not describe it as rank-1 or as selecting a single codeword. This is a **measured finite-oracle** result over the 82-code set, not a general theorem.
3. Charge selection depends only on occupations, so `P_surv` is blind to link content — that is exactly why (2) holds.

**Side effects** Rebuilds all six observable groups per call.
**Empty/degenerate and errors** Empty label list ⇒ `(0,0)` matrix (an all-zero projector on an empty space, no error).
**Enforcement** **UNENFORCED directly.** `tests/test_dynamics.py::test_channel_masks_partition_N4_sector` (line 44) asserts `int(surv.sum()) == 2` (line 50) — but for `su2qc.dynamics.scan._classify`, a different implementation; it is **indirect** corroboration of the count only.

### su2qc.ham.route_gausskernel.P_meson

**Signature** `P_meson(basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:482-483` (`_obs` `:459-460`)
**Inputs** `basis_labels`.
**Outputs** New CSR diagonal indicator; entry `1` iff `all_v |q_v| == 1` (`:459-460`); integer dtype.
**Invariants**
1. **R15 (structural, exact):** the predicate forces `n = (1,1,1,1)`, hence `N = 4` and `Σ_v q_v = 0`, for every selected state. Every meson-channel state lies in the `N=4` sector at any `jmax`. See Front matter A. — Structurally exact from `conventions.py:51,53,57`; **no supplied test asserts it**.
2. **Measured (82-code oracle only):** `oracle-diagnostics.json` reports `non_N4_meson_codes: []` and `singleton_closure_failures: []` over the 82 physical codes. Finite inspection; explicitly not a channel amendment or sign-off.
3. Disjoint from `P_BBbar` (`all |q|=1` excludes `any |q|=2`) and from `P_surv` (which needs `q_3 = q_4 = 0`). Not exhaustive — see Front matter B.

**Side effects** Rebuilds all six observable groups per call.
**Empty/degenerate and errors** Empty label list ⇒ `(0,0)` matrix.
**Enforcement** **UNENFORCED directly.** Indirect count corroboration only: `test_dynamics.py:50` asserts `int(mes.sum()) == 2` for `scan._classify`.

### su2qc.ham.route_gausskernel.P_BBbar

**Signature** `P_BBbar(basis_labels)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py:486-487` (`_obs` `:461-462`)
**Inputs** `basis_labels`.
**Outputs** New CSR diagonal indicator; entry `1` iff `any_v |q_v| == 2` (`:461-462`); integer dtype.
**Invariants**
1. Given `n_v ∈ {0,1,2}` and `N_VAC = (0,2,0,2)`, `|q_v| = 2` means `n_v = 2` at `v1`/`v3` or `n_v = 0` at `v2`/`v4`. — Structural; **UNENFORCED**.
2. **No precedence logic is implemented.** The three indicators are independent diagonal matrices computed in one pass (`:457-462`); the "takes precedence" wording appears only in route 1's docstring (`route_spinnet.py:668`). Any precedence must be imposed by the caller. — **UNENFORCED**.

**Side effects** Rebuilds all six observable groups per call.
**Empty/degenerate and errors** Empty label list ⇒ `(0,0)` matrix.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_spinnet.enumerate_basis

**Signature** `enumerate_basis(jmax: float) -> list[tuple]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:234-312` (gauge predicate `_check_vertex_gauge_invariant` `:173-231`)
**Inputs** `jmax` compared by **exact equality** to `0.5` then `1.0` (`:240,242`). `jmax = 1` (int) is accepted because `1 == 1.0`; anything else raises `ValueError` (`:245`).
**Outputs** A **new** `list` of labels `((j1,j2,j3,j4), (n1,n2,n3,n4), 0)` with `j` as Python floats and `n` as Python ints; tag always `0` (`:310`). Order is deterministic: `j1` outermost through `j4`, then `n1..n4`, each ascending (`:248-306`).
**Invariants**
1. Per-vertex gauge rule (`:9-12`, `:254-301`): `j_a == j_b ⇒ n_v ∈ {0,2}`; `|j_a − j_b| = 1/2 ⇒ n_v = 1`; `|j_a − j_b| = 1 ⇒ vertex forbidden` (only reachable at `jmax=1`). Vertex-to-link incidence is `v1:(l4,l1)`, `v2:(l1,l2)`, `v3:(l2,l3)`, `v4:(l3,l4)`.
2. `len(enumerate_basis(0.5)) == 82` and `len(enumerate_basis(1.0)) == 152` — **DIRECT**: `tests/test_route_spinnet.py::TestBasisDimensions::test_basis_dimension` (line 28), assert line 30, parametrised over both.
3. Sector dims at `jmax=0.5`: `{0:2, 2:20, 4:38, 6:20, 8:2}` — **DIRECT**: `TestBasisDimensions::test_sector_decomposition` (line 33), asserts lines 44-46.
4. Sector dims at `jmax=1.0`: `{0:3, 2:36, 4:74, 6:36, 8:3}` and agreement with route 2's label count — **DIRECT**: `runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py::test_jmax1_sector_counts_match_independent_transfer_polynomial` (line 30), asserts lines 37-39; line 33 additionally checks those counts against an independently coded transfer polynomial (lines 15-27). Note line 40 asserts route-2 `P` orthonormality, not route-1 content.
5. The `_check_vertex_gauge_invariant` call at `:308` is **redundant**: the per-vertex option lists at `:254-301` already encode the same rules, so the filter can never reject. — **UNENFORCED**.
6. `ValueError` for unsupported `jmax` (`:245`). — **UNENFORCED** (no supplied test asserts the raise).

**Side effects** None. **No caching**: every call re-enumerates. All six projector functions and both Hamiltonian builders in this module call it afresh, so a projector plus a Hamiltonian costs two full enumerations.
**Empty/degenerate and errors** `ValueError` as in (6). A `jmax` that is a numpy float equal to 0.5 passes the `==` test.
**Enforcement** Items 2-4 direct as cited; items 1, 5, 6 **UNENFORCED** as standalone statements (item 1 is exercised only through the dimension counts).

### su2qc.ham.route_spinnet.build_hamiltonian

**Signature** `build_hamiltonian(g2: float, m: float, jmax: float) -> tuple[csr_matrix, list]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:433-528` (terms: `_electric_diag` `:317-319`, `_mass_diag` `:322-324`, `_hopping_matrix_element` `:329-367`, `_magnetic_matrix_element` `:390-430`)
**Inputs** `g2`, `m` unvalidated; `jmax` forwarded to `enumerate_basis`.
**Outputs** **Two**-tuple `(H, basis)` — note the arity difference from route 2's three-tuple. `H` is `csr_matrix`, complex, shape `(D, D)`. `basis` is a fresh list (not cached, not aliased), in the same order as the matrix rows/columns.
**Invariants**
1. `H = H_elec + H_mass + H_hop + H_mag` with `H_elec = (g2/2)Σ_l j_l(j_l+1)` (`:319`, hardcoded rather than via `coupling_electric`), `H_mass = m Σ_v PARITY[v] n_v` (`:324`), `H_hop = (1/2) Σ_l (η_l ψ†_s U_l ψ_t + h.c.)` (`:366`), `H_mag = −(1/(2g2)) Tr(U_box + U_box†)` (`:515`, hardcoded rather than via `coupling_magnetic`).
2. **Hermiticity is enforced by construction**, not merely checked: each hopping element writes both `H[j,i] += me` and `H[i,j] += conj(me)` (`:483-484`), and each magnetic pair writes both orientations under the `j_idx > i` guard that visits every unordered pair once (`:513-520`). The comment at `:525-527` states this. — **DIRECT** check at four `(g2, m)` points, tolerance `1e-13`: `tests/test_route_spinnet.py::TestHermiticity::test_H_hermitian` (line 59, parameters lines 53-58), assert line 63. Because Hermiticity is imposed structurally, this assertion has little power to detect a wrong matrix element.
3. `[H, N] = 0` at three parameter points, tolerance `1e-13` — **DIRECT**: `TestCommutator::test_H_commutes_with_N` (line 75, parameters lines 70-74), assert line 87, using an **inline** number operator (lines 80-83) rather than `total_number()`.
4. Only the forward hopping direction (`n_s+1`, `n_t−1`) is computed; the conjugate is written into the transposed entry (`:340`, `:468-484`). Occupations are clamped to `0 ≤ n ≤ 2` (`:472`) and link spins to `[−1e-12, jmax+1e-12]` (`:476`).
5. Magnetic term flips **all four** links simultaneously by `±1/2` over the 16 enumerated sign patterns (`:494-497`) and is diagonal in `n` (`:510`); no same-state magnetic diagonal contribution is possible.
6. Pure-electric degeneracies `[16,16,18,16,16]` at `g2 = 1e6, m = 0` with `rel ≤ 1e-8` — **DIRECT**: `TestPureElectricDegeneracy::test_electric_degeneracies` (line 94), asserts lines 102 and 106. At `g2 = 1e6` the `O(1)` hopping and magnetic terms are ~1e-12 relative, so this test is **insensitive to the off-diagonal blocks**.
7. Shape `(152,152)` at `jmax = 1.0` — **DIRECT** but shape-only: `runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py:34,36`. No spectral property is asserted at `jmax=1`.
8. **No supplied test pins the numerical value of any hopping or magnetic matrix element.** Hermiticity (2) is structural, `[H,N]=0` (3) is insensitive to link-sector content, and (6) is insensitive to `O(1)` terms. The cross-route spectral comparison that would constrain them lives in `ham/compare.py`, which no supplied test imports. — **UNENFORCED**.

**Side effects** None external. Builds a dense-indexed `lil_matrix` and converts to CSR at `:523`; cost is dominated by the per-basis-state loops over links and 16 flip patterns.
**Empty/degenerate and errors** `g2 = 0.0` ⇒ `ZeroDivisionError` at `:515`. `jmax ∉ {0.5, 1.0}` ⇒ `ValueError` from `enumerate_basis` (`:245`). Complex `m` would be silently accepted by the complex `lil_matrix` and would break Hermiticity without any check.
**Enforcement** As annotated per invariant above.

### su2qc.ham.route_spinnet.build_hamiltonian_no_magnetic

**Signature** `build_hamiltonian_no_magnetic(g2: float, m: float, jmax: float) -> tuple[csr_matrix, list]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:531-577`
**Inputs** As `build_hamiltonian`.
**Outputs** `(H, basis)`, same ordering guarantee as `build_hamiltonian` (docstring `:534`), `H` complex CSR.
**Invariants**
1. Contains electric (`:547`), mass (`:551`), and hopping (`:554-574`) terms only; the hopping block is textually duplicated from `build_hamiltonian` rather than shared. — **UNENFORCED** that the two hopping blocks stay in sync.
2. Same basis ordering as `build_hamiltonian` — both call `enumerate_basis(jmax)`, which is deterministic. — **UNENFORCED** as an explicit comparison.
3. Shape is `(82,82)` at `jmax=0.5` — **DIRECT**: `tests/test_route_spinnet.py::TestNoMagnetic::test_no_magnetic_shape` (line 118), assert line 121, at three `(g2,m)` points, all with `jmax=0.5`. The `152` branch of the test's own expectation (line 120) is never exercised.
4. Hermitian to `1e-13` at `(1.0, 0.0, 0.5)` — **DIRECT**: `test_no_mag_hermitian` (line 126), assert line 130. Structural, as for `build_hamiltonian`.
5. `[H,N] = 0` to `1e-13` at `(1.0, 0.0, 0.5)` — **DIRECT**: `test_no_mag_commuting_N` (line 135), assert line 143, with an inline `N`.
6. `H_no_mag == H − H_mag` — **UNENFORCED**; no supplied test compares the two builders.
7. `g2 = 0.0` does **not** raise here (no magnetic division), unlike `build_hamiltonian`. — **UNENFORCED**.

**Side effects** None external. Lines `:540-541` allocate `j_labels`/`n_labels` object arrays that are never used — dead allocations proportional to `D`.
**Empty/degenerate and errors** `ValueError` from `enumerate_basis` for unsupported `jmax`.
**Enforcement** Items 3-5 direct as cited; 1, 2, 6, 7 **UNENFORCED**.

### su2qc.ham.route_spinnet.number_op

**Signature** `number_op(v: int)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:582-592`
**Inputs** `v` — captured by closure and **not validated at call time of `number_op`**; misuse surfaces only when the returned function runs.
**Outputs** A **function** `_no(dim_, basis_)`, not a matrix. `_no` returns a complex CSR diagonal matrix of shape `(dim_, dim_)` with entries `float(n_tuple[v])` (`:590-591`).
**Invariants**
1. Two-stage API: `number_op(v)(dim, basis)`. Callers must supply `dim` and `basis` **separately and consistently** — there is **no check that `dim_ == len(basis_)`**. `dim_ < len(basis_)` raises `IndexError` when assigning `H[i,i]`; `dim_ > len(basis_)` silently yields trailing all-zero rows and columns. — **UNENFORCED**.
2. Diagonal, aligned to the caller's `basis_` order; values `float(n_v) ∈ {0.0,1.0,2.0}` stored in a complex matrix (contrast the integer dtype of `route_gausskernel.n_op`).
3. `|v| ≥ 4` ⇒ `IndexError` inside `_no`; negative `v` wraps silently.

**Side effects** None. A fresh matrix per `_no` call; no caching.
**Empty/degenerate and errors** `dim_ = 0` with empty `basis_` gives a `(0,0)` matrix.
**Enforcement** **UNENFORCED.** No supplied test calls `number_op`; `test_route_spinnet.py:80-83` and `:139-140` construct the number operator inline with `numpy` instead.

### su2qc.ham.route_spinnet.total_number

**Signature** `total_number()`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:595-602`
**Inputs** None.
**Outputs** A **function** `_no(dim_, basis_)` returning a complex CSR diagonal matrix with entries `float(sum(n_tuple))` (`:600-601`).
**Invariants**
1. Same two-stage API and same unchecked `dim_`/`basis_` consistency hazard as `number_op` (1). — **UNENFORCED**.
2. Diagonal values in `{0.0, 2.0, 4.0, 6.0, 8.0}` for the physical basis — a property of the basis, not checked here.
3. `[H, N] = 0` for the `H` from this module — asserted only against an **inline-built** `N` (`test_route_spinnet.py:80-87`), never against this function's output. — **UNENFORCED for this function**.

**Side effects** None; fresh matrix per call.
**Empty/degenerate and errors** As `number_op`.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_spinnet.casimir_link

**Signature** `casimir_link(l: int)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:605-612`
**Inputs** `l` — unvalidated, captured by closure.
**Outputs** A **function** `_no(dim_, basis_)` returning a complex CSR diagonal matrix with entries `cv.casimir(j_tuple[l])` (`:610-611`).
**Invariants**
1. Same two-stage API and unchecked `dim_`/`basis_` hazard as `number_op`. — **UNENFORCED**.
2. Values `{0.0, 0.75, 2.0}` for `j ∈ {0, 1/2, 1}` via `conventions.casimir` (`conventions.py:69`).
3. This is the per-link electric energy **without** the `g²/2` coefficient; the coefficient is applied only inside the Hamiltonian builders (`:319`). Consumers computing `⟨E²⟩` must not double-count it. — **UNENFORCED**.
4. `|l| ≥ 4` ⇒ `IndexError` inside `_no`.

**Side effects** None; fresh matrix per call.
**Empty/degenerate and errors** As `number_op`.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_spinnet.P_stretched

**Signature** `P_stretched(g2: float, m: float, jmax: float) -> csr_matrix`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:634-638` (`_charge_projector` `:617-631`)
**Inputs** `g2` and `m` are accepted and **never used** — they appear nowhere in the body (`:636-638`). Only `jmax` has any effect. Callers must not infer any coupling dependence.
**Outputs** Complex CSR diagonal indicator of shape `(D, D)` with `D = len(enumerate_basis(jmax))`; entry `1.0` iff `q == (1, −1, 0, 0)` (`:628-630`).
**Invariants**
1. `q_v = int(n_v − N_VAC[v])` computed inline at `:628` (duplicating `conventions.charge`).
2. Idempotent 0/1 Hermitian projector by construction. — **UNENFORCED**.
3. **Rank 2 at `jmax=1/2`**, per the two survival codewords 2058 and 3793 recorded in `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` (`survival_occupation_codes`) — both with occupations `[1,1,0,2]`, differing in link spins. Not rank-1.
4. Identical in output to `P_short` and `P_surv` in this module — see those entries.

**Side effects** Re-runs `enumerate_basis(jmax)` on every call (`:636`); no caching.
**Empty/degenerate and errors** `ValueError` from `enumerate_basis` for unsupported `jmax`. No error path for the ignored `g2`/`m`.
**Enforcement** **UNENFORCED.** Indirect count-only corroboration: `tests/test_dynamics.py::test_channel_masks_partition_N4_sector` (line 44) asserts `int(surv.sum()) == 2` (line 50) for `su2qc.dynamics.scan._classify`, a different implementation.

### su2qc.ham.route_spinnet.P_short

**Signature** `P_short(g2: float, m: float, jmax: float) -> csr_matrix`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:641-645`
**Inputs** `g2`, `m` ignored; `jmax` as above.
**Outputs** Complex CSR diagonal indicator for `q == (1, −1, 0, 0)` — **the same charge tuple as `P_stretched`** (`:645`).
**Invariants**
1. **Semantic collision:** despite the docstring "the short sector" (`:642`), `P_short` is **bit-for-bit identical** to `P_stretched` and `P_surv` in this module. At the route-1 level there is no distinct "short" channel. Any analysis that treats route-1 `P_short` and `P_stretched` as independent channels is unsupported by the source. — **UNENFORCED** (nothing tests the intended distinction).
2. Contrast with the twin layer: `runs/campaign_v060/tests/gate_C0/test_estimator.py::test_v11_synthetic_channels_support_signed_weights_and_exact_closure` (line 7) asserts `P_stretched ≈ 0.7` (line 15), `P_short ≈ 0.2` (line 16) and `P_surv ≈ 0.9` (line 17) with `P_surv >= P_stretched + P_short` (line 22) for `su2qc.twin.twin.channel_weights`. That is a **different implementation with finer channels**, whose source is not in this bundle; the route-1 projectors here do not implement it and are not covered by that test.
3. Rank 2 at `jmax=1/2`, as for `P_stretched`.

**Side effects** Re-runs `enumerate_basis(jmax)` per call.
**Empty/degenerate and errors** As `P_stretched`.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_spinnet.P_surv

**Signature** `P_surv(g2: float, m: float, jmax: float) -> csr_matrix`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:648-652`
**Inputs** `g2`, `m` ignored; `jmax` as above.
**Outputs** Complex CSR diagonal indicator for `q == (1, −1, 0, 0)` (`:652`) — identical to `P_stretched` and `P_short`.
**Invariants**
1. Route 1's `P_surv(g2, m, jmax)` takes **three** arguments (two ignored) whereas route 2's `P_surv(basis_labels)` takes a label list and returns an **integer**-dtype matrix (`route_gausskernel.py:478-479`). The two are not drop-in substitutes: differing signature, differing dtype, and differing basis provenance. — **UNENFORCED**.
2. Same selection predicate as route 2's `P_surv`, so the two agree entrywise **provided** the two label lists are in the same order — an alignment that no supplied test verifies. — **UNENFORCED**.
3. Rank 2 at `jmax=1/2` (codes 2058 and 3793, `oracle-diagnostics.json`); **not rank-1**.

**Side effects** Re-runs `enumerate_basis(jmax)` per call.
**Empty/degenerate and errors** As `P_stretched`.
**Enforcement** **UNENFORCED**; indirect count-only corroboration at `test_dynamics.py:50`.

### su2qc.ham.route_spinnet.P_meson

**Signature** `P_meson(g2: float, m: float, jmax: float) -> csr_matrix`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:655-664`
**Inputs** `g2`, `m` ignored (never referenced in `:657-664`); `jmax` selects the basis.
**Outputs** Complex CSR diagonal indicator built inline (not via `_charge_projector`); entry `1.0` iff `all(abs(q) == 1 for q in q)` (`:662-663`).
**Invariants**
1. **R15 (structural, exact):** selection forces `n = (1,1,1,1)`, therefore `N = 4` and `Σ_v q_v = 0`, at any `jmax`. The prompt's non-`N=4` meson hazard and its `jmax=1` recurrence are false under `n ∈ {0,1,2}` with `N_VAC = (0,2,0,2)` and are superseded (Front matter A). — **UNENFORCED** by any test; the argument is structural.
2. **Measured (82 codes only):** `oracle-diagnostics.json` `non_N4_meson_codes: []`. Finite inspection of the `jmax=1/2` code set; no statement about `jmax=1`.
3. At `jmax=1/2` the additional route-1 vertex rule (`n_v = 1` requires `|j_a − j_b| = 1/2` at every vertex, `:257,269,281,293`) restricts the link spins to alternate around the four-link cycle. — **UNENFORCED** as an explicit assertion.
4. Disjoint from `P_BBbar` and from `P_surv`; the three do not close (Front matter B). — **UNENFORCED**.

**Side effects** Re-runs `enumerate_basis(jmax)` per call.
**Empty/degenerate and errors** `ValueError` for unsupported `jmax`.
**Enforcement** **UNENFORCED directly.** Indirect count-only: `test_dynamics.py:50` asserts `int(mes.sum()) == 2` for `scan._classify`; `test_dynamics.py:49` asserts that four masks from that other module partition the `N=4` sector (38 states, line 48).

### su2qc.ham.route_spinnet.P_BBbar

**Signature** `P_BBbar(g2: float, m: float, jmax: float) -> csr_matrix`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:667-676`
**Inputs** `g2`, `m` ignored; `jmax` selects the basis.
**Outputs** Complex CSR diagonal indicator; entry `1.0` iff `any(abs(q) == 2)` (`:674-675`).
**Invariants**
1. `|q_v| = 2` ⇔ `n_v = 2` at `v1`/`v3` or `n_v = 0` at `v2`/`v4`, given the occupation domain. — **UNENFORCED**.
2. The docstring's "(takes precedence)" (`:668`) corresponds to **no code**: there is no ordering, no exclusion, and no interaction with the other projectors. Precedence is a caller responsibility. — **UNENFORCED**.
3. The `N=0` and `N=8` states (2 each at `jmax=1/2`, `conventions.py:74`) satisfy this predicate at multiple vertices simultaneously; the indicator is 1 regardless of how many vertices qualify.

**Side effects** Re-runs `enumerate_basis(jmax)` per call.
**Empty/degenerate and errors** `ValueError` for unsupported `jmax`.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_spinnet.charge

**Signature** `charge(v: int, n: int) -> int`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:680-682`
**Inputs** `v`, `n` — neither validated. `N_VAC` here is the module-level alias imported from `conventions` (`route_spinnet.py:43`), so the value is the frozen `(0,2,0,2)`.
**Outputs** `n - N_VAC[v]`, behaviourally identical to `conventions.charge` (`conventions.py:55-57`).
**Invariants**
1. Duplicate definition of `conventions.charge`; if the frozen `N_VAC` ever changed, both would follow (shared constant), but the duplication itself means two public entry points expose the same contract. — **UNENFORCED**.
2. The projectors in this module do **not** call it — they inline `int(n_tuple[v] - N_VAC[v])` at `:628`, `:661`, `:673`. So this function is unused within its own module.

**Side effects** None.
**Empty/degenerate and errors** `|v| ≥ 4` ⇒ `IndexError`; negative `v` wraps; out-of-domain `n` accepted silently.
**Enforcement** **UNENFORCED.**

### su2qc.ham.route_spinnet.validate_dimensions

**Signature** `validate_dimensions(jmax: float = 0.5) -> dict`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:687-714`
**Inputs** `jmax`, forwarded to `enumerate_basis`, then used as a dict key twice (`:699-700`).
**Outputs** `dict` with keys `"jmax"`, `"dim"`, `"expected_dim"`, `"dim_match"` (bool), `"sector_dims"` (dict over `{0,2,4,6,8}`), `"expected_sectors"`. **Conditionally**, when `expected_sectors` is truthy (i.e. `jmax=0.5` only), five further keys `"sector_N0_match"` … `"sector_N8_match"` are added (`:710-712`).
**Invariants**
1. **Key set depends on `jmax`.** At `jmax=1.0`, `expected_sectors` is `None` (`:700`) and the `sector_N*_match` keys are **absent**; a caller indexing them gets `KeyError`. — **UNENFORCED**.
2. `sector_dims` is pre-seeded with only the even keys `{0,2,4,6,8}` and increments only if `N in sector_dims` (`:693-697`); any odd-`N` state would be **silently discarded** rather than reported. — **UNENFORCED**.
3. `"dim_match"` is `True` iff `dim == expected_dim` (`:706`), with `expected_dim ∈ {82, 152}` (`:699`) — consistent with `conventions.EXPECTED_DIM` (`conventions.py:72`) but hardcoded here rather than imported.
4. This function **returns** a report and raises nothing on failure; it is not an assertion. — **UNENFORCED**.
5. `dim_match` at both `jmax=0.5` and `jmax=1.0` — **DIRECT**: `tests/test_route_spinnet.py::TestCorePhysics::test_basis_dimensions_match` (line 150), asserts lines 153 and 155.
6. All five `sector_N*_match` flags at `jmax=0.5` — **DIRECT**: `TestCorePhysics::test_sector_dims` (line 157), asserts lines 160-164. The test asserts the **booleans**, not the underlying `sector_dims` values.

**Side effects** None; one full `enumerate_basis` per call.
**Empty/degenerate and errors** `jmax ∉ {0.5, 1.0}` ⇒ `ValueError` from `enumerate_basis` (`:245`) before the dict lookups at `:699-700` can raise `KeyError`.
**Enforcement** Items 5-6 direct; items 1-4 **UNENFORCED**.

### su2qc.ham.route_spinnet.validate_hermiticity

**Signature** `validate_hermiticity(H: csr_matrix, atol: float = 1e-13) -> dict`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:717-724`
**Inputs** `H` — any object supporting `.toarray()`; **no** check that it is square or sparse. `atol` — default `1e-13`.
**Outputs** `dict` with `"hermitian"` — the result of `diff <= atol`, which is a **`numpy.bool_`, not a Python `bool`** (`:722`) — and `"max_diff"`, a Python `float` (`:723`).
**Invariants**
1. `max_diff = max |H − H†|` over the **dense** array (`:719-720`), using conjugate transpose, so it is correct for complex `H`.
2. `H` is densified: memory `O(D²)`. For `D = 82` this is negligible; the contract still forbids passing a large sparse operator casually. — **UNENFORCED**.
3. Returns a report; raises nothing on failure. — **UNENFORCED**.
4. `"hermitian"` is truthy for `build_hamiltonian(1.0, 0.0, 0.5)` at the default `atol` — **DIRECT**: `tests/test_route_spinnet.py::TestCorePhysics::test_hermiticity_via_validator` (line 171), assert line 175. **One parameter point only**, and `atol` is never varied by a supplied test.

**Side effects** None.
**Empty/degenerate and errors** A `0×0` matrix makes `np.max` raise `ValueError: zero-size array to reduction operation`. A non-square `H` makes `H_arr - H_arr.T.conj()` raise a broadcast `ValueError`. Neither is guarded.
**Enforcement** Item 4 direct; items 1-3 **UNENFORCED**.

### su2qc.ham.route_spinnet.validate_commutator

**Signature** `validate_commutator(H: csr_matrix, N_op: csr_matrix, atol: float = 1e-13) -> dict`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:727-736`
**Inputs** `H`, `N_op` — both densified via `.toarray()` (`:729-730`); **no** shape or type compatibility check, and **no** check that `N_op` is a number operator (any matrix is accepted).
**Outputs** `dict` with key `"[H,N]"` (note the literal bracket key) holding a `numpy.bool_`, and `"max_comm"`, a Python `float` (`:734-735`).
**Invariants**
1. `max_comm = max |HN − NH|` on dense arrays (`:731-732`).
2. Returns a report; raises nothing on failure. — **UNENFORCED**.
3. The result is meaningful only if `N_op` shares `H`'s basis ordering — unchecked. — **UNENFORCED**.

**Side effects** None; two dense `O(D²)` arrays plus two `O(D³)` matrix products.
**Empty/degenerate and errors** Shape mismatch ⇒ `ValueError` from `@`. `0×0` inputs ⇒ `ValueError` from `np.max`.
**Enforcement** **UNENFORCED.** No supplied test calls it: `tests/test_route_spinnet.py::TestCommutator::test_H_commutes_with_N` (line 75) and `TestNoMagnetic::test_no_mag_commuting_N` (line 135) both compute the commutator inline (lines 84-87 and 141-143) rather than through this validator.

### su2qc.ham.route_spinnet.pure_electric_check

**Signature** `pure_electric_check(g2_big: float = 1e6) -> dict`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py:739-753`
**Inputs** `g2_big`. `m = 0.0` and `jmax = 0.5` are hardcoded (`:746`).
**Outputs** `dict` with `"degeneracies"` (`list[int]`, length 5), `"rel_dev"` (float), `"ok"` (Python `bool`) — the same shape as `limits.pure_electric_check`.
**Invariants**
1. `ok = (got == [16,16,18,16,16]) and (rel <= 1e-8 * g2_big/1e6 * 100)` (`:752`). The effective relative tolerance is **1e-6 at the default `g2_big`** and **scales linearly with `g2_big`** — larger coupling gives a *looser* acceptance. — **UNENFORCED** (no supplied test varies `g2_big`).
2. Degeneracies are tallied only for `k ∈ 0..4` (`:750`); eigenvalues rounding outside that range are excluded from `got` while still entering `rel`.
3. `ok` is truthy at the default — **DIRECT**: `tests/test_route_spinnet.py::TestCorePhysics::test_pure_electric_check` (line 166), assert line 169 (`assert pe["ok"]`). This asserts the composite flag only; it does not separately expose `degeneracies` or `rel_dev`.
4. Near-duplicate of `limits.pure_electric_check` (`limits.py:28-43`) with the same tolerance expression; the two are independent copies, and nothing enforces that they stay in sync. — **UNENFORCED**.
5. The `su2qc.conventions` import at `:744` is unused; the build is imported by absolute module path at `:745`, re-entering this same module.

**Side effects** None external. Full route-1 build at `g2 = 1e6` plus a dense `82×82` `eigh` (`:746-747`).
**Empty/degenerate and errors** `g2_big = 0.0` ⇒ `ZeroDivisionError` at `route_spinnet.py:515` (magnetic term), before `unit` is formed.
**Enforcement** Item 3 direct; items 1, 2, 4, 5 **UNENFORCED**.

### su2qc.replicate.sha256_file

**Signature** `sha256_file(path: str | Path) -> str`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py:13-14`
**Inputs** `path` — `str` or `Path`; no existence, type, or size check.
**Outputs** Lowercase hex SHA-256 digest string (64 characters) of the file's **bytes**.
**Invariants**
1. Content is read with `Path(path).read_bytes()` — the **entire file is loaded into memory**; there is no streaming or chunking. Large inputs are a memory hazard. — **UNENFORCED**.
2. Hashing is over raw bytes, so line endings and trailing whitespace are significant; no text normalisation and no encoding assumption.
3. Symlinks are **followed** (`read_bytes` opens the target); the digest describes the target's content, not the link. — **UNENFORCED**.

**Side effects** Reads the filesystem. No writes.
**Empty/degenerate and errors** An empty file returns the well-defined SHA-256 of the empty byte string, not an error. `FileNotFoundError`, `IsADirectoryError`, and `PermissionError` propagate unchanged and uncaught.
**Enforcement** **UNENFORCED.** No supplied test imports `su2qc.replicate`.

### su2qc.replicate.manifest

**Signature** `manifest(paths: list[str | Path]) -> dict[str, str]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py:17-18`
**Inputs** `paths` — any iterable of `str`/`Path` (the annotation says `list`; the body only iterates).
**Outputs** `dict` mapping `str(Path(path))` to the SHA-256 hex digest.
**Invariants**
1. Insertion order follows `sorted(paths, key=str)` (`:18`). Since Python 3.7 dicts preserve insertion order, the mapping is deterministically ordered — but sorting is on the **original string form**, while keys are the **`Path`-normalised** form, so the key order is not guaranteed to be sorted by key.
2. Keys are normalised by `Path` construction: `"./a"` → `"a"`, `"a//b"` → `"a/b"`, a trailing slash is stripped. **Distinct input strings can therefore collide onto one key**, silently keeping the last computed value. — **UNENFORCED**.
3. No `.resolve()` is applied: relative paths stay relative, so the manifest is **CWD-dependent** and not portable between working directories. — **UNENFORCED**.
4. Duplicated paths are hashed once per occurrence (no dedup before hashing), costing repeated I/O.

**Side effects** Reads every listed file. No writes.
**Empty/degenerate and errors** `paths = []` returns `{}` — a vacuous manifest, with no error and no warning. Any unreadable path aborts the whole call with the underlying `OSError` subclass; there is no partial result and no per-path error capture.
**Enforcement** **UNENFORCED.**

### su2qc.replicate.compare_manifests

**Signature** `compare_manifests(expected: dict[str, str], actual: dict[str, str]) -> dict[str, object]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py:21-24`
**Inputs** Two mappings. No check that they are non-empty or that their key spaces overlap.
**Outputs** `dict` with `"pass"` (Python `bool`, `not mismatches`), `"mismatches"` (sorted `list[str]` of keys), `"count"` (`int`).
**Invariants**
1. Comparison is over the **union** of keys (`:22`) using `.get()`, so a key present in only one mapping compares `hash` vs `None` and is reported as a mismatch — missing and extra files are both caught, but the report does not distinguish *missing*, *extra*, and *changed*. — **UNENFORCED**.
2. `"count"` is the size of the **union**, not the number of files compared on both sides nor the number of matches. Reporting it as "files verified" would overstate it. — **UNENFORCED**.
3. `"mismatches"` is in sorted key order (inherited from `sorted(...)` at `:22`).
4. **Vacuous pass:** two empty dicts yield `{"pass": True, "mismatches": [], "count": 0}`. A caller that forgets to populate `expected` gets a green result. — **UNENFORCED**.
5. Digest comparison is exact string equality — case-sensitive, so a manifest produced with uppercase hex would mismatch. `sha256_file` always emits lowercase.

**Side effects** None; no filesystem access.
**Empty/degenerate and errors** No error paths; non-hashable or non-mapping arguments raise from `set()`/`.get()`.
**Enforcement** **UNENFORCED.**

### su2qc.replicate.write_manifest

**Signature** `write_manifest(paths: list[str | Path], output: str | Path) -> dict[str, str]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py:27-30`
**Inputs** `paths` as for `manifest`; `output` — destination file path, unvalidated.
**Outputs** Returns the manifest `dict` (the same object it wrote), so the caller need not re-read the file.
**File writes — exact behaviour** `Path(output).write_text(json.dumps(values, indent=2, sort_keys=True) + "\n")` (`:29`). Concretely:
1. JSON object, keys **sorted** (`sort_keys=True`) — note this differs from `manifest`'s insertion order, so the on-disk order is sorted by normalised key while the returned dict's order is not.
2. Two-space indentation, and exactly **one trailing newline** appended after the JSON text.
3. **Overwrites unconditionally.** No existence check, no backup, no confirmation, no `exist_ok` guard.
4. **Not atomic.** No temp-file-plus-rename; an interrupted write leaves a truncated file.
5. Encoding is `Path.write_text`'s default, i.e. `locale.getpreferredencoding(False)` — **not pinned to UTF-8**. Non-ASCII path components can therefore produce different bytes on different systems; `json.dumps` defaults to `ensure_ascii=True`, which escapes non-ASCII in the JSON body and limits but does not eliminate this exposure.
6. Parent directories are **not** created: a missing parent raises `FileNotFoundError`.

**Invariants**
1. The returned dict equals the file's decoded content. — **UNENFORCED**.
2. All items 1-6 above. — **UNENFORCED**.

**Side effects** Reads every input file; writes exactly one output file. No stdout, no logging, no network.
**Empty/degenerate and errors** `paths = []` writes the literal `{}` plus a newline and returns `{}` — a valid, empty, passing manifest. `PermissionError`/`IsADirectoryError` on `output` propagate; any read error aborts before the write, leaving the previous file intact.
**Enforcement** **UNENFORCED.** No supplied test imports `su2qc.replicate`, so none of the write semantics above is covered.

---

## Appendix — CLI / `__main__` blocks among the listed functions

Recorded for accuracy; none of these is a listed entry, and **none writes a file**.

* `ham/compare.py:109-114` — calls `spectra_comparison()` with all defaults, prints each row dict on its own line, then calls `time_series_comparison()` and prints `"time_series_max_abs_dev"` followed by `dev`. No arguments are parsed, no thresholds applied, no exit code set on deviation, no file written.
* `ham/limits.py:125-128` — prints the return dicts of `pure_electric_check()`, `frozen_matter_check()`, and `magnetic_off_check()`, all with defaults. No argument parsing, no non-zero exit on `ok == False`, no file written.
* `ham/route_spinnet.py:756-775` — prints `validate_dimensions(0.5)` results including per-sector OK/FAIL lines (`:761-762`), then `validate_dimensions(1.0)` dimension only (note the per-sector keys are absent at `jmax=1.0`, so only `dim_match` is printed, `:766`), then `validate_hermiticity` on `build_hamiltonian(1.0, 0.0, 0.5)` (`:769-771`), then `pure_electric_check()` (`:774-775`). The "FAIL" strings are printed, not raised; the block always exits 0. No file written.
* `ham/route_gausskernel.py`, `conventions.py`, `replicate.py` — no `__main__` block.

The only listed function that writes to disk is `su2qc.replicate.write_manifest` (`replicate.py:29`), documented above. Separately, and outside the listed functions, `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:27-29` writes `runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json` from within a test, using a CWD-relative path.

## Appendix — evidence index

* `runs/campaign_v060/sessions/c060_p0_20260908_3/seed-diagnosis.json` — EMULATED; status partial (exit 124 at the 2400-second cap during r1; no completed r1 counts). Cited for: `shift_equal: true`, `shift_matches: 1023` of 1024 shots on both production and compact paths, `same_index_matches` 424 / 414.
* `runs/campaign_v060/sessions/c060_p0_20260908_3/equal-seed-control.json` — EMULATED; `simulator_seed_option_before: 101` → `after: 500`, five runtime seeds of 500, `distinct: 1`. Scope: independent pre-fix r0 control, **not** the post-fix R8 r0/r1 controls.
* `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` — finite 82-code inspection; cited for `non_N4_meson_codes: []`, `vacuum_occupations: [0,2,0,2]`, `survival_occupation_codes` (2058, 3793), `invalid_input` (residual 0.0 on an undecodable code), `empty_physical_yield` (`ZeroDivisionError`), `empty_postselect` (`[{}, 0.0]`). Self-described as `"Finite code inspection only; no channel-definition amendment or gate sign-off."`

### su2qc.circuits.strang_l12.params

**Signature** `params(g2=None, m=None)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:46-56`
**Inputs** Optional `g2`, `m`; any type is accepted and stored unvalidated (lines 52-55).
**Outputs** A newly built `dict` with exactly the keys `g2, m, dt, r_max`; defaults `4.0, 0.75, 0.8333333333333334, 3` (line 47). The dict is fresh on every call and safe to mutate.
**Invariants** Key set is always exactly those four (lines 47, 51) — UNENFORCED. Explicit arguments always win over the file (lines 52-55) — UNENFORCED. Only keys present in `window.json` overwrite defaults (line 51) — UNENFORCED.
**Side effects** Reads `RUN/physics/window.json` on **every** call (lines 48-51), where `RUN = Path(__file__).resolve().parents[3]` (line 42), i.e. the run directory `runs/section8_v0.5.0_20260907T0628Z`. No caching, so returned values depend on current filesystem state. No writes.
**Empty/degenerate and errors** Missing file → silent defaults (line 49). Malformed JSON → `json.JSONDecodeError` propagates (line 50). No type or range validation of `dt`, `r_max`, `g2`, `m` from the file.
**Enforcement** No test calls `params` for its own contract. It is executed at import of `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:13` and inside `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py:48-49`, which consume the values but assert nothing about them: indirect, non-enforcing.

### su2qc.circuits.strang_l12.terms

**Signature** `terms(g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:59-65` (decorated `@lru_cache(maxsize=8)`, line 59)
**Inputs** `g2`, `m` — cast with `float()` only *inside* the body (line 63), while the cache key uses the raw arguments, so `terms(4, 0.75)` and `terms(4.0, 0.75)` occupy distinct cache entries computing identical results.
**Outputs** `(basis, dict)` where the dict has seven keys: `D, h0, h1, h2, h3, B, H` (lines 64-65). Note the docstring says "{group: 82x82 ndarray}"; the returned mapping additionally contains `H`, the **full** dense Hamiltonian, which is not a Strang group. At the module default `jmax=0.5` used by `_term_split` (`scan.py:208`), all matrices are 82×82 dense complex/real ndarrays and `basis` has 82 labels.
**Invariants** `D + Σ h_l + B == H` to 1e-13 — enforced *inside the producer* by the assert at `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:232`, and directly by `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py::test_term_split_is_exact:36`. Each `h_l` Hermitian with zero diagonal — enforced at `tests/test_dynamics.py:39-40`.
**Side effects** Imports `su2qc.dynamics.scan` lazily at call time (line 62), which itself imports matplotlib only later. Populates the LRU cache. **Returns the cached objects, not copies**: mutating any returned array or the returned dict corrupts every later caller.
**Empty/degenerate and errors** Non-numeric `g2`/`m` → `TypeError`/`ValueError` from `float()` (line 63). Unhashable arguments → `TypeError` from the cache. Cache eviction beyond 8 entries silently recomputes.
**Enforcement** Split exactness: direct (`tests/test_dynamics.py:36`). Cached-object aliasing: UNENFORCED. Presence of the `H` key: used at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:110`, no assertion on the key set — UNENFORCED.

### su2qc.circuits.strang_l12.code_index

**Signature** `code_index()`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:68-71` (`@lru_cache(maxsize=1)`)
**Inputs** None.
**Outputs** `(codes, index)` where `codes = physical_codes()` is the ascending list of the 82 physical integers and `index` maps each code to its **position in that sorted list** (line 71), which is *not* in general the dynamics-basis row order used by `basis_to_code`.
**Invariants** `len(codes) == 82`, all distinct — enforced indirectly on the underlying `physical_codes()` at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:19-20`. `index[codes[i]] == i` — UNENFORCED.
**Side effects** Caches. **The same list and dict objects are returned on every call**; mutation is globally visible and persists.
**Empty/degenerate and errors** None reachable; failure would only come from `physical_codes()`.
**Enforcement** Consumed by `leakage_prob` (line 236), itself checked at `tests/test_l12.py:89`: indirect only. Cache-aliasing behaviour UNENFORCED.

### su2qc.circuits.strang_l12.basis_to_code

**Signature** `basis_to_code(basis)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:74-75`
**Inputs** An iterable of canonical route-spinnet labels.
**Outputs** `np.ndarray` of the encoded integers, in **input order** (line 75); dtype `int64` for a non-empty input. New array per call.
**Invariants** Order-preserving one-to-one image of the input labels — UNENFORCED directly; relied on by `to_basis` (line 231) and the test harness `tests/test_l12.py:35-51`.
**Side effects** None beyond warming `l12._maps()`. Cost is O(82) label comparisons per element (`encodings/l12.py:35-37`), i.e. quadratic over a full basis; recomputed on every call, no caching.
**Empty/degenerate and errors** Any non-physical label → `ValueError` from `encode` (`encodings/l12.py:38`). **Empty basis → `np.array([])` of dtype `float64`**, which will raise `IndexError` if used as a fancy index downstream; unvalidated.
**Enforcement** Used inside `tests/test_l12.py:36` and `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py:41,47`; no test asserts its return shape or dtype — UNENFORCED.

### su2qc.circuits.strang_l12.local_matrix

**Signature** `local_matrix(M, codes_of_basis, S)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:126-135`
**Inputs** `M` a square matrix in basis order; `codes_of_basis` the parallel integer codes; `S` a qubit-index sequence assumed sorted (docstring line 127) but **not checked**. Bit `k` of the local pattern is qubit `S[k]` (lines 131-132), so the returned operator's qubit order is the order of `S` as given, matching the `qc.append(..., S)` convention at line 161.
**Outputs** New `2^|S| × 2^|S|` complex ndarray, zero-filled outside the assigned entries (lines 128-133).
**Invariants** Hermiticity to 1e-13 — enforced by the in-body `assert` at line 134 (skipped under `python -O`; this is a runtime assert, not a test). Well-definedness of the pattern map is **not** checked: entries are **assigned, not accumulated** (line 133), so if two `(i,j)` pairs collapse to the same `(x,y)` with different values the last write silently wins. Consistency is only guaranteed upstream by `_support` (lines 80-123), whose greedy search the docstring itself calls "minimal-ish".
**Side effects** None.
**Empty/degenerate and errors** `S = []` → 1×1 matrix. Entries with `|M| ≤ 1e-14` are dropped (line 130): the 1e-14 cut is a hard-coded, unvalidated sparsity threshold. Non-Hermitian input → `AssertionError` (line 134).
**Enforcement** Indirect only, through the exactness of the block unitaries: `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py::test_block_unitary_exact_and_leak_free:63-64` and `tests/test_synth_l12.py:40-41`. The silent-overwrite behaviour is UNENFORCED.

### su2qc.circuits.strang_l12.supports

**Signature** `supports(g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:138-142` (`@lru_cache(maxsize=8)`)
**Inputs** `g2`, `m`, forwarded unchanged to `terms` (line 140).
**Outputs** `dict` with exactly the five keys `h0, h1, h2, h3, B` (line 142), each a sorted list of qubit indices. **There is no `D` key** — the diagonal group is handled separately (line 153-157); requesting `supports(...)["D"]` raises `KeyError`.
**Invariants** Each support is sorted ascending (`_support` returns `sorted(S)`, line 123) — UNENFORCED. `|S| ≤ 10` is asserted only as prose in the module docstring (line 16) — UNENFORCED. Sufficiency of the support (that `U_S ⊗ I` reproduces the lifted operator) is established by the greedy loop at lines 114-122, not by a test on this function.
**Side effects** Caches; **the same dict object is returned every call**. Expensive: `_support` runs `n_conflicts` over all 82² index pairs per candidate qubit (lines 101-112, 116-121).
**Empty/degenerate and errors** Same cache-key aliasing caveat as `terms`.
**Enforcement** Indirect, via block-unitary exactness at `tests/test_l12.py:63-64` and `tests/test_synth_l12.py:40`. Minimality of the support is **not** claimed by the source and is UNENFORCED.

### su2qc.circuits.strang_l12.unitary

**Signature** `unitary(group, theta, g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:147-162` (`@lru_cache(maxsize=64)`)
**Inputs** `group` a string; `theta` a real angle; `g2`, `m` forwarded to `terms`/`supports`. Cache key is the raw 4-tuple.
**Outputs** A 12-qubit `QuantumCircuit` named `U_{group}` implementing `exp(-i θ E T_group E†)`. For `group == "D"`: a single `Diagonal` gate on all 12 qubits whose vector is 1 on every unphysical code and `exp(-i θ Re diag(D))` on the 82 physical codes (lines 154-156) — the identity on the complement by construction, hence leakage-free by construction rather than by check. Otherwise: one `UnitaryGate` of dimension `2^|S|` appended to the support qubits in sorted order (lines 158-161).
**Invariants** Restricted to the 82 codes the circuit equals `expm(-i θ T[group])` to 1e-12, with leakage norm ≤ 1e-12 — **directly** enforced for all six groups at θ ∈ {0.13, 0.61} and the window `(g2, m)` by `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py::test_block_unitary_exact_and_leak_free:58-64`. Exactness at other θ, `g2`, `m` is UNENFORCED.
**Side effects** Caches; **returns the shared cached circuit object**. Callers that mutate it (e.g. appending gates) corrupt every subsequent consumer; `strang_step` and `full_circuit` only pass it as the *argument* of `compose(..., inplace=True)`, which mutates the receiver, not the cached object.
**Empty/degenerate and errors** An unknown `group` raises `KeyError` from `T[group]`/`supports(...)[group]` (lines 158-159) — **not** `ValueError`; this differs from `synth_unitary`, which raises `ValueError` (`synth_l12.py:252-253`). `theta` is not restricted; float/int mixing produces duplicate cache entries.
**Enforcement** Direct, as above (`tests/test_l12.py:63-64`), limited to the two θ values, the six groups, and the single `(g2, m)` window read at `tests/test_l12.py:13-14`.

### su2qc.circuits.strang_l12.strang_step

**Signature** `strang_step(dt, g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:165-172`
**Inputs** `dt`, `g2`, `m`. Each angle is cast with `float()` at composition time (line 171).
**Outputs** A fresh 12-qubit circuit composed of exactly eleven blocks in the fixed order `D(dt/2), h0(dt/2), h2(dt/2), h1(dt/2), h3(dt/2), B(dt), h3(dt/2), h1(dt/2), h2(dt/2), h0(dt/2), D(dt/2)` (lines 167-169). `B` receives the **full** `dt`; every other block receives `dt/2`.
**Invariants** Equals `exact_strang_matrix(dt, g2, m)` on the 82 codes to 1e-10, leakage ≤ 1e-12 — **directly** enforced at the window `dt` by `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py::test_full_strang_step_matches_exact_product:68-74`. Ordering equivalence with `dynamics.scan.strang_step_matrix` is UNENFORCED (no test compares the two implementations).
**Side effects** None beyond warming the `unitary` cache.
**Empty/degenerate and errors** `dt = 0` yields an identity-equivalent circuit of eleven trivial blocks (still emitted). No validation of `dt` sign or magnitude.
**Enforcement** Direct at one `(dt, g2, m)` point only (`tests/test_l12.py:72-74`).

### su2qc.circuits.strang_l12.prep_stretched

**Signature** `prep_stretched(qc=None)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:175-181`
**Inputs** Optional circuit to extend.
**Outputs** The circuit with `X` applied to every qubit whose bit is set in `encode(STRETCHED)` (lines 177-180), where `STRETCHED = ((0.0,0.5,0.5,0.5),(1,1,0,2),0)` (line 43) and the code is 3793 (asserted at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:28`), i.e. seven `X` gates on qubits 0, 4, 6, 7, 9, 10, 11 under the q0-least-significant convention (`encodings/l12.py:1-6`).
**Invariants** From `|0…0>` the prepared state is exactly the computational basis state 3793 — enforced indirectly: `tests/test_l12.py:27-29` fixes the code value, and `tests/test_l12.py:83-96` checks that the full circuit built on this preparation has zero leakage.
**Side effects** **A non-empty passed circuit is mutated in place and returned.** Because line 176 uses `qc or QuantumCircuit(NQ)` and `QuantumCircuit` defines `__len__`, an **empty** passed circuit is falsy and is silently discarded in favour of a new 12-qubit circuit — the caller's object is then *not* modified. UNENFORCED.
**Empty/degenerate and errors** A passed circuit with fewer than 12 qubits raises from `qc.x(q)`; no width check.
**Enforcement** Indirect only (`tests/test_l12.py:27-29`, `:83-96`). The falsy-empty-circuit substitution is UNENFORCED.

### su2qc.circuits.strang_l12.full_circuit

**Signature** `full_circuit(r, dt=None, g2=None, m=None, merge_D=True)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:184-204`
**Inputs** `r` an integer step count; `dt` overrides `params()["dt"]` when not `None` (line 186); `g2`, `m` are forwarded to `params` (line 185) and thence to `unitary`; `merge_D` selects the merged-diagonal layout.
**Outputs** A fresh 12-qubit circuit. `r == 0` returns the preparation **only** (lines 187-189) — no evolution blocks; the routed `r=0` resource footprint recorded in `runs/campaign_v060/sessions/c060_p0_20260908_3/seed-diagnosis.json` is `{"n_2q": 0, "depth_2q": 0, "depth": 1}`. `merge_D=False`: `r` verbatim `strang_step` copies (lines 190-193). `merge_D=True`: `D(dt/2)`, then for each of `r` rounds the nine-block core followed by `D(dt)`, except `D(dt/2)` on the last round (lines 194-203).
**Invariants** Merged and unmerged constructions give the same statevector to 1e-12 at `r = 2` — **directly** enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:76-79`. Zero leakage of the noiseless statevector at `r = r_max` — enforced at `tests/test_l12.py:87-89` (`leakage_prob ≤ 1e-14`) and, for sampled 10 000-shot noiseless counts, `flagged == 0` at `tests/test_l12.py:92-96`. Second-order Trotter scaling is asserted for the **matrix** reference `exact_strang_matrix`, not for this circuit (`tests/test_l12.py:100-132`).
**Side effects** Calls `params`, hence reads `physics/window.json` (line 185).
**Empty/degenerate and errors** `r < 0` with `merge_D=True` returns preparation + a single `D(dt/2)` block, because `range(r)` is empty (line 199) — not the preparation-only circuit; unvalidated. Non-integer `r` → `TypeError` from `range`. `dt` unvalidated.
**Enforcement** Merge equivalence: direct at `r=2` (`tests/test_l12.py:79`). Leakage: direct at `r=r_max` (`tests/test_l12.py:89,96`). Behaviour at negative `r`: UNENFORCED.

### su2qc.circuits.strang_l12.exact_strang_matrix

**Signature** `exact_strang_matrix(dt, g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:209-222`
**Inputs** `dt`, `g2`, `m`.
**Outputs** New 82×82 complex ndarray for one Strang step, accumulated by **left**-multiplication: starting from `expm(-i D dt/2)` (line 215), then `h0, h2, h1, h3` each at `dt/2` (lines 214, 216-217), then `B` at `dt` (line 218), then the same four in reverse (lines 219-220), then `D dt/2` (line 221). Operator order therefore reads right-to-left as `D/2 · h0/2 · h2/2 · h1/2 · h3/2 · B · h3/2 · h1/2 · h2/2 · h0/2 · D/2`, matching the docstring (lines 210-212) and `strang_step`'s gate sequence.
**Invariants** Agreement with the circuit construction to 1e-10 — enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:73` and `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py:49`. Second-order accuracy: log-log slopes in [−2.3, −1.7] for `P_surv`, `E2`, and state norm over `r ∈ {8,16,32,64,128}` — enforced at `tests/test_l12.py:131-132`, which also **writes** `circuits/trotter_scaling.json` (`tests/test_l12.py:125-130`); the stored file is byte-compared against `HEAD` at `runs/campaign_v060/tests/gate_C0/test_v1_regression.py:17-18` and its slopes re-checked at `:26`.
**Side effects** None (11 dense `expm` calls per invocation).
**Empty/degenerate and errors** No validation of `dt`; `dt = 0` returns the identity.
**Enforcement** Direct as cited.

### su2qc.circuits.strang_l12.circuit_state

**Signature** `circuit_state(qc)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:225-227`
**Inputs** Any unitary `QuantumCircuit`.
**Outputs** `Statevector(qc).data`, a new complex array of length `2^qc.num_qubits`. The docstring says 4096, but the width is **not** checked; a non-12-qubit circuit returns a different length.
**Invariants** Little-endian Qiskit amplitude ordering, so index `c` is the computational basis state whose bit `q` is `(c >> q) & 1`, consistent with `encodings/l12.py:1-6` — UNENFORCED here, relied on by `to_basis` and `leakage_prob`.
**Side effects** None.
**Empty/degenerate and errors** Circuits containing measurements, resets, or classical control raise from `Statevector` construction; unguarded.
**Enforcement** UNENFORCED. The tests build statevectors directly (`tests/test_l12.py:49`, `tests/test_synth_l12.py:28`) rather than through this helper.

### su2qc.circuits.strang_l12.to_basis

**Signature** `to_basis(vec4096, basis)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:230-232`
**Inputs** A 4096-length amplitude vector and a label list.
**Outputs** New array `vec4096[cb]` in **basis order** (line 232), i.e. the amplitudes on the physical codes ordered by the supplied basis, not by code value.
**Invariants** Output length equals `len(basis)` — UNENFORCED.
**Side effects** Recomputes `basis_to_code` on every call (line 231); no caching, so O(82·|basis|) label comparisons per call.
**Empty/degenerate and errors** Short input vector → `IndexError`; no length check. Empty `basis` → float-dtype empty index array → `IndexError`.
**Enforcement** UNENFORCED; no test calls it.

### su2qc.circuits.strang_l12.leakage_prob

**Signature** `leakage_prob(vec4096)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:235-239`
**Inputs** A 4096-length amplitude vector.
**Outputs** `float` — the summed `|amplitude|²` over the 4096 − 82 = 4014 unphysical codes (lines 236-239). Non-negative. It is a probability only if the input is normalized; the function does **not** normalize or check the norm, so an unnormalized input yields an unnormalized number.
**Invariants** Complement mask is exactly the physical-code set from `code_index()` (lines 236-238) — UNENFORCED for the mask itself; the 82-code set is enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:19-25`.
**Side effects** None; builds a fresh 4096-length boolean mask per call.
**Empty/degenerate and errors** Input length ≠ 4096 → `IndexError` from the boolean-mask application; unvalidated (the mask is hard-sized by `N = 4096`, line 39).
**Enforcement** Direct at one point: `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:89` asserts `≤ 1e-14` for `full_circuit(RMAX)`.

### su2qc.circuits.strang_l12.resources

**Signature** `resources(circ)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py:244-250`
**Inputs** Any circuit.
**Outputs** `{"n_2q": int, "depth_2q": int, "depth": int}` after `transpile` to basis `["cz","rz","sx","x","id"]` at `optimization_level=1`, `seed_transpiler=7`, with **no coupling map** (lines 245-246) — i.e. all-to-all, unrouted counts.
**Invariants** `n_2q` counts every instruction with `num_qubits == 2` and **does not exclude barriers** (line 247). This differs from `compile/route.py:51-52` and `compile/run_g4.py:30`, which both exclude `barrier`. `depth_2q` likewise does not exclude barriers (line 249). All three values are Python `int`. UNENFORCED.
**Side effects** None (no file writes). Results depend on the installed Qiskit transpiler version despite the fixed seed.
**Empty/degenerate and errors** Empty circuit → all zeros except `depth` 0. No validation.
**Enforcement** UNENFORCED — no test asserts any value returned by this function.

### su2qc.circuits.synth_l12.synth_unitary

**Signature** `synth_unitary(group, theta, g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py:249-259` (`@lru_cache(maxsize=64)`, line 248)
**Inputs** `group` must be in `GROUPS = sl.GROUPS` (line 22, i.e. `D, h0, h1, h2, h3, B`); `theta`, `g2`, `m` are cast to `float` **inside** the body (line 251), after the cache key has been formed from the raw arguments, so int/float callers create duplicate entries.
**Outputs** A 12-qubit `QuantumCircuit` named `synth_{group}` built only from one-qubit and controlled gates: for `D`, a degree-three phase polynomial emitted as `global_phase`, `rz`, and CX ladders (`_diagonal`, lines 226-245); otherwise Gray-path two-level blocks with minimal control sets and exact 3×3 Givens factors (`_synth_local`, lines 187-210).
**Invariants** On the 82 codes the circuit equals `expm(-i θ T[group])` to **1e-10** with leakage ≤ 1e-12 — **directly** enforced for all six groups at θ ∈ {0.13, 0.61} and `(g2, m) = (4.0, 0.75)` by `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py::test_synth_block:36-41`. Note the tolerance is 1e-10 here versus 1e-12 for `strang_l12.unitary` (`tests/test_l12.py:63`).
**Side effects** Caches and **returns the shared cached circuit object**.
**Empty/degenerate and errors** `group not in GROUPS` → `ValueError(group)` (lines 252-253) — contrast `strang_l12.unitary`, which raises `KeyError`. A local component of size other than 1, 2, or 3 → `ValueError` from `_synth_local:198`; a failed Givens elimination → `ArithmeticError` from `_givens_decomposition:141`. Both are reachable only through this entry point and are UNENFORCED (no test exercises them).
**Enforcement** Direct as cited, at two θ values and one `(g2, m)`.

### su2qc.circuits.synth_l12.synth_strang_step

**Signature** `synth_strang_step(dt, g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py:262-268`
**Inputs** `dt`, `g2`, `m`.
**Outputs** A fresh 12-qubit circuit with the same eleven-block sequence and the same `B(dt)` / others-`dt/2` split as `strang_l12.strang_step` (lines 264-265).
**Invariants** Matches `sl.exact_strang_matrix(dt, g2, m)` on the 82 codes to 1e-10 with leakage ≤ 1e-12 — **directly** enforced at the window `dt` and `(4.0, 0.75)` by `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py::test_synth_strang:45-50`. Gate-level equivalence to `strang_l12.strang_step` is not asserted anywhere — UNENFORCED.
**Side effects** None beyond the `synth_unitary` cache.
**Empty/degenerate and errors** No validation of `dt`.
**Enforcement** Direct at one `(dt, g2, m)` point.

### su2qc.circuits.synth_l12.synth_full_circuit

**Signature** `synth_full_circuit(r, dt=None, g2=None, m=None, merge_D=True)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py:271-287`
**Inputs** As `strang_l12.full_circuit`; `sl.params(g2, m)` supplies defaults (line 272), so this reads `physics/window.json`.
**Outputs** `sl.prep_stretched()` for `r == 0` (lines 273-275); otherwise `r` verbatim steps (`merge_D=False`, lines 276-279) or the merged-`D` layout `D(dt/2)` + `r ×` (core + `D(dt)`, last `D(dt/2)`) (lines 280-287).
**Invariants** No test asserts equality of merged and unmerged forms for this synthesized variant, and none compares it with `strang_l12.full_circuit` — **UNENFORCED**. The corresponding merge-equivalence check exists only for the `strang_l12` construction (`tests/test_l12.py:76-79`).
**Side effects** Reads `physics/window.json` via `sl.params` (line 272). Used at `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py:41` to build every logical circuit that is later routed and run on the twin.
**Empty/degenerate and errors** `r < 0` with `merge_D=True` yields preparation + one `D(dt/2)` block (line 283), as in `full_circuit`; unvalidated.
**Enforcement** Only indirectly exercised, through `write_resources` at `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py:55`, which asserts nothing about the circuits themselves beyond `n_2q >= 0` (`:67`).

### su2qc.circuits.synth_l12.write_resources

**Signature** `write_resources(path="circuits/resources_synth.md")`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py:296-307`
**Inputs** `path`, interpreted **relative to the current working directory** via `Path(path)` (line 306) — not relative to the run directory.
**Outputs** Returns `rows`: a list of 11 `(name, resources_dict)` pairs — six group rows named `group {g} (theta={dt/2:.4f})` at θ = `dt/2` including `D` (lines 298-299), one `one Strang step` row at `dt` (line 300), and four rows `full circuit r={r} (prep + steps, merged D)` for `r` in 0..3 (lines 301-302). Each resources dict comes from `_resources` (lines 290-293): `transpile` to `["cz","rz","sx","x","id"]` at `optimization_level=3`, `seed_transpiler=7`, no coupling map; `n_2q` is a `sum` of booleans and `depth_2q`/`depth` are raw `depth()` results — **not** cast to `int` here (contrast `strang_l12.resources:248-250`).
**Side effects** **Writes and silently overwrites** the markdown file at `path` (line 306). Content is fixed: an H1 title, a blank line, a window line `Window: g2=…, m=…, dt=….4f.`, a blank line, the table header `| circuit | 2q count | 2q depth | total depth |` with its separator, then one row per entry, terminated by a trailing newline (lines 303-306). The `r` loop is hard-coded to `range(4)` (line 301) and ignores `p["r_max"]`.
**Empty/degenerate and errors** The parent directory is **not** created; a missing `circuits/` directory under the CWD raises `FileNotFoundError`. No path sanitization.
**Enforcement** `runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py::test_resources_and_json:54-67` calls it with the default path — so the test writes into the CWD — and asserts only that `circuits/resources_synth.md` **exists** (`:56`) and that every `n_2q >= 0` (`:67`). It indexes rows by the exact names `"one Strang step"` and `"full circuit r=3 (prep + steps, merged D)"` (`:62-64`), which pins those two name strings. **No resource value, and no file content, is asserted.**

### su2qc.compile.route.fake_heron

**Signature** `fake_heron()`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py:30-32`
**Inputs** None.
**Outputs** A **new** `FakeTorino()` instance on every call (line 32); no caching, no singleton.
**Invariants** The Heron-class target identity is asserted nowhere in source beyond the constructor call — UNENFORCED.
**Side effects** Lazy import inside the body (line 31), so `ImportError` surfaces at call time, not import time. Note that **importing the module itself** mutates `sys.path`, inserting `REPO/src` (`route.py:21-25`).
**Empty/degenerate and errors** `ImportError` if `qiskit_ibm_runtime` is unavailable.
**Enforcement** UNENFORCED — no test file in the snapshot imports `su2qc.compile.route`. It is executed only by `compile/run_g4.py:25` and the `__main__` block at `route.py:122`.

### su2qc.compile.route.route

**Signature** `route(circ, backend=None, opt=3, seed=7, initial_layout=None)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py:35-47`
**Inputs** `circ`; `backend` defaulting to a fresh `fake_heron()` (line 36); `opt` → `optimization_level`; `seed` → `seed_transpiler`; optional `initial_layout` passed straight through (line 38).
**Outputs** `(isa, layout_info)` where `layout_info` has exactly two keys: `initial_physical` — `[int(lay.initial_layout[q]) for q in circ.qubits]`, the physical index carrying each **original** circuit qubit (lines 40, 45) — and `final_index_layout` — `[int(x) for x in isa.layout.final_index_layout()]` (line 46).
**Invariants** When `isa.layout is None`, **both** lists fall back to the hard-coded `list(range(12))` (lines 40, 47) regardless of the circuit's actual width; no widths are checked. The local `final` computed at lines 41-44 is **dead code** — never returned or used. UNENFORCED.
**Side effects** None beyond transpilation. Determinism is only as strong as the fixed `seed_transpiler` plus the installed Qiskit version.
**Empty/degenerate and errors** A backend whose coupling map cannot host the circuit raises from `transpile`. `initial_layout` mismatches raise from `transpile`; unvalidated here.
**Enforcement** UNENFORCED. Used at `compile/run_g4.py:64` (per-step) and `:69` (per-`r`, pinned to the step's `initial_physical`), and at `route.py:124`.

### su2qc.compile.route.routed_resources

**Signature** `routed_resources(isa)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py:50-55`
**Inputs** A routed circuit.
**Outputs** `{"n_2q": int, "depth_2q": int, "depth": int}`.
**Invariants** `n_2q` counts two-qubit instructions **excluding** `barrier` (lines 51-52), whereas `depth_2q` uses a filter that only tests `num_qubits == 2` and therefore **includes** two-qubit barriers (line 54). The two figures are consequently not derived from the same instruction set. UNENFORCED.
**Side effects** None.
**Empty/degenerate and errors** Empty circuit → zeros. No validation.
**Enforcement** UNENFORCED — no test asserts these values; `run_g4.py` uses its own `n2`/`d2` helpers instead (`run_g4.py:29-34`).

### su2qc.compile.route.routed_equivalence

**Signature** `routed_equivalence(logical, isa)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py:58-85`
**Inputs** The logical circuit and its routed ISA counterpart. Both must be measurement-free in effect: `measure`, `barrier`, and `delay` are dropped from the reduced circuit (line 70) but a measurement in `logical` would raise at line 62.
**Outputs** `float(1.0 - abs(np.vdot(vec, psi_l)))` (line 85) — one minus the modulus of the overlap, hence **global-phase insensitive**, valued in [0, 1], with 0 meaning agreement. It is a fidelity-deficit-like scalar, not a squared infidelity.
**Invariants** The routed state is pulled back through `final_index_layout` so logical qubit `i` is read from physical `fil[i]` (lines 64, 75), with axis arithmetic `n-1-order[i]` reflecting Qiskit little-endian storage (lines 78-82). **Row 0 of the reshaped array is taken (line 84), which assumes every non-logical active qubit is left in exactly `|0>` and unentangled**; if routing leaves an ancilla populated or entangled, the extracted `vec` is a sub-normalized slice and the returned number silently absorbs that lost weight rather than reporting a permutation error. The vector is **not** renormalized. UNENFORCED.
**Side effects** None. The `Operator` import at line 61 is unused dead code.
**Empty/degenerate and errors** `isa.layout is None` → `AttributeError` at line 64. `logical.num_qubits` greater than the number of active physical qubits → `KeyError`/`IndexError` at line 75. No guard.
**Enforcement** UNENFORCED by tests. Executed only in `compile/run_g4.py:75` and `:89` (per-`r`) and at `route.py:126`; those call sites print or serialize the value without a threshold assertion.

### su2qc.compile.route.pyzx_pass

**Signature** `pyzx_pass(circ, strategy="basic")`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py:88-110`
**Inputs** A circuit expressible in OpenQASM 2 (`qasm2.dumps`, line 98) — the caller is responsible for pre-flattening, as `run_g4.py:50-51` does. `strategy` ∈ {`"basic"`, `"full_reduce"`}.
**Outputs** A **new** `QuantumCircuit` parsed back from PyZX's QASM (line 110). `"basic"` → `zx.optimize.basic_optimization(..., do_swaps=False)` (line 102), described in the docstring as topology-preserving. `"full_reduce"` → graph `full_reduce` then `extract_circuit(..., up_to_perm=False).to_basic_gates()` (lines 104-107).
**Invariants** **No equivalence check is performed inside this function**; the docstring (lines 89-92) states the dense 12-qubit `Operator` check was replaced by a caller-side statevector check. Angles are converted through a rational approximation with denominator bound `2**40`, set on the PyZX global `zx.settings.float_to_fraction_max_denominator` and **restored in a `finally` block** (lines 95-100); the returned circuit is therefore only approximately equal to the input at that resolution. UNENFORCED.
**Side effects** Temporarily mutates PyZX module-global settings (restored). Lazy imports of `qasm2` and `pyzx` (lines 93-94).
**Empty/degenerate and errors** Unknown `strategy` → `ValueError(strategy)` (line 109). Gates not representable in QASM 2 raise during `dumps`/`from_qasm`; `run_g4.py:58-86` wraps the whole pipeline in a bare `except Exception` and records `{"error": repr(e)}` (`run_g4.py:84-86`).
**Enforcement** UNENFORCED. The only equivalence evidence is `run_g4.py:61-63`, which calls `state_equivalence` on the prepared step circuit and merely records the number.

### su2qc.compile.route.state_equivalence

**Signature** `state_equivalence(a, b)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py:113-116`
**Inputs** Two circuits, assumed the same width (docstring line 114); not checked.
**Outputs** `float(1.0 - abs(np.vdot(va, vb)))` from `|0>` — global-phase insensitive, in [0, 1].
**Invariants** Same-width requirement — UNENFORCED; differing widths raise `ValueError` from `np.vdot`.
**Side effects** None.
**Empty/degenerate and errors** Circuits with measurements raise from `Statevector`.
**Enforcement** UNENFORCED; used at `compile/run_g4.py:61-63` where the result is stored as `pre_route_equiv_step` and formatted into `compile/resources_routed.md` (`run_g4.py:115`) without an assertion.

### su2qc.compile.run_g4.n2

**Signature** `n2(c)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py:29-30`
**Inputs** Any circuit.
**Outputs** `int` count of instructions with `num_qubits == 2` and `name != "barrier"` (line 30).
**Invariants** Barrier exclusion matches `compile/route.py:51-52` but **not** `strang_l12.resources:247`. UNENFORCED.
**Side effects** None from the function. **Importing `su2qc.compile.run_g4` executes the entire production script** — see the module note under `d2`.
**Empty/degenerate and errors** Empty circuit → 0.
**Enforcement** UNENFORCED.

### su2qc.compile.run_g4.d2

**Signature** `d2(c)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py:33-34`
**Inputs** Any circuit.
**Outputs** `int(c.depth(lambda x: x.operation.num_qubits == 2))` — the filter does **not** exclude barriers, so `d2` and `n2` are computed over different instruction sets. UNENFORCED.
**Side effects** None from the function itself. **Module-level import side effects and CLI behaviour** (`run_g4.py:13-152`): inserts `"src"` on `sys.path` (`:13`); reads the window via `sl.params()` (`:21`); creates `compile/` (`:23`); instantiates `FakeTorino` (`:25`); builds `synth_full_circuit(r)` for `r` in 0..`r_max` (`:41`); routes three pipelines (`:58-86`), printing per-pipeline lines (`:82-83`) or `FAILED` plus the exception repr (`:86`); prints per-`r` routed equivalences (`:90`). It then **writes**, all relative to the CWD: `compile/resources_routed.json` (`:98-102`, containing `chosen`, `pipelines`, `equivalence_rmax`, `equivalence_per_r`, `backend`, `notes`), `compile/layout.json` (`:103-105`, containing `backend`, `initial_physical`, `final_index_layout`, `seed_transpiler: 7`, `optimization_level: 3`), and `compile/resources_routed.md` (`:107-119`, a table plus a fixed budget line `~250 CZ/step, ~1000 CZ/circuit, 2q depth < ~200 (+10% slack)` and a per-`r` CZ line). It then builds the twin (`:122`), computes the exact reference via `scan.timeseries_at(..., tag="exact_at_window")` (`:124`) — which itself writes `analysis/tables/exact_at_window.csv` and three PNGs (`scan.py:131-138,144-172`) — runs 5 repeats × 4000 shots per `r` with per-`r` caller seed `500 + 10*r` (`:131`), bootstraps with `n_boot=300, seed=r` (`:132`), creates `analysis/tables/` (`:143`) and writes `analysis/tables/twin_timeseries.csv` with header `r,t,observable,exact,twin_mean,twin_2sigma,within,yield` (`:144-147`) and `compile/twin_check.json` (`:148-151`, keys `yield_deepest`, `yields`, `n_points_within_2sigma`, `repeats`, `shots`, `mode`, `backend`, `arm`). The "within 2σ" flag at `:137` uses `max(two_sig[key], 1e-12)` as the tolerance — and, per the status block, **every v0.5.0 twin sigma is void as independent-repeat uncertainty**, so `n_points_within_2sigma` is not a valid coverage statistic.
**Empty/degenerate and errors** If the `qiskit_L3` pipeline raises, its entry contains only `"error"` and line `:89` raises `KeyError` on `isa_by_r`, or `:96` on `best["per_step"]`; the bare `except` at `:84` does not protect the downstream code.
**Enforcement** UNENFORCED — no test imports this module or asserts any written artifact from it.

### su2qc.dynamics.engine.evolve

**Signature** `evolve(H, psi0, times)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py:15-32`
**Inputs** `H` a **sparse** matrix (`.toarray()` is required, line 28); `psi0` any array-like, flattened and cast to complex (line 22); `times` array-like of floats (line 30).
**Outputs** Array of shape `(len(times), dim)`, row `t` being `V (e^{-iEt} ⊙ c0)` computed as `(phases * c0[None, :]) @ V.T` (line 32) — `V.T`, not `V.conj().T`, which is correct for reconstructing `V·(…)` from an `eigh` decomposition.
**Invariants** `psi0` is **normalized in place of the caller's scaling** (line 23): the returned trajectory always starts from a unit vector regardless of the input norm; `psi0` itself is copied by `flatten()`, so the caller's array is not mutated. `H` is assumed Hermitian; `eigh` reads only one triangle, so a non-Hermitian `H` is silently symmetrized and no error is raised. The docstring (lines 16-21) describes cumulative dense `expm` per step, which the implementation does **not** do — it uses a single eigendecomposition; the docstring is stale, the results agree mathematically.
**Side effects** None. Cost: one dense `eigh` of `dim × dim` per call, independent of `len(times)`.
**Empty/degenerate and errors** Zero `psi0` → division by zero at line 23 producing `NaN`s with a numpy warning, **no exception**. Empty `times` → shape `(0, dim)`. Dense `H` → `AttributeError` at line 28.
**Enforcement** Agreement with a direct `expm` to 1e-12 at `t = 7.3` for `(g2, m) = (1.0, 0.2)` — **directly** enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py::test_evolve_matches_expm:23-30`. Normalization behaviour and the non-Hermitian silent path are UNENFORCED.

### su2qc.dynamics.engine.self_check

**Signature** `self_check(g2: float, m: float, jmax: float, t_max: float)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py:35-130`
**Inputs** Coupling, mass, truncation, and horizon. No range validation.
**Outputs** `{"expm_krylov_dev": float, "energy_drift": float, "N_drift": float}` (lines 126-130): the max inf-norm deviation between the dense and Krylov trajectories over 21 times (lines 104-105), and the max drifts of `<H>` and `<N>` **computed from the dense trajectory only** (lines 110-124). The Krylov path's own conservation is therefore not measured.
**Invariants** The dense path is **cumulative** — `psi_dense[k] = expm(-i H dt) @ psi_dense[k-1]` (lines 86-92) — while the Krylov path recomputes from `psi0` at each absolute time (lines 99-101); the comparison is thus between an accumulating and a non-accumulating scheme. The docstring targets ≤1e-9 / ≤1e-10 / ≤1e-10 (line 42) are **not enforced inside the function**; it returns numbers and never raises on them. `H_diag` is built at lines 54-65 and **never used** (energies come from `H_arr`, line 112) — dead code. The initial state falls back **silently** to basis index 0 if the stretched label is absent (lines 70-73).
**Side effects** None; no file writes. Cost: 20 dense `expm` plus 20 `expm_multiply` calls per invocation.
**Empty/degenerate and errors** `t_max = 0` gives a degenerate grid where every `dt < 1e-15` branch copies the previous state (lines 88-89) and all three outputs are 0. No exception paths of its own.
**Enforcement** The three targets are asserted **only** at `(4.0, 0.75, 0.5, 10.0)` by `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py::test_self_check:15-19` — direct, single-point, and historical.

### su2qc.dynamics.scan.channel_probs

**Signature** `channel_probs(basis, states)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:59-62`
**Inputs** The label list and a `(T, dim)` state array.
**Outputs** The 4-tuple `(P_surv, P_meson, P_BBbar, P_other)`, each an array of length `T`, obtained as `|states|²` contracted with the four masks (lines 61-62). **Order of the tuple is fixed and every caller unpacks it positionally** (`scan.py:88, 120, 186, 284, 313`).
**Invariants** The masks come from `_classify` (lines 33-50) with the strict if/elif order: `any |q_v| == 2` → BBbar; `q == (1,-1,0,0)` → surv; `all |q_v| == 1` → meson; `Σ n_v == 4` → other. Channels are mutually exclusive by construction; they are **not** exhaustive over the full 82-state space, so the four probabilities need not sum to 1 (states outside `N=4` and not BBbar receive no channel). The BBbar predicate is occupation-difference based and is not restricted to `N=4`. Per R15, the meson branch necessarily has `N=4`. **Directly** enforced on the masks: `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py::test_channel_masks_partition_N4_sector:44-50` asserts 38 states with `N=4`, that the four masks partition exactly that subspace, and `surv.sum() == 2`, `meson.sum() == 2` — consistent with the two survival codewords listed in `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json`.
**Side effects** None; masks are rebuilt on every call (no caching).
**Empty/degenerate and errors** `basis`/`states` length mismatch → `ValueError` from the matrix product; unvalidated.
**Enforcement** Masks: direct (`tests/test_dynamics.py:49-50`). The contraction itself and the tuple order: UNENFORCED.

### su2qc.dynamics.scan.mass_scan

**Signature** `mass_scan(g2_values=(1.0, 2.0, 4.0, 8.0), n_m=25, t_window=(0.0, 40.0), jmax=0.5)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:67-108`
**Inputs** As given; `m` is scanned over `linspace(0, 0.5*g2, n_m)` per `g2` (line 80) and the time grid is 401 points over `t_window` (line 78).
**Outputs** `{"mstar_over_g2": {str(g2): float}, "mstar_over_g2_tb": {str(g2): float}, "n_mass_points": n_m, "n_g2_values": len(g2_values), "t_window": list, "tree_level": 0.1875}` (lines 103-105). **Two distinct estimators are reported and must not be conflated**: `mstar_over_g2` is `argmax` of the time-averaged pair weight `W̄` (line 97), `mstar_over_g2_tb` is `argmin` of the breaking time `t_b` (line 98). Both are divided by `g2` (dimensionless). The docstring (lines 69-71) records that they differ at strong coupling.
**Invariants** `t_b` is the first time with `P_surv ≤ 0.5`, **or**, if no such time exists, the `argmin` time is substituted with no flag (lines 89-90) — a non-breaking trajectory silently reports a finite `t_b`. `W̄ = ∫(P_meson + P_BBbar) / (t_max − t_min)` via `np.trapezoid` (line 91). Dict keys are `str(g2)`, so float formatting fixes the key text. UNENFORCED.
**Side effects** **Writes** `analysis/tables/exact_mass_scan.csv` with header `g2,m,t_b,W_bar,P_meson_avg,P_BBbar_avg` and `%.10g` fields (lines 99-102), and `physics/resonance.json` (lines 106-107). It creates `analysis/tables/` (line 74) but **not** `physics/`, so a missing `physics/` directory raises `FileNotFoundError` at line 106 after the CSV has already been written. Both files are overwritten. Paths are anchored to `RUN_DIR` (lines 19-20), not the CWD. Cost: `len(g2_values) × n_m` Hamiltonian builds and eigendecompositions.
**Empty/degenerate and errors** `_idx` raises `KeyError` if `STRETCHED` is absent from the basis (line 30). `n_m = 1` gives `m = 0.0` only. Empty `g2_values` → empty dicts.
**Enforcement** No test executes `mass_scan`. `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py::test_artifacts_and_window:54-58` reads the **stored** `physics/resonance.json` and asserts `n_mass_points >= 21`, `n_g2_values >= 2`, and existence of the CSV — that is an assertion about a historical artifact, not about this function's behaviour. UNENFORCED as a function contract.

### su2qc.dynamics.scan.timeseries_at

**Signature** `timeseries_at(g2, m, jmax=0.5, times=None, tag="exact_timeseries")`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:113-141`
**Inputs** `times` defaults to `linspace(0, 12, 121)` (lines 114-115); `tag` names the output CSV.
**Outputs** A dict with keys `t, P_surv, P_meson, P_BBbar, P_other, E2, n, energy, P_stretched, P_short` (lines 139-141). `E2` and `n` are `(T, 4)` arrays (per-link Casimir and per-vertex occupation, lines 121-124); `energy` is the real expectation `<ψ|H|ψ>` (line 128); `P_stretched`/`P_short` are the single-amplitude probabilities of the two labelled states (lines 125-126), **not** channel sums. `t` is the same array object that was passed in.
**Invariants** Channel semantics are exactly those of `channel_probs`. `E2` uses `cv.casimir` per link (line 54). The `n` column order is vertex order `v = 0..3`; `run_g4.py:135` reads `exact["n"][r][2]` as `n_v3`, consistent with the 1-based CSV header at line 133. UNENFORCED.
**Side effects** **Writes** `analysis/tables/{tag}.csv` (creating the directory, lines 129-137) with header `t,P_stretched,P_short,P_surv,P_meson,P_BBbar,P_other,E2_l1..4,n_v1..4,energy` and `%.10g` fields, and calls `_figures` (line 138), which forces the matplotlib `Agg` backend and writes three PNGs — `analysis/figures/exact_channels.png`, `exact_casimir.png`, `exact_density.png` (lines 144-172). All are overwritten silently. **`tag` is interpolated into the filename with no sanitization** (line 131), so a `tag` containing path separators writes outside the tables directory.
**Empty/degenerate and errors** `_idx` raises `KeyError` if `STRETCHED` or `SHORT` is missing (line 125) — note `SHORT` is required even though it is only a diagnostic.
**Enforcement** UNENFORCED. Called by `compile/run_g4.py:124` with `tag="exact_at_window"`; no test asserts its outputs.

### su2qc.dynamics.scan.truncation

**Signature** `truncation(g2, m)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:177-203`
**Inputs** `g2`, `m`. The time grid is hard-coded `linspace(0, 12, 121)` (line 179) and the two truncations are hard-coded `0.5` and `1.0` (line 181).
**Outputs** `{"max_abs_dprob": float, "g2": g2, "m": m}` (line 189), where the deviation is the max absolute difference across the four channels **and** all 121 times of the two `4 × 121` stacks (lines 187-188).
**Invariants** The comparison is valid only if the two bases' channel definitions coincide; both use `_classify`, so this holds by construction of the code path. The `jmax=1` sector counts used by the larger basis are checked independently at `runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py:30-40` (152 labels; sectors `{0:3, 2:36, 4:74, 6:36, 8:3}` against a transfer-polynomial prediction) — that is a basis-dimension check, **not** a check of this function.
**Side effects** **Writes** `physics/truncation_error.json` (lines 190-191) and `physics/truncation_error.md` (lines 192-202); the `physics/` directory is **not** created. The 0.1 threshold at line 197 only selects which of two prose sentences is written — it raises nothing and returns nothing different. No threshold was changed.
**Empty/degenerate and errors** `FileNotFoundError` if `physics/` is absent, after both evolutions have run.
**Enforcement** UNENFORCED — no test calls it and no test reads its artifacts.

### su2qc.dynamics.scan.strang_step_matrix

**Signature** `strang_step_matrix(D, hs, B, dt)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:236-247`
**Inputs** `D` diagonal block, `hs` a sequence of at least four hopping blocks, `B` magnetic block, all square and conformable; `dt`.
**Outputs** New dense matrix accumulated by left-multiplication in the order `hs[0], hs[2], hs[1], hs[3]` at `dt/2` around `B` at `dt`, wrapped by `D` at `dt/2` on both ends (lines 239-246) — the same operator ordering as `circuits/strang_l12.exact_strang_matrix:209-222`.
**Invariants** Ordering equality with the `strang_l12` reference — **UNENFORCED**; no test compares the two implementations. Element types: `expm` of dense arrays, so `hs` entries must be dense; a sparse input raises.
**Side effects** None; 11 dense `expm` calls per invocation.
**Empty/degenerate and errors** `len(hs) < 4` → `IndexError` at line 239. Shape mismatches raise from the matrix products. No validation.
**Enforcement** Indirect only, through `strang_error`, whose value is asserted `≤ 0.05` at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:137` and via `verify_window` at `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py:62`.

### su2qc.dynamics.scan.strang_error

**Signature** `strang_error(g2, m, dt, r, jmax=0.5)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:250-266`
**Inputs** Window parameters and step count.
**Outputs** A single non-negative `float`: the **maximum over three observable deviations** at `t = r·dt` (lines 262-266) — `|ΔP_surv|`, `max_v |Δ⟨n_v⟩|`, and `max_l |Δ⟨E²_l⟩|`. It is an **observable** error, **not** a state-vector distance; a state error with the same magnitude is not implied.
**Invariants** The exact reference is `expm(-i H (r·dt)) ψ0` with `ψ0` the stretched string (lines 253-259). The step operator is rebuilt per call from a fresh `_term_split`, whose exactness is asserted internally at line 232. UNENFORCED for the observable-vs-state distinction.
**Side effects** None. Cost: one `_term_split` (two Hamiltonian builds) plus 11 `expm` calls plus one large `expm` per invocation; `select_window` calls it inside a double loop (line 287).
**Empty/degenerate and errors** `r = 0` returns exactly `0.0` (both states equal `ψ0`), which is a vacuous pass against any threshold. Negative `r` behaves as `r = 0` for the Strang side while the exact side evolves backwards, giving a nonzero, unflagged value.
**Enforcement** `≤ 0.05` at the stored window — **direct** at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py::test_window_strang_error:135-137`, and again through `verify_window` at `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py:62`. Both are single-point historical checks.

### su2qc.dynamics.scan.select_window

**Signature** `select_window(g2=1.0, m=None, jmax=0.5)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:269-303`
**Inputs** `g2`; `m` optional — when `None` it is read from `physics/resonance.json` as `mstar_over_g2[str(g2)] * g2` (lines 272-274), i.e. the `W̄`-argmax estimator, **not** the `t_b` estimator.
**Outputs** A candidate dict `{"g2", "m", "dt", "r_max", "expected": {"psurv_drop", "pair_weight", "strang_err"}, "shortfall_flagged"}` (lines 288-292). The search is a fixed nested loop: `r_max ∈ (3, 2)` outer, `t_tot ∈ (3.0, 2.5, 3.5, 4.0, 2.0, 5.0, 6.0, 1.5)` inner, `dt = t_tot / r_max` (lines 279-281). The **first** candidate satisfying `strang_err ≤ 0.05` **and** `drop ≥ 0.3` **and** `pair ≥ 0.05` is written and returned immediately (lines 293-297); otherwise the best-by-largest-`psurv_drop` among candidates with `strang_err ≤ 0.05` is returned with `shortfall_flagged = True` (lines 298-303). The three thresholds are hard-coded and unchanged.
**Invariants** `drop = P_surv(0) − P_surv(t_tot)` and `pair = P_meson(t_tot) + P_BBbar(t_tot)` at exactly two evaluation times `[0, t_tot]` (lines 282-286). The returned `expected` values are those two-point quantities, not trajectory extrema. UNENFORCED.
**Side effects** **Writes** `physics/window.json` on both the accepting path (lines 295-296) and the shortfall path (lines 301-302); overwrites. `physics/` is not created here. Reads `physics/resonance.json` when `m is None`.
**Empty/degenerate and errors** If **no** candidate satisfies `strang_err ≤ 0.05`, `best` remains `None` and line 300 raises `TypeError: 'NoneType' object does not support item assignment` — after 16 full evaluations and with no file written. `KeyError` if `str(g2)` is absent from `resonance.json`; `FileNotFoundError` if the file is missing.
**Enforcement** UNENFORCED as a function. Its **artifact** is checked at `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py:59-64`: `r_max ∈ (2, 3)`, and re-verified criteria where the `psurv_drop` and `pair_weight` assertions are disjunctions with `w.get("shortfall_flagged")` and are therefore vacuous whenever that flag is set.

### su2qc.dynamics.scan.verify_window

**Signature** `verify_window(w)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py:306-316`
**Inputs** A window dict; only `g2, m, dt, r_max` are read (line 308).
**Outputs** `{"psurv_drop": float, "pair_weight": float, "strang_err": float}` (lines 314-316), recomputed from scratch at times `[0, r·dt]`.
**Invariants** **`jmax` is hard-coded to 0.5** (line 309) and any `jmax` recorded in `w` is ignored; the nested `strang_error` call also uses its own default `jmax=0.5` (line 316). The function applies **no** thresholds and never raises on a failing window — the comparison lives entirely in the caller. UNENFORCED.
**Side effects** None; no file writes. Cost: one Hamiltonian build plus one `strang_error`.
**Empty/degenerate and errors** Missing keys → `KeyError` at line 308. `r_max = 0` gives `psurv_drop = 0`, `strang_err = 0.0` — a vacuous pass.
**Enforcement** Called at `runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py::test_artifacts_and_window:61`, which asserts `strang_err ≤ 0.05` directly (`:62`) and the other two only in disjunction with `shortfall_flagged` (`:63-64`). Historical.

### su2qc.encodings.l12.encode

**Signature** `encode(label) -> int`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py:33-38`
**Inputs** A canonical route-spinnet label `(js, ns, tag)`.
**Outputs** The 12-bit integer code. Qubit `3v, 3v+1, 3v+2` hold (first link, second link, matter) for vertex `v`, with **q0 the least significant bit**, so displayed Qiskit strings read `q11…q0` (module docstring, lines 1-6, and `_maps`, lines 22-30). The matter bit is `1` iff `ns[v] == 2` (line 29); link bits are `int(round(2*j))` (line 25).
**Invariants** Round-trip `encode(decode(c)) == c` for all 82 codes — **directly** enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:22`. `encode(STRETCHED) == 3793` — direct at `tests/test_l12.py:27-28`. Matching is exact tuple equality by linear scan over the 82 entries (lines 35-37): a label with numerically equal but differently typed components will not match.
**Side effects** Warms the `lru_cache(maxsize=1)` `_maps()` (line 18). O(82) comparisons per call.
**Empty/degenerate and errors** Any unmatched label → `ValueError(f"not a physical L12 label: {label!r}")` (line 38).
**Enforcement** Direct as cited.

### su2qc.encodings.l12.decode

**Signature** `decode(bits)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py:40-48`
**Inputs** Either a **12-character** `"01"` string or an `Integral` in `[0, 4096)`.
**Outputs** The label tuple, or `None`. String path: **strict** length-12 and alphabet check, else `None` (lines 42-44). Integer path: non-`Integral` or out-of-range → `None` (lines 46-47). In-range but unphysical → `None` from `_maps().get` (line 48). Returned label tuples come from the shared cached map; they are immutable, but `_maps()` itself is a shared mutable dict.
**Invariants** `None` exactly for non-physical in-range integers — supported by the exhaustive count `n_phys == 82` over `range(4096)` at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:24-25` (which tests `is_physical`, and is consistent with the 82-entry map) and by round-trip at `:22`; bit-string form checked at `:29`. Measured: `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` `invalid_input: {code: 1, decode_is_none: true}`.
**Side effects** None beyond the cache.
**Empty/degenerate and errors** `bool` is `Integral`, so `decode(True)` looks up code 1 and returns `None`. Non-string, non-`Integral` inputs return `None` rather than raising — callers cannot distinguish "wrong type" from "unphysical". **Length asymmetry with `leakage_flags`/`is_physical`, which apply no length check to strings** (lines 56-57): a short string such as `"0000"` yields `is_physical == True` but `decode == None`. UNENFORCED.
**Enforcement** Direct for the round-trip and bit-string cases (`tests/test_l12.py:22, 29`); the length asymmetry is UNENFORCED.

### su2qc.encodings.l12.physical_codes

**Signature** `physical_codes() -> list[int]`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py:50-51`
**Inputs** None.
**Outputs** `sorted(_maps())` — a **new** ascending list of the 82 physical integer codes on every call; mutating it is safe.
**Invariants** Exactly 82 entries, all distinct — **directly** enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:19-20`; the count is corroborated by `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` `physical_code_count: 82` and by the basis dimension 82 at `runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py:28-30`. Ascending order — UNENFORCED, though `code_index` depends on it.
**Side effects** Builds the cached `_maps()` on first use (which enumerates the full `jmax=0.5` basis, line 21).
**Empty/degenerate and errors** None.
**Enforcement** Direct as cited.

### su2qc.encodings.l12.leakage_flags

**Signature** `leakage_flags(bits)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py:53-65`
**Inputs** An integer code or a binary string.
**Outputs** `{"vertex": (bool,)*4, "link": (bool,)*4}`. **`True` means a violation.** `vertex[v] = (bit(3v) XOR bit(3v+1)) AND bit(3v+2)` (lines 58-59). `link[l]` compares the two endpoint copies of link `l`, located through the fixed `_VLINKS` incidence order (lines 62-64); `True` means the copies disagree.
**Invariants** String inputs are converted by `int(bits, 2)` with **no length check** (line 56); on `ValueError` the function returns the all-violation dict `{"vertex": (True,)*4, "link": (True,)*4}` (line 57) — a parse failure is reported as maximal leakage rather than as an error. UNENFORCED.
**Side effects** None.
**Empty/degenerate and errors** `""` → `int("", 2)` raises `ValueError` → all-`True` dict. Non-string non-integer inputs reach `_bit`, whose `int(code)` truncates floats silently and raises `TypeError` for e.g. `None` (line 16). No validation.
**Enforcement** Only through `is_physical`; the flag semantics themselves are UNENFORCED (no test inspects the returned dict).

### su2qc.encodings.l12.is_physical

**Signature** `is_physical(bits) -> bool`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py:67-69`
**Inputs** As `leakage_flags`.
**Outputs** `True` iff no vertex flag and no link flag is set (line 69).
**Invariants** Over the **integers** `0..4095`, `is_physical` selects exactly 82 codes — **directly and exhaustively** enforced at `runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py:24-25`, and `is_physical(c)` holds for every code in `physical_codes()` at `:23`. For **strings** the guarantee is weaker: no length check is applied, so shorter binary strings are zero-extended by `int(bits, 2)` and can be reported physical while `decode` returns `None` — this asymmetry is **UNENFORCED** and is the mechanism by which `postselect` (which uses `is_physical`) can retain a key that `observables` (which uses `decode`) cannot unpack.
**Side effects** None.
**Empty/degenerate and errors** Unparseable strings → `False` (all flags `True`).
**Enforcement** Direct on integers (`tests/test_l12.py:24-25`); string handling UNENFORCED.

### su2qc.twin.twin.twin_backend

**Signature** `twin_backend(seed=1234, backend=None, compact=False)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:28-37`
**Inputs** `seed`, an optional backend (defaulting to a fresh `FakeTorino()`, lines 30-32), and `compact`.
**Outputs** `compact=False` → `AerSimulator.from_backend(backend, seed_simulator=seed)` (line 37). `compact=True` → `AerSimulator(noise_model=NoiseModel.from_backend(backend))` (lines 33-36) — **the `seed` argument is silently ignored on this branch**; no `seed_simulator` is set. In either case the caller's seed is subsequently **overwritten** by `run_counts` (twin.py:60). Measured confirmation: `runs/campaign_v060/sessions/c060_p0_20260908_3/equal-seed-control.json` records `simulator_seed_option_before: 101` and `simulator_seed_option_after: 500`.
**Invariants** The two branches build **different** simulator objects — `from_backend` carries the backend's basis, coupling map, and timing, while the compact branch carries only the noise model. Results from the two paths are not interchangeable. UNENFORCED.
**Side effects** Lazy imports (lines 29-35). **Importing the module** inserts `RUN/src` on `sys.path` (twin.py:20-22).
**Empty/degenerate and errors** No validation of `backend`; an incompatible object raises inside `from_backend`/`NoiseModel.from_backend`.
**Enforcement** Exercised with `seed=101, compact=True` at `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:11`; that test asserts nothing about the seed's effect. The ignored-seed branch is UNENFORCED.

### su2qc.twin.twin.add_measurements

**Signature** `add_measurements(isa)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:40-51`
**Inputs** A routed circuit, ideally carrying a layout.
**Outputs** A **copy** (line 46) with a new 12-bit `ClassicalRegister` named `"c"` (lines 47-48) and `measure(qc.qubits[fil[i]], cr[i])` for `i` in 0..11 (lines 49-50). Therefore `c[i]` holds **logical** qubit `i`, and the Qiskit count strings read `q11…q0` in logical order — the same bit order assumed by `l12.decode` (`encodings/l12.py:1-6`).
**Invariants** `fil = isa.layout.final_index_layout()` when a layout exists, else `list(range(len(isa.qubits)))` (lines 44-45); the count-string convention holds only if that mapping is correct. The input circuit is **not** mutated. UNENFORCED directly.
**Side effects** None beyond the copy.
**Empty/degenerate and errors** A circuit already containing a register named `"c"` raises on `add_register` (line 48). Fewer than 12 qubits, or `len(fil) < 12`, raises `IndexError` at line 50. The register width is hard-coded 12 (line 47). No guards.
**Enforcement** Exercised at `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:13` and `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py:130`; no test asserts the bit ordering. UNENFORCED.

### su2qc.twin.twin.run_counts

**Signature** `run_counts(isa_meas_list, shots, seed, sim)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:54-63`
**Inputs** A list of measured ISA circuits, a shot count, a base `seed`, and a simulator.
**Outputs** A list of plain `dict` count mappings, one per input circuit, in input order (lines 57, 62).
**Behaviour, exactly.** For each index `k`: (1) **re-transpile** the circuit with `optimization_level=0` and a **fixed** `seed_transpiler=seed` — the same transpiler seed for every `k`, and the work is repeated even when the list holds the same circuit object five times, as at `run_g4.py:131` and `test_twin_variance.py:14` (line 58); (2) if the simulator exposes `set_options`, **mutate it** with `seed_simulator = seed + k` (lines 59-60) — this mutation **persists after the function returns**, leaving `sim` at `seed + len(list) − 1`; (3) run with `seed_simulator = seed + k` passed again as a run argument (line 61). The per-circuit seeds are therefore **consecutive integers**.
**Invariants / independence.** **Independence of repeats is VIOLATED in the measured backend and path.** From `runs/campaign_v060/sessions/c060_p0_20260908_3/seed-diagnosis.json`: on the **production** path, `shift_equal: true`, `shift_matches: 1023` of `shots_shift: 1024` with `same_index_matches: 424`, `equal_seed_counts_equal: true`, `equal_multisets: false`; on the **compact** path, `shift_matches: 1023` of 1024 with `same_index_matches: 414`. That is, after a **one-shot shift**, 1023 of 1024 per-shot outcomes coincide between consecutive seeds — on **both** the production and compact paths. Complementarily, `runs/campaign_v060/sessions/c060_p0_20260908_3/equal-seed-control.json` records `runtime_seeds: [500,500,500,500,500]`, `distinct: 1`, `distinctness_check_rejected: true`, and the caller seed 101 overwritten to 500. Both files are **EMULATED**; `seed-diagnosis.json` further records `status: "partial: diagnostic process exited 124 at 2400-second cap during r1; no completed r1 counts"` and `not_run: ["post-fix tests; BUILD blocked", "R8 post-fix acceptance"]`. **This finding is scoped to the measured backend/simulator path and must not be extrapolated to every random generator or backend.** A repair is **PROPOSED, NOT IMPLEMENTED**; campaign physics acceptance is **DEFERRED**.
**Side effects** Mutates the caller's `sim` options persistently (line 60). No file writes.
**Empty/degenerate and errors** Empty list → `[]` and no mutation. `shots = 0` returns empty count dicts from Aer. No validation of `seed` type or of `sim`; a simulator lacking `set_options` skips step (2) but still receives the run-time seed.
**Enforcement** `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:17-35` asserts only that the five returned dictionaries are pairwise **distinct** (`:30`), that some bootstrap `two_sigma` is positive (`:32`), that no mean is NaN (`:33`), and that forcing a repeated dictionary is detected (`:35`); `:38-39` asserts re-run reproducibility. **Distinctness of count dictionaries is not independence**, and the measured shift-overlap above is consistent with all of those assertions passing. The independence contract is therefore **UNENFORCED**, and those outputs are historical, not a gate pass.

### su2qc.twin.twin.postselect

**Signature** `postselect(counts)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:66-69`
**Inputs** A mapping from bit-string keys to weights.
**Outputs** `(kept, fraction)` — a **new** dict of the entries whose key satisfies `l12.is_physical` (line 67), and `sum(kept.values()) / tot` where `tot` is the sum over **all** input entries (lines 68-69). The input is not mutated; weights pass through untouched (ints stay ints, floats stay floats).
**Invariants** Empty input, or any input with `tot == 0`, returns `({}, 0.0)` via the `if tot else 0.0` guard (line 69) — measured as `empty_postselect: [{}, 0.0]` in `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json`. **This guard is present here and absent from `physical_yield`** (twin.py:152-155). Filtering uses `is_physical`, which does not length-check string keys, so a short key such as `"0000"` is **kept** even though `decode` would reject it — and `observables` would then raise. UNENFORCED.
**Side effects** None.
**Empty/degenerate and errors** Signed weights summing to zero yield `0.0` rather than an error. Non-string keys are handled by `is_physical`'s integer path.
**Enforcement** The empty-input return is measured (oracle JSON) but **UNENFORCED** by any test assertion; `postselect` is exercised only indirectly inside `bootstrap` (twin.py:165).

### su2qc.twin.twin.observables

**Signature** `observables(kept)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:72-102`
**Inputs** A mapping of **decodable** keys to weights, normally the first element of a `postselect` result.
**Outputs** A fresh dict with exactly 15 keys: `P_surv, P_meson, P_BBbar, P_other, P_stretched, P_short` (lines 74-75), `E2_l1..E2_l4` (lines 97-98), `n_v1..n_v4` (lines 99-100), and `dC` (line 101). Weights are **normalized** by `tot = sum(kept.values())` (lines 73, 80). Channel assignment order is BBbar → surv → meson → other (lines 83-94), identical to `channel_weights` and to `scan._classify`. `P_stretched` and `P_short` are tallied **inside** the surv branch (lines 87-90), so they are **sub-tallies of `P_surv`**, not additional channels. `dC = Σ_l E²_l − 2.25`, with the `9/4` reference hard-coded (line 101).
**Invariants** Per R15, the meson branch implies `n = (1,1,1,1)`, `N = 4`. The survival selector matches **two** distinct codewords (2058 and 3793) for the single occupation pattern `(1,1,0,2)` per `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json`; it is **not** rank-1. Key set constancy is what makes `bootstrap`'s `zip` safe (twin.py:168-174) — UNENFORCED.
**Side effects** None.
**Empty/degenerate and errors** `observables({})` returns all zeros with `dC = -2.25` and **no** exception, because the loop is skipped before any division (lines 78-101). A **non-empty** input whose weights sum to zero (possible with signed weights) raises `ZeroDivisionError` at line 80. An undecodable key raises `TypeError` at line 81 (`js, ns, _ = lab` with `lab is None`) — **`observables` does not skip undecodable keys, unlike `channel_weights` (line 111-112)**. All UNENFORCED.
**Enforcement** No test asserts any value returned by `observables`. `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:32-33` asserts only positivity of some bootstrap sigma and non-NaN means downstream of it. UNENFORCED.

### su2qc.twin.twin.channel_weights

**Signature** `channel_weights(kept)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:105-127`
**Inputs** A mapping of keys to weights, which may be **signed** and need not be normalized.
**Outputs** A fresh dict with exactly the six keys `P_surv, P_meson, P_BBbar, P_other, P_stretched, P_short`, all initialized to `0.0` (lines 107-108) and accumulated **without renormalization** (docstring line 106). `P_stretched`/`P_short` remain sub-tallies of `P_surv` (lines 119-122); the stretched/short discrimination is exact tuple equality on `js` against `(0.0,0.5,0.5,0.5)` and `(0.5,0.0,0.0,0.0)`.
**Invariants** Undecodable keys are **skipped silently** (lines 110-112). Channel order is BBbar → surv → meson → other (lines 115-126). Negative and unnormalized weights are **caller preconditions**, not validated guarantees: the function performs pure accumulation and asserts nothing about weight sign, scale, or type. **Directly** enforced for a 3-label synthetic set at `runs/campaign_v060/tests/gate_C0/test_estimator.py:7-22` — `P_stretched == 0.7`, `P_short == 0.2`, `P_surv == 0.9`, `P_BBbar == 0.1`, and `P_surv >= P_stretched + P_short`. Those assertions cover three codes and one weight vector; behaviour over the full 82-code set is UNENFORCED.
**Side effects** None.
**Empty/degenerate and errors** Empty input → all six keys `0.0`. Keys must be `int` or 12-character `"01"` strings for `decode`; **float or otherwise-typed keys are a caller precondition** and silently produce `None` → skipped.
**Enforcement** Direct but narrow, as cited.

### su2qc.twin.twin.channel_closure_residual

**Signature** `channel_closure_residual(kept)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:130-143`
**Inputs** As `channel_weights`.
**Outputs** `float(lhs − rhs)` with the equation reproduced exactly in the R15 section above: `lhs` sums the four channel keys `P_surv, P_meson, P_BBbar, P_other` (line 133), excluding the `P_stretched`/`P_short` sub-tallies; `rhs` sums the weight of every **decodable** key satisfying `Σ n_v == 4 or ∃v |q_v| == 2` (lines 135-142).
**Invariants** Under the R15 occupation domain the two sides select the same decodable keys, so the residual is algebraically zero for any weights, signed or unnormalized. **Undecodable keys with nonzero weight are skipped by `channel_weights` (line 111) and by the `rhs` loop (line 137) alike, so they cannot move the residual: the residual cannot detect an invalid code.** Measured: `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json` gives `invalid_input: {code: 1, decode_is_none: true, residual: 0.0}` and `singleton_closure_failures: []`. **The R9 demand that this residual detect invalid codes is UNSATISFIABLE AS WRITTEN; a ruling is awaited.**
**Side effects** None; recomputes `channel_weights` internally (line 132), so the decode work is done twice per call.
**Empty/degenerate and errors** Empty input → `0.0`.
**Enforcement** **Directly** enforced on a 3-label synthetic set: `runs/campaign_v060/tests/gate_C0/test_estimator.py:19` (`|residual| ≤ 1e-10`) and `:26` (same, after driving one weight negative at `:24-25`). That is a two-case check on three codes with signed weights; it does **not** establish closure over the 82-code set, and it does **not** test invalid-code detection.

### su2qc.twin.twin.matched_subtraction

**Signature** `matched_subtraction(observed, control)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:146-149`
**Inputs** Two observable dicts.
**Outputs** A fresh dict over the **union** of keys, each value `float(observed.get(key, 0.0) − control.get(key, 0.0))` (lines 148-149) — i.e. `O(t) − O(0)`.
**Invariants** A key absent from either side is silently treated as `0.0`, so a missing control entry returns the raw observed value rather than flagging a mismatch. No check that the two dicts describe the same circuit, shot count, or normalization. UNENFORCED.
**Side effects** None; inputs not mutated.
**Empty/degenerate and errors** Both empty → `{}`. Non-numeric values raise `TypeError`.
**Enforcement** **Directly** enforced for two shared keys at `runs/campaign_v060/tests/gate_C0/test_estimator.py:29-34` (`ΔP_stretched == −0.3`, `ΔP_meson == 0.2`). The missing-key path is UNENFORCED.

### su2qc.twin.twin.physical_yield

**Signature** `physical_yield(counts, physical_keys)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:152-155`
**Inputs** A counts mapping and a container of physical keys.
**Outputs** `float(Σ_{key ∈ physical_keys} counts[key] / total)` where `total = sum(counts.values())` (lines 154-155). **The denominator includes every reported shot**, physical or not, and **can be zero**.
**Invariants** Membership is plain `in` on the caller's container, so the encoding of `physical_keys` (bit-strings versus integers, and string width) must match the count keys exactly; **this is a caller precondition, not a validated guarantee** — no width, type, or membership check exists. Numerator terms are summed as given: signed or float weights pass through.
**Side effects** None.
**Empty/degenerate and errors** **Empty `counts` (or any `counts` with `total == 0`) raises `ZeroDivisionError`** — measured as `empty_physical_yield: {exception: "ZeroDivisionError", message: "division by zero"}` in `runs/campaign_v060/sessions/c060_p0_20260908_3/oracle-diagnostics.json`. This **contrasts with `postselect`, which returns `({}, 0.0)` for the same degenerate input** (twin.py:69). The asymmetry is **UNENFORCED**: no test covers the empty case for either function.
**Enforcement** One direct case: `runs/campaign_v060/tests/gate_C0/test_estimator.py:35-36` asserts `physical_yield({"0000": 3, "1111": 1}, physical_keys={"0000"}) == 0.75`. Note the test uses 4-character keys — the function performs no width validation, so this passes without exercising the 12-bit convention.

### su2qc.twin.twin.bootstrap

**Signature** `bootstrap(counts_list, n_boot=400, seed=0)`
**Source** `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:158-175`
**Inputs** `counts_list` — one element per repeat (docstring line 159); `n_boot`; `seed` for `np.random.default_rng` (line 161).
**Outputs** `(mean_dict, two_sigma_dict, yield_mean)` (lines 174-175). `mean` is the plain across-repeat mean of the per-repeat observables (line 172). `two_sigma` is `2.0 × std(bootstrap means, ddof=1)` over the `n_boot` resamples (line 173). `yield_mean` is `float(np.mean(ys))` over the per-repeat `postselect` yields (lines 165-167, 175). Key order is taken from `per[0]` (line 168) and reused for both dicts.
**Resampling semantics.** `boots` resamples **elements of `counts_list`** — `A[rng.integers(0, n, n)].mean(axis=0)`, i.e. `n` draws with replacement from the `n` repeat rows (line 171). **Because the returned `2*s` is a resampling of those elements, it is not a valid independent-repeat uncertainty when the elements are themselves correlated** — which is exactly the measured situation for `run_counts` on the measured backend/path (1023 of 1024 shots overlapping after a one-shot shift on both the production and compact paths; `runs/campaign_v060/sessions/c060_p0_20260908_3/seed-diagnosis.json`). **Every v0.5.0 twin sigma is void as independent-repeat uncertainty on this basis.** Independence alone would not be sufficient either: ordinary bootstrap adequacy additionally requires **representative replicates and a sufficient sample size** — the production call sites use `n = 5` repeats (`run_g4.py:126,132`; `test_twin_variance.py:14`).
**Invariants** All per-repeat dicts must share the key set of `per[0]` for the `zip` at lines 174-175 to align; this holds because `observables` always emits the same 15 keys (lines 74-101) — UNENFORCED. The diagnostic file reports per-observable `two_sigma`, `pooled_variance`, `expected_bootstrap_se`, and `ratio`, with `structural_zero_in_pooled_sample: true` for `P_meson`, `P_other`, `P_short`, and (production) `E2_l3`, `E2_l4` — those zero sigmas reflect an absent or degenerate channel population in that EMULATED sample, not a measured precision.
**Side effects** None; no file writes.
**Empty/degenerate and errors** Empty `counts_list` → `IndexError` at line 168 (`per[0]`). Repeats whose `postselect` result is empty do **not** raise (see `observables`), contributing an all-zero row with `dC = -2.25`, which silently biases the mean. `n_boot = 1` makes `std(..., ddof=1)` degenerate. `n = 1` yields `two_sigma == 0.0` for every key, with no warning. All UNENFORCED.
**Enforcement** `runs/campaign_v060/tests/gate_C0/test_twin_variance.py:31-33` asserts only that **some** `two_sigma` value is `> 0` and that no mean is NaN, for `n_boot=250, seed=77`, `n = 5`. No test asserts calibration, coverage, or independence. The `n_points_within_2sigma` figure written by `compile/run_g4.py:140,148-151` uses these sigmas and is therefore not a valid coverage statistic. Historical only; **campaign physics acceptance DEFERRED**.
