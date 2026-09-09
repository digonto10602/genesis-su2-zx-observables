# User-approved clarifications to v0.6.3

Recorded after reading the prompt and before any implementation.

1. User permits the mandatory bounded Fable planning pass, subject to fresh budget check, retaining documentation-only scope. No production physics edits, gate runs, C1 amendments or hardware operations.
2. Correct R15's meson claim to the source-supported contract: with occupation domain {0,1,2} and N_VAC=(0,2,0,2), all |q|=1 forces n=(1,1,1,1), N=4. Increasing link-spin truncation alone does not change this. Record the correction explicitly; do not publish the contradictory required paragraph as true.
3. Manifest hashes payload files. External receipt verifies MANIFEST.json, its sidecar and the final SELFTEST.json. No self-referential SHA-256 requirement. Automated archive verification checks the precisely declared payload/control-file partition.
4. User additionally permits a top-level tools/ compatibility directory containing the originals linked by the unchanged legacy inventory.
5. The follow-up cleanliness question timed out without an answer. No relaxation of the acceptance-table Cleanliness row is assumed (the question's R26 label was erroneous; this prompt has rulings through R19). The question also incorrectly characterized the pre-existing changes; the saved Git baseline, not that characterization, is authoritative.

Other preflight facts:
- AST scan: 23 Python modules, 95 public top-level functions in the Section-8 su2qc package. Public classes/methods/imported callables still require classification before final coverage count.
- Existing diagnostic ZIP is 23,283,552 compressed bytes, 201,538,582 expanded bytes. The prompt's approximate 195 MB refers to expanded contents, not compressed ZIP size. Record both sizes for the query bundle.
- Pre-existing untracked paths: artifacts/SU2ZX_latest_update_723d083_complete.zip; prompts/gi_cost_campaign_v.0.6.2.md; prompts/gi_cost_campaign_v.0.6.3.md; runs/campaign_v060/sessions/c060_p0_20260908_3/. Preserve prior user work; scoped commits must not silently absorb it. New prompt may be included as this task input. Literal clean status may remain unmet without further disposition.
- No repository-local SOUL.md exists; no outside-root access attempted.
- Fable's separate per-model usage meter is not the percentage of the shared weekly allocation. Do not repeat the prior conflation.
