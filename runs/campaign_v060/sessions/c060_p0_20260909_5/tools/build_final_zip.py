"""Zip the session's final report and the evidence it cites."""
import hashlib, json, subprocess, zipfile, datetime as dt
from pathlib import Path

ROOT = Path.cwd().resolve(); TAG = "c060_p0_20260909_5"
S = ROOT / "runs/campaign_v060/sessions" / TAG
OUT = ROOT / "zip_results"
UTC = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
COMMIT = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()

REPORT = ["FINAL_REPORT.md", "SESSION_SUMMARY.md", "plan.md",
          "ruling-R9-closure-residual.md", "physics-check-variance.md",
          "c2-prep-note.md", "v040-seed-pattern-finding.md", "review-brief.md",
          "c1-amendment-prepared.md", "ruling-empty-repeat-bootstrap.md"]
EVIDENCE = ["twin_variance.json", "twin-row-calibrated.json", "seed-mechanism.json",
            "v10-prefix-baseline.json", "slope-conditioning.json",
            "gate_C0.xml", "gate_C0.log", "gate_C0_V10_128shots.xml", "v10-128shots.log",
            "gate_C0-aborted-1024shots.log", "evidence-manifest.json",
            "evidence-manifest.json.sha256", "git-status-final.txt", "gate-census.json"]
CAMPAIGN = ["GATE_LEDGER.jsonl", "CAMPAIGN_STATE.json", "GATE_THRESHOLDS.yaml",
            "PREREGISTRATION.md", "CLAIM_TABLE.md"]
TESTS = ["test_twin_variance.py", "test_estimator.py", "test_v1_regression.py",
         "test_jmax1_counts.py", "conftest.py"]


def add_all(z, rows):
    manifest = []
    for arc, path in rows:
        if not path.is_file():
            continue
        data = path.read_bytes()
        z.writestr(arc, data)
        manifest.append({"path": arc, "bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest()})
    return manifest


def main():
    OUT.mkdir(exist_ok=True)
    name = f"SU2ZX_C0_REPORT_{COMMIT}_{UTC}.zip"
    rows = []
    rows += [(f"report/{n}", S / n) for n in REPORT]
    rows += [(f"evidence/{n}", S / n) for n in EVIDENCE]
    rows += [(f"campaign/{n}", ROOT / "runs/campaign_v060" / n) for n in CAMPAIGN]
    rows += [(f"tests/{n}", ROOT / "runs/campaign_v060/tests/gate_C0" / n) for n in TESTS]
    rows += [("src/twin.py", ROOT / "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py")]
    rows += [(f"c2_prep/{p.name}", p) for p in sorted((S / "c2_prep").glob("*.json"))]
    rows += [("prompts/gi_cost_campaign_v.0.6.4.md", ROOT / "prompts/gi_cost_campaign_v.0.6.4.md")]

    path = OUT / name
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        manifest = add_all(z, rows)
        z.writestr("MANIFEST.json", json.dumps(
            {"commit": COMMIT, "built_utc": UTC, "session": TAG,
             "gate_C0": "PARTIAL", "files": manifest}, indent=2))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    (path.with_suffix(".sha256")).write_text(digest + "  " + name + "\n")
    print(json.dumps({"archive": str(path), "bytes": path.stat().st_size,
                      "files": len(manifest) + 1, "sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
