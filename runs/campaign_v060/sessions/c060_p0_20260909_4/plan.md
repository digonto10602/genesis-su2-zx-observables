Planning pass only, from the supplied sources; no tools, no file edits.

# Plan · c060_p0_20260909_4 · documentation-only v0.6.3

## 0. Authority and scope

- Authorized: R13–R19 documentation and packaging work, generator scope repair, Graphify AST refresh, query bundle. User clarifications 1–5 override conflicting prompt text.
- Prohibited (stop conditions): any edit under `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/`, any edit to `runs/campaign_v060/tests/gate_C0*`, any C0/G1–G3 run or re-gate, any C1 or `PREREGISTRATION.md` change, hardware, push, threshold/band/seed/channel/Hamiltonian change, any optional Fable call.
- This plan is a documentation deliverable. REVIEW of documents is permitted. Campaign physics sign-off (C0 PASS, σ validity, repair acceptance) is not in scope and no document may imply it.
- Inherited reference "R26" does not exist in v0.6.3 (rulings run R13–R19). By named topic it resolves to §2 step 1 and the §3 "Cleanliness" row. It stays **blocked** while the four pre-existing untracked entries remain; see D6.

## 1. Goals

1. Repair `tools/function_inventory.py` scope without forking, with byte-identical legacy output.
2. Author `docs/SU2QC_CONTRACTS.md` (corrected R15), `docs/SU2QC_LOGIC_AND_TESTS.md` (R14), `docs/SU2QC_FUNCTION_INVENTORY.md` (R13).
3. Refresh Graphify with `su2qc` in corpus; resolve or retire the 11 out-of-corpus nodes; label staleness on the report's first screen.
4. Build `zip_results/SU2ZX_QUERY_<commit>_<UTC>.zip` with the R18 layout, payload manifest, exclusions, and a passing `SELFTEST.json` under the clarified payload/control partition.
5. Scoped commits that absorb none of the four pre-existing untracked entries.

## 2. Exact acceptance criteria

| Row | PASS requires | Evidence (this session) |
|---|---|---|
| A1 Generator legacy invariance | `git diff --no-index <(git show HEAD:docs/CODE_FUNCTION_INVENTORY.md) docs/CODE_FUNCTION_INVENTORY.md` is empty after regeneration with the modified generator. | `inventory-legacy.diff` (empty), command log |
| A2 su2qc inventory | `docs/SU2QC_FUNCTION_INVENTORY.md` emitted by the same generator; per-entry schema identical (linked path, module docstring, `### sig — line N`, docstring, sorted `Direct call expressions`, disclaimer verbatim); all 23 modules present; test-assertion blocks emitted for su2qc test directories. | file, module count log |
| A3 Contracts | One entry per public callable (95 top-level functions preliminary; public classes/methods/imported callables classified and counted before the final number). Each entry has inputs, outputs, invariants, side effects, empty/degenerate behaviour, enforcing test or `UNENFORCED`, derived from source lines. No generic filler. Mandatory entries per §4 with the R15 meson correction recorded. | `docs/SU2QC_CONTRACTS.md`, coverage count in summary |
| A4 Logic doc | Mermaid flow for the Section-8 pipeline renders; every one of the 23 modules narrated; each claim cites `path:line`; no numbers restated. | `docs/SU2QC_LOGIC_AND_TESTS.md` |
| A5 Status integrity | Grep of new docs and bundle top-level files shows no upgraded status; `INDEX.md` lines 1–10 state: bundle purpose, not-a-gate/not-a-sign-off/no-hardware, commit, UTC, triple "C0 PARTIAL / C1 unamended / C2 NOT STARTED", and the σ-void sentence. All noisy numbers labelled EMULATED. | `CLAIMS.md`, `INDEX.md`, status-grep log |
| A6 Graph | Before/after node/edge/community counts recorded; `su2qc` paths present in `graph.json`; the 11 nodes resolved or listed as retired in `GRAPH_REPORT.md`; staleness sentence on first screen. | `graph-counts-before.json`, `graph-counts-after.json`, `GRAPH_REPORT.md` |
| A7 Bundle | Compressed ZIP ≤ 25 MB target, ≤ 30 MB hard cap; expanded size also recorded; top-level layout exactly R18 plus the user-approved `tools/` compatibility directory; every exclusion has path, size, SHA-256, reason class. | `MANIFEST.json`, `EXCLUSIONS.md`, `bundle-sizes.json` |
| A8 Self-test | All five R19 checks pass on the extracted archive under the clarified partition (payload hashed in manifest; `MANIFEST.json`, `MANIFEST.sha256`, `SELFTEST.json` hashed only in the external receipt). Final extract-and-recheck matches. | `SELFTEST.json`, `bundle-receipt.json` |
| A9 Legacy docs carried | `CODE_FUNCTION_INVENTORY.md`, `CODE_LOGIC_AND_TESTS.md`, `V040_COMPLETION_AUDIT.md`, `REFERENCES.md` byte-identical to HEAD inside the bundle; their existing relative links resolve via alias paths, not rewrites. | SHA comparison log, link check |
| A10 Cleanliness | Scoped commits made; `git status` shows only the four pre-existing untracked entries plus this session directory. Literal "clean" row is **blocked, not fail**, pending the user's disposition. | `git-status-final.txt` |

