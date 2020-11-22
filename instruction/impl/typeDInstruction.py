from instruction.instruction import Instruction
from instruction.register import Register


class TypeDInstruction(Instruction):
    def __init__(self, id, name, immediate, register_d):
        self.id = id
        self.name = name
        self.immediate = immediate
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.immediate} {self.registerD}"

    def execute(self):
        pass
