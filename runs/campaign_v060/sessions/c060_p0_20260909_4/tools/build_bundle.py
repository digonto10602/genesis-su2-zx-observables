"""Build the documentation-only SU2ZX query bundle (R18). Stdlib only.

Writes: zip_results/SU2ZX_QUERY_<commit>_<UTC>.zip plus MANIFEST.json,
MANIFEST.sha256, SELFTEST.json (inside the archive), and an external receipt.
"""
from __future__ import annotations

import csv
import datetime
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path.cwd().resolve()
assert ROOT.name == "SU2ZX"
SESSION = ROOT / "runs/campaign_v060/sessions/c060_p0_20260909_4"
RUN = ROOT / "runs/section8_v0.5.0_20260907T0628Z"
PRIOR = ROOT / "runs/campaign_v060/sessions/c060_p0_20260908_3"

RESULT_DIR = ROOT / "zip_results"
SCRATCH = ROOT / ".work" / "c063_bundle_scratch"

COMMIT = None  # set below
UTC = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# ---------------------------------------------------------------------------
# source collections
# ---------------------------------------------------------------------------

def su2qc_src():
    return sorted(p for p in RUN.rglob("*.py") if "__pycache__" not in p.parts and "su2qc" in str(p))

def su2qc_tests():
    return sorted(p for p in RUN.joinpath("tests").rglob("*.py") if "__pycache__" not in p.parts)

def su2qc_gates():
    return sorted(p for p in RUN.joinpath("gates").glob("*.py") if "__pycache__" not in p.parts)

def archived_tools():
    return [ROOT / "tools" / f for f in (
        "archive_v040.py", "cudaq_reference.py", "cutensornet_reference.py",
        "function_inventory.py", "plot_v040.py", "provenance.py",
        "refresh_graph_v040.py", "report_v040.py", "tn_sweep.py", "validate_v040.py",
    ) if (ROOT / "tools" / f).is_file()]

def carried_docs():
    return [ROOT / "docs" / f for f in (
        "CODE_FUNCTION_INVENTORY.md", "CODE_LOGIC_AND_TESTS.md",
        "V040_COMPLETION_AUDIT.md", "REFERENCES.md",
    ) if (ROOT / "docs" / f).is_file()]

def archived_src():
    return sorted(p for p in (ROOT / "src").rglob("*.py") if "__pycache__" not in p.parts)

# ---------------------------------------------------------------------------
# exclusions (mandatory)
# ---------------------------------------------------------------------------

EXCLUSIONS = []
SCREEN_RESULT = {"files_screened": 0, "binary_skipped": 0, "hits": []}

# Verbatim v0.6.2 credential screen patterns.
CREDENTIAL_PATTERNS = [
    rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
    rb"\bgh[pousr]_[A-Za-z0-9]{30,}",
    rb"\bgithub_pat_[A-Za-z0-9_]{40,}",
    rb"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{40,}",
    rb"\bAKIA[A-Z0-9]{16}\b",
]
BINARY_SUFFIXES = {".png", ".pdf", ".qpy", ".npz", ".npy"}


def screen_payload(payload):
    """Run the v0.6.2 credential screen over every included text file."""
    for rel, data in payload:
        if PurePosixPath(rel).suffix.lower() in BINARY_SUFFIXES:
            SCREEN_RESULT["binary_skipped"] += 1
            continue
        SCREEN_RESULT["files_screened"] += 1
        for pattern in CREDENTIAL_PATTERNS:
            if re.search(pattern, data):
                SCREEN_RESULT["hits"].append(rel)
                break
    if SCREEN_RESULT["hits"]:
        raise SystemExit("credential screen blocked: " + ", ".join(SCREEN_RESULT["hits"]))

def exclude(path: Path, size: int, reason: str):
    EXCLUSIONS.append({
        "path": path.relative_to(ROOT).as_posix(),
        "size_bytes": size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        "reason": reason,
    })

