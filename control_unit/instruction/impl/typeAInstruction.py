from control_unit.instruction.instruction import Instruction
from control_unit.register.register import Register


class TypeAInstruction(Instruction):
    def __init__(self, id_, name, immediate, register_m, register_d):
        self.id = id_
        self.name = name
        self.immediate = immediate
        self.registerM = Register(register_m)
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.immediate} {self.registerM} {self.registerD}"
