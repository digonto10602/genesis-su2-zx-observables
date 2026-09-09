"""Run R19 self-test on the extracted bundle."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path.cwd().resolve()
RESULT_DIR = ROOT / "zip_results"
ARCHIVE = ROOT / "zip_results" / "SU2ZX_QUERY_2166dd4_20260909T173934Z.zip"
# Use the latest SU2ZX_QUERY_*.zip in zip_results
QUERY_ARCHIVES = sorted(RESULT_DIR.glob("SU2ZX_QUERY_*.zip"))
if not QUERY_ARCHIVES:
    raise SystemExit("no query archives found")
ARCHIVE = QUERY_ARCHIVES[-1]
print(f"Using archive: {ARCHIVE}")
SCRATCH = ROOT / ".work" / "c063_bundle_scratch" / "extract"

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

TOOL = Path(__file__).resolve().with_name("query_bundle.py")
_spec = importlib.util.spec_from_file_location("query_bundle", TOOL)
query_bundle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(query_bundle)
check_manifest = query_bundle.check_manifest
check_links = query_bundle.check_links


def check_source_fidelity(root: Path) -> dict:
    """Verify every source file matches the working tree and the 200-file legacy manifest."""
    errors = []
    checked = 0
    for src in root.rglob("*.py"):
        if not src.is_file():
            continue
        rel = src.relative_to(root).as_posix()
        if not rel.startswith(("src/", "runs/section8_")):
            continue
        # Map bundle paths to repo paths
        if rel.startswith("src/runs/section8_v0.5.0_20260907T0628Z/"):
            repo_rel = rel[len("src/"):]
        elif rel.startswith("src/su2zx/") or rel.startswith("runs/section8_"):
            repo_rel = rel
        else:
            continue
        repo_path = ROOT / repo_rel
        if not repo_path.is_file():
            errors.append(f"missing in repo: {repo_rel}")
        elif sha256(src) != sha256(repo_path):
            errors.append(f"diverged from repo: {repo_rel}")
        else:
            checked += 1
    # legacy manifest
    legacy = ROOT / "runs/campaign_v060/sessions/c060_p0_20260908_3/diagnostic-source-manifest.json"
    if legacy.is_file():
        legacy_manifest = json.loads(legacy.read_text())
        legacy_checked = 0
        for path, expected in legacy_manifest.items():
            repo_path = ROOT / path
            if not repo_path.is_file():
                errors.append(f"legacy manifest missing: {path}")
            elif sha256(repo_path) != expected:
                errors.append(f"legacy manifest mismatch: {path}")
            else:
                legacy_checked += 1
        return {"pass": not errors, "src_checked": checked, "legacy_checked": legacy_checked, "errors": errors}
    return {"pass": not errors, "src_checked": checked, "errors": errors}

def check_compileall(root: Path) -> dict:
    """Run python -m compileall over src/ trees."""
    errors = []
    for base in (root / "src",):
        if base.is_dir():
            proc = subprocess.run([sys.executable, "-m", "compileall", str(base)], capture_output=True, text=True)
            if proc.returncode != 0:
                errors.append(f"compileall failed on {base}: {proc.stderr}")
    return {"pass": not errors, "errors": errors}

def check_sizes(root: Path) -> dict:
    """Record total size, largest file, file count."""
    total = 0
    largest = (0, "")
    count = 0
    for p in root.rglob("*"):
        if p.is_file():
            sz = p.stat().st_size
            total += sz
            count += 1
            if sz > largest[0]:
                largest = (sz, p.relative_to(root).as_posix())
    return {"total_bytes": total, "largest_file": largest[1], "largest_bytes": largest[0], "file_count": count}

def main():
    import datetime
    SCRATCH.mkdir(parents=True, exist_ok=True)
    # extract
    with zipfile.ZipFile(ARCHIVE) as z:
        z.extractall(SCRATCH)
    # find the actual extracted directory (may be the archive contents directly)
    extracted = SCRATCH
    if len(list(SCRATCH.iterdir())) == 1 and (SCRATCH / list(SCRATCH.iterdir())[0]).is_dir():
        extracted = SCRATCH / list(SCRATCH.iterdir())[0]
    
    print("Extracted to:", extracted)
    
    # run all five checks
    results = {
        "check1_manifest": check_manifest(extracted),
        "check2_links": check_links(extracted),
        "check3_source_fidelity": check_source_fidelity(extracted),
        "check4_sizes": check_sizes(extracted),
        "check5_compileall": check_compileall(extracted),
    }
    all_pass = all(r.get("pass", True) for r in results.values() if "pass" in r)
    results["overall_pass"] = all_pass
    
    # write SELFTEST.json
    SELFTEST = json.dumps(results, indent=2)
    (extracted / "SELFTEST.json").write_text(SELFTEST)
    
    # also write to session dir for reference
    session_dir = ROOT / "runs/campaign_v060/sessions/c060_p0_20260909_4"
    (session_dir / "SELFTEST.json").write_text(SELFTEST)
    
    print(json.dumps(results, indent=2))
    
    # rebuild archive with real SELFTEST.json
    # read original payload
    with zipfile.ZipFile(ARCHIVE) as z:
        original = {name: z.read(name) for name in z.namelist() if name != "SELFTEST.json"}
    original["SELFTEST.json"] = SELFTEST.encode()
    
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in original.items():
            z.writestr(name, data)
    
    # verify final
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        print("Final archive CRC OK")
    
    # receipt
    receipt = {
        "archive": str(ARCHIVE),
        "bytes": ARCHIVE.stat().st_size,
        "sha256": sha256(ARCHIVE),
        "self_test": results,
        "external_manifest_sha256": (extracted / "MANIFEST.sha256").read_text().strip(),
    }
    (ARCHIVE.with_suffix(".sha256")).write_text(sha256(ARCHIVE) + "  " + ARCHIVE.name + "\n")
    (ARCHIVE.with_suffix(".receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n")
    print("Receipt written")

if __name__ == "__main__":
    main()