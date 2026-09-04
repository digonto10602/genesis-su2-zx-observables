"""Direct cuTensorNet contraction of a Qiskit SU2ZX circuit."""

from __future__ import annotations

import argparse
import json

from cuquantum.tensornet import CircuitToEinsum, contract, contract_path

from su2zx.core import plaquette_chain_terms, strang_evolution


def scalar(value) -> complex:
    return complex(value.item() if hasattr(value, "item") else value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plaquettes", type=int, default=5)
    parser.add_argument("--x", type=float, default=2.0)
    parser.add_argument("--time", type=float, default=0.32)
    parser.add_argument("--repetitions", type=int, default=2)
    args = parser.parse_args()

    circuit = strang_evolution(
        args.plaquettes,
        args.x,
        args.time,
        args.repetitions,
        initial_ones=(args.plaquettes // 2,),
    )
    converter = CircuitToEinsum(circuit, dtype="complex128", backend="cupy")
    energy = 0.0 + 0.0j
    first_path = None
    for term in plaquette_chain_terms(args.plaquettes, args.x, include_identity=True):
        expression, operands = converter.expectation(term.word[::-1], lightcone=True)
        path, info = contract_path(expression, *operands)
        energy += term.coefficient * scalar(
            contract(expression, *operands, optimize=path)
        )
        if first_path is None:
            first_path = str(info)

    central = "".join(
        "1" if q == args.plaquettes // 2 else "0" for q in range(args.plaquettes)
    )
    expression, operands = converter.amplitude(central)
    amplitude = scalar(contract(expression, *operands))
    print(
        json.dumps(
            {
                "plaquettes": args.plaquettes,
                "x": args.x,
                "time": args.time,
                "repetitions": args.repetitions,
                "energy": energy.real,
                "energy_imaginary_residual": energy.imag,
                "central_survival_probability": abs(amplitude) ** 2,
                "first_contraction_report": first_path,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
