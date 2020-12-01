import logging
from enum import Enum

from lib.control_unit.register.register_bank import RegisterBank

console = logging.getLogger(__name__)

reg_bank = RegisterBank()


class Register(Enum):
    HeapArrayRegister = 0
    AccumulatorRegister = 1
    TemporaryRegister = 2
    SecondRegister = 3
    FramePointer = 4
    GlobalPointer = 5
    UserSPKeeper = 6
    SystemCallRegister = 7
    StoredSpecReg = 8
    LinkRegister = 12
    PCKeeper = 13
    StackPointer = 14
    ProgramCounter = 15
    StackPointer2 = 16
    SpecReg = 999

    def shortName(self):
        names = {
            self.HeapArrayRegister: "H0",
            self.AccumulatorRegister: "A0",
            self.TemporaryRegister: "T1",
            self.SecondRegister: "SXR",
            self.FramePointer: "FP",
            self.GlobalPointer: "GP",
            self.UserSPKeeper: "USPK",
            self.SystemCallRegister: "SC",
            self.StoredSpecReg: "SXR",
            self.LinkRegister: "LR",
            self.PCKeeper: "PCK",
            self.StackPointer: "SP",
            self.ProgramCounter: "PC",
            self.StackPointer2: "SP2",
            self.SpecReg: "XR"
        }
        return names.get(self)

    def getValue(self):
        return reg_bank.getRegister(self.value)

    def setValue(self, value):
        if self == Register.ProgramCounter:
            raise ValueError("Illegal PC update")
        console.debug(f"\t{self} <= {value}")
        return reg_bank.setRegister(self.value, value)

    def setPrivilegedValue(self, value):
        console.debug(f"\t{self} <= {value}")
        return reg_bank.setRegister(self.value, value)

    def copyValueFrom(self, reg: 'Register'):
        value = reg.getValue()
        console.debug(f"\t{self} <= {reg} = {value}")
        return reg_bank.setRegister(self.value, value)

    def increment(self, increment=1):
        old_val = self.getValue()
        val = reg_bank.increment(self.value, increment)
        console.debug(f"\t{self} <= {old_val} + {increment} = {val}")
        return val

    def decrement(self, decrement=1):
        old_val = self.getValue()
        val = reg_bank.decrement(self.value, decrement)
        console.debug(f"\t{self} <= {old_val} - {decrement} = {val}")
        return val

    def __str__(self):
        return f"${self.shortName()}"
