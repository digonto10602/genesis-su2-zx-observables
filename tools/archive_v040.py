"""Curated, scanned, non-overwriting final archive with exact-file integrity receipt."""

# ruff: noqa: E501
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from datetime import UTC, datetime

from su2zx.paths import project_path


def archive_files(root):
    files = []
    roots = [
        "src",
        "tests",
        "scripts",
        "tools",
        "config",
        "docs",
        "prompts",
        "artifacts/data",
        "artifacts/figures",
        "artifacts/provenance",
        "artifacts/logs",
    ]
    for directory in roots:
        for path in (root / directory).rglob("*"):
            if path.name == "archive_integrity.json":
                continue  # receipt is generated after the exact final ZIP
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(root)
            if "__pycache__" in relative.parts or path.suffix in [".pyc", ".tmp"]:
                continue
            if root not in path.resolve().parents:
                raise RuntimeError("archive file escapes root")
            files.append(path)
    files.extend(
        root / name
        for name in [
            "README.md",
            "AGENTS.md",
            "RESEARCH_RESULTS.md",
            "VALIDATION.md",
            "GRAPHIFY_UPDATE.md",
            "RELEASE_NOTES_v0.3.0.md",
            "RELEASE_NOTES_v0.4.0.md",
            "RUN_MANIFEST.md",
            "pyproject.toml",
            "CITATION.cff",
            "LICENSE",
            ".gitignore",
            ".graphifyignore",
            "graphify-out/graph.json",
            "graphify-out/GRAPH_REPORT.md",
            "graphify-out/graph.html",
        ]
    )
    return sorted(set(files))