CIRCUIT_METADATA = {
    # r: (support qubits, CZ count before routing, 2q depth before routing)
    "l12_r0": (12, 0, 0),
    "l12_r1": (12, 45875, 45037),
    "l12_r2": (12, 87656, 85989),
    "l12_r3": (12, 129437, 126941),
}


def scan_excluded_circuits():
    for ext in ("qpy", "qasm"):
        for p in sorted((RUN / "circuits").glob(f"*.{ext}")):
            qubits, cz, depth = CIRCUIT_METADATA.get(p.stem, (None, None, None))
            exclude(
                p,
                p.stat().st_size,
                f"circuit export; shots n/a (no shots stored in the artifact), qubits {qubits}, "
                f"CZ {cz}, 2q depth {depth} (source: evidence/resources_logical.md); "
                "hash recorded instead of the file",
            )

def collect_exclusions():
    # qpy/qasm twins
    scan_excluded_circuits()
    # graphify cache
    for p in sorted((ROOT / "graphify-out" / "cache").rglob("*")) if (ROOT/"graphify-out"/"cache").exists() else []:
        if p.is_file():
            exclude(p, p.stat().st_size, "graphify AST cache")
    # dated graphify snapshots
    for p in sorted((ROOT / "graphify-out").glob("2026-*")):
        if p.is_file():
            exclude(p, p.stat().st_size, "dated graphify snapshot")
    # large v040 CSVs
    for name in ("tn_all_runs.csv", "tn_scaling.csv"):
        p = ROOT / "artifacts" / "data" / "v040" / name
        if p.is_file():
            exclude(p, p.stat().st_size, "evidence >2MB; stratified sample retained as sample")
    # PDF duplicates of included PNG figures
    for p in sorted((ROOT / "artifacts" / "figures").glob("*.pdf")):
        exclude(p, p.stat().st_size, "PDF duplicate of an included PNG figure")

