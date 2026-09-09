# C1 amendment, prepared text (R12), not yet applied

Applied only after the C0 gate rows, ledger and state are written, so that the
preregistration hash recorded as "of record" is the one that exists after this
amendment.

## Hash block to inline into PREREGISTRATION.md

Verified on this snapshot before amending:

| file | SHA-256 (first 16) | recorded where |
|---|---|---|
| GATE_THRESHOLDS.yaml | a7d1135ebd09c2a3 | CAMPAIGN_STATE.hashes.thresholds, matches |
| PREREGISTRATION.md (pre-amendment) | b587c4859c16ec44 | CAMPAIGN_STATE.hashes.preregistration, matches |
| 00_conventions.md | d7de725c3895d5f5 | CAMPAIGN_STATE.hashes.conventions, matches |
| src/su2qc/conventions.py | fb3b7525b1a1d69b | PREREGISTRATION "Conventions SHA-256", matches |

## The conventions-hash ambiguity, resolved

Both recorded values are correct and neither is wrong; they hash different
files. The state file's `hashes.conventions` is the campaign conventions
document `runs/campaign_v060/00_conventions.md`. The preregistration's
"Conventions SHA-256" is the frozen code module
`runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py`. The amendment
records both under labelled keys in both files, so the ambiguity cannot recur:

- `conventions_md` for the campaign document
- `conventions_py` for the frozen module

## Prespecified defect classes to add

Carried from the v0.5.0 Phase 5 list, plus:

- KR K-scan changes after a Hamiltonian fix, rerun V8, new C3 row.
- Twin seed derivation changes, rerun V10, new C0 row. This class is what the
  present session exercised: the derivation moved from `seed + k` to spawned
  seeds, so V10 was rerun and a new C0 row was written.

## One-line reasons to add to R1, R3, R4

- R1: a log-slope has no meaningful 1e-12 stability criterion, so the primary
  arrays carry the 1e-12 comparison and the slope carries a propagated bound.
- R3: orthogonal distance regression closure needs the full error model, which
  does not exist before Phase 5, so it is a V12 sub-row rather than a C0 row.
- R4: a twin whose repeats are seeded by increment cannot produce an
  independent-repeat sigma, so the seed derivation is part of the acceptance
  rather than an implementation detail.
