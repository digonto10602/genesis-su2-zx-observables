# Discrepancies between prompt/predictions and code (§4.3: code wins)

All numbers below are produced by src/su2qc/dynamics (routes agree to 1e-15).

## D-A. The baryon–antibaryon channel DOMINATES; the meson channel is subdominant

Prediction (physics/predictions_G2.md, following the prompt's Cataldi-style
expectation): meson channel dominant, BB̄ subdominant (second-order process).
Measured at the operating point (g² = 4, m = 3g²/16 = 0.75, t ∈ [0,12]):
max P_BBbar = 0.833, max P_meson = 0.073; P_surv minimum 7e-4. The same
ordering holds for every (g², m) scanned (analysis/tables/exact_mass_scan.csv).

Root cause (exact first-order structure of H at resonance, from the stretched
row of H): the stretched string |(0,½,½,½); n=(1,1,0,2)⟩ (E = 3.0) is coupled
at FIRST order in the hopping to five states, and at m = 3g²/16 four of them
are exactly degenerate with it (ΔE = 0):

| partner | q pattern | channel (prompt §5.3 rules) | amplitude |
|---|---|---|---|
| (0,0,½,½), n=(1,0,1,2) | (+1,−2,+1,0) | BB̄ (|q_2| = 2) | −0.500 |
| (0,½,½,0), n=(2,1,0,1) | (+2,−1,0,−1) | BB̄ (|q_1| = 2) | −0.500 |
| (0,½,0,½), n=(1,1,1,1) | (+1,−1,+1,−1) | meson | +0.354 |
| (½,½,½,½), n=(0,2,0,2) | (0,0,0,0)  | other (vacuum + flux loop) | −0.354 |
| (½,0,0,0), n=(1,1,0,2) | short string | surv, ΔE = −3 | +0.125 |

On a single plaquette the quark (v1) and antiquark (v2) are nearest neighbours
along l1. Moving the antiquark's remaining fermion off v2 (or a second fermion
onto v1) is a ONE-hop process that produces |q| = 2 at that vertex, so the
prompt's precedence rule classifies two of the three resonant partners as BB̄,
with larger amplitude (½ vs 1/(2√2)) than the single meson partner. The
"BB̄ subdominant" expectation is a ladder/large-lattice statement (pair
creation far from the endpoints) and does not hold on the one-plaquette patch.
This is the non-Abelian channel structure the prompt asked to measure — it is
simply the dominant one here. Consequence for the hypothesis text: the
"meson-versus-baryon split" is reproduced as BB̄ ≫ meson, and the report must
say so.

## D-B. The W̄-argmax resonance estimator does not locate 3g²/16

Prompt criterion: m* = argmax of the time-averaged pair-creation weight
W̄(m) = ⟨P_meson + P_BB̄⟩. Measured argmax m*/g² ∈ {0, 0.0625, 0, 0} for
g² ∈ {1,2,4,8}: W̄ is nearly flat in m (0.56–0.66 at g² = 1) because the BB̄
channel is populated at all m through the flux-loop mixing, so W̄ is not a
resonance-sensitive observable on this patch. The breaking-time estimator
(argmin t_b) is reported alongside (mstar_over_g2_tb). At g² = 4 and 8 the
exact spectrum shows the degeneracy at m = 3g²/16 explicitly (table above,
ΔE = 0.000), so the tree-level resonance is confirmed by level structure rather
than by W̄. The operating point is therefore set to the tree-level value
(g², m) = (4, 0.75), which also satisfies all window criteria (D-C).

## D-C. Truncation error exceeds 0.1

At (g², m) = (4, 0.75): max |Δp| (jmax=1 vs jmax=½) over channels and
t ∈ [0,12] = 0.257 (> 0.1). At g² = 1 it is 0.348. The hardcore-gluon
truncation is a LEADING systematic on this patch: the resonant flux-loop state
(½,½,½,½) connects to j = 1 configurations at first order in the magnetic
term. Flagged prominently per Phase-2 criterion 4; it enters the error budget
as the largest term. Choosing a larger g² reduces it (1/(2g²) magnetic
coupling) but does not bring it under 0.1 within the scanned range; the
window keeps the tree-level operating point and reports the shortfall.

## Window chosen (physics/window.json)
g² = 4, m = 0.75, δt = 0.8333, r_max = 3 (t = 2.5):
exact P_surv drop 0.993 (≥ 0.3 ✓), pair weight 0.819 (≥ 0.05 ✓),
Strang error 0.016 (≤ 0.05 ✓). No shortfall flag on window criteria.

## D-E. v0.5.0 twin repeats were not independent

The v0.5.0 twin seeded its repeats `seed + k` (`src/su2qc/twin/twin.py`,
`run_counts`). Under Aer's per-shot seeding, consecutive seeds produce the same
shot stream offset by one shot, so repeats overlap in N - 1 of N shots. Every
v0.5.0 twin sigma is therefore void as an independent-repeat uncertainty. No
v0.5.0 twin number was ever gated, so no gate result changes.

Mechanism evidence, measured on the production path
`AerSimulator.from_backend(FakeTorino)` at 12 qubits and 1,024 shots:
`runs/campaign_v060/sessions/c060_p0_20260909_5/seed-mechanism.json` records
same-index matches 0 and shift matches 1,023 of 1,024 for the seed pair
(500, 501), against 1 of 1,024 for seeds spawned from a numpy SeedSequence.
The repair replaces the increment with spawned seeds and is recorded in the
campaign C0 gate, not here.
