"""Measure whether run_counts-style adjacent seeds give overlapping shot streams.

Mechanical probe. Writes JSON to stdout. Touches no historical evidence.
"""
import json, sys
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeTorino

SHOTS = 1024

def memories(sim, circ, seeds):
    out = []
    for s in seeds:
        res = sim.run(circ, shots=SHOTS, seed_simulator=int(s), memory=True).result()
        out.append(res.get_memory())
    return out

def overlap(a, b):
    """same-index matches, and matches after shifting b by one shot."""
    same = sum(1 for x, y in zip(a, b) if x == y)
    shift = sum(1 for x, y in zip(a[1:], b[:-1]) if x == y)
    return same, shift

def main():
    backend = FakeTorino()
    sim = AerSimulator(noise_model=NoiseModel.from_backend(backend))
    qc = QuantumCircuit(4)
    qc.h(range(4)); qc.cx(0, 1); qc.cx(2, 3)
    qc.measure_all()
    circ = transpile(qc, sim, optimization_level=0, seed_transpiler=7)

    base = 500
    adjacent = memories(sim, circ, [base + k for k in range(3)])
    ss = np.random.SeedSequence(base)
    spawned = [int(c.generate_state(1, dtype=np.uint32)[0]) for c in ss.spawn(3)]
    independent = memories(sim, circ, spawned)

    def pairs(ms):
        return [{"pair": f"{i}-{i+1}", "same_index_matches": overlap(ms[i], ms[i+1])[0],
                 "shift_matches": overlap(ms[i], ms[i+1])[1]} for i in range(len(ms) - 1)]

    print(json.dumps({
        "shots": SHOTS,
        "adjacent_seeds": [base + k for k in range(3)],
        "adjacent": pairs(adjacent),
        "spawned_seeds": spawned,
        "spawned": pairs(independent),
        "expectation": "shift_matches near shots means the streams are the same sequence offset by one shot",
    }, indent=2))

if __name__ == "__main__":
    main()
