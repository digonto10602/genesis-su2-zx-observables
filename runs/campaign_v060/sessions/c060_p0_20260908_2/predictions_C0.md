# predictions_C0.md

# P0 physics predictions — gate C0 (campaign v0.6.1, Phase 0)

**Written by:** Opus 5 (REVIEW/PHYSICS lane), 2026-09-08, **before** lanes A0a and A0d are run
(v0.6.1 §2.1 item 4). Preregistered: nothing below may be edited after A0a/A0d produce numbers;
a disagreement is a `DISCREPANCIES.md` entry and a failed row, never a test edit
(v0.6.1 §5, bullet 4).

**Sources used** (repository only; no other material):
`prompts/gi_cost_campaign_v.0.6.1.md` §§0–2, 5; `prompts/gi_cost_campaign_v.0.6.0.md` lines 117,
142, 242 (V10 row, Phase-0 item 2, decision rule D-C0 — v0.6.0 remains the campaign document per
v0.6.1 §0); `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py`;
`.../ham/route_spinnet.py`; `.../ham/route_gausskernel.py`; and, for §3 only,
`.../twin/twin.py`, `.../compile/run_g4.py`, `.../circuits/synth_l12.py`,
`.../circuits/strang_l12.py`, `.../encodings/l12.py` (working-tree state as of 2026-09-08;
`twin.py` is one of the modified paths in the dirty tree, so the reader should confirm the
line numbers against the snapshot the gate actually runs).

Every statement is tagged **[S]** if it is read from a source, or **[D]** if it is my derivation
from those sources. Illustrative arithmetic that depends on a quantity not present in any source
(e.g. FakeTorino readout error rates) is tagged **[illustrative]** and is not a preregistered
number.

---

## 1. The j_max = 1 sector generating function

### 1.1 Inputs (frozen conventions only — no route label lists were read for this derivation)

- **[S]** Geometry. `conventions.py:20` gives four vertices; `conventions.py:34` gives
  `LINKS = ((0,1,"x"), (1,2,"y"), (3,2,"x"), (0,3,"y"))`, i.e. l1: v1→v2, l2: v2→v3, l3: v4→v3,
  l4: v1→v4. **[D]** Vertex incidences are therefore v1:{l4,l1}, v2:{l1,l2}, v3:{l2,l3},
  v4:{l3,l4}: every vertex is 2-valent and the patch is a single 4-cycle
  l1 – v2 – l2 – v3 – l3 – v4 – l4 – v1 – l1.
- **[S]** Truncation. `conventions.py:9–15, 64–65`: j ∈ {0, ½} at `JMAX_HALF`, j ∈ {0, ½, 1} at
  `JMAX_ONE`; one spin label per link.
- **[S]** Matter. `conventions.py:50–53`: two-color staggered fermions, one doublet per vertex,
  four Fock states per site — n = 0 (color-singlet vacuum), n = 1 (doublet), n = 2 (doubly
  occupied singlet). **[D]** As SU(2)-color representations the site Fock space decomposes as
  **1 ⊕ 2 ⊕ 1**: the matter spin is j_m = 0 for n ∈ {0, 2} and j_m = ½ for n = 1.
- **[D]** Gauss law at a 2-valent vertex v with incident link spins (j_a, j_b) and matter spin
  j_m: the physical states are the SU(2) singlets of V_{j_a} ⊗ V_{j_b} ⊗ V_{j_m}. The number of
  such singlets is the multiplicity of j_m in j_a ⊗ j_b, i.e. **1** if
  |j_a − j_b| ≤ j_m ≤ j_a + j_b with j_a + j_b − j_m integral, and **0** otherwise. Link
  orientation is irrelevant because V_j ≅ V_j* for SU(2), so the same count applies whether the
  end carries U or U†.
- **[D]** Specialising: j_m = 0 ⇒ j_a = j_b, and then n ∈ {0, 2} (two states);
  j_m = ½ ⇒ |j_a − j_b| = ½, and then n = 1 (one state); |j_a − j_b| = 1 admits neither, so such
  link pairs are excluded. Multiplicity never exceeds 1, which is why a 2-valent intertwiner tag
  carries no information (`conventions.py:97–100`, `LABEL_DOC`, tag ≡ 0).

  *Consistency note (not an input):* this reproduces the rule stated in the route-1 docstring
  (`route_spinnet.py:9–12`) and the structural condition under which route 2's `_local_singlet`
  returns a vector rather than `None` (`route_gausskernel.py:84–101`). The derivation above does
  not use either.

