# SU2ZX · GI-Cost Campaign · The measured price of exact gauge invariance

**Hermes prompt v0.6.0 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.0.md`**
**Supersedes the *objective* of `prompts/section8_overnight_v.0.5.0.md` (hereafter "v0.5.0"); inherits its machinery. Sources of truth for what changed: the v0.5.0 status review (7 Sept 2026) and the overlap analysis of the Sufian report "2+1D SU(2) Gauge Dynamics" (25 Aug 2026), both in the SU2QC Ideas project; copy both into `$REPO/docs/refs/` before the first session.**

**Launch (human, one line, from the SU2ZX repository root):** `hermes` then
`@prompts/gi_cost_campaign_v.0.6.0.md  Run phase 0. T0 is now.` — or, for any later session, `Run next phase.`
Everything below is addressed to you, the Hermes orchestrator session.

**How to read this file (orchestrator).** Sections 0–3 now, in full, every session. Section 4 one phase at a time. Sections 5–9 are reference (thresholds, decision rules, session protocol, tree, summary format). **Inherit unchanged from v0.5.0:** §5 (lanes, Hermes mechanics, two-stage review plus physics audit, independence rules), §9.3–9.5 (dry-run lints, submission and polling, provenance labels), §10.4–10.5 (re-plan, resume and watchdog), §13 D1–D2 and D6–D11 (decision rules), Appendix A (delegation templates), Appendix C (conventions). Where this file and v0.5.0 disagree, this file wins. Numbers marked "preliminary" tell you what to expect, not what to report.

---

## 0. What changed and why (read once per session)

v0.5.0 finished the science half and it stands: 82 gauge-invariant states at j_max = 1/2 by two independent routes agreeing at 10⁻¹⁵ (sectors 2, 20, 38, 20, 2; 152 at j_max = 1), exact gauge-invariant Strang circuits with zero noiseless leakage, the stretched-string codeword 3793 in the 12-qubit local encoding, the resonance μ* = 3/8 (m* = 3g²/16). The engineering half stopped at a structural gap: **2,156 two-qubit gates per Strang step before routing** (D = 16, h0–h3 = 248/248/239/241, B = 174; routed 3,976 on heavy-hex) against a 250 budget, an **8.6× logical gap that no synthesis trick closes**. The review also found that the primary endpoint could not pass as coded (r = 0: exact 1.000 versus twin 0.946, a 5.4 % device error judged against a 0.004 statistical error bar).

Meanwhile an independent report (Sufian, 25 Aug 2026) ran the same hard-core SU(2) Kogut–Susskind model on IBM Kingston at **13 native CZ** by projecting onto a state-adapted Krylov subspace (K = 6 or 8, three qubits) and synthesizing a generic unitary. That circuit is valid for one initial state at one time, needs the full classical solution to construct, and by the report's own §18.2 is not a scalable algorithm. Its model differs from ours by two static fundamental charges at opposite corners (one plaquette: 112 total / 54 half-filled; two plaquettes: 2,417 / 977; ours: 82 / 38 and 1,727 / —). Its coupling point is far into strong coupling (hopping and magnetic terms 0.02 of the electric term; ours 0.5 and 0.25).

The campaign's object is therefore no longer "first with-matter hardware time series". It is:

> **The measured price of exact gate-level gauge invariance.** On one Hamiltonian, one observable set and one device, compare an extensible gauge-invariant product-formula circuit (arm **GI**) with a validated state-adapted Krylov playback circuit (arm **KR**), and report cost, accuracy, gauge-error detectability and extensibility as measured quantities, at two coupling points.

The 8.6× gap is the headline number, not the failure. Every phase below either sharpens that number, makes the KR baseline strong enough that the comparison is fair, or turns a review finding into a passed test.

**Non-negotiables (v0.5.0 §0 rules 1–9 still hold; these are added).**

10. **Two arms or nothing.** No hardware submission of one arm without the other on the same backend, same qubit set where the qubit counts allow it, same calibration window, matched t = 0 controls, equal total shots per observable group. A one-arm result is EMULATED-only until the other arm exists.
11. **The KR baseline must be the best KR, not a strawman.** Its K-scan, synthesis search and layout search are preregistered with a budget at least equal to the Sufian report's (K-scan at every time point; exact and approximate synthesis; ≥ 3 optimization levels × ≥ 20 transpiler seeds × all operational Heron backends).
12. **Every session begins by rerunning every previous gate's tests.** A gate that stops passing halts the campaign until fixed (Section 7). Long tests may be cached by hash; the cache is invalidated by any change to the files the test reads.
13. **Never compare across coupling points, models or sources in one number.** Tables carry `point ∈ {P-A, P-S}`, `model ∈ {OURS-82, STATIC-112}`, `arm ∈ {GI, KR}`, `source ∈ {EXACT, NOISELESS, EMULATED, HARDWARE}` columns.

---

## 1. Hypotheses, endpoints, claim table (preregistered in Phase 1; verbatim into `PREREGISTRATION.md`)

### 1.1 Hypotheses

> **H-COST.** For the hard-core SU(2) single plaquette with four staggered two-color fermion sites (82 gauge-invariant states, 38 in the N = 4 sector), an exactly gauge-invariant second-order product-formula circuit in the 12-qubit local encoding costs, after routing to a Heron heavy-hex map, more than 10× the two-qubit gates of a state-adapted Krylov playback circuit validated to the same 10⁻³ full-space accuracy at the same time point and coupling point, at both coupling points P-A and P-S.

> **H-DETECT.** On hardware, the GI arm's leakage flags detect a nonzero gauge-violation rate that the KR arm cannot measure at all, and post-selection on those flags changes at least one primary observable by more than 2σ.

> **H-CROSS.** The Krylov dimension K needed for 10⁻³ accuracy grows with time and with system size (82 → 1,727 states) faster than the GI cost per step (fixed per step, linear in the number of links and plaquettes), so that a crossover time or size exists within exact reach at coupling point P-A, and either exists or is shown absent at P-S.

### 1.2 Endpoints (each is one table with the four columns of rule 13)

- **E1 Resource frontier (deterministic).** For each (point, arm, time point): qubits, logical two-qubit gates, routed CZ, two-qubit depth, state-preparation CZ, basis-change CZ, and the noiseless full-space accuracy the circuit was validated to (state infidelity, maximum observable error, process infidelity where defined, leakage). The cost ratio CZ_GI / CZ_KR per row.
- **E2 Hardware accuracy (restated from the review, option i).** For each arm, observable and time point: |HARDWARE_mitigated − NOISELESS_arm| ≤ 2σ_stat + δ_dev, where σ_stat is the bootstrap standard error over repetitions and time blocks and δ_dev = |TWIN − NOISELESS_arm| is the calibration-derived noisy-twin bias computed and frozen before submission. NOISELESS_arm − EXACT (Trotter bias for GI; Krylov truncation bias for KR) is tabulated beside every value and never subtracted. Both arms also go on one figure: absolute observable error versus routed CZ, same device, same day.
- **E3 Trend endpoint (option iii, robust to uniform depolarizing).** At each hardware time point, for each arm: the sign pattern ΔP_S3 < 0, ΔC_string < 0, Δ⟨N⟩ on the two intermediate vertices > 0, ΔP_baryonic > 0 holds at ≥ 2σ; and the ordering P_baryonic > P_meson holds at ≥ 2σ (preliminary: the one-plaquette ratio is about 11 at P-A).
- **E4 Gauge-error detectability.** GI arm: leakage-flag rate per circuit (HARDWARE), yield after post-selection, and the change in each primary observable from post-selection with its 2σ. KR arm: the entry is "not measurable: no gauge redundancy in the encoding", stated as a measured limitation, not omitted.
- **E5 Extensibility (deterministic, classical).** K_min(t) for 10⁻³ accuracy at 82 states and at 1,727 states (the 2×3 ladder), at both coupling points; GI logical two-qubit gates per step at one plaquette (measured) and at 2×3 (synthesized, not routed, from the term-group structure: 7 hopping groups, 2 plaquette groups, one diagonal layer); the crossover (t, size) where routed CZ_KR ≥ routed CZ_GI at r = 1, or a statement that none exists within exact reach; and the classical-dependence flag: KR requires exp(−iHt)|S3⟩ in the full space to construct Q_K, GI does not.

### 1.3 Claim table (copy into `CLAIM_TABLE.md` unchanged)

| Supported if the gates pass | Not supported by this campaign |
|---|---|
| A measured cost ratio between exactly gauge-invariant and Krylov-playback circuits for SU(2) with dynamical matter on a plaquette, at two coupling points, on one device | Any statement about string tension, a continuum limit, hadron phenomenology, or the 8×8 physics of Cataldi et al. |
| A hardware accuracy-versus-cost curve for both arms with a decomposed error budget (truncation, Trotter or Krylov, compile, device, shot) | A classically intractable calculation; every number has an exact reference |
| A hardware-measured gauge-violation rate and its effect under post-selection, and the statement that the playback arm cannot measure it | Quantum advantage, AI advantage, or the superiority of either arm in general |
| The Krylov-dimension growth with time and with size from 82 to 1,727 states, and the crossover or its absence within exact reach | Baryon blockade, the 2+1D claim (reserved for 2×3 and beyond on hardware), or any hardware result above one plaquette |
| The v0.5.0 Section 8 physics (channel structure, resonance, truncation error) as the shared reference of both arms | That the 8.6× gap is closable; only that it was not closed inside the preregistered synthesis budget |

---

## 2. The two arms, the two coupling points, the shared physics

### 2.1 Shared reference (from v0.5.0 §2, unchanged)

Hamiltonian v0.5.0 §2.1 in code units H/g_E with coefficients (electric, mass, hopping, magnetic) = (1, μ, 1/(2g_E), 1/(4g_E²)); conventions file `00_conventions.md` as frozen in the last v0.5.0 run (rule D2); gauge-invariant space and sector table v0.5.0 §2.2; named states, channel projectors and bare energies v0.5.0 §2.3; observables v0.5.0 §2.4; Trotter tolerance 0.05 (density) and 0.0375 (Casimir). Initial state S3 (stretched string, codeword 3793 in the 12-qubit encoding; verify it again at every session boot).

**Primary observables (both arms, identical operators, identical estimator):** the four site densities ⟨N_n⟩, the four link Casimirs ⟨j_ℓ(j_ℓ+1)⟩, P_S3, P_S1, P_pair, P_meson, P_baryonic (and its sub-projectors P_BB̄, P_antivac), P_vacmatter, the string-link Casimir average C_string over ℓ₁, ℓ₂, ℓ₃, the energy ⟨H⟩ where the settings allow it. For the KR arm every observable is O_K = Q_K† O Q_K, built from the exact-basis operator, never re-derived in the reduced space.

### 2.2 Coupling points (frozen in Phase 1)

| Point | electric : hopping : magnetic | μ | equivalent | time points | why |
|---|---|---|---|---|---|
| **P-A** | 1 : 0.5 : 0.25 | 3/8 | our g_E = 1 | the r ≤ 2 GI-admissible points of the v0.5.0 `window.json` (preliminary: t ∈ {0.75, 1.5}/g_E; add 2.25 if r = 2 passes there) | our regime; hopping comparable to bare gaps; Krylov space fills fast |
| **P-S** | 1 : 0.02 : 0.02 | 3/8 | the Sufian benchmark w = g_B = 1, g_E = 50, m = 18.75 rescaled to electric units | τ = t·g_E ∈ {5, 12.5} (Sufian's t = 0.10, 0.25) | their regime; perturbative in hopping; the regime where 13 CZ was possible |

P-S is **not** on our one-parameter family (hopping 1/(2g_E) and magnetic 1/(4g_E²) cannot both equal 0.02): the Hamiltonian builders must accept the four coefficients independently. Extend `H(gE, mu, jmax)` to `H(coeffs=(cE, cM, cH, cB), jmax)` with the old signature kept as a wrapper; re-run the v0.5.0 G1 agreement test on the new signature at both points (gate C2).

### 2.3 Arm GI (gauge-invariant, extensible) — the v0.5.0 circuits, REDUCED

The v0.5.0 Phase 3 circuits (strategy BU or HY, whichever passed G3 with leakage ≤ 10⁻¹²), 12-qubit local encoding with leakage flags, second-order Strang with gauge-invariant term grouping, each grouped factor an exact block unitary. **REDUCED scope (review N7):** r ∈ {1, 2} only; time points restricted to those where the Trotter tolerance holds at that r and the G2 visibility criterion still holds (the "surviving signal"). At P-S the Trotter error at r = 1 is expected to be small even at τ = 12.5 because the non-commuting terms are 0.02 of the electric term; verify, do not assume.

**One bounded synthesis sprint (Phase 4, ≤ 4 h wall clock, one session).** Target: reduce the per-step logical two-qubit count below 2,156 by exact, leak-free means only (the pair-structure multiplexed-rotation construction of v0.5.0 Phase 3 BU; first-order Lie–Trotter at r = 1 as a separate, labeled variant; reuse of the diagonal layer across steps; nothing that re-splits into Pauli strings). Whatever the count is when the box closes is the count. The review's verdict stands as the prior: no single hot spot (hoppings 976 versus plaquette 174), so expect at most a modest factor. Record the attempt and its result in `04_gi_arm/synthesis_sprint.md`; H-COST is judged on the best leak-free circuit that exists at the end of the sprint.

### 2.4 Arm KR (Krylov playback) — rebuilt from the Sufian method on our model

For each (point, time point): Lanczos/Arnoldi from |S3⟩ under H restricted to the N = 4 sector (38 states at j_max = 1/2); orthonormal Q_K; H_K = Q_K† H Q_K; U_K(t) = exp(−i H_K t); n_q = ⌈log₂ K⌉ qubits with unused codewords padded by the identity. Initial state = first Krylov vector = |0…0⟩, so state preparation is free. Circuits: (a) exact synthesis of U_K by Qiskit `UnitaryGate` + transpile; (b) approximate synthesis by a parameterized ansatz (line-connected, depth scanned) fitted to U_K, accepted only under the acceptance rules below. Observables O_K = Q_K† O Q_K measured by Pauli grouping on n_q qubits; report the number of measurement circuits.

**K-scan (mandatory, per point and time point):** the smallest K such that, over the whole interval [0, t] at 101 times, full-space state infidelity 1 − |⟨Ψ(t′)|Q_K Ψ_K(t′)⟩|² ≤ 10⁻³ and max over all primary observables |O_exact − O_K| ≤ 10⁻³, with gauge leakage identically zero (Q_K ⊂ H_phys by construction; assert it numerically ≤ 10⁻¹²). Report the full K(t) curve for K up to 38, not only the chosen K. Preliminary expectation: at P-S, K in the range 4–8 at τ ≤ 12.5 (the Sufian values on their model); at P-A, K substantially larger at t = 1.5/g_E (the v0.5.0 preliminary Krylov dimension from S3 was 28 of 38).

**Acceptance of a KR circuit for hardware (the Sufian criteria, adopted verbatim so the arms are judged the same way):** full-space state infidelity ≤ 10⁻³ against the exact 82-state evolution (not the reduced target); max observable error ≤ 10⁻³; process infidelity reported; probability in unused codewords ≤ 10⁻⁵ noiselessly; gauge leakage zero; ISA-compatible on the frozen backend. Layout search: all operational Heron backends × optimization levels {1, 2, 3} × 20 seeds, ranked by calibrated two-qubit error sum; record that the top ten share a structure if they do (the Sufian null result on layout search is expected to recur).

**What KR cannot do, stated as measured facts in E4 and E5:** no leakage flags (every computational state is physical); no reuse across time points (a new unitary per t); no constructibility without exp(−iHt)|S3⟩ in the full space.

### 2.5 Matched-experiment rules (both arms)

Same backend and calibration window; the KR qubits chosen inside the GI qubit path where the calibration ranking allows, otherwise the best-ranked connected triple and the reason recorded; matched t = 0 control circuits per arm (state preparation + measurement only) and reporting of ΔO(t) = ⟨O⟩_t − ⟨O⟩_0 beside absolute values (adopted from the Sufian protocol); independent readout calibration per arm per job; equal total shots per observable group (4,096 per group, 5 repetitions, shot allocation across groups by variance contribution allowed if the total is conserved); mitigation arms M0 (readout inversion only), M1 (readout + DD + Pauli twirling + ODR), M2 (M1 + linear ZNE at fold scales {1, 3}); quadratic ZNE is not run (the Sufian scale-5 result is cited as the reason); leakage post-selection for GI only, with pre- and post-selection values both reported; bootstrap 1,000 resamples over repetitions and time blocks, including the calibration counts.

---

## 3. Physics-based validation ladder (every gate is one or more of these; every test reads its threshold from `GATE_THRESHOLDS.yaml`)

| ID | Validation | Method | Threshold |
|---|---|---|---|
| V1 | v0.5.0 G1–G3 regression | rerun `tests/gate_G1..G3` from the last v0.5.0 run directory against the current package | all pass, values unchanged to 10⁻¹² |
| V2 | Four-coefficient Hamiltonian | route A and route B agree at P-A and P-S (spectra, aligned matrix elements, S3 observables over [0, 20]); wrapper reproduces the old H(gE, mu, jmax) exactly | 10⁻¹²; 10⁻¹²; 10⁻¹⁰ |
| V3 | j_max = 1 in both routes (review D1/N4) | route B extended to the 9-state link (3 qubits per link no longer suffice: 4 qubits or a direct 9-level register); 152 states; sectors 3, 36, 74, 36, 3; route A/B agreement at j_max = 1; the stale j_max = 1 test assertion corrected | exact counts; 10⁻¹² |
| V4 | Truncation error per observable (review N4) | j_max = 1 versus 1/2 at every hardware time point, both coupling points, every primary observable | reported; the statement "truncation error < device error bar" checked per observable |
| V5 | **Bridge to the Sufian model** | add static fundamental charges (B^a_v, spin-1/2 registers) at v0 and v2 to route B's Gauss law; count the kernel: 112 total, N-sectors 2, 27, 54, 27, 2; then 2×3 with charges at the two far corners: 2,417 total, sectors 4, 119, 597, 977, 597, 119, 4 | exact counts (independent of phase conventions) |
| V6 | Bridge, dynamics | on STATIC-112 at P-S from the lower minimal string (Sufian eq. 67), the K-scan reproduces K = 6 at τ = 12.5 with infidelity ≤ 10⁻³; on STATIC-2,417 from Sufian's index-630 string, K = 4 at τ = 5 and K = 8 at τ = 12.5 | K equal, or within ±2 with the joint phase convention recorded as the candidate cause; not a campaign blocker |
| V7 | 2×3 ladder exact reference (review N5, E5) | 1,727 states at j_max = 1/2 on OURS by both routes; exact dynamics from the stretched string; P_BB̄/P_meson at matched times versus the one-plaquette value; K_min(t) at both points | 10⁻¹² agreement; numbers reported |
| V8 | KR arm correctness | for every accepted KR circuit: full-space infidelity, max observable error, process infidelity, unused-codeword probability, leakage, all against EXACT on OURS-82 | 10⁻³; 10⁻³; reported; 10⁻⁵; 10⁻¹² |
| V9 | GI arm correctness (REDUCED) | grouped-factor unitary checks; Trotter exponent on the max-over-observables error; absolute Trotter error at r ∈ {1, 2} at the chosen points; noiseless leakage; compiled-versus-Strang equivalence; no pipeline with pre-route equivalence < 1 − 10⁻¹⁰ is hardware-eligible (retires `pyzx_basic_TP` unless fixed) | 10⁻¹⁰; [1.8, 2.2]; ≤ tolerance; ≤ 10⁻¹²; 10⁻¹⁰ |
| V10 | Twin variance (review N1) | five repeats of the calibration-derived Aer twin at r = 0 produce five distinct count dictionaries; bootstrap σ > 0 and ≈ the multinomial expectation; the `seed_simulator = 101` construction-time override removed or shown harmless | pass |
| V11 | Estimator | post-selected, readout-mitigated estimator on synthetic quasi-distributions with known answers including negative entries; matched-subtraction ΔO on synthetic data; channel closure re-reported after ODR | 10⁻¹⁰ on exact quantities |
| V12 | Endpoint pre-test | E2 and E3 evaluated on EMULATED data for both arms before any submission; δ_dev frozen per (arm, observable, t) | E2 passes on EMULATED at ≥ 2 time points per arm, else no submission |
| V13 | Independent audit | one row of every results table recomputed from raw exports by a fresh child with a different script | 10⁻¹⁰ (exact), bootstrap resolution (counts) |
| V14 | Replication | `su2qc.replicate` (review Tier 2) rebuilds every table and figure from `raw_immutable/`, exact references and saved noiseless/emulated outputs in a fresh venv; hashes match | all |

---

## 4. Campaign phases (one phase per session by default; Section 7 governs sessions)

| Phase | Object | Gate | Validations | Session budget |
|---|---|---|---|---|
| 0 | Repair and hygiene (review Tier 0 + Tier 2) | C0 | V1, V10, V11 | 4 h |
| 1 | Reframe and preregister | C1 | — (documents + thresholds) | 3 h |
| 2 | Reference extension: four coefficients, j_max = 1, bridge, 2×3 | C2 | V2–V7 | 8 h |
| 3 | Arm KR: K-scans, synthesis, layout search, both points | C3 | V8 | 8 h |
| 4 | Arm GI REDUCED: surviving signal, synthesis sprint, compile, frontier | C4 | V9, E1, E5 | 8 h |
| 5 | Matched design, twin, rehearsal, endpoint pre-test | C5 | V12 | 6 h |
| 6 | Hardware: dry run, pilot, full run, second calibration window | C6 | v0.5.0 lints; G8-style stop/go | 8 h + queue |
| 7 | Analysis, error budget, endpoints E1–E5, audit | C7 | V13 | 6 h |
| 8 | Paper, release, replication | C8 | V14 | 6 h |

### Phase 0 · Repair and hygiene (Tier 0 and Tier 2 of the review)

1. Boot per Section 7. Inventory the last v0.5.0 run directory; locate `GATE_LEDGER.jsonl`, `window.json`, `strang_table.md`, `resource_table.md`, `resources_synth.md`, `run_g4.py`, the twin module, `circuits/`, and the nine untracked Phase-4 paths named in the review. Commit the untracked paths (`git add`, message `campaign: commit phase-4 artifacts from v0.5.0`).
2. **N1, twin variance (V10).** Builder A0a: write `tests/gate_C0/test_twin_variance.py` — five `run_counts` repeats at r = 0 must return five distinct count dicts; bootstrap σ of a density must be within a factor 2 of the multinomial expectation; then locate and remove (or prove harmless) the construction-time `seed_simulator = 101` override. Reviewer B checks the test would have failed on the old code (run it against the pre-fix commit).
3. **N3, close G4 honestly.** Orchestrator: append to the v0.5.0 ledger an INFO row `G4: decision = REDUCED (campaign v0.6.0); gap = 2156/250 = 8.6x logical, 3976 routed` with evidence paths. GO is not available on the numbers; PLAN B is not taken because the campaign's object no longer needs a sub-250 circuit to be a result.
4. **Tier 2.** Ruff and mypy on `src/su2qc` (fix or explicitly ignore with a reason per finding; no blanket ignores); the stale j_max = 1 test assertion corrected against the 152/(3, 36, 74, 36, 3) counts; `pyzx_basic_TP` either fixed to pre-route equivalence ≥ 1 − 10⁻¹⁰ or retired with a ledger row; `su2qc.replicate` skeleton written (full implementation in Phase 8); V11 estimator test written against the existing estimator (`tests/gate_C0/test_estimator.py`), including matched subtraction.
5. **V1 regression.** Gatekeeper reruns v0.5.0 `tests/gate_G1`, `gate_G2`, `gate_G3` from a clean shell against the current package; writes rows.

**C0 exit:** V1, V10, V11 rows pass; Tier 2 items each have a ledger row (`done` or `retired`, with reason); repository clean (`git status` empty); `CAMPAIGN_STATE.json` advanced to phase 1.

### Phase 1 · Reframe and preregister

- **F1 Scribe:** `PREREGISTRATION.md` with Section 1 verbatim (hypotheses, E1–E5, claim table), Section 2.2 coupling points with the four coefficients written out at both points, Section 2.5 matched-experiment rules, the KR search budget (rule 11) and the GI synthesis-sprint box (2.3) as frozen budgets, the mitigation arms, the shot policy, the prespecified defect classes (v0.5.0 Phase 5 list plus: "KR K-scan changes after a Hamiltonian fix → rerun V8, new C3 row"), and empty slots for the frozen backend, qubit path, time points, δ_dev table and hashes (filled at C5). `CLAIM_TABLE.md`. `GATE_THRESHOLDS.yaml` from Section 5 verbatim; record its SHA-256.
- **F1b:** `docs/refs/README.md` listing the two reference documents and the Sufian numbers used by V5–V6 (Appendix A of this file), so that a fresh child can find them without this prompt.
- **Orchestrator:** decide `HARDWARE_MODE` provisionally (v0.5.0 §9.1); write the campaign todo list (one item per phase and per validation).

**C1 exit:** preregistration hash present; thresholds hash present; claim table present; nothing else. Short session by design.

### Phase 2 · Reference extension (V2–V7)

Dispatch in background waves (slots permitting):

- **A2a Route A, four coefficients + j_max = 1 (already supported per the review) + static-charge option + 2×3 geometry.** API: `H(coeffs, jmax, geometry='1x1'|'2x3', static_charges=None|'corners')`; basis labels extended with the geometry's link and vertex lists (Appendix C label format generalizes: link tuple then vertex tuple, in the geometry's frozen order written to `00_conventions.md`).
- **A2b Route B, the same API, independently.** j_max = 1 needs a 9-state link register (4 qubits, codes 9–15 unphysical) or a direct 9-level sparse register; static charges are an extra spin-1/2 register at the charged vertices entering G^a_v as +B^a_v; 2×3 is 6 vertices, 7 links. Route B at 2×3 without static charges is 7 links × 5 states × 4⁶ matter = 320,000 raw states; with j_max = 1/2 only. j_max = 1 at 2×3 is **not required** this campaign (rule D-C2).
- **C2 Physics auditor:** from the conventions file alone, independent generating-function counts for every (geometry, jmax, static) combination in the V5/V7 table; the 2×3 count 1,727 recomputed by a third method (spin-network enumeration); bare energies at both coupling points; the P-S resonance check 2m = ¾ g_E in the report's units mapped to μ = 3/8 in ours.
- **A2c Exact dynamics at 2×3 (V7):** stretched-string initial state along the long way round on the 2×3 ladder (define it in `00_conventions.md`: quark on an even corner, antiquark hole on the adjacent odd vertex, flux along the five-link path; the review's N5 geometry), expm/Krylov evolution in the N = 6 sector at both coupling points; P_BB̄/P_meson versus t; K_min(t) curves; figures.
- **A2d Truncation (V4):** j_max = 1 versus 1/2 at the hardware time points of both coupling points, every primary observable, on one plaquette.
- **A2e Bridge dynamics (V6):** K-scan on STATIC-112 and STATIC-2,417 at P-S from the Sufian initial strings; this child gets the Sufian initial-state definitions from Appendix A and nothing from the KR arm's code (Phase 3 has not started).

**Gate C2 (gatekeeper):** V2 (both points), V3, V5 (all four counts), V6 (recorded pass, near-pass or fail; never a blocker), V7 (1,727 by three methods; dynamics file present; K_min curves present), V4 table present. Failure loop as v0.5.0 G1 (diagnosis child, route-owner fix, 45-minute box); route disagreement after the box → C2 partial, campaign continues on the route that passes the counts, no hardware in Phase 6 until resolved (rule D7).

### Phase 3 · Arm KR (V8)

- **A3a Krylov reduction library** `src/su2qc/krylov/`: Lanczos with full reorthogonalization in the N = 4 (or N = 6) sector; Q_K, H_K, O_K; K-scan per Section 2.4 returning the full K(t) curve; unit tests against expm at K = full dimension (must be exact to 10⁻¹²) and against the V6 bridge values.
- **A3b Synthesis:** exact `UnitaryGate` route and approximate ansatz route for every (point, t, K) that the scan accepts; acceptance per Section 2.4 against EXACT on OURS-82; report logical two-qubit count, and after routing on the frozen-or-fake backend the CZ count and depth for every candidate; keep the rejected candidates in `03_kr_arm/rejected.jsonl` with the failing criterion (the Sufian report's practice of preserving negative results is adopted).
- **A3c Layout search** per rule 11; ranked table; the "top ten share a structure" observation recorded true or false.
- **C3 Auditor:** recompute one accepted K(t) point by a different Krylov implementation (Arnoldi from scratch, no reorthogonalization trick), check O_K = Q†OQ against a direct expectation-value comparison, verify zero leakage by projecting Q_K's columns with the Gauss-law projectors.

**Gate C3:** at least one accepted KR circuit per (point, hardware time point) with the V8 row; K(t) curves at both points on OURS-82 filed; the rejected list present; the layout table present. If at P-A no K ≤ 38 passes at some time point (it must at K = 38, which is exact), record the K and the qubit count; a KR circuit with K > 16 (5 qubits) is still an arm, just an expensive one, and that is a result.

### Phase 4 · Arm GI REDUCED (V9, E1, E5)

- **A4a Surviving signal (review N7):** at both coupling points, for r ∈ {1, 2}, the per-observable Trotter error at every candidate time point and the G2 visibility test; choose the GI time points (≥ 2 per point; preliminary at P-A: {0.75, 1.5}/g_E; at P-S: τ ∈ {5, 12.5} if r = 1 passes the tolerance, which it should).
- **A4b Synthesis sprint** (Section 2.3, 4-hour box, one builder plus one auditor for leakage and unitary checks; the orchestrator closes the box on the clock, not on progress). Deliver `04_gi_arm/synthesis_sprint.md` with the best leak-free per-step count and every variant tried.
- **A4c Compile:** K1 Qiskit level 3 and K2 PyZX topology-preserving on the frozen path (K3 only if it was hardware-eligible in v0.5.0); compiled-versus-Strang equivalence 10⁻¹⁰; resource rows per (point, r, t).
- **A4d E5 synthesis at 2×3:** term groups for the 2×3 ladder from route A's four-coefficient H (7 hopping groups, 2 plaquette groups, diagonal layer); the same block-unitary construction, logical two-qubit count per step, **not routed, not run**.
- **C4 Auditor:** V9 items; the E1 table assembled with the four columns of rule 13; the E5 crossover computed from the C3 K(t) curves and the C4 counts, both plaquette and 2×3.

**Gate C4:** V9 rows; `E1_resource_frontier.md` complete for both arms at both points (NOISELESS accuracy columns filled); `E5_extensibility.md` with K(t, size) curves, GI counts at both sizes, the crossover statement, and the classical-dependence flag; the sprint closed on time with its number. **Decision row:** `GI hardware circuits = <routed CZ, depth> at (point, r, t)`. There is no Plan B in this campaign: a GI circuit that is too deep for a nonzero hardware signal is still submitted once (pilot), because a measured null at a stated depth is the price being measured (rule D-C4).

### Phase 5 · Matched design, twin, rehearsal, endpoint pre-test (V12)

- **A5a Measurement plan** per arm: GI diagonal setting plus the energy settings of v0.5.0 Phase 5 if the per-circuit budget permits (they may be dropped by the fit-to-cap rung; E2 needs only the diagonal setting); KR Pauli groups on n_q qubits; the matched t = 0 control per arm; the number of circuits and the QPU estimate for pilot + full + second window, both arms, three mitigation arms.
- **A5b Twin:** calibration-derived Aer twin (from the frozen backend snapshot) for every hardware circuit of both arms; δ_dev per (arm, observable, t) written to `05_design/delta_dev.json` and frozen into the preregistration; V10 rerun on the actual twin.
- **A5c Rehearsal (detached):** full pipeline on the twin for both arms, all three mitigation arms, EMULATED labels; E2 and E3 evaluated on EMULATED; V11 rerun on the real estimator code path.
- **Fit-to-cap rung (v0.5.0 §9.3 order, applied to both arms symmetrically; never drop one arm's repetitions below the other's).**
- **F5 Preregistration completed:** backend, qubit path (GI 12 + KR n_q, with the overlap rule of 2.5), time points, δ_dev table, shot allocation, hashes; signed.

**Gate C5:** V12 (E2 passes on EMULATED at ≥ 2 time points per arm; E3 sign pattern on EMULATED per arm reported); δ_dev frozen; preregistration hash; QPU estimate inside the cap and the approval file.

### Phase 6 · Hardware

Inherit v0.5.0 Phases 7–10 and §9 verbatim with these substitutions: "pilot" = both arms' t = 0 controls plus one time point per arm, M1 only, 3 × 2,048 shots; stop/go review checks per arm (GI: S3 codeword 3793 recovered above the readout floor, flags mostly zero, yield; KR: |0…0⟩ recovered, unused-codeword population at the readout floor); "full run" = both arms, all time points, all three mitigation arms (M2 dropped first by the rung), 5 × 4,096; "second calibration window" = the full run's diagonal setting repeated for both arms ≥ 24 h later (Sufian §18.4 item 2 adopted: replicate on a second calibration date), and a second backend if the cap allows. Submission blockers: v0.5.0 D7 plus rule 10 (both arms or nothing).

**Gate C6:** pilot PASS per arm (HARDWARE rows); full run returned and immutably exported; second window returned or its job IDs listed with the one-line analysis command.

### Phase 7 · Analysis (E1–E5, V13)

`07_analysis/`: `E1_resource_frontier.md` (final, with HARDWARE accuracy columns added); `E2_accuracy_table.md` per arm, observable, t, mitigation arm, with NOISELESS_arm − EXACT beside, pass/fail per row, and the accuracy-versus-routed-CZ figure with both arms and both calibration windows; `E3_trend_table.md`; `E4_gauge_detectability.md` (flag rates, yields, pre/post-selection deltas with 2σ; the KR "not measurable" row); `E5_extensibility.md` (final); `error_budget.md` per arm (truncation from V4; Trotter or Krylov from NOISELESS − EXACT; compile from compiled − Strang/unitary; device from EMULATED − NOISELESS and HARDWARE − EMULATED; shot from bootstrap); `drift.md` (window 1 versus window 2 per arm). **C7 auditor** recomputes one row of every table from `raw_immutable/` by an independent script (V13).

**Gate C7:** every table with the four columns of rule 13 and provenance; V13 rows; the three hypotheses each marked supported / refuted / not tested with the deciding numbers.

### Phase 8 · Paper, release, replication (V14)

- `08_release/PAPER_DRAFT.md`: title (working: *The price of exact gauge invariance: gauge-invariant versus Krylov-playback circuits for SU(2) with dynamical matter on a quantum processor*); abstract stating the cost ratio, the accuracy-versus-cost result, the gauge-detectability result, the K(t, size) growth and the crossover; methods (both arms, both points, the bridge to the static-charge model as the cross-validation against the Sufian report); results by E1–E5; the claim table with each row marked; limitations (one plaquette; two coupling points; single device family; the sprint box; what a 2×3 hardware run would add); data and code availability. The Sufian report is cited as the source of the KR method and of the negative ZNE and layout-search results; its 13-CZ number is quoted as its own, never as ours.
- `08_release/LIMITATIONS.md`, `CONTINUATION.md` (2×3 GI on Nighthawk-class hardware as the next step; Idea 2 syndromes on the redundant encoding as the natural follow-on of E4).
- `su2qc.replicate` completed; `replication_log.md` (fresh venv, `make reproduce`, hashes match).
- `CAMPAIGN_SUMMARY.md` (Section 9) and the memory pointer set to `complete`.

**Gate C8:** V14; paper draft, limitations, continuation, replication log present; every gate row of the campaign has an evidence path.

---

## 5. Gate thresholds (frozen at C1 into `GATE_THRESHOLDS.yaml`; never loosened)

| Gate | Criteria | Thresholds |
|---|---|---|
| C0 | V1 regression; V10 twin variance; V11 estimator; Tier 2 rows; clean repo | unchanged to 10⁻¹²; distinct counts and σ within 2× multinomial; 10⁻¹⁰; present; `git status` empty |
| C1 | preregistration, claim table, thresholds file with hashes | present |
| C2 | V2 at P-A and P-S; V3 counts 152/(3,36,74,36,3); V5 counts 112/(2,27,54,27,2) and 2,417/(4,119,597,977,597,119,4); V7 count 1,727 by three methods and route agreement; V4 table; V6 recorded | 10⁻¹²/10⁻¹⁰; exact; exact; 10⁻¹²; present; pass/near/fail (never blocking) |
| C3 | V8 per accepted KR circuit; K(t) curves both points; rejected list; layout table | infidelity ≤ 10⁻³, obs error ≤ 10⁻³, unused-codeword ≤ 10⁻⁵, leakage ≤ 10⁻¹²; present |
| C4 | V9; E1 draft; E5 draft; sprint closed ≤ 4 h; decision row | unitary 10⁻¹⁰; exponent [1.8, 2.2]; Trotter ≤ 0.05/0.0375; leakage ≤ 10⁻¹²; equivalence 10⁻¹⁰; present |
| C5 | V12; δ_dev frozen; preregistration signed; QPU estimate in cap | E2 on EMULATED at ≥ 2 t per arm; present; hash; ≤ cap |
| C6 | pilot PASS per arm (HARDWARE); full run exported; second window returned or listed | per-arm stop/go; hashes; present |
| C7 | tables complete with rule-13 columns; V13; hypotheses marked | present; 10⁻¹⁰ / bootstrap; present |
| C8 | V14; paper, limitations, continuation, replication log | hashes match; present |

Ledger row format, `source` values, and the rule that only the gatekeeper writes `pass` are inherited from v0.5.0 §7.

---

## 6. Decision rules added to v0.5.0 §13 (apply, log the rule number, never ask)

- **D-C0 Twin fix ambiguity.** If the twin's five repeats are distinct after removing the `seed_simulator = 101` override but σ is still zero at r = 0, the r = 0 circuit has no two-qubit gates and the readout-noise-only twin may be deterministic under the noise model's readout-error implementation: test at r = 1 as well; record which case applies.
- **D-C2 Scope of j_max = 1.** One plaquette only; 2×3 at j_max = 1 is out of scope; a request for it in any child summary is ignored and logged.
- **D-C3 KR arm at P-A too large.** If the smallest passing K at a P-A time point exceeds 32 (6 qubits) the arm is still built and costed; the E5 crossover statement uses it; hardware submission of that circuit follows the same rules as any other (it is unlikely to be cheaper than GI, which is the finding).
- **D-C4 GI arm too deep for signal.** Submit the pilot anyway (one time point, M1). If the pilot's t = 0 control recovers 3793 above the floor but the t > 0 observables are consistent with the fully mixed state within 2σ, the full run of the GI arm is reduced to the shortest time point at r = 1 and the null is reported as the measured price with its depth; the KR full run proceeds in full.
- **D-C5 Cap too small for both arms.** Apply the fit-to-cap rung symmetrically; if even the last rung does not fit both arms, submit neither (rule 10), report EMULATED for both, and leave the ready command.
- **D-C6 Second backend unavailable.** The second calibration window on the same backend ≥ 24 h later satisfies the replication requirement; a second backend is optional.
- **D-C7 Sufian bridge fails (V6 outside ±2).** Not a blocker; list the joint phase convention and the initial-state definition as candidate causes; the KR arm on OURS-82 is validated by V8 against our own exact reference regardless.
- **D-C8 Review item without a stated method (N6, W̄ estimator).** Time-box 1 h in Phase 2; if unresolved, report μ* by the bare crossing and the two v0.5.0 dynamical estimators only, and mark N6 `retired` with the reason.

---

## 7. Session protocol (how the campaign proceeds step by step)

`CAMPAIGN_STATE.json` in `$REPO/runs/campaign_v060/` holds: `phase`, `gates` (id → pass/fail/partial, utc, evidence), `hashes` (thresholds, preregistration, conventions), `sessions` (list of tag, t0, phase, outcome), `hardware` (mode, backend, job IDs), `next_action`.

**Every session, in order:**

1. **Boot (≤ 20 min).** Record T0 and the session tag `c060_p<phase>_<YYYYMMDD>[_n]`. Read `CAMPAIGN_STATE.json`; a launch message "Run phase n" must match `phase` or be n = phase (a mismatch is logged and the file wins). Verify the three hashes against the files. Environment probe as v0.5.0 Phase 0 step 2. Create the watchdog and `RESUME_LOCK` (v0.5.0 §10.5). Reload skills if any.
2. **Regression (rule 12).** Gatekeeper reruns every previous gate's test directories (`tests/gate_C0..C<phase−1>` and, from C0 on, the v0.5.0 G1–G3 tests) from a clean shell; cached long tests are accepted only if the hash of every file they read is unchanged. Any failure halts the phase: the session becomes a repair session for that gate (time box 2 h), and if unrepaired it stops with the failure as the summary's first line.
3. **Phase work** per Section 4, with the v0.5.0 operating model: background waves, two-stage review, physics audit, hourly `PHYSICS_STATUS.md` (the P-list for this campaign is E1–E5 plus V-items of the phase), 30-minute checkpoints, `wait_for_done.sh` loop, no early turn end before the gate or the session cutoff.
4. **Gate.** Gatekeeper child; rows appended; `CAMPAIGN_STATE.json` updated; commit `campaign: C<k> <pass|fail|partial> <one line>`.
5. **Stop or continue.** Default `STOP_AT: phase`: write `SESSION_SUMMARY.md` (Section 9), update memory, delete the watchdog, end the session. With `AUTOPILOT: true` in `CONFIG.resolved.yaml`, continue to the next phase inside the same session while the session cutoff (default 12 h, hard) allows; Phase 6 always stops after submission so a human sees the job IDs.

Session budgets in Section 4 are targets; the hard session cutoff is 12 h. A phase not gated by its budget continues in the next session from its artifacts; a phase not gated after two sessions triggers the re-plan protocol (v0.5.0 §10.4) with the scope-cut ladder below.

**Scope-cut ladder for this campaign (in order; never loosen a threshold; never drop an arm, a coupling point, the bridge counts V5, or the regression step):** drop M2 (ZNE) → drop the energy settings → drop the second backend (keep the second window) → drop V6 bridge dynamics (keep V5 counts) → reduce the KR layout search to one backend × 3 levels × 20 seeds → reduce 2×3 dynamics to one coupling point (P-A) → reduce hardware time points to one per point per arm → run replication in the existing environment and say so.

---

## 8. Deliverables tree (`$REPO/runs/campaign_v060/`)

```
CAMPAIGN_STATE.json  CONFIG.resolved.yaml  GATE_THRESHOLDS.yaml  GATE_LEDGER.jsonl  PREREGISTRATION.md  CLAIM_TABLE.md
00_conventions.md (copied from the last v0.5.0 run, extended for 2x3 and static charges)
sessions/<tag>/  ENV.md  RUN_LOG.md  TIME_LEDGER.md  PHYSICS_STATUS.md  SESSION_SUMMARY.md  RESUME_LOCK
00_repair/       twin_fix.md  tier2_ledger.md
02_reference/    route_A/ route_B/ agreement_{PA,PS}.json  jmax1/  bridge/{static112,static2417}/  ladder_2x3/{counts,dynamics,kmin}/  truncation_{PA,PS}.json
03_kr_arm/       kscan_{PA,PS}.json  circuits/  rejected.jsonl  layout_search.md  validation_V8.jsonl
04_gi_arm/       surviving_signal.md  synthesis_sprint.md  circuits/  compile/{K1,K2}/  E1_resource_frontier.md  E5_extensibility.md  ladder_2x3_counts.md
05_design/       measurement_plan.md  delta_dev.json  twin/  rehearsal_EMULATED/  fit_to_cap.md
06_hardware/     backend_snapshot_*.json  dryrun/  pilot/  full/  second_window/  raw_immutable/  jobs.log  poll_jobs.py
07_analysis/     E1..E5 tables  error_budget.md  drift.md  figures/  audit/
08_release/      PAPER_DRAFT.md  LIMITATIONS.md  CONTINUATION.md  replication_log.md  requirements.lock  Makefile
tests/           gate_C0 ... gate_C8  (one directory per gate; one command each; thresholds read from GATE_THRESHOLDS.yaml)
docs/refs/       (repo-level) v050_review_20260907.md  sufian_overlap_20260907.md  README.md
```

Reusable code goes into `src/su2qc/` (`hamiltonian/` with the four-coefficient API, `krylov/`, `circuits/`, `analysis/`, `replicate.py`) with tests; the run directory holds configurations, results and logs.

---

## 9. Session summary (`SESSION_SUMMARY.md`, under one page) and campaign summary

1. One sentence: what this session established, or the first failing regression if rule 12 fired.
2. Phase gate row(s): pass/fail/partial with the deciding numbers and evidence paths.
3. Validation table: each V-item of the phase with its value, threshold, source.
4. Headline numbers so far: the per-step GI count (logical, routed), the best KR count per (point, t), the current cost ratio, K(t) at both points, the E5 crossover if computed, δ_dev if frozen, hardware job IDs if any.
5. What the next session will do first (the `next_action` field, verbatim).
6. Anything the human must know before trusting a number.

`CAMPAIGN_SUMMARY.md` (Phase 8) is the same six items over the whole campaign, plus the three hypotheses with verdicts and the claim table with every row marked.

---

## Appendix A · Reference numbers from the Sufian report used by V5–V6 (do not treat as our results)

Model: KS SU(2), hard-core j_max = 1/2, staggered two-color fermions, two static fundamental (j_b = 1/2) background charges entering Gauss's law as +B^a_v. Couplings in the report's units: H_E = g_E Σ E², w = g_B = 1, g_E = 50, m = 18.75 (2m = ¾ g_E). One plaquette: static charges at v0 (bottom-left) and v2 (top-right); staggered vacuum occupations (n0, n1, n2, n3) = (0, 2, 0, 2); minimal strings (j0, j1, j2, j3) = (½, ½, 0, 0) lower and (0, 0, ½, ½) upper; dimensions by N = 0, 2, 4, 6, 8: 2, 27, 54, 27, 2 (total 112); K = 16 accepted over 0 ≤ t ≤ 5, K = 6 at t = 0.25. Two adjacent plaquettes: 6 sites, 7 links, static charges at v0 and v5; dimensions by N = 0…12: 4, 119, 597, 977, 597, 119, 4 (total 2,417); three shortest three-link strings (indices 630, 426, 127 in the report's basis; 630 is the initial state); fixed-window K = 128 for 0 ≤ t ≤ 5; time-adapted K = 4 at t = 0.10 (2 qubits, 3 CZ) and K = 8 at t = 0.25 (3 qubits, 27 CZ exact / 13 CZ approximate). Acceptance: 1 − F ≤ 10⁻³, max observable error ≤ 10⁻³. Hardware: IBM Kingston qubits {82, 83, 96}; mitigation finding: scale 1 for five observables, linear ZNE for endpoint screening only, quadratic ZNE rejected; matched-error reduction 35.3 % (one plaquette) and 48.6 % (two plaquettes) from 27 → 13 CZ. Report time t = 0.25 at g_E = 50 corresponds to τ = t·g_E = 12.5 in our electric units; t = 0.10 to τ = 5.

## Appendix B · References the paper must cite

The v0.5.0 Appendix D list, plus: Sufian, *2+1D SU(2) Gauge Dynamics*, working research-group report, 25 Aug 2026 (the KR method, the static-charge model, the mitigation and layout-search negative results); the SU2QC v0.5.0 status review (7 Sept 2026); the overlap analysis (7 Sept 2026).

---

**Start now.** Record T0, read `CAMPAIGN_STATE.json` (create it at phase 0 if absent), run the regression step, then the phase. The campaign is judged on E1–E5, on the honesty of the ledger, and on whether a physicist can rebuild every number from the tree.
