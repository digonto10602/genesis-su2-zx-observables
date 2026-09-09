# REVIEW / D1 — `tools/function_inventory.py` — **FAIL**

Implementation is largely sound and the AST-only property is well demonstrated, but three containment/stability gaps and one evidence gap block a PASS.

## Blockers

**B1. Legacy byte-identity is asserted, not evidenced.**
`inventory-verification.json` claims `legacy_byte_identical: true` with a SHA-256, but it is a hand-written artifact. The only execution evidence supplied is `inventory-green.log` (3 tests, OK), and none of the three tests exercises the default no-argument invocation or compares the regenerated `docs/CODE_FUNCTION_INVENTORY.md` against the committed one. Per D1 criteria, review cannot substitute for the test. Add a test that runs the script with no arguments into a scratch base and diffs the bytes, or supply the generating command and diff output.

**B2. No test for the new `gates` root.**
The new behavior is `TEST_DIRECTORIES = tuple(d for d in DIRECTORIES if (ROOT / d).name in {"tests", "gates"})`. `inventory-verification.json` claims assertion extraction on gates for 34 files, but no supplied test asserts that a `--roots gates` run emits `Decorator:` lines and the ```` ```python ```` assertion block, nor that a non-test root suppresses them. This is exactly the "test assertions for new roots" item in scope and it is uncovered. Also untested: `--roots` deduplication, and rejection of an `--output` that escapes the project.

**B3. Symlinked *directories* bypass the symlink guard.**
The pre-parse scan rejects only `candidate.is_symlink()` for `*.py` files. A symlinked subdirectory under a selected root is not itself matched by `rglob("*.py")`, and whether `rglob` descends into it is Python-version dependent (`recurse_symlinks` defaults changed in 3.13). On affected interpreters, out-of-root sources are parsed and emitted with lexically-in-root relative links, defeating the containment check. Reject any symlinked component, e.g. scan `selected.rglob("*")` and error on `is_symlink()` regardless of type, or resolve each candidate and re-check `is_relative_to`.

**B4. Non-default base can clobber the committed legacy inventory.**
`main()` writes to `docs/CODE_FUNCTION_INVENTORY.md` whenever `OUTPUT` equals that literal string, independent of `ROOT`. So `--base /tmp/x --output docs/CODE_FUNCTION_INVENTORY.md` overwrites the shipped artifact with foreign content. Given the campaign's "never overwrite historical results" rule this is a real hazard. Remove the string comparison from `main()`: have `main()` return text only, and let the caller write to `destination` unconditionally.

## Suggestions (non-blocking)

- `selected.resolve()` is compared against a possibly-unresolved `ROOT = project_path(arguments.base)`. If either path traverses a symlink the lexical `is_relative_to` can misjudge in both directions. Resolve the base once and compare resolved-to-resolved.
- Output containment rests entirely on unverified `project_path` semantics; `Path(root) / absolute` discards the left operand under pathlib, so an absolute `--output` may escape. Validate `destination.resolve().is_relative_to(project_root)` explicitly.
- `main()` reading module globals makes it untestable in-process and impure. Prefer explicit parameters with the globals as defaults; the "config below main" trick that preserves `main`'s `lineno` and call-expression set is clever and does hold, but it should be pinned by B1's test rather than by a comment.
- Tests require a pre-existing `ROOT/.work`; create it in `setUpClass`.
- Minor TOCTOU between the symlink scan and parsing in `main()`.

## Confirmed good

AST-only with no execution of scanned sources (the `raise RuntimeError` sentinel probe is a strong check); no archived-package import; validation and `parser.error` precede any write, so failures leave no partial output; `__pycache__` skipped with `PYTHONDONTWRITEBYTECODE=1`.

Not physics sign-off.