### 1.2 Vertex weight and transfer matrix

**[D]** Grade states by the total fermion number N = Σ_v n_v (this is the sector label used by
`validate_dimensions`, `route_spinnet.py:692–698`, and by `EXPECTED_SECTOR_DIMS`,
`conventions.py:74`). Track it with a formal variable x, giving each vertex the weight

  w(j_a, j_b) = 1 + x²      if j_a = j_b        (n = 0 or n = 2)
  w(j_a, j_b) = x           if |j_a − j_b| = ½  (n = 1)
  w(j_a, j_b) = 0           otherwise.

Because the patch is a 4-cycle of links with one vertex between each consecutive pair, the full
gauge-invariant generating function factorises into a transfer matrix on the link-spin alphabet:

  Z_{j_max}(x) = Σ_{j_1 j_2 j_3 j_4} w(j_4,j_1) w(j_1,j_2) w(j_2,j_3) w(j_3,j_4) = **Tr T⁴**,

with T indexed by the allowed spins and T[j, j'] = w(j, j'). Writing a = 1 + x² and b = x:

  j_max = 1:  T = ⎡a b 0⎤   j_max = ½:  T = ⎡a b⎤
                  ⎢b a b⎥                    ⎣b a⎦
                  ⎣0 b a⎦

**[D]** T = a·1 + b·A, where A is the adjacency matrix of the path graph on d = 2 j_max + 1
spins (only Δj = ±½ neighbours are connected). Its eigenvalues are
λ_k = a + 2b cos(kπ/(d+1)), k = 1 … d, so in general

  **Z(x) = Σ_{k=1}^{d} ( a + 2b cos(kπ/(d+1)) )⁴,  a = 1 + x², b = x.**

For j_max = 1 (d = 3) the eigenvalues are a + √2 b, a, a − √2 b, hence

  Z_1(x) = (a+√2b)⁴ + a⁴ + (a−√2b)⁴ = **3a⁴ + 24a²b² + 8b⁴**.

### 1.3 Expansion and the predicted counts

**[D]** With a = 1 + x², b = x:

  3(1+x²)⁴ = 3 + 12x² + 18x⁴ + 12x⁶ + 3x⁸
  24x²(1+x²)² =     24x² + 48x⁴ + 24x⁶
  8x⁴ =                     8x⁴

  **Z_1(x) = 3 + 36x² + 74x⁴ + 36x⁶ + 3x⁸**

| N = Σ n_v | 0 | 2 | 4 | 6 | 8 | total |
|---|---:|---:|---:|---:|---:|---:|
| **predicted dim, j_max = 1** | **3** | **36** | **74** | **36** | **3** | **152** |

Checks, all **[D]**:

1. **Total.** Z_1(1) = 3·2⁴ + 24·2²·1 + 8 = 48 + 96 + 8 = **152**, matching
   `EXPECTED_DIM[JMAX_ONE] = 152` (`conventions.py:72`).
2. **Palindromy.** Particle–hole conjugation n_v ↦ 2 − n_v multiplies each vertex weight by x²
   (a ↦ x²a, b ↦ x²·x⁻¹·… more directly: x⁸ Z_1(1/x) = Z_1(x)), so the sector list must be a
   palindrome — 3, 36, 74, 36, 3 is.
3. **j_max = ½ cross-check with the same machinery.** d = 2 gives
   Z_{1/2}(x) = (a+b)⁴ + (a−b)⁴ = 2a⁴ + 12a²b² + 2b⁴
   = 2 + 20x² + 38x⁴ + 20x⁶ + 2x⁸, total 82 — reproducing
   `EXPECTED_SECTOR_DIMS = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}` and `EXPECTED_DIM[JMAX_HALF] = 82`
   (`conventions.py:72–74`) exactly. The same formula therefore predicts both truncations from
   one structure, which is the strongest available evidence that the j_max = 1 numbers are not a
   transcription of the route output.
