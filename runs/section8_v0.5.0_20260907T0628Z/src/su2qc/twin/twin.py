"""Noise-model twin: FakeTorino (or a real backend's properties) via
AerSimulator.from_backend, with leakage post-selection and observables.

  twin_backend(seed)              -> AerSimulator noise twin
  run_counts(isa_circs, shots, seed, backend) -> list of counts dicts (physical
        bit order already mapped back to LOGICAL q11..q0 strings via the
        circuit's final layout, so l12.decode applies directly)
  postselect(counts)              -> (kept_counts, yield_fraction)
  observables(kept_counts)        -> dict of P_surv, P_meson, P_BBbar, P_other,
        E2_l (4), n_v (4), from decoded labels (all Z-basis, diagonal)
  bootstrap(counts_list, fn, n_boot, seed) -> mean, 2sigma per observable
"""
from __future__ import annotations

import os
import sys

import numpy as np

RUN = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(RUN, "src"))

from su2qc import conventions as cv  # noqa: E402
from su2qc.encodings import l12  # noqa: E402


def twin_backend(seed=1234, backend=None, compact=False):
    from qiskit_aer import AerSimulator
    if backend is None:
        from qiskit_ibm_runtime.fake_provider import FakeTorino
        backend = FakeTorino()
    if compact:
        from qiskit_aer.noise import NoiseModel
        noise = NoiseModel.from_backend(backend)
        return AerSimulator(noise_model=noise)
    return AerSimulator.from_backend(backend, seed_simulator=seed)


def add_measurements(isa):
    """Measure the 12 logical qubits (at their final physical positions) into
    classical bits c[i] = logical i, so the count strings read q11..q0."""
    from qiskit import ClassicalRegister
    fil = (isa.layout.final_index_layout() if isa.layout is not None
           else list(range(len(isa.qubits))))
    qc = isa.copy()
    cr = ClassicalRegister(12, "c")
    qc.add_register(cr)
    for i in range(12):
        qc.measure(qc.qubits[fil[i]], cr[i])
    return qc


def run_counts(isa_meas_list, shots, seed, sim):
    from qiskit import transpile
    out = []
    for k, qc in enumerate(isa_meas_list):
        t = transpile(qc, sim, optimization_level=0, seed_transpiler=seed)
        if hasattr(sim, "set_options"):
            sim.set_options(seed_simulator=seed + k)
        res = sim.run(t, shots=shots, seed_simulator=seed + k).result()
        out.append(dict(res.get_counts()))
    return out


def postselect(counts):
    kept = {s: n for s, n in counts.items() if l12.is_physical(s)}
    tot = sum(counts.values())
    return kept, (sum(kept.values()) / tot if tot else 0.0)


def observables(kept):
    tot = sum(kept.values())
    acc = {"P_surv": 0.0, "P_meson": 0.0, "P_BBbar": 0.0, "P_other": 0.0,
           "P_stretched": 0.0, "P_short": 0.0}
    e2 = np.zeros(4)
    nv = np.zeros(4)
    for s, n in kept.items():
        lab = l12.decode(s)
        w = n / tot
        js, ns, _ = lab
        q = tuple(ns[v] - cv.N_VAC[v] for v in range(4))
        if any(abs(x) == 2 for x in q):
            acc["P_BBbar"] += w
        elif q == (1, -1, 0, 0):
            acc["P_surv"] += w
            if tuple(js) == (0.0, 0.5, 0.5, 0.5):
                acc["P_stretched"] += w
            elif tuple(js) == (0.5, 0.0, 0.0, 0.0):
                acc["P_short"] += w
        elif all(abs(x) == 1 for x in q):
            acc["P_meson"] += w
        elif sum(ns) == 4:
            acc["P_other"] += w
        e2 += w * np.array([cv.casimir(j) for j in js])
        nv += w * np.array(ns, float)
    for l in range(4):
        acc[f"E2_l{l+1}"] = float(e2[l])
    for v in range(4):
        acc[f"n_v{v+1}"] = float(nv[v])
    acc["dC"] = float(e2.sum() - 2.25)
    return acc


def channel_weights(kept):
    """Return signed-weight channel totals without renormalizing the input."""
    out = {"P_surv": 0.0, "P_meson": 0.0, "P_BBbar": 0.0,
           "P_other": 0.0, "P_stretched": 0.0, "P_short": 0.0}
    for bits, weight in kept.items():
        lab = l12.decode(bits)
        if lab is None:
            continue
        js, ns, _ = lab
        q = tuple(ns[v] - cv.N_VAC[v] for v in range(4))
        if any(abs(x) == 2 for x in q):
            out["P_BBbar"] += weight
        elif q == (1, -1, 0, 0):
            out["P_surv"] += weight
            if tuple(js) == (0.0, 0.5, 0.5, 0.5):
                out["P_stretched"] += weight
            elif tuple(js) == (0.5, 0.0, 0.0, 0.0):
                out["P_short"] += weight
        elif all(abs(x) == 1 for x in q):
            out["P_meson"] += weight
        elif sum(ns) == 4:
            out["P_other"] += weight
    return out


def channel_closure_residual(kept):
    """Check the corrected V11 closure identity on signed quasi-weights."""
    channels = channel_weights(kept)
    lhs = sum(channels[k] for k in ("P_surv", "P_meson", "P_BBbar", "P_other"))
    rhs = 0.0
    for bits, weight in kept.items():
        lab = l12.decode(bits)
        if lab is None:
            continue
        _, ns, _ = lab
        q = tuple(ns[v] - cv.N_VAC[v] for v in range(4))
        if sum(ns) == 4 or any(abs(x) == 2 for x in q):
            rhs += weight
    return float(lhs - rhs)


def matched_subtraction(observed, control):
    """Compute O(t)-O(0) over the union of observable keys."""
    return {key: float(observed.get(key, 0.0) - control.get(key, 0.0))
            for key in set(observed) | set(control)}


def physical_yield(counts, physical_keys):
    """Return the fraction of counts in the supplied physical-key set."""
    total = sum(counts.values())
    return float(sum(value for key, value in counts.items() if key in physical_keys) / total)


def bootstrap(counts_list, n_boot=400, seed=0):
    """Bootstrap over repeats (each element of counts_list is one repeat).
    Returns (mean dict, two_sigma dict, yield mean)."""
    rng = np.random.default_rng(seed)
    per = []
    ys = []
    for c in counts_list:
        k, y = postselect(c)
        per.append(observables(k))
        ys.append(y)
    keys = list(per[0].keys())
    A = np.array([[p[k] for k in keys] for p in per])
    n = len(per)
    boots = np.array([A[rng.integers(0, n, n)].mean(axis=0) for _ in range(n_boot)])
    mean = A.mean(axis=0)
    two_sigma = 2.0 * boots.std(axis=0, ddof=1)
    return (dict(zip(keys, mean.tolist())), dict(zip(keys, two_sigma.tolist())),
            float(np.mean(ys)))
