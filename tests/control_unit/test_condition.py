import pytest

from lib.alu import *
from lib.control_unit.condition import Condition


@pytest.fixture
def alu():
    return ALU()


def test_eq(alu: ALU):
    alu.sub_or_cmp(0, 0)
    assert Condition.EQ.getResult(alu) is True
    assert Condition.LE.getResult(alu) is True
    assert Condition.GE.getResult(alu) is True


def test_less(alu: ALU):
    alu.sub_or_cmp(0, 10)
    assert alu.zero == 0
    assert alu.negative == 1
    assert alu.overflow == 0
    assert alu.carry == 0

    assert Condition.EQ.getResult(alu) is False
    assert Condition.LE.getResult(alu) is True
    # assert Condition.LS.getResult(alu) is True
    assert Condition.LT.getResult(alu) is True
    assert Condition.GE.getResult(alu) is False
