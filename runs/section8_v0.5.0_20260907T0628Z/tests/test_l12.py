import pytest

from su2qc.encodings.l12 import decode, encode, is_physical, physical_codes

pytestmark = pytest.mark.unit

def test_roundtrip_and_dimension():
    assert len(physical_codes()) == 82
    assert len(set(physical_codes())) == 82
    for code in physical_codes():
        assert is_physical(code)
        assert encode(decode(code)) == code

def test_stretched_string_integer_and_bit_order():
    label = ((0., .5, .5, .5), (1, 1, 0, 2), 0)
    assert encode(label) == 3793
    assert format(encode(label), "012b") == "111011010001"  # q11 ... q0
    assert decode("111011010001") == label
