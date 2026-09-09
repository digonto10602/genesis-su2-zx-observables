"""Write the C0 gate ledger rows and campaign state (R11 step 2).

Reads the gate XML and this session's evidence, derives each row's verdict from
the measured artifacts, and refuses to record a pass it cannot substantiate.
Run from the repository root after the gate command, before the manifest.
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path.cwd().resolve()
TAG = "c060_p0_20260909_5"
SESSION = ROOT / "runs/campaign_v060/sessions" / TAG
CAMPAIGN = ROOT / "runs/campaign_v060"
UTC = dt.datetime.now(dt.timezone.utc).isoformat()


def load_xml():
    root = ET.parse(SESSION / "gate_C0.xml").getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    cases = {}
    for case in suite.iter("testcase"):
        name = f"{case.get('classname','')}::{case.get('name')}"
        failed = any(child.tag in ("failure", "error") for child in case)
        skipped = any(child.tag == "skipped" for child in case)
        cases[name] = "fail" if failed else ("skip" if skipped else "pass")
    return {
        "tests": int(suite.get("tests", 0)),
        "failures": int(suite.get("failures", 0)),
        "errors": int(suite.get("errors", 0)),
        "skipped": int(suite.get("skipped", 0)),
        "time": float(suite.get("time", 0.0)),
        "cases": cases,
    }


def by_file(cases, needle):
    return {k: v for k, v in cases.items() if needle in k}


def main() -> int:
    xml = load_xml()
    cases = xml["cases"]
    variance = json.loads((SESSION / "twin-row-calibrated.json").read_text())
    slopes = json.loads((SESSION / "slope-conditioning.json").read_text())
    prefix = json.loads((SESSION / "v10-prefix-baseline.json").read_text())

    def all_pass(needle):
        rows = by_file(cases, needle)
        return bool(rows) and all(v == "pass" for v in rows.values())

    v10_rows = {r: variance[r] for r in ("0", "1") if r in variance}
    # V10 is judged here, not by a gate test: the R8 test could not run to
    # completion at R8's own shot count (see the calibration below).
    v10_r0_ok = variance["0"]["distinct_dictionaries"] == 5
    v10_r1_measurable = variance["1"]["N_kept_mean"] >= 1.0
    rows = [
        {
            "gate": "C0", "item": "V1 restored evidence and conditioned slopes",
            "pass": all_pass("test_v1_regression"), "rule": "R1/R10",
            "value": {
                "observables": {row["observable"]: {
                    "slope": row["slope_stored"],
                    "max_error_array_delta": row["max_error_array_delta"],
                    "propagated_abs_bound": row["propagated_abs_bound"],
                    "measured_slope_delta": row["measured_slope_delta"],
                    "ratio_to_bound": row["ratio_to_bound"],
                } for row in slopes},
                "note": "Rerun reproduced the committed error arrays bit for bit, so the "
                        "propagated bound is exactly zero and the slope assertion is 0 <= 0. "
                        "The 1e-12 primary-array comparison is the binding check here; the "
                        "conditioning bound was not exercised by this run.",
            },
            "evidence": f"runs/campaign_v060/sessions/{TAG}/slope-conditioning.json",
        },
        {
            "gate": "C0", "item": "V10 twin variance",
            "pass": False, "status": "partial", "rule": "R4/R7/R8",
            "value": {
                "pre_fix": prefix,
                "post_fix": {r: {"shots": v.get("shots"),
                                 "distinct_dictionaries": v.get("distinct_dictionaries"),
                                 "seeds": v.get("seeds"),
                                 "N_kept_mean": v.get("N_kept_mean"),
                                 "variance_checked": v.get("variance_checked"),
                                 "structurally_empty": v.get("structurally_empty")}
                             for r, v in v10_rows.items()},
                "negative_control": variance.get("negative_control"),
                "D_C0_case": variance.get("D_C0_case"),
                "D_C0_mechanism": variance.get("D_C0_mechanism"),
                "seed_derivation": "numpy.random.SeedSequence(seed).spawn(n), 31-bit; "
                                   "replaces seed + k, which reproduced one shot stream "
                                   "offset by one draw (seed-mechanism.json)",
                "r0_verdict": ("PASS at R8's 4000 shots: 5 distinct dictionaries of 5, "
                               "against 4 of 5 on the pre-fix code, N_kept_mean 2553.4")
                              if v10_r0_ok else "FAIL at r=0",
                "r1_verdict": ("COST-BLOCKED, not met. The r=1 circuit transpiles to "
                               "821,320 operations at depth 506,888 on the 133-qubit "
                               "target and costs a measured 27.5 s per shot, so R8's "
                               "1024 shots x 5 repeats needs about 39 hours on this "
                               "machine. Three attempts were aborted at 88, 44 and 28 "
                               "minutes. A token run at 8 shots gave 5 distinct raw "
                               "dictionaries but a mean kept count of 0.2 shots, which "
                               "is statistically empty and is NOT offered as evidence."),
                "r8_shot_count_not_met": True,
                "threshold_untouched": ("R8's shot count was NOT amended to fit the "
                                        "hardware; the row is recorded as unmet instead."),
                "calibration": variance.get("r1_calibration"),
            },
            "evidence": f"runs/campaign_v060/sessions/{TAG}/twin-row-calibrated.json",
        },
        {
            "gate": "C0", "item": "V11 estimator", "pass": all_pass("test_estimator"),
            "rule": "R3/R9",
            "value": "Four R9 rows at 1e-10 against an in-test oracle, including the "
                     "violating-input residual, which the 2026-09-09 ruling on the "
                     "undecodable-weight term made satisfiable.",
            "evidence": f"runs/campaign_v060/sessions/{TAG}/gate_C0.xml",
        },
        {
            "gate": "C0", "item": "V11 ODR closure", "pass": None, "status": "deferred",
            "rule": "R3/R9", "value": "Deferred to Phase 5 (V12); not a C0 failure.",
            "evidence": "runs/campaign_v060/PREREGISTRATION.md",
        },
        {
            "gate": "C0", "item": "Tier 2 stale test and counts",
            "pass": all_pass("test_jmax1_counts"), "rule": "R4",
            "value": "j_max=1 kernel dimension 152, sector histogram by both routes, "
                     "projector orthonormality, transfer polynomial written in-test.",
            "evidence": f"runs/campaign_v060/sessions/{TAG}/gate_C0.xml",
        },
    ]
    for row in rows:
        row.update({"utc": UTC, "session": TAG})

    status = subprocess.check_output(["git", "status", "--short"], text=True, cwd=ROOT)
    clean_rows = [line for line in status.splitlines()
                  if line and f"sessions/{TAG}" not in line]
    rows.append({
        "gate": "C0", "item": "repository cleanliness", "pass": not clean_rows,
        "rule": "R2/R12", "utc": UTC, "session": TAG,
        "value": {"dirty_paths_excluding_this_session": clean_rows},
        "evidence": f"runs/campaign_v060/sessions/{TAG}/git-status-final.txt",
    })

    gate_pass = all(r.get("pass") for r in rows if r.get("pass") is not None)
    failed = [r["item"] for r in rows if r.get("pass") is False]

    with (CAMPAIGN / "GATE_LEDGER.jsonl").open("a") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")

    state_path = CAMPAIGN / "CAMPAIGN_STATE.json"
    state = json.loads(state_path.read_text())
    state["gates"]["C0"] = {
        "status": "pass" if gate_pass else "partial",
        "utc": UTC,
        "evidence": f"runs/campaign_v060/sessions/{TAG}",
        "failed": failed,
    }
    state.setdefault("sessions", [])
    if TAG not in state["sessions"]:
        state["sessions"].append(TAG)
    state["baseline"] = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                text=True, cwd=ROOT).strip()
    if gate_pass:
        state["phase"] = 1
        state["next_action"] = "Amend C1 per R12, then open C2 (V2-V7)."
    state_path.write_text(json.dumps(state, indent=2) + "\n")

    print(json.dumps({"xml": {k: v for k, v in xml.items() if k != "cases"},
                      "rows": [{"item": r["item"], "pass": r.get("pass"),
                                "status": r.get("status")} for r in rows],
                      "gate": state["gates"]["C0"]["status"], "failed": failed}, indent=2))
    return 0 if gate_pass else 2


if __name__ == "__main__":
    sys.exit(main())