4. **Odd sectors.** Z contains only even powers of x, so all odd-N sectors are empty **[D]** —
   a consequence of the 4-cycle having an even number of vertices and each n = 1 vertex
   contributing exactly one power of x, with the number of |Δj| = ½ edges around a cycle
   necessarily even.

### 1.4 What the C0/C2 tests must find

- **[S/D]** `tests/gate_C0/test_jmax1_counts.py` (v0.6.1 §2.1 item 5) compares route 1's
  `enumerate_basis(1.0)` and route 2's `kernel_dimension(1.0)` against the table above. Route 2
  emits exactly one basis column per (js, ns) for which all four vertices admit a local singlet
  (`route_gausskernel.py:110–152`), and route 1 enumerates the same admissibility conditions
  vertex by vertex (`route_spinnet.py:234–312`); **[D]** both must therefore reproduce Z_1(x)
  identically, including the per-N breakdown, not merely the total 152. A route that returns
  152 with a different sector split is a route bug.
- **[S]** Route 2 builds only the *kernel dimension* at j_max = 1; `build_hamiltonian` raises
  `NotImplementedError` for j_max > 0.75 (`route_gausskernel.py:422–427`). The count row is
  therefore testable at C0; the j_max = 1 *Hamiltonian* agreement is V3 at C2 (v0.6.1 §4,
  priority 2), not a C0 row.
- **[S]** A mismatch fails the row, is written to `DISCREPANCIES.md`, and is not edited away
  (v0.6.1 §2.1 item 5 and §5).

---

## 2. Bootstrap-SE expectations for V10 (R = 5, multinomial observable variance)

### 2.1 The prescribed formula

**[S]** v0.6.1 §2.1 item 4 fixes the criterion as

  **SE = √( Var_s / (R · N̄_kept) ),  Var_s multinomial,  R = 5**,

adopted from the Fable amendment §3 via ruling R4 (v0.6.1 §0: bootstrap-SE, *not* per-repeat SD,
with multinomial variance). **[S]** v0.6.0 line 117 (V10) requires five repeats at r = 0 to
produce five distinct count dictionaries with bootstrap σ > 0 and ≈ the multinomial expectation;
v0.6.0 line 142 fixes "≈" as **within a factor 2**. **[S]** v0.6.1 §2.1 item 5 additionally
requires the pre-fix and post-override runs to be *distinct and within 2 × SE* for
"override harmless" to be recorded.

### 2.2 Definitions, made explicit for the twin's estimator

**[S]** `twin.observables()` (`twin.py:66–96`) decodes each kept bitstring to a label and
accumulates weights w = n/tot, i.e. every observable is a **self-normalised** average over the
post-selected sample. **[D]** Conditional on the number of kept shots, the kept sample is a
multinomial draw over the physical codewords with probabilities {p_k}. For a diagonal observable
O taking value o_k on codeword k, with Ō = Σ_k p_k o_k:

  **Var_s = Σ_k p_k (o_k − Ō)² = Σ_k p_k o_k² − Ō².**

Special cases used by the V10 rows **[D]**:

| observable | values o_k | Var_s |
|---|---|---|
| channel probability (`P_surv`, `P_meson`, `P_BBbar`, `P_other`, `P_stretched`, `P_short`) | {0, 1} | **P(1 − P)** |
| two-valued observable (`n_v3` ∈ {0, 2} at r = 0; `E2_l1` ∈ {0, 0.75}) | {o_lo, o_hi} | **(Δo)² p(1 − p)** |
| general `E2_l`, `n_v` | multi-valued | Σ p_k o_k² − Ō² |

**[D]** N̄_kept is the mean number of post-selected shots per repeat, i.e. `shots × yield` with
the yield returned by `postselect()` (`twin.py:60–63`). **[S]** In the v0.5.0 twin run
`REPEATS, SHOTS = 5, 4000` (`run_g4.py:125`), so R · N̄_kept = 20 000 × yield unless the C0
lane changes the shot count. **[D]** The fluctuation of N_kept itself enters a self-normalised
ratio only at second order, so the formula is exact to O(1/N) conditional on N̄_kept.