No row may cite a prior session's artifact as its own evidence; prior-session JSONs are cited by the documents as evidence *for claims*, which is different.

## 3. R13 generator design constraints (BUILD must honour)

The generator inventories itself because `tools` is a legacy root. Invariants for A1:

- `def main` stays at line 10 with signature `main()`; no new function or class anywhere under `src/`, `tests/`, `tools/`.
- The set of direct call expressions inside `main` is unchanged, including the literals `project_path('docs/CODE_FUNCTION_INVENTORY.md').write_text`, `', '.join`, `'\n'.join`.
- Recommended mechanism (record the choice): module-level configuration names (`ROOT`, `DIRECTORIES`, `TEST_DIRECTORIES`, `OUTPUT`) placed **after** `main`; `main` reads them, keeps the guarded literal legacy write, and returns the text; the `if __name__` block parses `sys.argv` without defining functions and writes non-default outputs. Any `import sys` goes on an existing import line or after `main`, so line 10 holds.
- `directory == "tests"` becomes membership in `TEST_DIRECTORIES` (no new call); gate scripts under `gates/` are configurable as test-like.
- Root set for su2qc: `runs/section8_v0.5.0_20260907T0628Z/{src,tests,gates}`. AST parse only; no import of `su2qc`.
- Link resolution: the repo copy links `../runs/section8.../…`. The bundle copy is produced by a second, logged invocation with root set to the run directory so links resolve to `../src/…` inside the bundle. The two copies differ only in link prefix; `CODE_MAP.md` records this. Alternative if the user prefers a single copy: mirror the run-relative alias tree in the bundle (costs duplicate source).
- Session-local scripts only: bundle builder, self-test, link checker, credential screen wrapper live under `runs/campaign_v060/sessions/c060_p0_20260909_4/tools/`, never under legacy roots.

## 4. R15 mandatory entries, as to be recorded

| Callable | Status to record |
|---|---|
| `run_counts` (`twin.py:54-63`) | Seeds `seed + k`; shift-by-one memory equality MEASURED (cite `seed-diagnosis.json`, `equal-seed-control.json`); `repeats are independent` **VIOLATED**; `sim.set_options` mutates caller state (MEASURED 101→500, persists); re-transpile per circuit with fixed `seed_transpiler`; repair `PROPOSED, NOT IMPLEMENTED — blocked on Fable`. |
| `channel_weights` / `channel_closure_residual` (`:105-143`) | Closure identity stated. **Correction (clarification 2):** with n ∈ {0,1,2} and `N_VAC=(0,2,0,2)`, all |q_v|=1 forces n=(1,1,1,1), N=4, Σq=0; the prompt's Σq ∈ {0,±2,±4} hazard is not realizable in this occupation domain, and raising link-spin truncation alone does not change it. Record the prompt paragraph as superseded, keep the 82-code exhaustive check as consistent MEASURED evidence (`oracle-diagnostics.json`); no channel-definition change. |
| `channel_closure_residual` invalid keys | Both sides skip `decode is None`; rejected code contributes zero residual (MEASURED: code 1, weight 0.25, residual 0.0). R9 nonzero demand **UNSATISFIABLE AS WRITTEN**, awaiting ruling. |
| `physical_yield` vs `postselect` (`:152-155` vs `:66-69`) | Empty input: `ZeroDivisionError` vs `({}, 0.0)`; **UNENFORCED**. |
| `bootstrap` (+ `observables`, `matched_subtraction`, `postselect`, `twin_backend`, `add_measurements`) | Full entries; bootstrap 2σ is over `counts_list` elements and is an uncertainty **only** under independence, which `run_counts` violates. |

## 5. Lanes

**BUILD (Codex).** D1 generator; session-local bundle builder, self-test, link checker, credential-screen wrapper (reuse the v0.6.2 screen invocation verbatim); stratified 500-row samplers for `tn_all_runs.csv` and `tn_scaling.csv`; head/tail excerpt writer for >2 MB evidence; `EXCLUSIONS.md` generator that hashes only *candidate research artifacts* it enumerates by listing, treating `.git/`, `.mamba/`, `.work/`, nested archives and credential-pattern matches as **directory/policy-scope exclusions recorded without reading**.

