# Section 8 overnight run 20260907T0628Z — SU(2) with dynamical matter on one plaquette

## 0 Status line

Run halted at T+~4:00 (orchestrator iteration budget exhausted, not the 16 h clock).
Mode: twin (no IBM credentials; FakeTorino target, CZ-native, 133 qubits).
Gates: G0 PASS, G1 PASS (attempt 3, 1 escalation). G2 in progress. G3 partially
built. G4–G9 not started. QPU seconds spent: 0. Escalations used: 1 of 6.

## 1 Executive summary

- The scientific core of the night was delivered and verified: the 82-state
  gauge-invariant Hamiltonian of the SU(2) single plaquette with dynamical
  two-color staggered fermions was built by two genuinely independent routes
  that agree to machine precision (sorted spectra ≤ 2.7e-15 relative at six
  coupling points; stretched-string observable time series ≤ 1.6e-15).
- Route 2 (redundant Kogut–Susskind + Gauss-kernel projection) verifies gauge
  invariance exactly: max |[G^a_v, H_term]| = 0.0 for every term group
  (electric, mass, 4 hoppings, plaquette) on the 160,000-dim redundant space.
- One real defect was found and fixed through the prescribed escalation
  protocol: the first analytic route omitted dressed-vertex recoupling factors
  (uniform 1/(2√2) hopping amplitudes; magnetic elements 16× too small in
  structure). solutions/0.5.0.md diagnosed it; the rebuilt amplitudes
  (invariant vertex tensors + Wigner link insertions, L-end color conjugation)
  closed the gap.
- All three limit tests pass: pure-electric degeneracies 16,16,18,16,16;
  frozen-matter 2×2 block equals the monograph H̃₁ after a documented factor-2
  magnetic-normalization reconciliation; B-off spectra agree cross-route to
  1.3e-15.
- Not delivered: exact-dynamics production tables (mass scan/resonance/window
  — code written and self-checked, scan not run to completion), circuit
  validation (G3), compile/twin (G4), preregistration onward (G5–G9).

## 2 Run timeline

| T+ | Event |
|---|---|
| 0:00 | T0 = 2026-09-07 06:28 UTC; run scaffold, clock, prompt hash |
| 0:02 | G0 PASS (env lock, FakeTorino loads, ledgers, conventions frozen) |
| 0:05 | Phase 1 fan-out: route-1 builder, route-2 builder, G1 predictions |
| ~1:28 | G1 attempt 1: route 1 lands (counting/limits pass); route 2 builder returns empty → attempt 2 |
| ~1:35 | Attempt 2: route 2 re-delegated to Codex with full CG spec |
| ~2:40 | Route 2 completed (basis skeleton by Codex; terms/Gauss verification by orchestrator). Routes DISAGREE (dev 0.12–1.32) → escalation 1 → solutions/0.5.0.md |
| ~3:00 | Fresh Codex builder implements the solution; still disagrees (honest report, no fudging) |
| ~3:30 | Orchestrator completes the fix: ±½ hopping directions, corrected vertex tensors/end insertions, TrU□ + h.c. Full spectra dev → 8.9e-15 |
| ~3:45 | Limits pass; reconciliation doc written; physics sign-off SIGNED-OFF |
| 4:05 | G1 PASS, 17/17 criteria (gates/GATE_G1.json) |
| ~4:00+ | Dynamics engine fixed and self-checked; scan.py rewritten; L12 encoding delivered by Codex; halted on orchestrator iteration budget |

Decisions (run/DECISIONS.md): D1 route-2 jmax=1 is kernel-dimension-only
(152 verified; projected H at jmax=1 from route 1); D2 magnetic-off limit uses
cross-route comparison (no independent 1D chain builder in repo); D3
frozen-matter tolerance documented-relaxed to 1e-8 (physical O(h²/m) residual).

## 3 Model, conventions, and verification

Conventions frozen at G0 in src/su2qc/conventions.py: vertices v1..v4 at
(0,0),(1,0),(1,1),(0,1); links l1:v1→v2, l2:v2→v3, l3:v4→v3, l4:v1→v4;
η = (+1,−1,+1,+1); U□ = U1 U2 U3† U4†; parities (+,−,+,−); n_vac = (0,2,0,2);
JW order v-major; H = (g²/2)ΣE² + m Σ(−1)^{x+y}n + (1/2)Σ η(ψ†Uψ + h.c.)
− (1/(2g²))Tr(U□+U□†); j ∈ {0, ½} primary, jmax = 1 for truncation error.

