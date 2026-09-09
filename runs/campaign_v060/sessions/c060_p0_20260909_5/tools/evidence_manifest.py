"""Write the C0 evidence manifest (R11 step 3): SHA-256 of every cited file.

Run from the repository root after the ledger and state rows are written and
before the review. Any later write to a manifested file invalidates it.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd().resolve()
TAG = "c060_p0_20260909_5"
SESSION = ROOT / "runs/campaign_v060/sessions" / TAG

CITED = [
    # gate output
    f"runs/campaign_v060/sessions/{TAG}/gate_C0.xml",
    f"runs/campaign_v060/sessions/{TAG}/gate_C0.log",
    # row evidence
    f"runs/campaign_v060/sessions/{TAG}/twin-row-calibrated.json",
    f"runs/campaign_v060/sessions/{TAG}/seed-mechanism.json",
    f"runs/campaign_v060/sessions/{TAG}/v10-prefix-baseline.json",
    f"runs/campaign_v060/sessions/{TAG}/ruling-R9-closure-residual.md",
    f"runs/campaign_v060/sessions/{TAG}/SESSION_SUMMARY.md",
    f"runs/campaign_v060/sessions/{TAG}/slope-conditioning.json",
    f"runs/campaign_v060/sessions/{TAG}/seed-mechanism.json",
    f"runs/campaign_v060/sessions/{TAG}/v040-seed-pattern-finding.md",
    # campaign state of record
    "runs/campaign_v060/GATE_LEDGER.jsonl",
    "runs/campaign_v060/CAMPAIGN_STATE.json",
    "runs/campaign_v060/GATE_THRESHOLDS.yaml",
    "runs/campaign_v060/PREREGISTRATION.md",
    "runs/campaign_v060/CLAIM_TABLE.md",
    # the tests that produced the rows, and the repaired module
    "runs/campaign_v060/tests/gate_C0/conftest.py",
    "runs/campaign_v060/tests/gate_C0/test_twin_variance.py",
    "runs/campaign_v060/tests/gate_C0/test_estimator.py",
    "runs/campaign_v060/tests/gate_C0/test_v1_regression.py",
    "runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py",
    "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
]


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main() -> int:
    rows, missing = [], []
    for rel in CITED:
        path = ROOT / rel
        if path.is_file():
            rows.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path)})
        else:
            missing.append(rel)
    manifest = {
        "tag": TAG,
        "files": rows,
        "missing": missing,
        "note": "Hashes are of the snapshot the review and sign-off read. "
                "Any write to a listed file after this point invalidates the manifest.",
    }
    body = json.dumps(manifest, indent=2, sort_keys=True).encode()
    (SESSION / "evidence-manifest.json").write_bytes(body)
    (SESSION / "evidence-manifest.json.sha256").write_text(
        hashlib.sha256(body).hexdigest() + "  evidence-manifest.json\n")
    print(json.dumps({"listed": len(rows), "missing": missing,
                      "manifest_sha256": hashlib.sha256(body).hexdigest()}, indent=2))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