### 2.3 The predicted relation between the formula and what `twin.bootstrap()` returns

**[S]** `twin.bootstrap()` (`twin.py:152–169`) resamples the **R = 5 repeats** with replacement
`n_boot` times, averages, and returns `two_sigma = 2 × std(boot means, ddof=1)`.

**[D]** Two consequences that must be stated before the run, because they change the number the
test compares against:

1. The nonparametric bootstrap SE of a mean of n values equals σ̂₀/√n, where σ̂₀ is the
   ddof = 0 sample SD. Relative to the ddof = 1 standard error of the mean — which is what
   √(Var_s/(R·N̄_kept)) estimates — this is low by a factor **√((R−1)/R) = √(4/5) = 0.894**.
   Hence the preregistered expectation is

   **`two_sigma` ≈ 2 × 0.894 × SE = 1.79 × SE**, i.e. `two_sigma/2` ≈ 0.89 × √(Var_s/(5·N̄_kept)),

   with a further ≈ 1/√(2·n_boot) ≈ 4 % Monte-Carlo jitter at n_boot = 300 (`run_g4.py:132`).
   The 11 % deficit is expected and is **not** a failure; it is well inside the factor-2 band.
2. An SD estimated from R = 5 repeats has ν = 4 degrees of freedom, so its own relative
   scatter is ≈ 1/√(2ν) = **35 % (1σ)**; a 2σ excursion spans roughly 0.5×–1.7× the true SE.
   This is the quantitative reason the V10 criterion is a factor-2 band rather than a tight
   tolerance, and the reason ruling R4 prefers the bootstrap-SE over the raw per-repeat SD.

### 2.4 Preregistered numeric expectations

**[D, parametric — the only non-illustrative form]** For a channel probability P at yield y with
S shots per repeat and R = 5:

  SE = √( P(1−P) / (5 · y · S) );  worst case (P = ½) SE = 1/(2√(5yS)).

**[illustrative]** at S = 4000 and y = 0.8 (R·N̄_kept = 16 000):

| observable / regime | Var_s | SE | expected `two_sigma` (= 1.79 SE) |
|---|---:|---:|---:|
| P = 0.50 (worst case) | 0.2500 | 3.95e-3 | 7.1e-3 |
| P = 0.97 (r = 0 `P_surv`, see §3) | 0.0291 | 1.35e-3 | 2.4e-3 |
| `n_v3` ∈ {0,2}, p(2) = 0.03 | 0.1164 | 2.70e-3 | 4.8e-3 |
| `E2_l1` ∈ {0,0.75}, p(0.75) = 0.03 | 0.0164 | 1.01e-3 | 1.8e-3 |

These four rows are illustrations of the formula, not predictions of the twin's output: the
actual P and y depend on FakeTorino error rates, which appear in no source read here. **The
preregistered claim is the formula, the 1.79 factor, the factor-2 acceptance band, and the
degenerate cases identified in §3.3 — not the table entries.**

### 2.5 Degenerate cases the V10 row must handle

**[D]** Var_s = 0 whenever the kept sample is concentrated on codewords that share the
observable's value — in particular P ∈ {0, 1} exactly. The multinomial formula then predicts
SE = 0, and an observed bootstrap σ = 0 is *agreement*, not a failure of the twin. The V10
"σ > 0" clause must therefore be evaluated on an observable whose P is interior; §3.3 predicts
which observables those are at r = 0. Reporting σ = 0 on a structurally empty channel as
evidence of a deterministic twin would be a false positive for D-C0.

---

## 3. Which D-C0 case applies at r = 0 — and whether r = 1 is required

### 3.1 The rule

**[S]** `prompts/gi_cost_campaign_v.0.6.0.md:242`, verbatim: "**D-C0 Twin fix ambiguity.** If the
twin's five repeats are distinct after removing the `seed_simulator = 101` override but σ is
still zero at r = 0, the r = 0 circuit has no two-qubit gates and the readout-noise-only twin may
be deterministic under the noise model's readout-error implementation: test at r = 1 as well;
record which case applies."

