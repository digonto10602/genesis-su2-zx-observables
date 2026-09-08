# Overlap analysis: Sufian "2+1D SU(2) Gauge Dynamics" (25 Aug 2026) versus SU2QC / SU2ZX v0.5.0

Prepared 7 September 2026. Compared: the 66-page working research-group report by Raza Sufian (`SU2_in_2_1D.pdf`, dated 25 August 2026) against the SU2QC Nine-Month Plan (7 Sept 2026), the v0.5.0 status review (7 Sept 2026), and the Section 8 overnight Hermes prompt v0.5.0. Numbers attributed to the report are quoted from it; numbers attributed to "ours" are from the v0.5.0 review's hand-verified values.

## Verdict in one paragraph

The report is the same physical model, the same regulator, the same resonance point, the same target paper and nearly the same observable list as Idea 1 / the rebuilt one-month project, but it takes the opposite route to hardware (a classically constructed, state-adapted Krylov playback circuit rather than an extensible gauge-invariant product formula), it adds two static background charges that change the Hilbert space, and it has already run on IBM hardware. It removes the "first with-matter hardware time series at one or two plaquettes" claim from the table. It does not touch the gauge-invariant circuit construction, the leakage-flag encoding, the 8.6× cost result, Gauss-law syndromes (Idea 2), tensor-network embedding (Idea 3), Gauge-JEPA, ladders beyond two plaquettes, or the j_max = 1 truncation study.

## What is the same

**Physics object.** Kogut–Susskind SU(2) in 2+1D with two-color staggered fermions, hard-core truncation j ∈ {0, ½}, five-state link |j, m_L, m_R⟩, E² = j(j+1), the four-term split (hopping, mass, electric, magnetic). The report's link transporter is the projected multiplication operator (non-unitary after projection, stated as a regulator artifact), which is the same construction as our route B.

**Resonance.** The report's benchmark couplings w = g_B = 1, g_E = 50, m = 18.75 satisfy 2m = ¾ g_E, i.e. m = 3g_E/8, which is our μ* = 3/8 (m* = 3g²/16 in the proposal's normalization), verified by hand in the v0.5.0 review.

**Geometry ladder.** One plaquette (4 sites, 4 links) → two adjacent plaquettes (6 sites, 7 links). The second is our 2×3 ladder.

**Target paper and framing.** Cataldi–Orlando–Halimeh arXiv:2509.08868; both documents describe their result as a local early-time precursor of string breaking, not a reproduction of the 8×8 tree-tensor-network curves.

**Observables.** Initial-string probability, shortest-string-manifold probability, electric Casimir (per link and patch average), meson-like single-occupancy density, baryon-pair double-occupancy density, with the expected sign pattern ΔP_init < 0, ΔP_str < 0, ΔC < 0, Δp_mes > 0, Δp_bar > 0 stated explicitly. These are our channel projectors and Casimir/density observables.

**Verification culture.** Two independent dimension counts (local Gauss-kernel diagonalization versus Clebsch–Gordan fusion-path propagation) agreeing exactly; Hermiticity and physical-subspace closure residuals at 10⁻¹⁵ and 10⁻²⁹; gauge leakage treated as a measured quantity; hard 10⁻³ acceptance thresholds on state infidelity and observable error; an explicit "supported / not supported" claim list; immutable hardware records with job IDs and hashes; a section on auditing versus asserting. Same discipline as our G1–G3 and gate ledger.

**AI framing.** "AI-assisted, physics-constrained quantum-circuit co-design and validation" with explicit refusal of "AI advantage", "AI invented an algorithm", or "AI outperforms physicists" — the same wording constraint the Nine-Month Plan imposes. The report also lists the evidence a future AI-advantage claim would need (human baseline, compiler-only baseline, scripted search, ablations without physics constraints or hardware feedback).

**ZX negative result.** PyZX rewrites preserved the circuit but did not lower entangling cost (§12.4 item 3). This matches the monograph's finding and the v0.5.0 `pyzx_basic_TP` problem.

