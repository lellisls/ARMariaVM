from random import random

import pytest

from lib.control_unit.register import Register
from lib.control_unit.register import RegisterBank


@pytest.fixture()
def register_bank():
    return RegisterBank()


def test_get_set_register(register_bank: RegisterBank):
    for register in Register:
        expected_value = int(random() * 1024)
        register_bank.setRegister(register, expected_value)
        value = register_bank.getRegister(register)
        assert value == expected_value


def test_get_set_register_value(register_bank: RegisterBank):
    for register in Register:
        expected_value = int(random() * 1024)
        register = int(register.value)
        register_bank.setRegister(register, expected_value)
        value = register_bank.getRegister(register)
        assert value == expected_value


def test_set_unhandled_register(register_bank: RegisterBank):
    with pytest.raises(ValueError):
        register_bank.setRegister(1000, 10)


def test_get_unhandled_register(register_bank: RegisterBank):
    with pytest.raises(ValueError):
        register_bank.getRegister(1000)
