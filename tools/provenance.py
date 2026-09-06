"""Write secret-free machine-readable provenance for the v0.3.0 run."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def command(arguments: list[str]) -> str:
    result = subprocess.run(arguments, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def package_version(*names: str) -> str:
    for name in names:
        try:
            return version(name)
        except PackageNotFoundError:
            continue
    return "not installed"


def main() -> None:
    root = Path.cwd().resolve()
    if root.name != "SU2ZX":
        raise SystemExit("run from the SU2ZX repository root")
    output = (root / "artifacts" / "provenance" / "run_v0.3.0.json").resolve()
    if root not in output.parents:
        raise SystemExit("provenance output escapes repository")
    output.parent.mkdir(parents=True, exist_ok=True)
    gpu_fields = command(
        [
            "nvidia-smi",
            "--query-gpu=name,compute_cap,driver_version,memory.total,memory.free",
            "--format=csv,noheader",
        ]
    ).split(",")
    generated_data = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "artifacts" / "data").glob("*")
        if path.is_file()
    )
    generated_figures = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "artifacts" / "figures").glob("*")
        if path.is_file()
    )
    payload = {
        "version": "v0.3.0",
        "utc_timestamp": datetime.now(UTC).isoformat(),
        "git": {
            "commit": command(["git", "rev-parse", "HEAD"]),
            "branch": command(["git", "branch", "--show-current"]),
            "dirty": bool(command(["git", "status", "--porcelain"])),
        },
        "python": sys.version,
        "packages": {
            name: package_version(*aliases)
            for name, aliases in {
                "qiskit": ("qiskit",),
                "qiskit_aer": ("qiskit-aer",),
                "qiskit_ibm_runtime": ("qiskit-ibm-runtime",),
                "pyzx": ("pyzx",),
                "cudaq": ("cudaq", "cuda-quantum"),
                "numpy": ("numpy",),
                "scipy": ("scipy",),
                "pandas": ("pandas",),
                "scikit_learn": ("scikit-learn",),
                "matplotlib": ("matplotlib",),
                "pytest": ("pytest",),
                "ruff": ("ruff",),
                "mypy": ("mypy",),
            }.items()
        },
        "hardware": {
            "platform": platform.platform(),
            "kernel": platform.release(),
            "machine": platform.machine(),
            "logical_cpus": os.cpu_count(),
            "memory_free_b": command(["free", "-b"]),
            "gpu": {
                "name": gpu_fields[0].strip() if len(gpu_fields) > 0 else "unavailable",
                "compute_capability": gpu_fields[1].strip()
                if len(gpu_fields) > 1
                else "unavailable",
                "driver": gpu_fields[2].strip() if len(gpu_fields) > 2 else "unavailable",
                "memory_total": gpu_fields[3].strip() if len(gpu_fields) > 3 else "unavailable",
                "memory_free": gpu_fields[4].strip() if len(gpu_fields) > 4 else "unavailable",
            },
        },
        "random_seeds": {"dataset": 7, "selector": 11, "transpiler": [11, 29, 47]},
        "experiment": {
            "sizes": [2, 3, 4, 5, 6],
            "trotter_repetitions": [1, 2, 4, 8],
            "term_orderings": ["current", "reversed", "symmetry"],
            "topologies": ["line", "ring", "grid", "heavy_hex_like", "irregular"],
            "compiler_strategies": [
                "qiskit",
                "basic",
                "basic_swaps",
                "teleport",
                "full_reduce",
                "full_reduce_depth",
            ],
        },
        "blocked_features": {
            "cuda_q_gpu": "BLOCKED_BY_HARDWARE",
            "tensor_network_gpu": "BLOCKED_BY_HARDWARE",
            "ibm_qpu": "NOT_RUN",
        },
        "generated_datasets": generated_data,
        "generated_figures": generated_figures,
    }
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(output.relative_to(root))


if __name__ == "__main__":
    main()