def scan(files):
    patterns = {
        "provider token": re.compile(
            rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-proj-[A-Za-z0-9_-]{30,})"
        ),
        "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "credential assignment": re.compile(
            rb"""(?i)(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)["']?\s*[:=]\s*["']([A-Za-z0-9_+/=-]{16,})["']"""
        ),
    }
    failures = []
    for path in files:
        if path.name.startswith(".env") or any(
            x in path.name.lower() for x in ["credential", "private_key"]
        ):
            failures.append((str(path), "sensitive filename"))
        payload = path.read_bytes()
        for label, pattern in patterns.items():
            if pattern.search(payload):
                failures.append((str(path), label))
    if failures:
        raise RuntimeError(f"Secret scan rejected files (values withheld): {failures}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--published-commit", help="Verified pushed main revision for post-push ZIP"
    )
    args = parser.parse_args()
    root = project_path(".")
    publication = None
    if args.published_commit:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], text=True
        ).strip()
        assert remote == "https://github.com/digonto10602/genesis-su2-zx-observables.git"
        published = subprocess.check_output(
            ["git", "ls-remote", "origin", "refs/heads/main"], text=True
        ).split()[0]
        assert commit == published == args.published_commit
        publication = dict(status="PASS", commit=commit, remote=remote, branch="main")
        (root / "artifacts/provenance/publication_v040.json").write_text(
            json.dumps(publication, indent=2)
        )
    validation = json.loads((root / "artifacts/logs/v040/graph_validation.json").read_text())
    assert validation["status"] == "PASS"
    # Require the actual current graph, not a stale validation record.
    assert (
        validation["graph_sha256"]
        == hashlib.sha256((root / "graphify-out/graph.json").read_bytes()).hexdigest()
    )
    check_logs = root / "artifacts/logs/v040/completion"
    if not check_logs.is_dir():
        check_logs = root / "artifacts/logs/v040"
    audit = json.loads((check_logs / "data_integrity.log").read_text())
    assert audit["status"] == "PASS"
    for filename, needle in [
        ("pytest.log", "passed"),
        ("ruff.log", "All checks passed"),
        ("mypy.log", "Success:"),
        ("format.log", "already formatted"),
    ]:
        assert needle in (check_logs / filename).read_text()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    destination = root / "zip_results" / f"SU2ZX_v0.4.0_{stamp}.zip"
    if destination.exists():
        raise FileExistsError(destination)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    manifest = f"""# SU2ZX v0.4.0 run manifest

- UTC archive timestamp: {stamp}
- Input Git commit: {commit}; release commit follows archival by required execution order.
- Archive: `zip_results/{destination.name}`
- Archive SHA256 and exact-file test receipt: `{destination.name}.sha256` and `{destination.name}.integrity.json` beside the archive.
- Baseline physics: PASS; final regression tests, Ruff, formatting, mypy, grouped leakage, frozen rule, seed reproducibility and data integrity: PASS.
- Compiler: 830/860 outputs pass; 30 excluded; 415 complete pairs.
- Robust families: Basic 33, Teleport 29, count ties 21; seed-sensitive 0; broader layout/topology result INCONCLUSIVE.
- ML: NULL. Prospective grouped-selected logistic regret 0.024954; strongest simple regret 0.008966.
- Symmetry: MIXED. 168 physics and 81 verified compiler records.
- Strang current-order exponent: full 1.865777, asymptotic 1.978062.
- TN: direct observables VALIDATED at N=5,8; no-statevector SCALING_DEMONSTRATED through N=32 at t=0.32,r=2.
- CUDA-Q CPU PASS; GPU BLOCKED_BY_HARDWARE; IBM metadata NOT_AVAILABLE; QPU NOT_RUN.
- Graphify: PASS, {validation["nodes"]} nodes / {validation["edges"]} relationships.
- Datasets: artifacts/data/v040/; 16 figures with PNG/PDF and source mappings: artifacts/figures/v040/.
- Provenance: artifacts/provenance/run_v0.4.0.json; validation logs: artifacts/logs/v040/.
- GitHub: existing digonto10602/genesis-su2-zx-observables remote; push occurs after commit and is recorded in the final response.

## Archive scope and limitations

Includes current code/tests/scripts, research/configuration/prompts, reports, data, plots, provenance, relevant logs and refreshed graph. Historical v0.3.0 data/release notes remain included. Excludes environments, caches, .git, .work, credentials and prior archives. The exact ZIP is tested and hashed after creation; its external integrity receipt names this exact file, avoiding a self-referential archive checksum.

Compiler targets are synthetic, calibration seed fixed, basis ECR only, grids bounded. Historical winner selection is enriched. Routed equivalence is randomized numerical validation. Large-N MPS has no exact-Hamiltonian reference; long-time entanglement growth is not studied. No QPU or unsupported GPU execution occurred. No continuum, physical-QCD or quantum-advantage claims.
"""
    if publication:
        manifest = manifest.replace(
            "release commit follows archival by required execution order.",
            "verified published main revision; this final reports ZIP was created after push.",
        ).replace(
            "push occurs after commit and is recorded in the final response.",
            "push PASS; remote main was independently verified before this archive.",
        )
        manifest += (
            "\n## Comprehensive final reports\n\n"
            "See docs/V040_COMPLETION_AUDIT.md, docs/CODE_LOGIC_AND_TESTS.md and "
            "docs/CODE_FUNCTION_INVENTORY.md. Full source and test implementations, "
            "datasets, figures and fresh completion logs/JUnit are included. "
            "Publication receipt: artifacts/provenance/publication_v040.json. "
            "Final archive receipts and this manifest are post-commit additions.\n"
        )
    (root / "RUN_MANIFEST.md").write_text(manifest)
    files = archive_files(root)
    scan(files)
    scan_log = root / "artifacts/logs/v040/secret_scan.json"
    scan_log.write_text(
        json.dumps(
            dict(
                status="PASS",
                utc_timestamp=stamp,
                files=len(files),
                scope="Curated archive and publish file set; token/private-key/credential-assignment signatures and sensitive filenames; not a guarantee against all possible secret formats.",
            ),
            indent=2,
        )
    )
    files = archive_files(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        destination, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())
    expected = {path.relative_to(root).as_posix() for path in files}
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == expected
        for path in files:
            assert (
                hashlib.sha256(archive.read(path.relative_to(root).as_posix())).digest()
                == hashlib.sha256(path.read_bytes()).digest()
            )
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix(".zip.sha256").write_text(f"{digest}  {destination.name}\n")
    receipt = dict(
        status="PASS",
        archive=destination.relative_to(root).as_posix(),
        sha256=digest,
        files=len(files),
        bytes=destination.stat().st_size,
        verified_contents=sorted(expected),
    )
    destination.with_suffix(".zip.integrity.json").write_text(json.dumps(receipt, indent=2))
    (root / "artifacts/logs/v040/archive_integrity.json").write_text(
        json.dumps(receipt, indent=2)
    )
    print(json.dumps({k: v for k, v in receipt.items() if k != "verified_contents"}, indent=2))


if __name__ == "__main__":
    main()