**Hardware class and protocol elements.** IBM Heron (Kingston); matched t = 0 control circuits and reporting of ΔO = O(t) − O(0); linear readout inversion with reported quasiprobability artifacts; ZNE by odd local CZ folding at scales {1, 3, 5}; bootstrap over physics and calibration counts.

## What is different

### 1. Static charges: the Hilbert spaces are not the same

The report places two static fundamental (j_b = ½) charges at opposite corners (v0, v2 for one plaquette; v0, v5 for two) entering Gauss's law as fixed background sources. That changes the gauge-invariant counts:

| Quantity | ours (no static charges) | report (static charges) |
|---|---|---|
| 1 plaquette, all N | 82 | 112 |
| 1 plaquette, half-filled (N = 4) | 38 | 54 (6 qubits) |
| 1 plaquette, by N = 0, 2, 4, 6, 8 | 2, 20, 38, 20, 2 | 2, 27, 54, 27, 2 |
| 2×3, all N | 1,727 | 2,417 |
| 2×3, half-filled (N = 6) | — (not yet computed) | 977 (10 qubits) |
| 2×3, by N = 0 … 12 | — | 4, 119, 597, 977, 597, 119, 4 |

Consequences: the report's sixth observable, endpoint screening (a projector onto the singlet of dynamical matter with the static charge at an endpoint), has no analogue in our model; our string-shortening channel (three-link path → one-link path between a dynamical quark and antiquark on adjacent vertices) is not the report's object, whose minimal strings are the two two-link paths between opposite corners.

### 2. The route to hardware is the opposite of ours

| | ours (v0.5.0) | report |
|---|---|---|
| Circuit | second-order Strang with gauge-invariant term grouping; each grouped factor an exact block unitary on the physical subspace | state-adapted Krylov projection K = 4/8/16 (2/3/4 qubits); generic unitary synthesis of exp(−iH_K t) |
| Gauge invariance | exact at gate level; noiseless leakage ≤ 10⁻¹²; leakage flags readable on hardware | exact by construction (K ⊂ H_phys) but no redundancy: gauge errors on hardware are invisible |
| Validity | one circuit family for all t; reusable; extensible | valid for one initial state at one time; new unitary per t; requires the full classical solution to construct Q_K |
| Qubits | 12 (local gauge-invariant encoding) | 2–3 for the hardware circuits |
| Cost | 2,156 logical two-qubit gates per step (D = 16, h0–h3 = 248/248/239/241, B = 174); routed 3,976; 8.6× over the 250 budget | 27 CZ exact / 13 CZ approximate at t = 0.25; 3 CZ at t = 0.10 |
| Scalability | the point of the construction | "not by itself a scalable quantum algorithm" (§2, §18.2) |

### 3. It ran