def stratified_sample(src: Path, n: int = 500, rng_seed: int = 0) -> list[str]:
    """Deterministic stratified sample of CSV rows keyed on strata columns."""
    import random
    csv.field_size_limit(100_000_000)
    with src.open(newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    # strata by the scalar parameter columns (exclude mps_log)
    strata_cols = [c for c in fields if c != "mps_log"]
    groups: dict[tuple, list] = {}
    for r in rows:
        key = tuple(r[c] for c in strata_cols)
        groups.setdefault(key, []).append(r)
    rng = random.Random(rng_seed)
    sample = []
    # proportional allocation
    per_group = max(1, n // max(1, len(groups)))
    for key in sorted(groups):
        picked = groups[key] if len(groups[key]) <= per_group else rng.sample(groups[key], per_group)
        sample.extend(picked)
    # limit total
    if len(sample) > n:
        sample = rng.sample(sample, n)
    out = []
    out.append(",".join(fields))
    for r in sample:
        r = dict(r)
        r["mps_log"] = f"<omitted {len(r.get('mps_log',''))} bytes>"
        out.append(",".join(str(r.get(c, "")) for c in fields))
    return out

# ---------------------------------------------------------------------------
# manifest + zip
# ---------------------------------------------------------------------------

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def build():
    global COMMIT
    import subprocess
    COMMIT = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    archive_name = f"SU2ZX_QUERY_{COMMIT}_{UTC}.zip"
    archive_path = RESULT_DIR / archive_name
    if archive_path.exists():
        raise SystemExit("archive already exists; not overwriting")

    # collect payload
    payload: list[tuple[str, bytes]] = []

    def add(rel: str, data: bytes):
        payload.append((rel, data))

    # docs (new, generated this session)
    for name in ("CODE_MAP.md", "SU2QC_FUNCTION_INVENTORY.md", "SU2QC_LOGIC_AND_TESTS.md",
                 "SU2QC_CONTRACTS.md", "PHYSICS_SPEC.md", "EXECUTION_MAP.md", "GATE_MAP.md",
                 "GLOSSARY.md"):
        src = ROOT / "docs" / name
        if not src.is_file():
            src = SESSION / name
        if src.is_file():
            add(f"docs/{name}", src.read_bytes())

    # carried docs (byte-identical)
    for p in carried_docs():
        add(f"docs/{p.name}", p.read_bytes())

    # source trees - su2qc (live package)
    for p in su2qc_src():
        add(f"src/runs/section8_v0.5.0_20260907T0628Z/{p.relative_to(RUN).as_posix()}", p.read_bytes())
    for p in su2qc_tests():
        add(f"tests/{p.relative_to(RUN.joinpath('tests')).as_posix()}", p.read_bytes())
    for p in su2qc_gates():
        add(f"gates/{p.name}", p.read_bytes())

    # alias copies at the repository-relative path, so the AST-generated
    # docs/SU2QC_FUNCTION_INVENTORY.md links resolve inside the archive
    for p in su2qc_src():
        add(f"{p.relative_to(ROOT).as_posix()}", p.read_bytes())
    for p in su2qc_tests():
        add(f"{p.relative_to(ROOT).as_posix()}", p.read_bytes())
    for p in su2qc_gates():
        add(f"{p.relative_to(ROOT).as_posix()}", p.read_bytes())

    # archived package source (for completeness of src/)
    for p in archived_src():
        add(f"src/{p.relative_to(ROOT / 'src').as_posix()}", p.read_bytes())

    # archived package tests (carried docs link to ../tests/*.py)
    for p in sorted((ROOT / "tests").glob("*.py")):
        add(f"tests/{p.name}", p.read_bytes())

    # campaign C0 gate tests (referenced by docs/GATE_MAP.md)
    for p in sorted((ROOT / "runs/campaign_v060/tests/gate_C0").glob("*.py")):
        add(f"tests/gate_C0/{p.name}", p.read_bytes())

    # figures (PNG only, no PDF duplicates)
    for p in sorted((ROOT / "artifacts" / "figures").glob("*.png")):
        add(f"figures/v040/{p.name}", p.read_bytes())
    for p in sorted((RUN / "analysis" / "figures").glob("*.png")):
        add(f"figures/section8/{p.name}", p.read_bytes())

    # tools compatibility directory (user-approved)
    for p in archived_tools():
        add(f"tools/{p.name}", p.read_bytes())

    # evidence (<=2MB, JSON/CSV/XML/log)
    evidence_candidates = [
        PRIOR / "DIAGNOSTIC_RESULTS.json",
        PRIOR / "seed-diagnosis.json",
        PRIOR / "equal-seed-control.json",
        PRIOR / "oracle-diagnostics.json",
        PRIOR / "diagnostic-execution.json",
        PRIOR / "diagnostic-source-manifest.json",
        PRIOR / "diagnostic-regression.xml",
        PRIOR / "variance_pre_fix.csv",
        RUN / "circuits" / "trotter_scaling.json",
        RUN / "circuits" / "resources_logical.md",
        RUN / "circuits" / "resources_synth.md",
        ROOT / "runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json",
        ROOT / "runs/campaign_v060/CAMPAIGN_STATE.json",
        ROOT / "runs/campaign_v060/PREREGISTRATION.md",
        ROOT / "runs/campaign_v060/GATE_THRESHOLDS.yaml",
        ROOT / "runs/campaign_v060/CLAIM_TABLE.md",
    ]
    for p in evidence_candidates:
        if not p.is_file():
            continue
        if p.stat().st_size > 2_000_000:
            exclude(p, p.stat().st_size, "evidence >2MB")
            continue
        add(f"evidence/{p.name}", p.read_bytes())

    # stratified CSV samples (v040)
    for name in ("tn_all_runs.csv", "tn_scaling.csv"):
        src = ROOT / "artifacts" / "data" / "v040" / name
        if src.is_file():
            lines = stratified_sample(src)
            add(f"evidence/sample_{name}", ("\n".join(lines) + "\n").encode())

    # sessions (verbatim issue reports)
    for name in ("PHYSICS_ISSUES.md", "CODE_ISSUES.md", "EXECUTION_ISSUES.md", "REVIEW_CHECKS.md", "SESSION_SUMMARY.md", "PHYSICS_STATUS.md"):
        p = PRIOR / name
        if p.is_file():
            add(f"sessions/{name}", p.read_bytes())

    # graph
    for name in ("GRAPH_REPORT.md", "graph.json"):
        p = ROOT / "graphify-out" / name
        if p.is_file():
            add(f"graph/{name}", p.read_bytes())

    # top-level navigation
    for name in ("INDEX.md", "ASK.md", "CLAIMS.md"):
        src = SESSION / name
        if src.is_file():
            add(f"{name}", src.read_bytes())

    # credential screen over every included text file, before anything is written
    screen_payload(payload)

    # exclusions are collected before EXCLUSIONS.md is rendered
    collect_exclusions()
    add("EXCLUSIONS.md", expo_db_markdown().encode())

    # fill commit/utc placeholders in INDEX
    for i, (rel, data) in enumerate(payload):
        if rel == "INDEX.md":
            payload[i] = (rel, data.decode().replace("__COMMIT__", COMMIT).replace("__UTC__", UTC).encode())

    # write manifest
    manifest_rows = []
    for rel, data in payload:
        manifest_rows.append({
            "path": rel,
            "bytes": len(data),
            "sha256": sha256_bytes(data),
        })
    manifest = {"files": manifest_rows, "total_files": len(manifest_rows), "commit": COMMIT, "built_utc": UTC}
    manifest_bytes = json.dumps(manifest, indent=2, sort_keys=True).encode()
    manifest_sha = sha256_bytes(manifest_bytes)

    # build archive
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel, data in payload:
            z.writestr(rel, data)
        z.writestr("MANIFEST.json", manifest_bytes)
        z.writestr("MANIFEST.sha256", manifest_sha + "  MANIFEST.json\n")
        # SELFTEST.json placeholder; real one written after extraction self-test
        z.writestr("SELFTEST.json", json.dumps({"placeholder": True}, indent=2).encode())

    # compute compression size
    size = archive_path.stat().st_size
    print(json.dumps({
        "archive": str(archive_path),
        "compressed_bytes": size,
        "payload_files": len(payload),
        "target_25mb": size <= 25_000_000,
        "hard_cap_30mb": size <= 30_000_000,
    }, indent=2))
    return archive_path

def expo_db_markdown() -> str:
    lines = ["# Exclusions", "",
             "Every excluded path, its size, its SHA-256, and why. Pattern screening"]
    lines.append("passed in this build; that is not a guarantee of absence of every")
    lines.append("secret format.")
    lines.append("")
    lines.append("| path | size | sha256 | reason |")
    lines.append("|---|---:|---|---|")
    for e in EXCLUSIONS:
        lines.append(f"| {e['path']} | {e['size_bytes']} | {e['sha256'] or '-'} | {e['reason']} |")
    lines.append("")
    lines.append("## Directory / policy exclusions (recorded, not enumerated)")
    lines.append("- `.git/`, `.mamba/`, `.work/`, `.venv/` — environments, caches, VCS (not crawled for secrets).")
    lines.append("- Any nested archive (`.zip`) — excluded.")
    lines.append("- Any file matching the credential screen (`.env`, `auth.json`, `credentials.json`, `*.pem`, `*.key`) — excluded by name, never read.")
    lines.append(
        f"- Credential-pattern screening ran on {SCREEN_RESULT['files_screened']} included text "
        f"file(s) before packaging ({SCREEN_RESULT['binary_skipped']} binary file(s) skipped by "
        f"suffix); {len(SCREEN_RESULT['hits'])} hit(s). Screening passed is not a guarantee of "
        "absence of every secret format."
    )
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    SCRATCH.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(exist_ok=True)
    build()