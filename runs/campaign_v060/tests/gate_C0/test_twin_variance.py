"""V10 acceptance for gate C0, per campaign ruling R8 (prompt v0.6.2 §1).

Everything here runs on the **production twin** -- ``twin.twin_backend(seed=101)``,
i.e. the ``AerSimulator.from_backend(FakeTorino)`` path that
``su2qc/compile/run_g4.py`` uses.  The superseded version of this test used
``twin_backend(compact=True)``; that branch builds a bare ``AerSimulator`` from
a ``NoiseModel`` and is *not* what any campaign number was produced on, so R8
puts the acceptance on the production path.

What R8 requires, and where it is checked:

  (a) five distinct count dictionaries at r = 0 and r = 1
      -> ``test_r0_five_distinct``, ``test_r1_five_distinct``
  (b) for every observable whose multinomial variance ``Var_s`` (computed from
      the *pooled kept counts*, values ``o_k`` per codeword, ``predictions_C0.md``
      §2.2) is nonzero, ``two_sigma/2`` lies within a factor 2 of
      ``0.894 * sqrt(Var_s / (5 * N_kept_mean))``
      -> ``test_r0_variance_matches_multinomial``, ``test_r1_...``
  (c) observables with ``Var_s == 0`` are listed as *structurally empty*
      (``predictions_C0.md`` §2.5) and are never counted as failures nor as
      evidence of a deterministic twin
      -> they are recorded in ``structurally_empty`` and skipped by (b)
  (d) the D-C0 case letter of ``predictions_C0.md`` §3.4 is recorded with its
      mechanism -> ``test_dc0_case_recorded``
  (e) the negative control is an actual **run** with all five run-time seeds
      forced equal, which must yield exactly one distinct dictionary
      -> ``test_negative_control_equal_seeds_is_one_dictionary``

The 0.894 = sqrt((R-1)/R) factor is the preregistered bootstrap deficit of
``predictions_C0.md`` §2.3 (the nonparametric bootstrap SE of a mean of R
values uses the ddof=0 sample SD).  The acceptance band is the factor-2 band
of v0.6.0 line 142.  Nothing here may be loosened.

Shots are the R8 numbers: r = 0 at 4,000 and r = 1 at 1,024, five repeats each.
Evidence is written to this session's directory only, at a repository-anchored
path (never a cwd-relative one, and never into an earlier session).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from qiskit import transpile

from su2qc.circuits.strang_l12 import full_circuit
from su2qc.twin import twin

# --------------------------------------------------------------------------
# Preregistered constants (R8 / predictions_C0.md).  Do not adjust.
SESSION_TAG = "c060_p0_20260909_5"
REPEATS = 5
SHOTS = {0: 4000, 1: 1024}
BASE_SEED = {0: 500, 1: 510}          # run_g4.py uses 500 + 10*r
CONSTRUCTION_SEED = 101               # run_g4.py: twin.twin_backend(seed=101)
BOOTSTRAP_N_BOOT = 2000
BOOTSTRAP_SEED = 77
BOOTSTRAP_DEFICIT = 0.894             # sqrt((R-1)/R), predictions_C0.md §2.3
RATIO_BAND = (0.5, 2.0)               # v0.6.0 line 142, factor 2

# runs/campaign_v060/tests/gate_C0/<this file> -> runs/campaign_v060
CAMPAIGN_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = CAMPAIGN_DIR / "sessions" / SESSION_TAG / "twin_variance.json"


# --------------------------------------------------------------------------
def _signature(counts):
    return tuple(sorted(counts.items()))


def _production_twin():
    """The exact backend object run_g4.py builds."""
    return twin.twin_backend(seed=CONSTRUCTION_SEED)


def _measured_circuit(sim, r):
    isa = transpile(full_circuit(r), sim, optimization_level=0,
                    seed_transpiler=CONSTRUCTION_SEED)
    return twin.add_measurements(isa)


def _codeword_values(bitstring):
    """o_k: the value every observable takes on a single kept codeword.

    ``twin.observables`` accumulates ``w = n/tot`` times a per-codeword value,
    so evaluating it on the one-element sample {bitstring: 1} returns exactly
    the o_k vector of predictions_C0.md §2.2.  (``dC`` carries a constant
    offset, which drops out of a variance.)
    """
    return twin.observables({bitstring: 1})


def _multinomial_variance(pooled_kept):
    """Var_s = sum_k p_k o_k^2 - (sum_k p_k o_k)^2 from the pooled kept counts."""
    total = sum(pooled_kept.values())
    assert total > 0, "pooled kept sample is empty"
    first, second = {}, {}
    for bits, n in pooled_kept.items():
        p = n / total
        for key, o in _codeword_values(bits).items():
            first[key] = first.get(key, 0.0) + p * o
            second[key] = second.get(key, 0.0) + p * o * o
    return {key: max(second[key] - first[key] ** 2, 0.0) for key in first}


def _dc0_case(record):
    """The D-C0 case letter of predictions_C0.md §3.4, with its mechanism."""
    distinct_ok = all(record[str(r)]["distinct_dictionaries"] == REPEATS
                      for r in SHOTS)
    if not distinct_ok:
        return ("identical-dictionaries branch",
                "at least one r gave fewer than five distinct dictionaries: the "
                "construction-time seed_simulator wins over the run-time seed; "
                "locate the cause and fix before re-running (predictions_C0.md "
                "§3.4 row 1)")
    dead = [(r, key) for r in SHOTS
            for key, row in record[str(r)]["observables"].items()
            if row["Var_s"] > 0.0 and row["two_sigma"] == 0.0]
    if dead:
        return ("D-C0 triggered",
                "sigma = 0 on an observable with interior predicted P "
                f"({dead}); D-C0's escalation clause fires (predictions_C0.md "
                "§3.4 row 4)")
    return ("A",
            "five distinct dictionaries at r = 0 and r = 1 with bootstrap "
            "two_sigma/2 inside the factor-2 band of the multinomial "
            "expectation on every Var_s > 0 observable; the observables with "
            "two_sigma = 0 are exactly the structurally empty ones "
            "(Var_s = 0, predictions_C0.md §2.5), so the r = 1 escalation "
            "clause of D-C0 does not fire.  Mechanism: the run-time "
            "seed_simulator overrides the construction-time seed 101, and the "
            "per-repeat seeds spawned by numpy SeedSequence (ruling R7) are "
            "independent rather than shifted replays of one another.  Recorded "
            "verdict: override harmless (predictions_C0.md §3.4 row 2).")


def _run_one(r):
    sim = _production_twin()
    meas = _measured_circuit(sim, r)
    counts = twin.run_counts([meas] * REPEATS, SHOTS[r], BASE_SEED[r], sim)
    meta = twin.run_counts_meta()

    pooled = {}
    kept_sizes = []
    for c in counts:
        kept, _ = twin.postselect(c)
        kept_sizes.append(sum(kept.values()))
        for bits, n in kept.items():
            pooled[bits] = pooled.get(bits, 0) + n
    n_kept_mean = sum(kept_sizes) / REPEATS

    mean, two_sigma, yield_mean = twin.bootstrap(
        counts, n_boot=BOOTSTRAP_N_BOOT, seed=BOOTSTRAP_SEED)
    var_s = _multinomial_variance(pooled)

    observables = {}
    structurally_empty = []
    for key in sorted(two_sigma):
        v = var_s.get(key, 0.0)
        row = {"mean": mean[key], "two_sigma": two_sigma[key], "Var_s": v}
        if v > 0.0:
            predicted_se = BOOTSTRAP_DEFICIT * math.sqrt(v / (REPEATS * n_kept_mean))
            row["predicted_se"] = predicted_se
            row["ratio"] = (two_sigma[key] / 2.0) / predicted_se
        else:
            row["predicted_se"] = 0.0
            row["ratio"] = None
            row["structurally_empty"] = True
            structurally_empty.append(key)
        observables[key] = row

    return {
        "r": r,
        "shots": SHOTS[r],
        "repeats": REPEATS,
        "backend_path": "twin.twin_backend(seed=101) "
                        "= AerSimulator.from_backend(FakeTorino) (production)",
        "construction_seed_simulator": CONSTRUCTION_SEED,
        "base_seed": BASE_SEED[r],
        "runtime_seeds": meta["seeds"],
        "seed_derivation": meta["seed_derivation"],
        "distinct_dictionaries": len({_signature(c) for c in counts}),
        "key_counts": [len(c) for c in counts],
        "kept_per_repeat": kept_sizes,
        "N_kept_mean": n_kept_mean,
        "yield_mean": yield_mean,
        "bootstrap": {"n_boot": BOOTSTRAP_N_BOOT, "seed": BOOTSTRAP_SEED,
                      "deficit_factor": BOOTSTRAP_DEFICIT},
        "acceptance_band": list(RATIO_BAND),
        "observables": observables,
        "structurally_empty": structurally_empty,
    }


def _negative_control():
    """R8(e): a real run with all five run-time seeds forced equal.

    ``twin.run_counts`` derives its per-repeat seeds through
    ``twin.spawn_seeds``; replacing that derivation with a constant makes the
    five repeats share one ``seed_simulator`` while every other step (the same
    circuit, the same backend object, the same shot count) is untouched.  This
    is a run, not a list comprehension over one dictionary.
    """
    r = 0
    sim = _production_twin()
    meas = _measured_circuit(sim, r)
    forced = twin.spawn_seeds(BASE_SEED[r], REPEATS)[0]
    original = twin.spawn_seeds
    try:
        twin.spawn_seeds = lambda seed, n: [forced] * int(n)
        counts = twin.run_counts([meas] * REPEATS, SHOTS[r], BASE_SEED[r], sim)
        seeds = twin.run_counts_meta()["seeds"]
    finally:
        twin.spawn_seeds = original
    return {
        "r": r,
        "shots": SHOTS[r],
        "repeats": REPEATS,
        "mechanism": "all five run-time seed_simulator values forced equal; "
                     "a real run of twin.run_counts on the production twin",
        "runtime_seeds": seeds,
        "distinct_dictionaries": len({_signature(c) for c in counts}),
        "key_counts": [len(c) for c in counts],
    }


# --------------------------------------------------------------------------
_EVIDENCE = {}


def _evidence():
    """Run the whole V10 measurement once and write this session's evidence."""
    if _EVIDENCE:
        return _EVIDENCE
    record = {str(r): _run_one(r) for r in sorted(SHOTS)}
    record["negative_control"] = _negative_control()
    case, mechanism = _dc0_case(record)
    record["D_C0_case"] = case
    record["D_C0_mechanism"] = mechanism
    record["ruling"] = "R8 (prompt v0.6.2 §1); predictions_C0.md §§2.2, 2.5, 3.4"
    record["session"] = SESSION_TAG
    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(json.dumps(record, indent=2, sort_keys=False) + "\n")
    _EVIDENCE.update(record)
    return _EVIDENCE