IBM Kingston, physical qubits {82, 83, 96}, t = 0.10 and 0.25 (in the report's units, g_E = 50), about 440 quantum seconds over five staged jobs plus three final matched jobs, all with job IDs. Matched 27-CZ baseline versus AI-selected 13-CZ: mean absolute observable error down 35.3 % (one plaquette, 9 of 9 observables improved) and 48.6 % (two plaquettes, 5 of 6). The patch-averaged Casimir change on two plaquettes was not resolved after compression. p_bar detected at only 1.90σ in the Stage-2 experiment.

### 4. It has already answered three of our open questions

- **Mitigation policy (our A0/A1/A2 arm question):** scale 1 for five observables, linear ZNE only for endpoint screening, quadratic ZNE rejected on real-device evidence after a scales-1, 3, 5 experiment; calibration-derived Aer had predicted broad ZNE benefit and was wrong.
- **Formulation comparison (our month-2 item):** an isolated-plaquette LSH recoupling is spectrally equivalent to the hard-core KS model and gives no circuit advantage after Krylov reduction; a six-state two-rishon QLM needs a 56-dimensional reduced model (6 qubits, 1,783 all-to-all CX, ≈ 2,971 device entanglers) and was rejected; a binary-tetrahedral discrete-group candidate was not Hamiltonian-matched.
- **Baryon channel (our N5):** their p_bar is a weak detection; their exact two-plaquette data could be used to test whether BB̄ dominance (≈ 11 : 1 on our one plaquette) is geometric.

### 5. Coupling regime

The report's point is deep in strong coupling: in electric units the four coefficients are (electric, hopping, magnetic, mass) = (1, 0.02, 0.02, 0.375). Ours at g_E = 1 are (1, 0.5, 0.25, 0.375). Their time t = 0.25 at g_E = 50 is τ = t·g_E = 12.5 in electric units but only 0.25 in hopping units, which is why a Krylov space of dimension 6–8 suffices. At our coupling the Krylov dimension reached from S3 is about 28 of 38 (v0.5.0 preliminary), so the same method would need far more qubits and gates. Their coupling point is not on our one-parameter family (hopping 1/(2g_E) and magnetic 1/(4g_E²) cannot both be 0.02).

### 6. What the report does not touch

Gauss-law syndromes and closed-loop control (Idea 2) — and its basis has no redundancy, so it cannot host that study, the same objection the plan raised against the monograph's gauge-reduced chain; tensor networks and hybrid embedding (Idea 3); Gauge-JEPA; ladders beyond two plaquettes; j_max = 1 truncation error; baryon blockade; any coupling scan.

### 7. Naming

The report is titled "2+1D" while its §15 concedes one or two isolated plaquettes. The Nine-Month Plan reserves "2+1D" for 2×3 and beyond, where an interior vertex exists. This should be reconciled before either document circulates.

## Collision risks

The report's §18.4 next milestones are: (1) freeze the present data as the Phase-I benchmark; (2) repeat on a second backend/calibration date; (3) three or four plaquettes only after repeating the dimension, sparsity and adaptive-K searches; (4) KS versus LSH on a coordination-four geometry; (5) an AI ablation study with fixed search budgets (human baseline, compiler-only, physics-reduction search, measurement search, full co-design); (6) a reference-free mitigation-selection rule using consistency, conserved quantities and held-out times. Items 5 and 6 are Idea 2's controlled study and its "verification by invariants beyond exact reach" in different words. If the report's author is a collaborator, this is a scope-coordination matter for the advisor before either document goes out; if not, it is a competitor in the Idea 2 direction.

## State of the report

It is a draft under review: live editorial notes remain in the text ("check angle of RZZ gate-KYU", "T-gate count…check", "each link 3—explain why all 3 not required", the red explanatory paragraph under Fig. 4 answering a reviewer's question about identical depths for one and two plaquettes). It should not be treated as a frozen result.

## Reference numbers for cross-validation (from the report; for our V5–V6 bridge tests)

Static-charge model at the report's coupling point (w = g_B = 1, g_E = 50, m = 18.75). One plaquette: staggered vacuum (n0, n1, n2, n3) = (0, 2, 0, 2); minimal strings (j0, j1, j2, j3) = (½, ½, 0, 0) and (0, 0, ½, ½); K = 16 accepted on 0 ≤ t ≤ 5 (max trajectory infidelity 6.91 × 10⁻⁴, max observable error 6.23 × 10⁻⁴); K = 6 at t = 0.25 (process infidelity 2.58 × 10⁻⁵, full-space state infidelity 5.05 × 10⁻⁵, max observable error 3.97 × 10⁻⁴). Two plaquettes: three shortest three-link strings at basis indices 630, 426, 127 (630 initial); sparse H with 10,885 nonzeros; fixed-window K = 128 (7 qubits) on 0 ≤ t ≤ 5; time-adapted K = 4 at t = 0.05 and 0.10, K = 8 at t = 0.25, K = 12 at t = 0.50, K = 32 at t = 1.00. Endpoint-screening projector: rank 297 in the 977-state basis. Acceptance: 1 − F ≤ 10⁻³, max observable error ≤ 10⁻³, zero gauge leakage.

## Recommendation recorded on 7 September 2026

Do not pivot. Reframe the claim from "first with-matter hardware run" to "the measured price of exact gate-level gauge invariance, against a validated non-invariant baseline on the same Hamiltonian, observables and device"; take the REDUCED path (r_max = 1, 2) rather than Plan B; run N5 against the two-plaquette exact data; treat the report's mitigation and formulation results as priors; and settle the Idea 2 collision with the advisor before opening that line. The Hermes campaign prompt v0.6.0 implements this.
