# Repo inventory (G0)
Reusable monograph scaffold (repo root src/su2zx/, v0.4.0):
- core.py: pure-gauge plaquette-chain H (Pauli terms), Strang circuits, exact expm reference,
  H_tilde=2H/g^2 convention, qiskit bit-order q_(N-1)..q_0. REUSE: H~1 one-plaquette block for
  G1 frozen-matter reconciliation; Strang skeleton pattern; equivalence-check style.
- compiler_study.py (841 L): PyZX pipelines incl. topology-preserving pass, routed-count
  accounting. REUSE for Phase 4 compiler comparison (secondary endpoint).
- robust_study.py / scaling_study.py: pairwise compiler selection, symmetry-aware scaling. Secondary.
- qpu.py / qpu_analysis.py: dry-run-first submission wrapper w/ approval token, quasiprobability
  handling, bootstrap analysis. REUSE for Phases 5-7 (twin mode).
- tn_study.py: Aer MPS cross-check harness. REUSE Phase 5 cross-checks.
- tests/: pytest suite for the above (passes under .mamba/envs/su2zx).
Not present: solutions/ dir (no 0.4.0.md file found - prompt says it exists; recorded as absent),
SU2QC plan document (not in repo), any with-matter Hamiltonian code (ALL NEW tonight).
prompts/: v0.3.0, v0.4.0 Codex prompts, v0.5.0.md (this run).