**PHYSICS-as-documentation (Opus).** First drafts of `SU2QC_CONTRACTS.md`, `SU2QC_LOGIC_AND_TESTS.md`, `PHYSICS_SPEC.md` from `conventions.py`, `twin.py`, `l12`, `ham/*`, `circuits/*`. The proposal excerpt is historical context for contract wording only. Output is contract text with `path:line` citations; no status upgrades.

**TEST-BENCH (mechanical Python, ≤ 2 NIM workers, no NIM required).** A1 diff; schema comparison of the two inventories; module/callable coverage counts; Graphify counts before/after; bundle build; extract to `.work/`; five R19 checks; final extract/recheck; receipt. Output redirected to the session directory; no v0.5.0 run-directory outputs touched.

**REVIEW (Opus).** Document review against source for every mandatory entry and every `CLAIMS.md` row; status-vocabulary grep; link-check confirmation; confirmation that no document implies a pass, valid σ, or existing repair. This is documentation review, not campaign sign-off. No Fable doc-verification call is required by this plan; it remains a user-invocable allowance, DEFERRED.

## 6. Gate schedule

| Gate | Content | PASS |
|---|---|---|
| D0 Boot (≤ 20 min) | Session tag, read `CAMPAIGN_STATE.json` and the four issue reports; `ENV.md` (done), `TIME_LEDGER.md`, `RESUME_LOCK`; baseline `git status` recorded and compared to the four known untracked entries. | Any unexpected modified/deleted path → stop and report before touching anything. |
| D1 Generator | A1 first, then A2. Commit `docs: extend function inventory to su2qc package`. | A1 empty diff; 60 min limit then fallback (§7). |
| D2 Contracts, then D3 Logic | Opus drafts → Codex fixes citations → REVIEW. | A3, A4. |
| D4 Graph | `.mamba/bin/graphify update .` with su2qc in corpus; counts; 11-node disposition; staleness sentence. | A6. Commit graph refresh as a scoped commit (dirty graphify-out from this step is session work, not pre-existing). |
| D5 Bundle + self-test | Build → manifest → zip → extract → self-test → append deterministic `SELFTEST.json` → final extract/recheck → external receipt. Each rebuild keeps the failed archive under a suffixed name in `zip_results/`. | A7, A8, A9. |
| D6 Commit and close | Scoped commits for docs, generator, graph, session directory. `git-status-final.txt`. Summary per prompt §5, plus corrected-R15 note and receipt hashes. | A10 recorded as **blocked** on the four entries unless the user rules. |

## 7. Stop conditions

- A1 non-empty diff not fixed within 60 min → ship su2qc inventory as a separate invocation; record non-reproducibility as a finding; do not touch the expectation.
- Dangling link, manifest mismatch, compileall failure → fix and rebuild; never describe the archive as complete with any failing check.
- Compressed size > 30 MB → exclude further with hash/size/reason; no compression tuning.
- Any contract found violated by code → the violated contract is the deliverable; no wording that implies satisfaction.
- Any credential-pattern hit inside a candidate file → exclude, record pattern class only, never the content.
- Any prohibited-scope temptation (twin.py edit, gate run, C1 edit, Fable optional call) → stop.
- Hard cutoff 2026-09-10T00:24:32Z → ship what passes self-test, mark the rest `partial`, `next_action` verbatim.

## 8. Unknowns flagged (not resolvable from supplied sources)

- Existence/contents of `tests/` and `gates/` under the run directory and whether `gates/` holds `.py` files.
- Whether the 23-module count includes `__init__.py`; final public-callable count pending class/method classification.
- Location and tracked status of `seed-diagnosis.json`, `equal-seed-control.json`, `oracle-diagnostics.json`, `diagnostic-source-manifest.json` (assumed under the untracked session 3 directory; bundle copies them verbatim under `sessions/`).
- Which tool constituted the v0.6.2 credential screen; reuse its recorded command.
- Size of `graph.json`; if > 2 MB, include it under `graph/` (R18 lists it explicitly) and note the evidence-file cap applies to `evidence/` only.
- Whether `zip_results/` is gitignored; verify before D5.
- Measured wall times for `EXECUTION_MAP.md` must come from existing logs; missing values are `UNKNOWN`, never measured by new runs.
- Which size (compressed or expanded) the prompt's ≤ 25 MB targets; plan gates on compressed and records both.

## 9. Standing statement

Fable planning/escalation and final sign-off remain DEFERRED under budget policy; C0 is PARTIAL, C1 is unamended, C2 is NOT STARTED; no production physics fix was implemented; no hardware job has ever been submitted; every v0.5.0 twin σ is void.
