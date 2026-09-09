"""Noise-model twin: FakeTorino (or a real backend's properties) via
AerSimulator.from_backend, with leakage post-selection and observables.

  twin_backend(seed)              -> AerSimulator noise twin
  run_counts(isa_circs, shots, seed, backend) -> list of counts dicts (physical
        bit order already mapped back to LOGICAL q11..q0 strings via the
        circuit's final layout, so l12.decode applies directly); per-repeat
        seeds are spawned from `seed` and reported by run_counts_meta()
  run_counts_meta()               -> {base_seed, shots, n_repeats, seeds, ...}
        for the last run_counts call (also module-level LAST_SEEDS)
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


#: Seeds actually handed to ``sim.run(..., seed_simulator=...)`` by the most
#: recent :func:`run_counts` call, in repeat order.  Read it through
#: :func:`run_counts_meta` so the gate ledger can record what was used.
LAST_SEEDS: list[int] = []

#: Metadata of the most recent :func:`run_counts` call (see run_counts_meta).
_LAST_META: dict = {}


def spawn_seeds(seed, n):
    """Derive ``n`` independent simulator seeds from a single ``seed``.

    Uses ``numpy.random.SeedSequence(seed).spawn(n)`` and reduces each child
    to a 31-bit non-negative int (the range Aer accepts).  Adjacent seeds are
    then unrelated, which the ``seed + k`` scheme they replace was not: Aer
    seeds shot ``i`` of a sampled-noise run with ``seed_simulator + i``, so a
    run at ``s + 1`` replayed shots 1..N-1 of the run at ``s`` (campaign
    ruling R7; mechanism evidence
    ``runs/campaign_v060/sessions/c060_p0_20260909_5/seed-mechanism.json``).

    Deterministic: the same ``seed`` and ``n`` always give the same list.
    """
    ss = np.random.SeedSequence(int(seed))
    return [int(child.generate_state(1, dtype=np.uint32)[0]) & 0x7FFFFFFF
            for child in ss.spawn(int(n))]


def run_counts(isa_meas_list, shots, seed, sim):
    """Run each measured ISA circuit once and return its counts dict.

    Per-repeat seeds are spawned from ``seed`` (see :func:`spawn_seeds`) and
    passed **only** through ``sim.run(..., seed_simulator=...)``; the backend
    object handed in by the caller is never mutated (the previous
    ``sim.set_options(seed_simulator=...)`` mutation is gone, ruling R7).
    The seeds used are exposed via :data:`LAST_SEEDS` / :func:`run_counts_meta`.
    """
    from qiskit import transpile
    global LAST_SEEDS, _LAST_META
    seeds = spawn_seeds(seed, len(isa_meas_list))
    out = []
    for k, qc in enumerate(isa_meas_list):
        # optimization_level=0 on an already-ISA circuit: kept inside the loop
        # and with the unchanged fixed seed_transpiler so the transpiled
        # circuits are bit-for-bit what the v0.5.0 pipeline produced.
        t = transpile(qc, sim, optimization_level=0, seed_transpiler=seed)
        res = sim.run(t, shots=shots, seed_simulator=seeds[k]).result()
        out.append(dict(res.get_counts()))
    LAST_SEEDS = list(seeds)
    _LAST_META = {"base_seed": int(seed), "shots": int(shots),
                  "n_repeats": len(isa_meas_list), "seeds": list(seeds),
                  "seed_derivation": "numpy.random.SeedSequence(seed).spawn(n), 31-bit"}
    return out


def run_counts_meta():
    """Metadata of the most recent :func:`run_counts` call.

    Keys: ``base_seed``, ``shots``, ``n_repeats``, ``seeds`` (the per-repeat
    ``seed_simulator`` values actually used) and ``seed_derivation``.
    Returns a copy; empty dict before the first call.
    """
    return dict(_LAST_META)


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


def undecodable_weight(kept):
    """Total weight of keys that ``l12.decode`` rejects.

    ``kept`` is by contract the output of :func:`postselect`, which admits only
    physical codes, so this is zero on any contract-satisfying input. A nonzero
    value means the caller handed in unfiltered or corrupted counts.
    """
    return float(sum(weight for bits, weight in kept.items()
                     if l12.decode(bits) is None))


def channel_closure_residual(kept):
    """Check the corrected V11 closure identity on signed quasi-weights.

    residual = sum of the four channel totals
             - [ W(N = 4) + W(N != 4 and some |q_v| = 2) + W(undecodable) ]

    The undecodable term is the campaign ruling of 2026-09-09 on R9 (session
    c060_p0_20260909_5, ``ruling-R9-closure-residual.md``). It is identically
    zero whenever every key decodes, so the residual is unchanged on every
    contract-satisfying input and no gated number moves; on an input carrying an
    unphysical key it makes the residual equal to minus that key's weight, which
    is what lets the gate detect the violation. Both sides previously skipped
    undecodable keys, so such a key perturbed neither and the residual could not
    see it. A decodable key that falls in no channel stays outside both sides,
    because it is legitimate physical weight the four channels do not claim.
    """
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
    rhs += undecodable_weight(kept)
    return float(lhs - rhs)


def matched_subtraction(observed, control):
    """Compute O(t)-O(0) over the union of observable keys."""
    return {key: float(observed.get(key, 0.0) - control.get(key, 0.0))
            for key in set(observed) | set(control)}


def physical_yield(counts, physical_keys):
    """Return the fraction of counts in the supplied physical-key set.

    An empty input (total count zero) returns ``0.0`` rather than raising
    ``ZeroDivisionError``, matching :func:`postselect`, which returns
    ``({}, 0.0)`` on the same input (Fable ruling, session
    ``c060_p0_20260909_5``).
    """
    total = sum(counts.values())
    if not total:
        return 0.0
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
