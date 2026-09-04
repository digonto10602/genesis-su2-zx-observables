"""Launch each CUDA-Q MPS bond dimension in a fresh process and plot convergence."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts")
    parser.add_argument("--plaquettes", default="5,10,20,40")
    parser.add_argument("--bonds", default="32,64,128,256")
    parser.add_argument("--time", type=float, default=0.32)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    output = (root / args.output).resolve()
    if root not in output.parents:
        raise ValueError("output escapes project root")
    rows = []
    for n in [int(value) for value in args.plaquettes.split(",")]:
        for bond in [int(value) for value in args.bonds.split(",")]:
            command = [
                sys.executable,
                "tools/cudaq_reference.py",
                "--target",
                "tensornet-mps",
                "--plaquettes",
                str(n),
                "--max-bond",
                str(bond),
                "--time",
                str(args.time),
            ]
            run = subprocess.run(
                command, cwd=root, capture_output=True, text=True, check=False
            )
            if run.returncode == 0:
                result = json.loads(run.stdout)
                rows.append({**result, "status": "PASS", "error": ""})
            else:
                rows.append(
                    {
                        "target": "tensornet-mps",
                        "plaquettes": n,
                        "max_bond": bond,
                        "energy": float("nan"),
                        "survival_probability": float("nan"),
                        "status": "BLOCKED",
                        "error": run.stderr[-2000:],
                    }
                )
    frame = pd.DataFrame(rows)
    (output / "data").mkdir(parents=True, exist_ok=True)
    (output / "figures").mkdir(parents=True, exist_ok=True)
    frame.to_csv(output / "data" / "tensor_network_sweep.csv", index=False)

    valid = frame[frame.status == "PASS"]
    if valid.empty:
        raise RuntimeError("no MPS sweep point completed")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for n, group in valid.groupby("plaquettes"):
        axes[0].plot(group.max_bond, group.energy, marker="o", label=f"N={n}")
        axes[1].plot(
            group.max_bond,
            group.survival_probability,
            marker="o",
            label=f"N={n}",
        )
    axes[0].set(xlabel="maximum bond dimension", ylabel="energy")
    axes[1].set(xlabel="maximum bond dimension", ylabel="survival probability")
    for axis in axes:
        axis.set_xscale("log", base=2)
        axis.legend(frameon=False)
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("CUDA-Q MPS bond-dimension convergence")
    fig.savefig(
        output / "figures" / "tensor_network_convergence.png",
        dpi=220,
        bbox_inches="tight",
    )
    fig.savefig(
        output / "figures" / "tensor_network_convergence.pdf",
        bbox_inches="tight",
    )


if __name__ == "__main__":
    main()
