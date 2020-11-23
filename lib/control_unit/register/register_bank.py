from typing import Union

from lib.control_unit.register import Register


class RegisterBank:
    def __init__(self):
        self.bank = dict({})
        for register in Register:
            self.bank[register] = 0

    def setRegister(self, reg: Union[Register, int], value):
        reg = Register(reg)
        self.bank[reg] = int(value)

    def getRegister(self, reg: Union[Register, int]):
        reg = Register(reg)
        return self.bank[reg]
