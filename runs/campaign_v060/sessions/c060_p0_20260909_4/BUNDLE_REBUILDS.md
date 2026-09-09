# Bundle rebuild record (R18/R19)

Every build is kept under its own timestamped name; no failed archive was
overwritten. Self-test results are read back out of each archive's own
`SELFTEST.json`.

| Archive (`zip_results/`) | Bytes | R19 result | Why it was rebuilt |
|---|---:|---|---|
| `SU2ZX_QUERY_2166dd4_20260909T190552Z.zip` | 481911 | FAIL (check 2: 22 dangling links) | `docs/SU2QC_FUNCTION_INVENTORY.md` was never added to the payload; `ASK.md` routed to `docs/CLAIMS.md` and to a `path:line` string; the archived package sat at `src/src/su2zx/` and its tests were absent, so the carried inventory's `../src/` and `../tests/` links did not resolve; `EXCLUSIONS.md` was rendered before exclusions were collected and shipped with an empty table; `figures/` was missing entirely. |
| `SU2ZX_QUERY_2166dd4_20260909T193333Z.zip` | 1771215 | FAIL (check 2: 48 dangling links) | Layout and content repaired, but backticked bundle paths in `docs/GATE_MAP.md` were resolved against the document's own directory instead of the archive root, and the AST-generated `su2qc` inventory's `../runs/section8.../` links had no target in the archive. |
| `SU2ZX_QUERY_2166dd4_20260909T193441Z.zip` | 1834914 | PASS (all five) | Superseded: the exclusions document asserted a credential screen the builder did not run, and `docs/CODE_MAP.md` described a link-mapping scheme that was never implemented. |
| `SU2ZX_QUERY_2166dd4_20260909T193542Z.zip` | 1835117 | PASS (all five) | Superseded: `docs/CODE_MAP.md` did not yet say that evidence cited by repository path is packaged flat under `evidence/`. |
| `SU2ZX_QUERY_2166dd4_20260909T193730Z.zip` | 1835249 | PASS (all five) | Superseded: built by scripts that lived only in ignored scratch, so the documented rebuild command was not reproducible from a clean checkout. |
| `SU2ZX_QUERY_2542af2_20260909T194325Z.zip` | 1835248 | **PASS (all five)** | Shipped build, from the tracked tools at commit `2542af2`. SHA-256 in the `.sha256` sidecar. |

Rebuild from a clean shell, from the repository root:

```
python3 runs/campaign_v060/sessions/c060_p0_20260909_4/tools/build_bundle.py && python3 runs/campaign_v060/sessions/c060_p0_20260909_4/tools/selftest_bundle.py
```

The builder refuses to overwrite an existing archive name; the self-test always
runs against the newest `zip_results/SU2ZX_QUERY_*.zip`, extracts it to
`.work/c063_bundle_scratch/extract`, and writes `SELFTEST.json` back into both
the archive and this session directory together with a `.receipt.json` and a
`.sha256` sidecar.
