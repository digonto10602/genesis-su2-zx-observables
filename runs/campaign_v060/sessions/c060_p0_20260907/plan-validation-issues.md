# Mandatory planning validation / physics escalation

Review your plan-retry.md.partial in this directory. Do not redesign the campaign; amend or block the plan concisely. No edits, no outside-repo access. Required physics escalation, not optional critique.

1. Deterministic comparison of working-tree circuits/trotter_scaling.json vs committed HEAD failed numeric stability. value-stability.json has measured slope deltas 4.989222368578794e-10 and 1.3983592062061234e-09 (threshold 1e-12). Underlying observable errors differ only at floating precision; amplification in log-slope fitting appears plausible but is not established. The working file is user-preserved. Cannot waive threshold, overwrite user's file, or silently substitute committed evidence for current results. Does this force STOP at regression repair? Specify permissible bounded diagnostic/repair, if any.

2. V11 closure in your plan is P_S3+P_meson+P_BBbar+P_other, but twin.py defines P_surv as the full (1,-1,0,0) occupation sector, P_stretched (S3) and P_short as strict subchannels. Closure with P_S3 alone excludes the short string. Read actual twin.py. Confirm exact identity and whether V11 readout-mitigation and after-ODR absence must make V11 PARTIAL rather than PASS. Prompt C0 cannot pass with omitted requirements.

3. Twin prompt explicitly allows proving seed override harmless. Your plan mandates pre-fix failure and switching construction-time seed to mutable options regardless. Per-run keyword currently changes seed+k. If pre-fix real test passes, must record harmless, not manufacture RED or change working seed semantics. Confirm conditional no-change path, and distinguish bootstrap SE requested in prompt from per-repeat SD used in your plan (density can take 0,1,2; use actual multinomial weighted variance, not Bernoulli p formula for general density).

4. resources_routed.md pre-route equiv is error, not fidelity. Orthogonality cannot be concluded from 1.0 until metric implementation in compile/route.py is checked. Retire on failed equivalence only, do not claim orthogonal without proof.

5. Phase 0 package skeleton path deviation: preserve existing single run-local package by placing su2qc.replicate there, or explicitly mark original module deliverable deferred if campaign-local replicate.py chosen. Neither path may be called complete if requirement not met.

Reply amended executable plan decisions with physics criteria and stop conditions; if V1 cannot be restored without violating preservation, return BLOCKED and whether independent stale-test repair remains permitted. No weaker-model substitution. Final sign-off still reserved; this is mandatory physics doubt escalation.
