# Phase 0 transfer report

Took over the running v0.6.0 GI-Cost Campaign at the user's request. The prior session left Phase 0 mid-flight (Fable planning and baseline regression still running). I let those jobs settle, then re-ran the mandatory planning pass.

## Established this session

- Baseline regression is green after a test-only repair. Original baseline: 45 tests, 44 passed, 1 failed (test_route_gausskernel.py asserted Route B's unsupported jmax=1 Hamiltonian; NotImplementedError by legacy decision D1). Fable's amendment authorized replacing that call with kernel_dimension(1.0)==152 plus projector orthonormality, with no jmax=1 Hamiltonian claim. Full four-file suite now 45/45, exit 0, run in an isolated .work snapshot so no historical JSON/figure/table was overwritten.
- Legacy gates re-run in sandbox: G1 17/17 PASS, G2 20/20 PASS, G3 PASS (S8/C7 still absent under D4). Opus review: repair PASS; regression evidence PASS with caveats.

## Blocked (recorded honestly, not skipped)

- V1 value stability: the rerun recomputes the three Trotter log-fit slopes; they differ from the committed values by up to 1.4e-9, exceeding the 1e-12 stability threshold. slope-conditioning.json proves the cause is floating-point conditioning of the slope fit (propagated bound matches measurement to two digits). The primary error arrays agree to ~5e-15. This is a user-ruling issue, not waivable. The working-tree trotter_scaling.json is user-preserved and was left untouched.
- Higher-priority failed-gate policy: no dependent BUILD lanes started this session. Only the independent stale-test repair and read-only diagnostics ran.
- V10, V11, and the remaining Tier 2 items were not run. C0 cannot pass; phase remains 0.
- Fable final sign-off is deferred to the final evidence packet (final-signoff reserve preserved; no optional Fable calls made).

## Quotas observed

Codex: 5h 49% left (resets 21:04), weekly 40% (resets Sep 11 16:05). Claude Fable week 46% used, weekly reset Sep 12. Codex CLI 0.153.4; no update or config change. git status unchanged outside the one test file.

## Key artifacts

runs/campaign_v060/sessions/c060_p0_20260907/: plan.md (Fable plan + amendment), repair-regression.xml, repair-G{1,2,3}.log, review-repair-2.md, review-regression-evidence.md, slope-conditioning.json, preservation-check.json, TAKEOVER.md, PHYSICS_STATUS.md.

State: phase still 0. next_action pending user resolution of the V1 slope-stability threshold and the preserved dirty paths before C0 can gate to phase 1.