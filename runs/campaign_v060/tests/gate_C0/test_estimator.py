"""V11 estimator test (campaign v0.6.2, ruling R9).

Four rows, each at 1e-10, each judged against an **independent oracle written
in this file**.  The oracle decodes labels with :func:`l12.decode` and then
classifies them with :func:`_channel_of` below, which is a transcription of the
classification rule of ``predictions_C0.md`` §2.2 / ``conventions.py``:

    q_v = n_v - N_VAC[v],  N_VAC = (0, 2, 0, 2),  N = sum_v n_v

    * BBbar      : some |q_v| = 2                     (any N)
    * surv       : else q = (1, -1, 0, 0)             (hence n = (1, 1, 0, 2), N = 4)
        - stretched : surv and j = (0, 1/2, 1/2, 1/2)
        - short     : surv and j = (1/2, 0, 0, 0)
    * meson      : else all |q_v| = 1
    * other      : else N = 4
    * (no channel): everything else

``twin.channel_weights`` and ``twin.channel_closure_residual`` are **never**
called to produce an expected value; they appear only on the measured side.
The test reads and writes nothing on disk.
"""
from __future__ import annotations

import math


from su2qc import conventions as cv
from su2qc.encodings import l12
from su2qc.twin import twin

TOL = 1e-10

# --------------------------------------------------------------------------
# Independent oracle
# --------------------------------------------------------------------------


def _charges(ns):
    """q_v = n_v - N_VAC[v] from the frozen conventions."""
    return tuple(ns[v] - cv.N_VAC[v] for v in range(4))


def _channel_of(bits):
    """Classify one key.

    Returns ``(channel, sub)`` where ``channel`` is one of
    ``"P_BBbar"``, ``"P_surv"``, ``"P_meson"``, ``"P_other"`` or ``None``
    (no channel), and ``sub`` is ``"P_stretched"``, ``"P_short"`` or ``None``.
    ``None, None`` is also returned for a key ``l12.decode`` rejects.
    """
    label = l12.decode(bits)
    if label is None:
        return None, None
    js, ns, _tag = label
    q = _charges(ns)
    if any(abs(x) == 2 for x in q):
        return "P_BBbar", None
    if q == (1, -1, 0, 0):
        if tuple(js) == (0.0, 0.5, 0.5, 0.5):
            return "P_surv", "P_stretched"
        if tuple(js) == (0.5, 0.0, 0.0, 0.0):
            return "P_surv", "P_short"
        return "P_surv", None
    if all(abs(x) == 1 for x in q):
        return "P_meson", None
    if sum(ns) == 4:
        return "P_other", None
    return None, None


def _oracle_channel_totals(weights):
    """Signed channel totals of ``{key: weight}``, computed by this file only."""
    out = {"P_surv": 0.0, "P_meson": 0.0, "P_BBbar": 0.0,
           "P_other": 0.0, "P_stretched": 0.0, "P_short": 0.0}
    for bits, w in weights.items():
        channel, sub = _channel_of(bits)
        if channel is not None:
            out[channel] += w
        if sub is not None:
            out[sub] += w
    return out


def _oracle_kept_rhs(weights):
    """W_kept(N = 4) + W_kept(N != 4 and some |q_v| = 2), oracle side."""
    n4 = 0.0
    bb_not4 = 0.0
    for bits, w in weights.items():
        label = l12.decode(bits)
        if label is None:
            continue
        _js, ns, _tag = label
        q = _charges(ns)
        if sum(ns) == 4:
            n4 += w
        elif any(abs(x) == 2 for x in q):
            bb_not4 += w
    return n4, bb_not4


# --------------------------------------------------------------------------
# Fixed synthetic codewords, verified by the oracle inside the tests below
# --------------------------------------------------------------------------

