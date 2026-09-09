"""Build and verify the documentation-only SU2ZX query bundle; stdlib only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit

CONTROL_FILES = {"MANIFEST.json", "MANIFEST.sha256", "SELFTEST.json"}


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_manifest(root: Path) -> dict:
    """Verify exact payload coverage and sidecar, excluding declared controls."""
    errors = []
    manifest = json.loads((root / "MANIFEST.json").read_text())
    rows = manifest["files"]
    names = [row["path"] for row in rows]
    if len(names) != len(set(names)):
        errors.append("duplicate manifest paths")
    present = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if set(names) & CONTROL_FILES:
        errors.append("control files must not hash themselves in the payload manifest")
    if present != set(names) | CONTROL_FILES:
        errors.append({"missing": sorted((set(names) | CONTROL_FILES) - present), "unlisted": sorted(present - set(names) - CONTROL_FILES)})
    checked = 0
    for row in rows:
        relative = PurePosixPath(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            errors.append("unsafe manifest path")
            continue
        path = root / relative
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            errors.append("manifest target escapes root or is a symlink")
        elif path.is_file():
            checked += 1
            if path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
                errors.append("payload mismatch: " + row["path"])
    sidecar = root / "MANIFEST.sha256"
    if sidecar.is_file() and sidecar.read_text().strip() != sha256(root / "MANIFEST.json") + "  MANIFEST.json":
        errors.append("manifest sidecar mismatch")
    return {"pass": not errors, "payload_files": len(names), "present_files": len(present), "hashes_checked": checked, "controls": sorted(CONTROL_FILES), "errors": errors}


def check_links(root: Path) -> dict:
    """Check R19 navigation targets and all Markdown links in docs/*.md."""
    required = [root / name for name in ("INDEX.md", "ASK.md", "CLAIMS.md", "docs/GATE_MAP.md")]
    files = sorted(set(required + list((root / "docs").glob("*.md"))))
    errors = []
    checked = 0
    for document in files:
        if not document.is_file():
            errors.append("missing navigation document: " + document.relative_to(root).as_posix())
            continue
        text = document.read_text()
        # Markdown links are relative to the document; backticked bundle paths in the
        # navigation documents are relative to the archive root.
        targets = [(value, document.parent) for value in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text)]
        if document in required:
            targets.extend((value, root) for value in re.findall(r"`([^`\n]+)`", text)
                           if re.match(r"^(?:docs|src|tests|gates|evidence|figures|sessions|graph|tools|runs)/", value))
        for target, base in sorted(set(targets), key=lambda item: (item[0], str(item[1]))):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            resolved = (base / unquote(parts.path)).resolve() if parts.path else document.resolve()
            checked += 1
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append({"document": document.relative_to(root).as_posix(), "target": target})
            elif re.fullmatch(r"L\d+(?:-L\d+)?", parts.fragment) and resolved.is_file():
                bounds = [int(value) for value in re.findall(r"\d+", parts.fragment)]
                if min(bounds) < 1 or max(bounds) > len(resolved.read_text().splitlines()):
                    errors.append({"document": document.relative_to(root).as_posix(), "target": target, "reason": "line anchor out of range"})
    return {"pass": not errors, "documents_checked": len(files), "references_checked": checked, "errors": errors}
