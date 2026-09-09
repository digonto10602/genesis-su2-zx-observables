"""Apply the C1 amendment (R12). Run from the repository root, after the C0 gate.

Inlines the three SHA-256 values, resolves the conventions-hash ambiguity under
labelled keys in both files, adds the prespecified defect classes and the R1/R3/R4
reasons, re-hashes, and records gates.C1 = pass (amended) with old and new hashes.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
CAMPAIGN = ROOT / "runs/campaign_v060"
PREREG = CAMPAIGN / "PREREGISTRATION.md"
STATE = CAMPAIGN / "CAMPAIGN_STATE.json"
THRESHOLDS = CAMPAIGN / "GATE_THRESHOLDS.yaml"
CONV_MD = CAMPAIGN / "00_conventions.md"
CONV_PY = ROOT / "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py"
UTC = dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


AMENDMENT = """
## Amendment, {utc}

Amended under ruling R12. The campaign's C0 gate was rerun after the twin seed
derivation was repaired; this amendment records the hashes of record, resolves
the conventions-hash ambiguity, and adds the defect class that the repair
exercised. No threshold, band, coupling, Hamiltonian, Gauss-law convention,
observable definition or acceptance criterion is changed by it.

### Hashes of record

| item | file | SHA-256 |
|---|---|---|
| thresholds | `runs/campaign_v060/GATE_THRESHOLDS.yaml` | `{thresholds}` |
| conventions_md | `runs/campaign_v060/00_conventions.md` | `{conv_md}` |
| conventions_py | `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py` | `{conv_py}` |
| preregistration, before this amendment | `runs/campaign_v060/PREREGISTRATION.md` | `{prereg_old}` |

The preregistration of record is this file *after* the amendment; its hash is
written into `CAMPAIGN_STATE.json` as `hashes.preregistration` by the same
tool that appended this section, and the pre-amendment value above is retained
so the change is auditable.

**Conventions-hash ambiguity, resolved.** The state file and this document
recorded different values under the same name. Both were correct and neither
was stale: they hash different artifacts. The campaign conventions *document*
is `00_conventions.md`; the frozen conventions *module* is `conventions.py`.
Both are now carried under the labelled keys `conventions_md` and
`conventions_py` in this file and in the state file, so the ambiguity cannot
recur.

### Prespecified defect classes

Carried from the v0.5.0 Phase 5 list, plus:

- A KR K-scan change after a Hamiltonian fix requires V8 to be rerun and a new
  C3 row written.
- **A change to the twin seed derivation requires V10 to be rerun and a new C0
  row written.** This class is not hypothetical: it is what the session of
  {utc} exercised. The derivation moved from `seed + k`, which reproduced one
  shot stream offset by a single draw, to seeds spawned from a seed sequence,
  so V10 was rerun end to end and a new C0 row was recorded.

### Reasons added to R1, R3 and R4

- **R1.** A fitted log-slope has no meaningful 1e-12 stability criterion, so the
  primary error arrays carry the 1e-12 comparison and the slope carries a
  first-order propagated bound instead.
- **R3.** Orthogonal-distance-regression closure needs the full error model,
  which does not exist before Phase 5, so it is a V12 sub-row rather than a C0
  row and is recorded as deferred, never as a failure.
- **R4.** A twin whose repeats are seeded by increment cannot produce an
  independent-repeat sigma at all, so the seed derivation is part of the V10
  acceptance rather than an implementation detail beneath it.
"""


def main() -> int:
    prereg_old = sha(PREREG)
    body = AMENDMENT.format(utc=UTC, thresholds=sha(THRESHOLDS), conv_md=sha(CONV_MD),
                            conv_py=sha(CONV_PY), prereg_old=prereg_old)
    PREREG.write_text(PREREG.read_text().rstrip("\n") + "\n" + body)
    prereg_new = sha(PREREG)

    state = json.loads(STATE.read_text())
    hashes = state.setdefault("hashes", {})
    hashes["thresholds"] = sha(THRESHOLDS)
    hashes["conventions_md"] = sha(CONV_MD)
    hashes["conventions_py"] = sha(CONV_PY)
    hashes.pop("conventions", None)
    hashes["preregistration"] = prereg_new
    state["gates"]["C1"] = {
        "status": "pass (amended)", "utc": UTC,
        "preregistration_sha256_before": prereg_old,
        "preregistration_sha256_after": prereg_new,
        "evidence": "runs/campaign_v060/PREREGISTRATION.md; CLAIM_TABLE.md; "
                    "GATE_THRESHOLDS.yaml; hashes in CAMPAIGN_STATE.json",
    }
    STATE.write_text(json.dumps(state, indent=2) + "\n")

    with (CAMPAIGN / "GATE_LEDGER.jsonl").open("a") as fh:
        fh.write(json.dumps({
            "gate": "C1", "item": "preregistration amended", "pass": True, "rule": "R12",
            "utc": UTC, "session": "c060_p0_20260909_5",
            "value": {"preregistration_before": prereg_old,
                      "preregistration_after": prereg_new,
                      "conventions_md": hashes["conventions_md"],
                      "conventions_py": hashes["conventions_py"],
                      "thresholds": hashes["thresholds"],
                      "note": "Hashes inlined, conventions ambiguity resolved under "
                              "labelled keys, twin-seed-derivation defect class added."},
            "evidence": "runs/campaign_v060/PREREGISTRATION.md",
        }) + "\n")

    print(json.dumps({"preregistration_before": prereg_old,
                      "preregistration_after": prereg_new,
                      "hashes": hashes}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
