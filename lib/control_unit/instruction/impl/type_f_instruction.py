from lib.control_unit.condition import Condition
from lib.control_unit.instruction.instruction import Instruction
from lib.control_unit.register import Register


class TypeFInstruction(Instruction):
    def __init__(self, id, name, condition, register_d):
        self.id = id
        self.name = name
        self.condition = Condition(condition)
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.condition.name} {self.registerD}"