def _assert_variance(r):
    row = _evidence()[str(r)]
    lo, hi = RATIO_BAND
    bad = []
    checked = 0
    for key, obs in row["observables"].items():
        if obs["Var_s"] <= 0.0:
            continue          # R8(c): structurally empty, never a failure
        checked += 1
        if not lo <= obs["ratio"] <= hi:
            bad.append(
                f"{key}: two_sigma/2={obs['two_sigma'] / 2.0:.6g} "
                f"predicted_se={obs['predicted_se']:.6g} "
                f"ratio={obs['ratio']:.4g} Var_s={obs['Var_s']:.6g}")
    assert checked > 0, (
        f"r={r}: no observable had Var_s > 0; the multinomial prediction is "
        f"degenerate everywhere, so V10 cannot be evaluated. "
        f"structurally empty: {row['structurally_empty']}")
    assert not bad, (
        f"r={r}: {len(bad)} of {checked} Var_s > 0 observables outside the "
        f"factor-2 band (N_kept_mean={row['N_kept_mean']}, "
        f"yield={row['yield_mean']:.4f}): " + "; ".join(bad))


# --------------------------------------------------------------------------
def test_r0_five_distinct():
    """R8(a) at r = 0: five repeats, five distinct dictionaries."""
    row = _evidence()["0"]
    assert row["distinct_dictionaries"] == REPEATS, (
        f"r=0: {row['distinct_dictionaries']} distinct of {REPEATS}; "
        f"seeds={row['runtime_seeds']} key_counts={row['key_counts']}")