# surv / stretched : j = (0, 1/2, 1/2, 1/2), n = (1, 1, 0, 2), N = 4
K_STRETCHED = "111011010001"
# surv / short     : j = (1/2, 0, 0, 0),     n = (1, 1, 0, 2), N = 4
K_SHORT = "100000001010"
# meson            : n = (1, 1, 1, 1), q = (1, -1, 1, -1), N = 4
K_MESON_A = "001010001010"
K_MESON_B = "010001010001"
# other            : N = 4, no |q_v| = 2, not all |q_v| = 1
K_OTHER_A = "001010100000"          # n = (0, 2, 1, 1)
K_OTHER_B = "100000100000"          # n = (0, 2, 0, 2), q = (0, 0, 0, 0)
# BBbar with N != 4 (required by R9 row 1)
K_BB_N2_A = "000100000000"          # n = (0, 0, 2, 0), q = (0, -2, 2, -2), N = 2
K_BB_N2_B = "000000000100"          # n = (2, 0, 0, 0), q = (2, -2, 0, -2), N = 2
# BBbar with N = 4
K_BB_N4 = "000000100100"            # n = (2, 2, 0, 0), q = (2, 0, 0, -2), N = 4
# N != 4 and no |q_v| = 2 -> no channel at all (required by R9 row 1)
K_NOCHANNEL = "001011010000"        # n = (0, 1, 0, 1), q = (0, -1, 0, -1), N = 2

# Keys l12.decode rejects (checked in the tests that use them).
K_UNPHYSICAL = "000000000001"
K_UNPHYSICAL_B = "111111111110"

# Signed quasi-weights.  Three entries are genuinely negative and the BBbar
# total is itself negative.
SYNTHETIC_WEIGHTS = {
    K_STRETCHED: 0.40,
    K_SHORT: -0.15,
    K_MESON_A: 0.25,
    K_MESON_B: -0.05,
    K_OTHER_A: 0.30,
    K_OTHER_B: -0.10,
    K_BB_N2_A: 0.20,
    K_BB_N2_B: -0.45,
    K_BB_N4: 0.10,
    K_NOCHANNEL: 0.60,
}


# --------------------------------------------------------------------------
# Row 1 - synthetic observables with negative quasi-weights
# --------------------------------------------------------------------------


def test_row1_signed_channel_weights_against_closed_form_literals():
    """R9 row 1.

    Ten codewords: two surv (one stretched, one short), two meson, two other,
    two BBbar with N = 2, one BBbar with N = 4, and one N = 2 codeword with no
    |q_v| = 2 which must fall in no channel at all.  Three weights are
    negative, and the BBbar total is negative.

    Closed-form expected values (literals, from the weights above):

        P_stretched =  0.40
        P_short     = -0.15
        P_surv      =  0.40 - 0.15                     =  0.25
        P_meson     =  0.25 - 0.05                     =  0.20
        P_other     =  0.30 - 0.10                     =  0.20
        P_BBbar     =  0.20 - 0.45 + 0.10              = -0.15
        (K_NOCHANNEL's 0.60 appears in none of the six)
    """
    # The oracle must agree with the hand-written channel assignment above.
    assert _channel_of(K_STRETCHED) == ("P_surv", "P_stretched")
    assert _channel_of(K_SHORT) == ("P_surv", "P_short")
    assert _channel_of(K_MESON_A) == ("P_meson", None)
    assert _channel_of(K_MESON_B) == ("P_meson", None)
    assert _channel_of(K_OTHER_A) == ("P_other", None)
    assert _channel_of(K_OTHER_B) == ("P_other", None)
    assert _channel_of(K_BB_N2_A) == ("P_BBbar", None)
    assert _channel_of(K_BB_N2_B) == ("P_BBbar", None)
    assert _channel_of(K_BB_N4) == ("P_BBbar", None)
    assert _channel_of(K_NOCHANNEL) == (None, None)

    # Structural requirements of R9 row 1, asserted rather than assumed.
    for key in (K_BB_N2_A, K_BB_N2_B):
        _js, ns, _tag = l12.decode(key)
        assert sum(ns) != 4
        assert any(abs(x) == 2 for x in _charges(ns))
    _js, ns_none, _tag = l12.decode(K_NOCHANNEL)
    assert sum(ns_none) != 4
    assert not any(abs(x) == 2 for x in _charges(ns_none))
    assert len({_channel_of(k)[0] for k in SYNTHETIC_WEIGHTS}) == 5  # 4 + None
    assert sum(1 for w in SYNTHETIC_WEIGHTS.values() if w < 0.0) >= 2

    measured = twin.channel_weights(SYNTHETIC_WEIGHTS)
    oracle = _oracle_channel_totals(SYNTHETIC_WEIGHTS)

    expected_literals = {
        "P_stretched": 0.40,
        "P_short": -0.15,
        "P_surv": 0.25,
        "P_meson": 0.20,
        "P_other": 0.20,
        "P_BBbar": -0.15,
    }
    for name, expected in expected_literals.items():
        assert math.isclose(oracle[name], expected, abs_tol=TOL), name
        assert math.isclose(measured[name], expected, abs_tol=TOL), name

    # A channel total may be negative; this one is.
    assert measured["P_BBbar"] < 0.0
    assert measured["P_short"] < 0.0

    # The unclassified codeword's weight leaks into nothing.
    assert math.isclose(
        sum(measured[k] for k in ("P_surv", "P_meson", "P_BBbar", "P_other")),
        0.50, abs_tol=TOL)