**[S]** v0.6.1 §2.1 item 5 independently orders the lane: "pre-fix run first at r = 0 **and**
r = 1; 'override harmless' recorded if distinct and within 2× SE; negative control with all five
run-time seeds forced equal must fail; only on identical dictionaries locate the cause and fix."

### 3.2 What the r = 0 circuit and the seed plumbing actually are

**[S]** Facts, with citations:

- `synth_full_circuit(0)` returns `prep_stretched()` and nothing else
  (`synth_l12.py:271–275`); `prep_stretched()` applies **X gates only**, one per set bit of the
  encoded stretched codeword (`strang_l12.py:175–181`).
- The codeword is `l12.encode(((0, ½, ½, ½), (1, 1, 0, 2)))`. **[D]** Working it out from the L12
  layout (`l12.py:18–31`: qubits 3v, 3v+1 carry the two incident link spins as 0/1, qubit 3v+2 is
  set iff n_v = 2): bits {0, 4, 6, 7, 9, 10, 11} = **3793**, i.e. **7 X gates**, confirming the
  boot codeword check of v0.6.1 §2.1 item 1.
- The twin is `AerSimulator.from_backend(FakeTorino, seed_simulator=seed)` with `seed = 101` at
  construction (`twin.py:28–34`, `run_g4.py:122`) — this is the override V10 targets.
- The five repeats are five copies of one measured circuit, run with **distinct run-time seeds**
  `seed + k` for k = 0…4, i.e. 500…504 at r = 0 and 510…514 at r = 1
  (`twin.py:50–57`, `run_g4.py:131`). The transpile inside `run_counts` is at
  `optimization_level=0` on an already-ISA circuit with a fixed `seed_transpiler`.

**[D]** Consequences:

- D-C0's premise "the r = 0 circuit has no two-qubit gates" is **true**: an X-layer routed with a
  fixed initial layout requires no SWAPs, so the r = 0 ISA circuit is 1q-only.
- The twin is nevertheless *not* noiseless at r = 0: the backend noise model attaches 1q gate
  error and idle relaxation to the X layer and readout-assignment error to all 12 measurements,
  and Aer samples readout error **per shot**. The premise "the readout-noise-only twin may be
  deterministic" is predicted **false**.
- Whether the five dictionaries differ turns on precedence: a run-time `seed_simulator` passed to
  `sim.run(...)` is expected to override the backend option set at construction. That expectation
  is exactly what V10 tests; it is not asserted here as a fact.

### 3.3 Predicted structure of the r = 0 kept sample

**[D]** From `l12.is_physical` (`l12.py:53–69`: the two endpoint copies of every link must agree,
and no vertex may have unequal link bits together with a set matter bit), the physical neighbours
of code 3793 are:

| Hamming distance from 3793 | physical? | resulting label | channel |
|---|---|---|---|
| flip bit 8 (v3 matter) | yes | n = (1,1,2,2), q₃ = +2 | **P_BBbar** |
| flip bit 11 (v4 matter) | yes | n = (1,1,0,0), q₄ = −2 | **P_BBbar** |
| any single link-copy flip | no | — | discarded by post-selection |
| distance 3 (e.g. bits 7, 9, 11) | yes | n = (1,1,1,1) | P_meson |
| distance 4 (e.g. bits 0, 7, 9, 10) | yes | N = 4, mixed q | P_other |
| the only other q = (1,−1,0,0) codeword is the short string j = (½,0,0,0), code **2058** | yes | — | P_short (**distance 8**) |

Therefore **[D]**, at r = 0:

- `P_surv` = `P_stretched` is interior — slightly below 1, with the deficit dominated by the two
  distance-1 matter-bit errors → **Var_s > 0, σ > 0**. Same for `P_BBbar`, `n_v3` (0 vs 2 on the
  v3 flip) and `E2_l1` (0 vs 0.75 on link-flip survivors), which are precisely the three
  observables the twin row checks (`run_g4.py:135–136`).
- `P_short` (distance 8), `P_meson` (distance 3, ≲ 1 expected count in 4000 shots at percent-level
  error rates **[illustrative]**) and `P_other` (distance 4) are predicted to be **identically
  zero in all five repeats**, giving σ = 0 *for a structural reason predicted in advance by the
  multinomial formula itself* (§2.5) — not because the twin is deterministic.

