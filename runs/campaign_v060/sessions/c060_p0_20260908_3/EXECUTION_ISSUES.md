# Execution issues and resume instructions

This continuation produced independent diagnostics only. It did not receive a new Fable plan, implement production physics fixes or advance any campaign gate.

## E1. Budget policy blocks planning/sign-off, not every tool

The live preflight meters were Claude session 10% used, all-model week 27% used, Fable week 51% used. These are independent meters, not an additive budget breakdown. They do not prove that the provider would reject another Fable call. The blocker is the configured 50% Fable budget ceiling and the inability to establish a permitted final-signoff reserve. The initial report's shorthand "unavailable" should be read as unavailable under policy, not as a measured API outage.

Codex showed 82% five-hour and 97% weekly capacity remaining; Opus was available and its bounded read-only code review exited 0. Neither bypasses the mandatory Fable step. No CLI was updated or reconfigured. Resume the mandatory planning/escalation when capacity under the policy is established.

## E2. Diagnostic containment protects old results

Fresh copy: .work/c062_diagnostics/SU2ZX. The original legacy run and campaign-test tree were hashed before execution. Existing tests/gates run inside the copy. Logs and JUnit reports are written to this session. The old C0 test's hardcoded historical write lands only in the sandbox, not in the actual c060_p0_20260908_2 directory.

The new diagnostic baseline harness stops after an unexpected legacy regression failure. Its process exit alone is not a gate result: individual child exit codes are in diagnostic-execution.json, and the C0 child did fail. Source preservation is checked in DIAGNOSTIC_RESULTS.json.

The harness's export safeguard was tightened while its first baseline process was already running: the saved current script exports only successfully executed gate files. The first process used the earlier export loop. In this actual run all G1-G3 commands completed with exit 0 before export, so the exported diagnostic gate JSONs are freshly produced. This distinction is recorded rather than claiming the running Python process reloaded the edit.

## E3. Baseline C0 failure is genuine, not hidden

Fresh legacy regression: 45 tests, zero failures/errors. G1/G2/G3 each exited 0; G3 keeps the historical D4 omission of S8/C7 explicit. No new Claude sign-off was attached to these numerical checks.

Unchanged C0: six tests, two failures (V10 distinctness and V1 byte-equality). Those two failures remain in baseline-C0.log and diagnostic-C0.xml. Passing the old V11 tests does not satisfy the new R9 coverage requirements.

## E4. One diagnostic attempt failed; its repair is limited to the harness

The compact simulator rejected the 133-wire routed circuit as wider than its 29-qubit target. attempt1/ preserves the exception and partial production evidence. The diagnostic was corrected to use the existing logical compact-test construction only for the compact comparison. Production still uses the structured circuit, frozen initial layout and from_backend twin. This harness fix does not repair seed derivation.

## E5. Evidence hashing needs an explicit lifecycle

Proposal: finalize each gate's test outputs, state and ledger first; hash exact bytes; freeze the referenced snapshot; review and sign the manifest hash. If a referenced file changes, generate a new manifest and new review/sign-off. C1 amendment needs its own snapshot; preserve the prior C0 snapshot. Post-signoff notes may be listed as exclusions, not given fictitious hashes before they exist.

R12's self-hash wording needs clarification. A practical solution is an external full-file SHA-256 sidecar/state/ledger entry, with ordinary external hashes in the document; an alternative is a precisely defined canonical-content digest. Those are different contracts. Do not insert a made-up full-file hash or silently change what is hashed.

This final ZIP has a separate archive manifest with exact SHA-256 values. It is a transport/integrity manifest, NOT the missing scientific gate manifest or physics sign-off.

## E6. Archives and Git cleanliness

The older named ZIP was moved, not deleted, to ignored zip_results/ with its checksum preserved. The newer user-requested artifacts/SU2ZX_latest_update_723d083_complete.zip remains untouched. The current prompt and session directory are untracked. No blanket git add, commit, reset, stash or push was used.

This diagnostic run's final ZIP belongs in zip_results/ and excludes other ZIPs. A clean-gate commit is not claimed; C0 is not passing, and the preserved user archive still requires an explicit disposition before any literal empty-status criterion can hold.

## E7. Graphify scope and warnings

Graphify's AST-only update completed and reported 2,075 nodes, 2,788 edges and 206 communities. It backed up the earlier curated graph to graphify-out/2026-09-08/. It warned that community labels are stale and retained 11 nodes from one file outside the current scan corpus. No LLM relabeling or semantic document/image extraction was run. The ZIP includes the current graph, its saved snapshots and graphify-update.log; a code graph refresh is not a scientific review.

## E8. The r=1 production batch exceeded the diagnostic budget

The second seed-diagnosis process exited 124 at its 2,400-second wall cap while executing five production r=1 repeats at 1,024 shots. The last saved stage was the completed r=0 batch. The process was actively using about two CPU cores during observation; no cause of the slow execution was established. Its Python child was absent after termination.

No complete r=1 counts returned, so its uncertainty table is missing. The plot explicitly labels r=1 incomplete rather than drawing invented zero-variance data. Raw shift memories and all completed r=0 counts remain available. The first compact-path failure is separately preserved under attempt1/; these are different execution failures.

Proposed execution repair for the next attempt: add diagnostic per-repeat checkpointing around actual production backend results, recording each completed count dictionary and metadata without changing seeding or measurement semantics. Benchmark and explicitly budget the production r=1 path before the next full batch. Do not reduce the prescribed shots, silently replace the backend, or claim partial repeats satisfy R8. This additional instrumented retry was not run here.

## Resume order (after reading the timeout note)

1. Read PHYSICS_ISSUES.md, CODE_ISSUES.md, REVIEW_CHECKS.md and the measured JSON/CSV files.
2. Obtain the mandatory Fable plan/escalation; resolve the raw-versus-effective-seed shift wording, invalid-key closure contract and hash lifecycle.
3. Obtain the prescribed Opus mechanism ruling on the completed diagnosis before editing twin.py.
4. Implement the approved minimal production/test changes; run the full pre/post/negative-control R7/R8 evidence, fresh V1 and independent R9 oracle tests. Do not select seeds to make the uncertainty test pass.
5. Freeze evidence, perform REVIEW and Fable sign-off on the exact manifest, then handle the scoped commit and C1 amendment. C2 stays blocked until dependencies pass.

Reproduction helpers (from repository root):
- diagnose_unchanged.py setup refuses an existing sandbox; preserve or choose a fresh sandbox for a new attempt.
- diagnose_unchanged.py baseline invokes the unchanged four-file suite and G1-G3, then the old C0 suite.
- diagnose_seeds.py runs the recorded two-path shift probes and production pre-fix repeats.
- diagnose_control.py performs the actual r=0 equal-seed control.
- diagnose_oracles.py performs the finite code/closure/empty-count probes.
Use .mamba/envs/su2zx/bin/python, except the stdlib-only setup/baseline orchestrator can use python3. Scripts and all raw evidence are included in the bundle. Do not rerun into a frozen session output directory; use a fresh session copy and update its paths explicitly.
