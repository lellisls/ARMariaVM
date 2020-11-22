from instruction.instruction import Instruction
from instruction.register import Register


class TypeIInstruction(Instruction):
    def __init__(self, id_, name, register_d):
        self.id = id_
        self.name = name
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.registerD}"

