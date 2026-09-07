# Review: route_spinnet.py (phase 1, review 1)

Verdict: PASS with history recorded (no blocking findings open).

Process note (honest record): the first delegated reviewer (nemotron-30b,
sa-1-98ed9b67) completed with verdict "pending_review" and wrote no findings
file; its independent spot checks in transcript showed no blocking issues on
the counting/diagonal structure. Between review start and this record, route 1's
off-diagonal amplitudes were REWRITTEN under escalation solutions/0.5.0.md
(dressed-vertex tensor contractions replacing guessed uniform factors, both
±1/2 hopping directions, Tr U□ + Tr U□† both included).

Verification evidence for the final file (all reproduced by gates/gate_G1.py):
- dims 82/152; sector dims 2,20,38,20,2; hermiticity 0.0; [H,N] 0.0.
- Spectra agree with the independently constructed, gauge-verified route 2
  ([G^a_v,H]=0 exactly on the redundant space) to ≤ 2.7e-15 relative at 6
  coupling points; stretched-string time series to ≤ 1.6e-15.
- Pure-electric degeneracies 16,16,18,16,16 (rel dev 2.1e-11 at g2=1e6).
- Magnetic-off spectra match route 2 B-off to 1.3e-15.
- 20/20 unit tests green.

Advisory (carried to G3): projector helpers P_stretched/P_short currently both
return the 2-dim q=(+1,-1,0,0) projector (P_surv); the dynamics lane must use
label-resolved projectors for the individual stretched/short states.