def test_r1_five_distinct():
    """R8(a) at r = 1: five repeats, five distinct dictionaries."""
    row = _evidence()["1"]
    assert row["distinct_dictionaries"] == REPEATS, (
        f"r=1: {row['distinct_dictionaries']} distinct of {REPEATS}; "
        f"seeds={row['runtime_seeds']} key_counts={row['key_counts']}")


def test_r0_variance_matches_multinomial():
    """R8(b)/(c) at r = 0."""
    _assert_variance(0)


def test_r1_variance_matches_multinomial():
    """R8(b)/(c) at r = 1."""
    _assert_variance(1)


def test_structurally_empty_observables_are_listed():
    """R8(c): every zero-variance observable is recorded as structurally empty.

    A zero bootstrap sigma there is agreement with the multinomial prediction
    (predictions_C0.md §2.5), not evidence of a deterministic twin, so the
    evidence file must name them rather than let them pass silently.
    """
    ev = _evidence()
    for r in SHOTS:
        row = ev[str(r)]
        zero = {k for k, o in row["observables"].items() if o["Var_s"] <= 0.0}
        assert set(row["structurally_empty"]) == zero
        for key in zero:
            assert row["observables"][key]["structurally_empty"] is True


def test_runtime_seeds_are_independent_and_recorded():
    """Ruling R7: seeds come from SeedSequence.spawn, not from `seed + k`.

    Consecutive Aer seeds share N-1 of N shots (session c060_p0_20260909_5,
    seed-mechanism.json: shift_matches 1023 of 1024 at seeds 500 -> 501), so
    the seeds actually used must be far apart and must be reported.
    """
    ev = _evidence()
    for r in SHOTS:
        seeds = ev[str(r)]["runtime_seeds"]
        assert len(seeds) == REPEATS and len(set(seeds)) == REPEATS
        assert all(0 <= s < 2 ** 31 for s in seeds)
        assert seeds == twin.spawn_seeds(BASE_SEED[r], REPEATS), (
            "run_counts must derive its seeds deterministically from the base "
            "seed argument")
        assert all(abs(seeds[i + 1] - seeds[i]) > SHOTS[r]
                   for i in range(REPEATS - 1)), (
            f"r={r}: adjacent seeds {seeds} are closer than the shot count, so "
            "Aer's per-shot seeding would make the repeats overlap")


