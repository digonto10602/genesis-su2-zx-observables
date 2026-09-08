import json
from pathlib import Path

from qiskit import transpile

from su2qc.circuits.strang_l12 import full_circuit
from su2qc.twin import twin


def _measured_repeats(r, shots=1024, seed=500):
    sim = twin.twin_backend(seed=101, compact=True)
    isa = transpile(full_circuit(r), sim, optimization_level=0, seed_transpiler=101)
    measured = twin.add_measurements(isa)
    return twin.run_counts([measured] * 5, shots, seed, sim)


def test_twin_variance_and_runtime_seed_detection():
    repeats = {}
    evidence = {}
    for r in (0, 1):
        counts = _measured_repeats(r)
        repeats[r] = counts
        evidence[str(r)] = {
            "distinct_dictionaries": len({tuple(sorted(c.items())) for c in counts}),
            "repeat_sizes": [len(c) for c in counts],
        }
        Path("runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json").write_text(
            json.dumps(evidence, indent=2) + "\n"
        )
        assert evidence[str(r)]["distinct_dictionaries"] == 5
        means, two_sigma, _ = twin.bootstrap(counts, n_boot=250, seed=77)
        assert any(value > 0.0 for value in two_sigma.values())
        assert all(value == value for value in means.values())
    # Negative control: forcing one run dictionary to repeat is detected.
    assert len({tuple(sorted(c.items())) for c in [repeats[0][0]] * 5}) == 1


def test_twin_seed_reproducibility():
    assert _measured_repeats(0) == _measured_repeats(0)
