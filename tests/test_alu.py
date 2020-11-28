import pytest

from lib.alu import *


@pytest.fixture
def alu():
    return ALU()


def test__value_with_carry(alu: ALU):
    v1 = max_32_bits
    assert alu._value_with_carry(v1) == v1
    assert alu.carry == 0

    assert alu._value_with_carry(v1 * 2) == max_32_bits
    assert alu.carry == 1

    assert alu._value_with_carry(v1 + 1) == 1
    assert alu.carry == 1

    v2 = min_32_bits
    assert alu._value_with_carry(v2) == v2
    assert alu.carry == 0

    assert alu._value_with_carry(v2 * 2) == min_32_bits
    assert alu.carry == 1

    assert alu._value_with_carry(v2 - 1) == -1
    assert alu.carry == 1


def test__value(alu: ALU):
    assert min_32_bits == alu._value(min_32_bits)
    assert alu.zero == 0
    assert alu.negative == 1

    assert max_32_bits == alu._value(max_32_bits)
    assert alu.zero == 0
    assert alu.negative == 0

    assert alu._value(0) == 0
    assert alu.zero == 1
    assert alu.negative == 0

    with pytest.raises(ValueError):
        alu._value(max_32_bits + 1)

    with pytest.raises(ValueError):
        alu._value(min_32_bits - 1)


def test_adc(alu: ALU):
    alu.previous_spec_reg_carry = 1
    assert alu.adc(1, 2) == 4
    assert alu.adc(max_32_bits, 0) == 1
    assert alu.carry == 1
    assert alu.adc(max_32_bits, 1) == 2
    assert alu.carry == 1
    assert alu.adc(min_32_bits, -2) == -1
    assert alu.carry == 1


def test_add_or_cmn(alu: ALU):
    assert alu.add_or_cmn(1, 2) == 3
    assert alu.add_or_cmn(max_32_bits, 1) == 1
    assert alu.carry == 1
    assert alu.add_or_cmn(min_32_bits, -10) == -10
    assert alu.carry == 1


def test_bitwise_and(alu: ALU):
    assert alu.bitwise_and(0, 1) == 0
    assert alu.bitwise_and(0, 0) == 0
    assert alu.bitwise_and(1, 0) == 0
    assert alu.bitwise_and(1, 1) == 1
    assert alu.bitwise_and(2, 1) == 0
    assert alu.bitwise_and(3, 1) == 1
    assert alu.bitwise_and(-1, -1) == -1
    assert alu.bitwise_and(-1, 0) == 0
    assert alu.bitwise_and(-1, -2) == -2
    assert alu.bitwise_and(-2, -3) == -4


def test_bic(alu: ALU):
    assert alu.bic(1, 1) == 0
    assert alu.bic(1, 0) == 1
    assert alu.bic(0, 1) == 0
    assert alu.bic(0, 0) == 0
    assert alu.bic(-1, -1) == 0
    assert alu.bic(-1, -3) == 2


def test_sub_or_cmp(alu: ALU):
    assert alu.sub_or_cmp(1, 2) == -1

    assert alu.sub_or_cmp(min_32_bits, 1) == -1
    assert alu.carry == 1

    assert alu.sub_or_cmp(max_32_bits, -10) == 10
    assert alu.carry == 1

    assert alu.sub_or_cmp(0, 0) == 0
    assert alu.zero == 1

    assert alu.sub_or_cmp(1, 1) == 0
    assert alu.zero == 1

    assert alu.sub_or_cmp(-1, -1) == 0
    assert alu.zero == 1


def test_bitwise_or(alu: ALU):
    assert alu.bitwise_or(2, 2) == 0
    assert alu.zero == 1
    assert alu.carry == 0
    assert alu.overflow == 0
    assert alu.negative == 0

    assert alu.bitwise_or(-1, -1) == 0
    assert alu.zero == 1
    assert alu.carry == 0
    assert alu.overflow == 0
    assert alu.negative == 0


def test_neg(alu: ALU):
    assert alu.sub_or_cmp(1, 2) == -1


def test_bitwise_or(alu: ALU):
    assert alu.bitwise_or(1, 2) == 3


def test_sbc(alu: ALU):
    alu.previous_spec_reg_carry = 1
    assert alu.sbc(5, 1) == 4

    alu.previous_spec_reg_carry = 0
    assert alu.sbc(5, 1) == 3


def test_mul(alu: ALU):
    assert alu.mul(3, 2) == 6
    assert alu.mul(max_32_bits, 1) == max_32_bits


def test_div(alu: ALU):
    assert alu.div(3, 2) == 1
    assert alu.div(4, 2) == 2
    assert alu.div(-4, 2) == -2
    assert alu.div(-8, -2) == 4
    assert alu.div(max_32_bits, 1) == max_32_bits


def test_rest(alu: ALU):
    assert alu.rest(max_32_bits, 1) == 0
    assert alu.rest(3, 2) == 1
    assert alu.rest(4, 2) == 0
    assert alu.rest(-4, 2) == 0
    assert alu.rest(-3, 2) == 1


def test_barrel_shifter_result(alu: ALU):
    assert alu.barrel_shifter_result(max_32_bits) == max_32_bits
    assert alu.barrel_shifter_result(min_32_bits) == min_32_bits


def test_xor(alu: ALU):
    assert alu.xor(2, 2) == 0
    assert alu.xor(2, 1) == 3


def test_logical_and(alu: ALU):
    assert alu.logical_and(2, -1) == 1
    assert alu.logical_and(1, 2) == 1
    assert alu.logical_and(0, 2) == 0