# --------------------------------------------------------------------------
# Row 2 - closure
# --------------------------------------------------------------------------


def test_row2_closure_identity_from_the_oracle_and_zero_residual():
    """R9 row 2.

    P_surv + P_meson + P_BBbar + P_other
        = W_kept(N = 4) + W_kept(N != 4 and some |q_v| = 2)

    Both sides are computed by this file's oracle.  With the row-1 weights:

        lhs = 0.25 + 0.20 + (-0.15) + 0.20 = 0.50
        W_kept(N = 4)  = 0.40 - 0.15 + 0.25 - 0.05 + 0.30 - 0.10 + 0.10 = 0.75
        W_kept(N != 4, some |q_v| = 2) = 0.20 - 0.45 = -0.25
        rhs = 0.75 - 0.25 = 0.50
    """
    oracle = _oracle_channel_totals(SYNTHETIC_WEIGHTS)
    lhs = sum(oracle[k] for k in ("P_surv", "P_meson", "P_BBbar", "P_other"))
    n4, bb_not4 = _oracle_kept_rhs(SYNTHETIC_WEIGHTS)

    assert math.isclose(lhs, 0.50, abs_tol=TOL)
    assert math.isclose(n4, 0.75, abs_tol=TOL)
    assert math.isclose(bb_not4, -0.25, abs_tol=TOL)
    assert math.isclose(lhs, n4 + bb_not4, abs_tol=TOL)

    assert math.isclose(twin.channel_closure_residual(SYNTHETIC_WEIGHTS),
                        0.0, abs_tol=TOL)


W_BAD = 0.37  # weight carried by the unphysical key of the violating input

VIOLATING_WEIGHTS = dict(SYNTHETIC_WEIGHTS)
VIOLATING_WEIGHTS[K_UNPHYSICAL] = W_BAD


def test_row2_unphysical_key_is_rejected_by_decode():
    """The violating input's extra key must be one ``l12.decode`` rejects."""
    assert l12.decode(K_UNPHYSICAL) is None
    assert not l12.is_physical(K_UNPHYSICAL)
    assert K_UNPHYSICAL in VIOLATING_WEIGHTS
    assert VIOLATING_WEIGHTS[K_UNPHYSICAL] == W_BAD
    # The physical part of the violating input is unchanged, so the whole of
    # any nonzero residual must be the unphysical key's weight.
    physical_part = {k: v for k, v in VIOLATING_WEIGHTS.items()
                     if l12.decode(k) is not None}
    assert physical_part == SYNTHETIC_WEIGHTS


