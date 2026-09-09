# Checks on the independent Opus review

The completed review is diagnostic-code-review.md. It is raw reviewer output, NOT automatically verified fact or gate acceptance. The following qualifications prevent its speculative findings from becoming unnecessary physics changes.

1. A9's proposed N-not-4 meson counterexample was not found. Exhaustive enumeration of all 82 physical codes returned no code with all |q|=1 and N!=4, and no singleton closure failure. The frozen vacuum is (0,2,0,2). The illustrative q=(1,1,1,-1) would require occupation 3 at the second site. No meson-definition repair is justified by this review claim. Evidence: oracle-diagnostics.json.

2. A11 says the old estimator test contains no N!=4 label. Its third label has occupations (2,0,0,0), so it is already an N=2 example. The real coverage defect remains: three labels are fewer than R9 requires; it lacks all-channel coverage, two negative entries with checked channel totals, the independent oracle and the prescribed yield path.

3. A8's assertion that a second transpile necessarily invalidates classical-bit mapping is unproven. A correct transpiler preserves circuit measurement semantics while routing. Do not remove transpilation or assert identity layouts merely on this speculation. If needed, test resulting classical-output semantics independently against noiseless known codewords and circuit equivalence.

4. C1 does not require a new production seeds-override API just to build a diagnostic negative control: five real single-circuit calls with the same base seed exercise the current production path and give one dictionary. diagnose_control.py performs those calls. For an approved repaired batch-path test, a test-only recording/forcing wrapper around sim.run can verify the emitted seeds without expanding the public physics API. That future test remains to be reviewed.

5. C2/C3: the governing prompts explicitly distinguish allowed source repairs/append-only discrepancy notes from forbidden overwrites of historical numeric outputs. A package move is not required before the authorized run-local source repair. No source repair was performed in this diagnostic-only continuation.

6. A14: the diagnostic sandbox is inside the repository, so Git can discover the parent .git directory. A plain copy is not intrinsically unable to run git show in this arrangement. Explicit cwd and a pinned reference commit are still better reproducibility controls. The stale-evidence problem in V1 is real independently of Git discovery.

7. A15: a full-file digest stored outside its target in state/ledger is normal verification, not inherently circular. R12's demand to embed the final full-file digest in its own target is the actual self-reference problem. Do not "fix" it by inventing a digest or silently hashing only part of the document.

8. Reviewer comments about the production caller were conditional because run_g4.py was outside its six-file scope. The orchestrator separately read run_g4.py:122-132 and confirmed twin_backend(seed=101), REPEATS=5, SHOTS=4000 and run_counts(...,500+10*r,...).

9. The independent review contains no C0 PASS verdict. Unresolved physics/sign-off decisions remain deferred to Fable, not decided by this note.
