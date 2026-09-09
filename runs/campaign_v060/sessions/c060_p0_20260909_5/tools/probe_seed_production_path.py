"""Adjacent-seed stream overlap on the production simulator path (from_backend).

High-entropy 12-qubit circuit so coincidental matches stay near zero and a
one-shot stream offset is unambiguous.
"""
import json, time
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeTorino

SHOTS = 1024

def mem(sim, circ, seed):
    return sim.run(circ, shots=SHOTS, seed_simulator=int(seed), memory=True).result().get_memory()

def compare(a, b):
    same = sum(1 for x, y in zip(a, b) if x == y)
    shift = sum(1 for x, y in zip(a[1:], b[:-1]) if x == y)
    return {"same_index_matches": same, "shift_matches": shift, "shots": SHOTS}

def main():
    t0 = time.time()
    backend = FakeTorino()
    sim = AerSimulator.from_backend(backend, seed_simulator=101)
    qc = QuantumCircuit(12)
    qc.h(range(12))
    qc.measure_all()
    circ = transpile(qc, sim, optimization_level=0, seed_transpiler=500)

    base = 500
    adj = {f"{base}->{base+1}": compare(mem(sim, circ, base), mem(sim, circ, base + 1)),
           f"{base+1}->{base+2}": compare(mem(sim, circ, base + 1), mem(sim, circ, base + 2))}
    ss = np.random.SeedSequence(base)
    sp = [int(c.generate_state(1, dtype=np.uint32)[0]) for c in ss.spawn(3)]
    spawned = {f"{sp[i]}->{sp[i+1]}": compare(mem(sim, circ, sp[i]), mem(sim, circ, sp[i + 1]))
               for i in range(2)}
    print(json.dumps({"path": "AerSimulator.from_backend(FakeTorino)", "qubits": 12,
                      "adjacent_seeds": adj, "spawned_seeds": {"seeds": sp, "pairs": spawned},
                      "seconds": round(time.time() - t0, 1)}, indent=2))

if __name__ == "__main__":
    main()
