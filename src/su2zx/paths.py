"""Small path guard shared by command-line modules."""

from __future__ import annotations

import json
from pathlib import Path


def project_path(value: str | Path) -> Path:
    root = Path.cwd().resolve()
    candidate = (
        (root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    )
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"path escapes project root: {candidate}")
    return candidate


def load_json(value: str | Path) -> dict:
    return json.loads(project_path(value).read_text(encoding="utf-8"))
