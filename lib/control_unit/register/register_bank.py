from typing import Union

from lib.control_unit.register import Register


class RegisterBank:
    def __init__(self):
        self.bank = dict({})
        for register in Register:
            self.bank[register] = 0

    def setRegister(self, reg: Union[Register, int], value):
        reg = Register(reg)
        print(f"SET {reg} = {value}")
        self.bank[reg] = int(value)

    def getRegister(self, reg: Union[Register, int]):
        reg = Register(reg)
        return self.bank[reg]

    def getRegisterHigh(self, reg: int):
        reg = Register(8 + reg)
        return self.bank[reg]

    def increment(self, reg: Union[Register, int], value: int = 1):
        self.setRegister(reg, self.getRegister(reg) + value)

    def decrement(self, reg: Union[Register, int], value: int = 1):
        self.setRegister(reg, self.getRegister(reg) - value)
