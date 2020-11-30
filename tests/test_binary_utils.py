from lib.alu import max_32_bits_signed, min_32_bits_signed
from lib.binary_utils import BinaryUtils


def test_positive():
    assert BinaryUtils.to_2cb(0) == '0' * 32
    assert BinaryUtils.to_2cb(1) == ('0' * 31 + '1')
    assert BinaryUtils.to_2cb(max_32_bits_signed) == ('0' + '1' * 31)


def test_negative():
    assert BinaryUtils.to_2cb(-1) == ('1' * 32)
    assert BinaryUtils.to_2cb(min_32_bits_signed) == ('1' + '0' * 31)


def test_negation():
    assert BinaryUtils.neg('1' * 32) == '0' * 32
    assert BinaryUtils.neg('0' * 32) == '1' * 32


def test_msb():
    assert BinaryUtils.msb(1) == 0
    assert BinaryUtils.msb(0) == 0
    assert BinaryUtils.msb(-1) == 1
