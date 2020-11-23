import pytest

from lib.memory_unit import Memory


@pytest.fixture
def memory():
    return Memory(3000)


def test_get_set(memory: Memory):
    memory.set(0, 10)
    value = memory.get(0)
    assert value == 10


def test_set_uint32_max(memory: Memory):
    value_32bit = int('1' * 32, 2)
    memory.set(100, value_32bit)
    value = memory.get(100)
    assert value == value_32bit


def test_set_uint64_max(memory: Memory):
    with pytest.raises(OverflowError):
        value_64bit = int('1' * 64, 2)
        memory.set(1000, value_64bit)
