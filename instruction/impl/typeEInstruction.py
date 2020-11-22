from instruction.instruction import Instruction
from instruction.register import Register


class TypeEInstruction(Instruction):
    def __init__(self, id, name, register_m, register_d):
        self.id = id
        self.name = name
        self.registerM = Register(register_m)
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.registerM} {self.registerD}"

    def execute(self):
        pass
