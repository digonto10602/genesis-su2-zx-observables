# Execution map (documentation only)

Wall times are copied from prior logged diagnostics; no new measurement was run. `UNKNOWN` marks values with no recorded source. No GPU, hardware or QPU job is documented here.

| probe | exit | seconds | evidence/log | notes |
|---|---:|---:|---|---|
| baseline-C0 | 1 | 181.7 | baseline-C0.log | /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.work/c062_diagnostics/SU2ZX |
| baseline-G1 | 0 | 123.8 | baseline-G1.log | /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.work/c062_diagnostics/SU2ZX/runs/section8_v0.5.0_20260907T0628Z |
| baseline-G2 | 0 | 2.3 | baseline-G2.log | /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.work/c062_diagnostics/SU2ZX/runs/section8_v0.5.0_20260907T0628Z |
| baseline-G3 | 0 | 404.9 | baseline-G3.log | /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.work/c062_diagnostics/SU2ZX/runs/section8_v0.5.0_20260907T0628Z |
| baseline-regression | 0 | 508.8 | baseline-regression.log | /home/digimonk/Projects/SU2ZX_Foundation_Code_Package/SU2ZX/.work/c062_diagnostics/SU2ZX/runs/section8_v0.5.0_20260907T0628Z |
| seed run seed-diagnosis.json r=0 | n/a | 32.3 | seed-diagnosis.json | 4000 |

Known timeouts (recorded, not re-measured): r=1 seed diagnosis exceeded a 2400 s cap and exited 124 with no completed counts.

## Scratch sandboxes, deleted 2026-09-09

The `.work/` sandboxes named in the table above — `c062_diagnostics`,
`c060_p0_legacy_baseline`, `c060_p0_repair_snapshot` and `c060_p0_final_sandbox`
— were deleted from disk at the user's request during the repository cleanup of
2026-09-09, reclaiming about 597 MB. They were isolated working copies of
`runs/section8_v0.5.0_20260907T0628Z/`, created so that regressions could run
without writing over committed evidence. Their measured outputs are the logs and
JSON files in the session directories, which are committed; the sandboxes
themselves held no unique evidence. To rerun any probe, make a fresh copy of the
committed run directory rather than expecting these paths to exist.
