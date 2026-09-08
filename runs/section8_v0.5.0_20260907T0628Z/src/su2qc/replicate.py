"""Minimal replication manifest helper for the campaign.

Phase 8 will extend this module to rebuild all tables and figures. Phase 0 only
provides deterministic file hashing and committed-vs-rerun comparison.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def manifest(paths: list[str | Path]) -> dict[str, str]:
    return {str(Path(path)): sha256_file(path) for path in sorted(paths, key=str)}


def compare_manifests(expected: dict[str, str], actual: dict[str, str]) -> dict[str, object]:
    keys = sorted(set(expected) | set(actual))
    mismatches = [key for key in keys if expected.get(key) != actual.get(key)]
    return {"pass": not mismatches, "mismatches": mismatches, "count": len(keys)}


def write_manifest(paths: list[str | Path], output: str | Path) -> dict[str, str]:
    values = manifest(paths)
    Path(output).write_text(json.dumps(values, indent=2, sort_keys=True) + "\n")
    return values
