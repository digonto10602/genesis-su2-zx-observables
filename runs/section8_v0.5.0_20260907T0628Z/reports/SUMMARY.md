# Summary — Section 8 overnight run 20260907T0628Z

Halted at T+~4:00 (orchestrator iteration budget, not the clock). Twin mode, 0 QPU s.

DONE:
- G0 PASS. Environment, FakeTorino target, frozen conventions, all ledgers.
- G1 PASS (attempt 3, 1 escalation): the 82-state SU(2)-with-matter plaquette
  Hamiltonian by two independent routes. Spectra agree to 2.7e-15; observable
  time series to 1.6e-15; route 2 gauge-invariant exactly ([G,H]=0.0 per term);
  dims 82/152; sectors 2,20,38,20,2; electric degeneracies 16,16,18,16,16;
  frozen-matter block = monograph H~1 after a documented factor-2 magnetic
  normalization reconciliation (physics/conventions_reconciliation.md).
- Escalation worked as designed: solutions/0.5.0.md diagnosed route 1's missing
  dressed-vertex recoupling factors; fix verified against the gauge-checked route.
- Dynamics engine self-checked (expm vs Krylov 2.3e-15; drifts <2e-15).
- L12 encoding delivered: 82 physical codes, leakage flags verified on all 4096
  codes, circuits exported r=0..3.

NOT DONE: mass scan / resonance / window tables (code ready, not run to
completion), G3 circuit validation, compile+twin (G4), prereg through analysis
(G5–G9). No production observables are claimed.

Resume: reports/REPORT.md §13 has the exact commands (mass_scan → gate_G2 →
finish test_l12 → Phases 4–9).
