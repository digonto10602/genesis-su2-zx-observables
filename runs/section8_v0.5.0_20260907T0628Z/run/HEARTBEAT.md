# Heartbeat
elapsed 00:05 | to 12h +714 min | to freeze(15h) +894 min | to stop(16h) +954 min
phase 1 running; lanes: B-route1(sa-0), B-route2(sa-1), P-predictions(sa-2); verifier compare.py/limits.py/gate_G1.py written by OPS; risks: route2 jmax=1 runtime, magnetic vertex factors sign conventions; next decision: on G1 group return; QPU sec spent: 0
elapsed 00:45 | to 12h +674 min | to freeze(15h) +854 min | to stop(16h) +914 min
T+~0:50: route1 module landed (82 states, stretched string found, spectra computed); test suite 18/19 -> builder fixing projector API; route2 CG coded, kernel construction in progress; predictions_G1 done (82/152/sectors/degeneracies all as expected). Verifier artifacts done. Next decision: G1 assembly on group return.
elapsed 01:43 | to 12h +616 min | to freeze(15h) +796 min | to stop(16h) +856 min
T+1:50: G1 att2: codex building route2 (physical basis fn exists); dynamics builder (sa-0-2edc26a5) + route1 reviewer (sa-1-98ed9b67) running; predictions_G2 delegated earlier. QPU sec: 0
elapsed 01:59 | to 12h +600 min | to freeze(15h) +780 min | to stop(16h) +840 min
T+2:45: G1 att2 failed on route agreement -> escalation 1 -> solutions/0.5.0.md written; fresh codex builder rebuilding route1 amplitudes; dynamics builder + route1 reviewer still running; G1 latest 2:45 passed but critical-path work active (extension policy notes this). QPU: 0
elapsed 02:36 | to 12h +563 min | to freeze(15h) +743 min | to stop(16h) +803 min
T+3:45: G1 escalation fix DONE by orchestrator (route1 dressed-vertex amplitudes rewritten; routes agree 2.7e-15). Limits pass. Waiting on signoff_G1 (sa-0-9e808e1a) then gate G1 run. Dynamics builder steered (wrong python path). predictions_G2 + route1 review recorded.
elapsed 02:42 | to 12h +557 min | to freeze(15h) +737 min | to stop(16h) +797 min
T+4:07 GATE G1 PASS (17/17 criteria). Phase 2 dynamics builder active; Phase 3 starts now.