### 3.4 The call

**Predicted case: D-C0 case A — the escalation clause does not fire at r = 0.** **[D]**

| branch | prediction | how it is recognised |
|---|---|---|
| five dictionaries **identical** | **not expected** | any two repeats equal as dicts ⇒ construction-time seed wins ⇒ §2.1 item 5's "identical dictionaries" branch: locate the cause and fix, then re-run |
| five dictionaries **distinct, σ > 0** on `P_surv`, `P_BBbar`, `n_v3`, `E2_l1` | **expected** | bootstrap `two_sigma`/2 within a factor 2 of √(Var_s/(5·N̄_kept)) (§2.3–2.4) ⇒ record **"override harmless"**, D-C0 not triggered |
| distinct but σ = 0 on `P_short`, `P_meson`, `P_other` | **expected, benign** | the multinomial prediction is *also* zero for these channels; record as structurally empty, **do not** invoke D-C0 |
| distinct but σ = 0 on an observable with interior predicted P | **not expected** | this alone triggers D-C0 ⇒ test at r = 1 and record the mechanism |

**Answer to "must D-C0 r = 0 use r = 1?"** **[D]** No — the r = 0 point is predicted to be
self-sufficient for the seed question, so D-C0's fallback to r = 1 is predicted not to be
required. But r = 1 is run regardless, for two independent reasons: **[S]** v0.6.1 §2.1 item 5
mandates the pre-fix run at both r = 0 and r = 1 irrespective of D-C0; and **[D]** r = 1 is the
only point at which the channels that are structurally empty at r = 0 (`P_meson`, `P_other`, and
`P_short`) acquire interior probabilities, so the "bootstrap σ ≈ multinomial expectation" half of
V10 (v0.6.0 line 117) can only be tested across all channels at r ≥ 1. Treat r = 1 as the
confirmatory point for the variance comparison, not as a D-C0 remedy.

**Negative control.** **[D]** With all five run-time seeds forced equal (and the transpile seed
already common across k), Aer is expected to return bit-identical dictionaries, so the control
run must fail the distinctness assertion. If the control *passes* — distinct dictionaries under
identical seeds — the twin has an unseeded stochastic path and the V10 row fails regardless of
the r = 0 result.

**What the ledger row must record**, per D-C0's "record which case applies" **[D]**: the case
letter from the table above, the mechanism (seed precedence, structural zero variance, or genuine
determinism), the observable each σ was evaluated on, `two_sigma/2`, the predicted SE with the
0.894 bootstrap factor applied, N̄_kept and yield, and the negative-control outcome.

---

## 4. Falsification summary (what makes each prediction wrong)

| # | prediction | falsified by |
|---|---|---|
| P1 | j_max = 1 sector counts (3, 36, 74, 36, 3), total 152, by both routes | either route returning a different total or a different split |
| P2 | j_max = ½ counts (2, 20, 38, 20, 2), total 82, from the *same* generating function | disagreement with `EXPECTED_SECTOR_DIMS` |
| P3 | all odd-N sectors empty at both truncations | any odd-N basis element |
| P4 | `two_sigma` ≈ 1.79 × √(Var_s/(5·N̄_kept)), inside the factor-2 V10 band | a ratio outside [0.5, 2] on an observable with interior P |
| P5 | at r = 0: five distinct dictionaries; σ > 0 on `P_surv`, `P_BBbar`, `n_v3`, `E2_l1`; σ = 0 on `P_short`, `P_meson`, `P_other` | identical dictionaries, or σ = 0 on the first group, or σ > 0 on `P_short` |
| P6 | D-C0 case A: the r = 1 escalation is not required by D-C0 (though r = 1 is run anyway) | any σ = 0 on an interior-P observable at r = 0 |

**Out of scope for this document:** the STATIC-112 and STATIC-2417 bridge counts and the 2×3
count 1,727 (v0.6.1 §4, priorities 3–4) are C2 rows; the static-charge convention is not fixed in
`conventions.py`, so no count is predicted here. The same transfer-matrix method extends to them
and will be used by the C2 auditor.
