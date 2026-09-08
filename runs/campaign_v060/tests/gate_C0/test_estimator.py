import math

from su2qc.encodings import l12
from su2qc.twin import twin


def test_v11_synthetic_channels_support_signed_weights_and_exact_closure():
    labels = [
        ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0),
        ((0.5, 0.0, 0.0, 0.0), (1, 1, 0, 2), 0),
        ((0.0, 0.0, 0.0, 0.0), (2, 0, 0, 0), 0),
    ]
    counts = {l12.encode(label): weight for label, weight in zip(labels, (0.7, 0.2, 0.1))}
    channels = twin.channel_weights(counts)
    assert math.isclose(channels["P_stretched"], 0.7, abs_tol=1e-10)
    assert math.isclose(channels["P_short"], 0.2, abs_tol=1e-10)
    assert math.isclose(channels["P_surv"], 0.9, abs_tol=1e-10)
    assert math.isclose(channels["P_BBbar"], 0.1, abs_tol=1e-10)
    assert math.isclose(twin.channel_closure_residual(counts), 0.0, abs_tol=1e-10)
    assert channels["P_stretched"] > 0
    assert channels["P_short"] > 0
    assert channels["P_surv"] >= channels["P_stretched"] + channels["P_short"]
    signed = dict(counts)
    signed[next(iter(signed))] -= 0.8
    assert signed[next(iter(signed))] < 0.0
    assert math.isclose(twin.channel_closure_residual(signed), 0.0, abs_tol=1e-10)


def test_v11_matched_subtraction_and_yield():
    before = {"P_stretched": 0.8, "P_meson": 0.1}
    after = {"P_stretched": 0.5, "P_meson": 0.3}
    delta = twin.matched_subtraction(after, before)
    assert math.isclose(delta["P_stretched"], -0.3, abs_tol=1e-10)
    assert math.isclose(delta["P_meson"], 0.2, abs_tol=1e-10)
    counts = {"0000": 3, "1111": 1}
    assert math.isclose(twin.physical_yield(counts, physical_keys={"0000"}), 0.75)