def test_row2_violating_input_must_give_the_correct_nonzero_residual():
    """R9 row 2, violating input.

    The input is the row-1 dictionary plus one key that ``l12.decode``
    rejects, carrying weight 0.37.  The physical part closes exactly
    (residual 0), so the identity's defect on this input is exactly the
    unphysical key's weight: |residual| must equal 0.37, and in particular
    must not be 0.
    """
    residual = twin.channel_closure_residual(VIOLATING_WEIGHTS)
    assert abs(residual) > TOL
    assert math.isclose(abs(residual), W_BAD, abs_tol=TOL)


# --------------------------------------------------------------------------
# Row 3 - remainder identity
# --------------------------------------------------------------------------

# Deterministic signed weights over every physical codeword, no RNG needed:
# a fixed irrational-ish sweep that produces both signs and no accidental
# cancellation pattern.
_ALL_CODE_WEIGHTS = {
    format(code, "012b"): math.sin(1.0 + 0.7 * i) * (1.0 + 0.25 * i)
    for i, code in enumerate(l12.physical_codes())
}

_ROW3_INPUTS = [
    SYNTHETIC_WEIGHTS,
    VIOLATING_WEIGHTS,
    {K_STRETCHED: 1.0},
    {K_SHORT: -2.5},
    {K_STRETCHED: -0.75, K_SHORT: 0.75},
    {K_STRETCHED: 0.3, K_SHORT: 0.2, K_MESON_A: -1.0, K_BB_N2_A: 4.0},
    {K_NOCHANNEL: 9.0, K_UNPHYSICAL: -3.0, K_UNPHYSICAL_B: 1.5},
    _ALL_CODE_WEIGHTS,
]


def test_row3_surv_splits_exactly_into_stretched_plus_short():
    """R9 row 3 - the remainder identity, with its derivation.

    Derivation (j_max = 1/2, conventions.py LINKS/N_VAC).  The q = (1, -1, 0, 0)
    sector is n = (1, 1, 0, 2) because q_v = n_v - N_VAC[v] with
    N_VAC = (0, 2, 0, 2).  Every vertex of the single-plaquette patch is
    2-valent, with incidences v1:{l4, l1}, v2:{l1, l2}, v3:{l2, l3},
    v4:{l3, l4}; Gauss's law at a 2-valent vertex says the matter spin j_m
    (j_m = 0 for n_v in {0, 2}, j_m = 1/2 for n_v = 1) must appear in
    j_a (x) j_b, i.e. j_a = j_b when n_v is 0 or 2 and |j_a - j_b| = 1/2 when
    n_v = 1.

      * v3 has n = 0 and v4 has n = 2, so both force equal incident spins:
        v3 gives j2 = j3 and v4 gives j3 = j4, hence j2 = j3 = j4.
      * v1 has n = 1 and v2 has n = 1, so both force |j4 - j1| = 1/2 and
        |j1 - j2| = 1/2; with j2 = j4 this says j1 differs from the common
        value j2 = j3 = j4 by exactly one half.

    At j_max = 1/2 the only spins are 0 and 1/2, so the common value is either
    1/2 (then j1 = 0) or 0 (then j1 = 1/2).  The sector therefore holds
    **exactly two** link configurations,

        (j1, j2, j3, j4) = (0, 1/2, 1/2, 1/2)   -- "stretched"
        (j1, j2, j3, j4) = (1/2, 0, 0, 0)       -- "short"

    and nothing else.  Consequently P_surv - P_stretched - P_short = 0 as an
    exact equality on any input.  (At j_max = 1 the same counting gives four;
    that is a Phase 2 note, not a C0 row.)
    """
    # Enumeration half of the row: l12 has exactly two physical codes with the
    # occupation pattern n = (1, 1, 0, 2), and they carry those two spin sets.
    matching = [c for c in l12.physical_codes()
                if l12.decode(c)[1] == (1, 1, 0, 2)]
    assert len(matching) == 2
    assert {tuple(l12.decode(c)[0]) for c in matching} == {
        (0.0, 0.5, 0.5, 0.5), (0.5, 0.0, 0.0, 0.0)}
    # ... and the q = (1, -1, 0, 0) sector is exactly that occupation pattern.
    assert [c for c in l12.physical_codes()
            if _charges(l12.decode(c)[1]) == (1, -1, 0, 0)] == matching

    for i, weights in enumerate(_ROW3_INPUTS):
        oracle = _oracle_channel_totals(weights)
        assert math.isclose(
            oracle["P_surv"] - oracle["P_stretched"] - oracle["P_short"],
            0.0, abs_tol=TOL), f"oracle input {i}"
        measured = twin.channel_weights(weights)
        assert math.isclose(
            measured["P_surv"] - measured["P_stretched"] - measured["P_short"],
            0.0, abs_tol=TOL), f"measured input {i}"