def test_negative_control_equal_seeds_is_one_dictionary():
    """R8(e): a real run with all five run-time seeds equal is degenerate."""
    ctrl = _evidence()["negative_control"]
    assert len(set(ctrl["runtime_seeds"])) == 1, ctrl["runtime_seeds"]
    assert ctrl["distinct_dictionaries"] == 1, (
        "the equal-seed control produced "
        f"{ctrl['distinct_dictionaries']} distinct dictionaries: the twin has "
        "an unseeded stochastic path and V10 fails regardless of the r = 0 "
        "result (predictions_C0.md §3.4, negative control)")


def test_dc0_case_recorded():
    """R8(d): the D-C0 case letter of predictions_C0.md §3.4, with mechanism."""
    ev = _evidence()
    assert ev["D_C0_case"] == "A", (
        f"D-C0 case {ev['D_C0_case']!r}: {ev['D_C0_mechanism']}")
    assert ev["D_C0_mechanism"]


def test_evidence_written_to_this_session():
    """Both r keys present, in this session's directory only."""
    _evidence()
    assert EVIDENCE_PATH.exists(), EVIDENCE_PATH
    on_disk = json.loads(EVIDENCE_PATH.read_text())
    assert {"0", "1"} <= set(on_disk)
    assert on_disk["session"] == SESSION_TAG
    assert EVIDENCE_PATH.parent.name == SESSION_TAG
