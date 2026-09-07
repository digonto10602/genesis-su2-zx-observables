# Run plan (adapted schedule)
Mode: TWIN (no IBM credentials; FakeTorino target, CZ native).
Phases per prompt Section 6, with these adaptations:
- All with-matter code is new under $RUN/src/su2qc/ (nothing in repo covers matter).
- Monograph reuse: H~1 block (core.py) for frozen-matter limit; compiler_study PyZX-TP pass
  for Phase 4; qpu.py dry-run/approval mechanism pattern for Phase 6; tn_study MPS harness.
- Concurrency 3 (delegate_task limit). Lanes overlap per Section 6 table.
- Cross-checks: CUDA-Q NOT AVAILABLE; use Aer statevector + Aer MPS.
- Escalations: solutions/0.5.0.md first (repo has no solutions/ dir; will create).