# --------------------------------------------------------------------------
# Row 4 - matched subtraction and yield
# --------------------------------------------------------------------------

# Synthetic pair: observed (t) and control (0) weight dictionaries over the
# same codewords, so DeltaO is a per-channel difference of oracle totals.
_PAIR_CONTROL = {
    K_STRETCHED: 0.50,
    K_SHORT: 0.10,
    K_MESON_A: 0.20,
    K_OTHER_A: 0.15,
    K_BB_N2_A: 0.05,
}
_PAIR_OBSERVED = {
    K_STRETCHED: 0.20,
    K_SHORT: 0.25,
    K_MESON_A: 0.30,
    K_OTHER_A: 0.05,
    K_BB_N2_A: -0.10,
}

# 600 of 1000 counts sit on codewords l12.decode accepts -> yield 0.6 exactly.
_YIELD_COUNTS = {
    K_STRETCHED: 300,
    K_SHORT: 200,
    K_MESON_A: 100,
    K_UNPHYSICAL: 250,
    K_UNPHYSICAL_B: 150,
}


def test_row4_matched_subtraction_and_postselected_yield():
    """R9 row 4.

    DeltaO on a synthetic (observed, control) pair, expected from the oracle's
    channel totals and cross-checked against closed-form literals:

        P_stretched : 0.20 - 0.50 = -0.30
        P_short     : 0.25 - 0.10 =  0.15
        P_surv      : 0.45 - 0.60 = -0.15
        P_meson     : 0.30 - 0.20 =  0.10
        P_other     : 0.05 - 0.15 = -0.10
        P_BBbar     : -0.10 - 0.05 = -0.15

    The yield is measured with ``twin.postselect`` on synthetic counts that
    mix physical and unphysical bitstrings: 300 + 200 + 100 = 600 physical of
    1000 total, so the physical fraction is exactly 0.6.  No caller-supplied
    key set is used anywhere in this row.
    """
    oracle_obs = _oracle_channel_totals(_PAIR_OBSERVED)
    oracle_ctl = _oracle_channel_totals(_PAIR_CONTROL)
    expected = {k: oracle_obs[k] - oracle_ctl[k] for k in oracle_obs}

    literals = {"P_stretched": -0.30, "P_short": 0.15, "P_surv": -0.15,
                "P_meson": 0.10, "P_other": -0.10, "P_BBbar": -0.15}
    for name, value in literals.items():
        assert math.isclose(expected[name], value, abs_tol=TOL), name

    delta = twin.matched_subtraction(twin.channel_weights(_PAIR_OBSERVED),
                                     twin.channel_weights(_PAIR_CONTROL))
    assert set(delta) == set(expected)
    for name, value in expected.items():
        assert math.isclose(delta[name], value, abs_tol=TOL), name

    # Yield through postselect, with the physical fraction known independently.
    physical_total = sum(n for k, n in _YIELD_COUNTS.items()
                         if l12.decode(k) is not None)
    total = sum(_YIELD_COUNTS.values())
    assert physical_total == 600 and total == 1000

    kept, yield_fraction = twin.postselect(_YIELD_COUNTS)
    assert set(kept) == {K_STRETCHED, K_SHORT, K_MESON_A}
    assert sum(kept.values()) == physical_total
    assert math.isclose(yield_fraction, 0.6, abs_tol=TOL)
    assert math.isclose(yield_fraction, physical_total / total, abs_tol=TOL)