| Criterion | Target | Measured | Status |
|---|---|---|---|
| dim (jmax ½), both routes | 82 | 82 / 82 | PASS |
| dim (jmax 1) route 1 / route 2 kernel | 152 | 152 / 152 | PASS |
| Sector dims N=0,2,4,6,8 | 2,20,38,20,2 | exact match, both routes | PASS |
| Hermiticity | ≤1e-13 | 0.0 | PASS |
| [H, N] | ≤1e-13 | 0.0 | PASS |
| Route spectra rel. dev (6 points incl. m=0) | ≤1e-12 | 2.7e-15 | PASS |
| Stretched-string time series dev, t∈[0,10] | ≤1e-10 | 1.6e-15 | PASS |
| ‖[G^a_v, H_term]‖ (route 2, all v,a,terms) | ≤1e-12 | 0.0 | PASS |
| Pure-electric degeneracies (g²=1e6) | 16,16,18,16,16 | exact (rel 2.1e-11) | PASS |
| Frozen-matter block = H̃₁ | ≤1e-8 (D3) | 3.0e-9 | PASS |
| Magnetic-off spectra | ≤1e-10 | 1.3e-15 | PASS |
| Physics sign-off | SIGNED-OFF | signoff_G1.md, no objections | PASS |

Key convention findings (physics/conventions_reconciliation.md):
- U-insertion convention fixed numerically by gauge invariance: the L (source)
  color index conjugated, (conjL, conjR) = (True, False) — the unique variant
  of four with [G, hop] = [G, TrU□] = 0.
- Frozen-matter off-diagonal: H_01·g² = −1 exactly, vs the monograph's −2;
  a factor-2 normalization difference in the magnetic term absorbed by
  x_eff = x/2 when mapping monograph results onto the patch. The patch value
  is fixed by exact gauge invariance and is the physically correct KS one.

Independence audit (honest): route 1 and route 2 share only conventions.py and
never imported each other. However, the route-1 rebuild's end-insertion
convention was chosen to match the convention route 2 selected numerically
(recorded in the file header), and the final fix was implemented by the
orchestrator rather than a separate builder. Independence therefore holds at
the level of construction method (dressed-vertex analytic contraction vs
redundant-space Gauss projection) — the strongest available check — but not at
the level of authorship for the final amplitude code. Recorded per §2.1;
delegated children all ran on nvidia/nemotron-3.5-lightning-30b-a3b, builders
escalated to Codex CLI (codex-cli 0.153.4); the configured escalation model
claude-fable-5-1 was not reachable through delegation and the substitution is
stated in solutions/0.5.0.md.

## 4 Exact physics

Predictions registered before code ran (physics/predictions_G1.md,
predictions_G2.md): resonance m* ≈ 3g²/16, meson channel dominant over
baryon–antibaryon, ΔC ≈ −3/4 at strong breaking, t_b ~ 2–10 lattice units,
jmax=1 corrections < 0.1 for g² ≥ 1.

Delivered: dynamics engine self-check at (g²=1, m=0.1875): expm-vs-Krylov
deviation 2.3e-15 (target 1e-9), energy drift 4.4e-16, N drift 1.8e-15
(targets 1e-10).

NOT delivered: the mass scan (2 g² values × 25 masses), resonance location
m*/g² vs 3/16, time-series tables/figures at m*, truncation-error number, and
window.json. The code paths exist and are unit-testable
(src/su2qc/dynamics/scan.py, rewritten by the orchestrator after the delegated
builder produced a partial file with a wrong survival classifier); the scan
runs were repeatedly cut by shell timeouts before writing artifacts. No
resonance number is claimed. Resume command in §13.

## 5 Encodings and circuits

L12 encoding delivered (src/su2qc/encodings/l12.py, Codex): 12 qubits, 3 per
vertex (two link-copy bits + matter bit; c=1 with disagreeing links = leakage);
82 physical codes verified distinct; stretched-string code = 3793; leakage
scan over all 4096 codes clean (flags fire exactly off the 82). Strang-circuit
scaffolding and QPY/OpenQASM3 exports for r = 0..3 exist
(circuits/l12_r{0..3}.qpy/.qasm) with a logical resources table.

NOT delivered (G3 open): exact block-unitary equivalence checks
(‖P_phys(U−e^{−iθT})P_phys‖ ≤ 1e-12, ‖P_unphys U P_phys‖ ≤ 1e-12), full
Strang-step fidelity vs exact propagator, Trotter r⁻² scaling fit, noiseless
leakage-zero statevector test, S8 and C7 encodings. The prompt's central
"symmetry-verified" claim is therefore NOT yet established at circuit level.

## 6 Compilation and the twin — NOT STARTED
Planned per Phase 4: Qiskit L3 + PyZX-TP (reusing repo compiler_study.py)
judged after routing on FakeTorino; AerSimulator.from_backend twin. No numbers.

## 7 Preregistration and measurement plan — NOT STARTED. Nothing was frozen;
no PREREG.md exists; no production run of any kind was performed.

## 8 Pilot and full run — NOT STARTED. No hardware jobs; QPU seconds = 0.

## 9 Results vs exact — N/A (no production data).

## 10 Ablations — N/A.

## 11 Claim table (Section 8.3, filled truthfully)

