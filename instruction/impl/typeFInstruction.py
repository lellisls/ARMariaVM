from instruction.instruction import Instruction
from instruction.register import Register


class TypeFInstruction(Instruction):
    def __init__(self, id, name, condition, register_d):
        self.id = id
        self.name = name
        self.condition = condition
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.condition} {self.registerD}"

    def execute(self):
        pass
