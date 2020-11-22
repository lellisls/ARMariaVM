from control_unit.instruction.instruction import Instruction
from control_unit.register.register import Register


class TypeCInstruction(Instruction):
    def __init__(self, id, name, immediate, register_n, register_d):
        self.id = id
        self.name = name
        self.immediate = immediate
        self.registerN = Register(register_n)
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.immediate} {self.registerN} {self.registerD}"