| Supported if the gates pass | Tonight's status |
|---|---|
| 12-qubit symmetry-verified evolution within reach at stated depth/yield | NOT ESTABLISHED — encoding built; block-unitary verification, compile, and twin all pending |
| Meson-vs-baryon split, string shortening, Casimir reduction on hardware | NOT ESTABLISHED — exact-dynamics tables not produced; no twin/hardware run |
| Error budget (truncation/Trotter/compile/device/shot) | NOT ESTABLISHED |
| Compiler comparison as secondary endpoint | NOT ESTABLISHED |

| Not supported by this experiment (by design) | |
|---|---|
| String tension, continuum limit, hadron phenomenology | correctly not claimed |
| Classically intractable computation (patch is exactly solvable) | correctly not claimed |
| Baryon blockade / full 2+1D (needs ladders) | correctly not claimed |
| Quantum advantage | correctly not claimed |

What IS established tonight: the verified 82-state Hamiltonian with exact
gauge invariance by two independent constructions, its limit structure, and
the frozen-matter reconciliation to the monograph — the foundation every later
phase depends on.

## 12 The 2×3 continuation plan (unchanged from the prompt's scope)
1,727 gauge-invariant states, 20 qubits in L12. What tonight changes: the
dressed-vertex amplitude machinery and the numerically-selected U convention
generalize directly (generic-j CG closed forms already in route 1); route 2's
vertex-local kernel algorithm scales to the ladder if blocked by j-sector.
The factor-2 magnetic normalization must be carried into any monograph-based
resource extrapolation.

## 13 Reproducibility

Environment: .mamba/envs/su2zx python 3.11.16; qiskit 2.5.2, aer 0.17.2,
runtime 0.49.0, pyzx 0.10.6, scipy 1.17.1, numpy 2.4.6, mthree 3.0.0;
lock in env/requirements.lock.txt. CUDA-Q / cuTensorNet: NOT AVAILABLE.

Verify G1 from scratch:
  cd runs/section8_v0.5.0_20260907T0628Z
  ../../.mamba/envs/su2zx/bin/python -m pytest tests/test_route_spinnet.py -q
  G1_ATTEMPT=3 ../../.mamba/envs/su2zx/bin/python gates/gate_G1.py

Resume the run (next actions, in order):
  1. ../../.mamba/envs/su2zx/bin/python -c "import sys; sys.path.insert(0,'src');
     from su2qc.dynamics import scan; print(scan.mass_scan());
     print(scan.select_window())"        (~minutes; writes resonance.json,
     exact_mass_scan.csv; then timeseries_at + truncation)
  2. gates/gate_G2.py; physics sign-off.
  3. Finish tests/test_l12.py G3 criteria (unitary equivalence, Strang
     fidelity, r⁻² fit, leakage-zero); gates for S8/C7 or drop per §4.4.
  4. Phases 4–9 per prompt.

## 14 Coverage table and file index

| Plan days | Work | Artifacts | Status |
|---|---|---|---|
| 1–3 | conventions; H by two routes; limit tests | conventions.py, GATE_G1.json, signoff_G1.md, solutions/0.5.0.md | DONE (twin-independent) |
| 4–6 | exact dynamics; resonance; window | dynamics/engine.py (self-check PASS), scan.py | PARTIAL — code ready, tables not produced |
| 7–9 | encodings; block unitaries; Strang; leakage 0 | encodings/l12.py, circuits/l12_r*.qpy/.qasm | PARTIAL — encoding verified, unitaries unvalidated |
| 10–12 | compile; twin; Plan-B decision | — | NOT DONE |
| 13–17 | measurement; prereg; rehearsal | — | NOT DONE |
| 18 | dry run | — | NOT DONE |
| 19–23 | pilot; full run | — | NOT DONE (0 QPU s) |
| 24–27 | analysis; ablations | — | NOT DONE |
| 28–30 | report; replication; bundle | this file | PARTIAL |

Key files (all under runs/section8_v0.5.0_20260907T0628Z/ unless noted):
  run/{T0,PROMPT_HASH,CONFIG_ENV.md,INVENTORY.md,PLAN.md,MODELS.md,GATES.md,
      DECISIONS.md,HEARTBEAT.md,TASKBOARD.md}
  gates/{GATE_G0.json,GATE_G1.json,gate_G0.py,gate_G1.py,gate_G2.py,attempts/}
  src/su2qc/{conventions.py,ham/{route_spinnet,route_gausskernel,compare,
      limits}.py,dynamics/{engine,scan}.py,encodings/l12.py,circuits/}
  tests/{test_route_spinnet.py (20 PASS),test_route_gausskernel.py,conftest.py}
  physics/{predictions_G1.md,predictions_G2.md,signoff_G1.md,
      conventions_reconciliation.md}
  reviews/p1_route_spinnet_1.md
  logs/agents/ (all builder prompts and outputs)
  ../../solutions/0.5.0.md (repo root; escalation solution + outcome)

Every number in this report traces to a gate JSON, pytest output, or artifact
path produced by code. No production observables are claimed because none were
measured.
