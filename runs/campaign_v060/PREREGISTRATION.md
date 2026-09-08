# PREREGISTRATION — GI-Cost Campaign v0.6.1

Status: frozen at C1. Thresholds and hashes are frozen; remaining backend/qubit/delta_dev slots are intentionally open until C5.
Hardware: HARDWARE_MODE: disabled — no IBM credentials are configured on the Hermes machine as of 2026-09-08. Phases 5–6 remain calibration-derived twin/emulated only until a human configures credentials and flips the mode. No QPU job has ever been submitted by this project.

Rulings applied: R1 V1 propagated slope conditioning; R2 preserved/restored signed evidence and explicit commits; R3 ODR deferred to Phase 5; R4 conditional twin seed, bootstrap-SE and estimator rules; R5 frozen coupling mapping; R6 supervised session scope.

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


## R5 coupling points and time points

P-A authority is `physics/window.json` and `conventions.py`: (cE,cM,cH,cB)=(2,0.75,0.5,0.125), g_E=g^2/2=2, mu=3/8, electric:hopping:magnetic=1:0.25:0.0625. Time points are t=r*0.8333333333333334 for r=1,2; t=2.5 only if Phase 4 establishes r=2 to r=3 admissibility.

P-S: (cE,cM,cH,cB)=(2,0.75,0.04,0.04), g_E=2, mu=3/8, t in (2.5, 6.25), corresponding to tau in (5, 12.5). The four-coefficient API is required; this point is not on the one-parameter family.

### 2.5 Matched-experiment rules (both arms)

Same backend and calibration window; the KR qubits chosen inside the GI qubit path where the calibration ranking allows, otherwise the best-ranked connected triple and the reason recorded; matched t = 0 control circuits per arm (state preparation + measurement only) and reporting of ΔO(t) = ⟨O⟩_t − ⟨O⟩_0 beside absolute values (adopted from the Sufian protocol); independent readout calibration per arm per job; equal total shots per observable group (4,096 per group, 5 repetitions, shot allocation across groups by variance contribution allowed if the total is conserved); mitigation arms M0 (readout inversion only), M1 (readout + DD + Pauli twirling + ODR), M2 (M1 + linear ZNE at fold scales {1, 3}); quadratic ZNE is not run (the Sufian scale-5 result is cited as the reason); leakage post-selection for GI only, with pre- and post-selection values both reported; bootstrap 1,000 resamples over repetitions and time blocks, including the calibration counts.


## Frozen implementation/search budgets

KR: K-scan every point and time; exact and approximate synthesis; at least 3 optimization levels x 20 seeds x all operational Heron backends when hardware is enabled. GI: one bounded <=4 hour leak-free synthesis sprint; no Pauli re-splitting.

Mitigation M0 readout inversion; M1 readout + DD + Pauli twirling + ODR; M2 M1 + linear ZNE folds (1, 3). Shots: 4,096 per group, 5 repetitions, symmetric fit-to-cap reductions only. Bootstrap: 1,000 resamples over repetitions/time blocks in hardware phases.

R1 V1: primary quantities compare at 1e-12; fitted Trotter slopes use 10x first-order propagated conditioning bound and lie in [-2.3,-1.7]. R3: ODR closure is a Phase 5/V12 sub-row. R4: no change to twin seed unless pre-fix dictionaries are identical; negative control required. R5: conventions/window authority supersedes v0.6.0's incorrect printed P-A row.

Backend: [to be filled at C5]
Qubit path: [to be filled at C5]
delta_dev: [to be filled at C5]
Threshold SHA-256: [see CAMPAIGN_STATE.json hashes.thresholds]
Preregistration SHA-256: [see CAMPAIGN_STATE.json hashes.preregistration]
Conventions SHA-256: fb3b7525b1a1d69bcb30ace986465880b972cc9fb23a417af5a9ca78ebade306
Four-coefficient API: H(coeffs=(cE,cM,cH,cB), jmax, geometry, static_charges), with H(gE,mu,jmax) wrapper reproducing v0.5.0 at gE=2.
