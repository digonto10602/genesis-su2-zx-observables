# G1 attempt 1 (T+0:05 - T+1:28)

Route 1 (spinnet, sa-0 nemotron-30b): SUCCESS. 82/152 dims, sectors 2,20,38,20,2,
hermitian 0.0, [H,N] 0.0, pure-electric degeneracies 16,16,18,16,16. 20/20 unit tests pass.

Route 2 (gausskernel, sa-1 nemotron-30b): FAILED — agent spent 83 min on CG convention
experiments, never produced a working module; final summary empty ("files": []). Root
cause: routed child model too weak for the E_L/E_R/U sign algebra; repeated convention
confusion (orthogonality check -0.4714 instead of 0).

Action: attempt 2 delegates route 2 to Codex CLI (different, stronger model) with a
fully specified CG table and the blockwise vertex-local kernel algorithm in
logs/agents/route2_attempt2.prompt.md. Per §4.2 this is attempt 2 with a different
hypothesis (fully specified conventions + stronger builder), not a rerun.
