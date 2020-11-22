from lib.control_unit.instruction.instruction import Instruction
from lib.control_unit.register.register import Register


class TypeEInstruction(Instruction):
    def __init__(self, id, name, register_m, register_d):
        self.id = id
        self.name = name
        self.registerM = Register(register_m)
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.registerM} {self.registerD}"
