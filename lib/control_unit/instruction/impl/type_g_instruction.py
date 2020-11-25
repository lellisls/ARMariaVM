from lib.control_unit.condition import Condition
from lib.control_unit.instruction.instruction import Instruction


class TypeGInstruction(Instruction):
    def __init__(self, id_, name, condition, offset):
        self.id = id_
        self.name = name
        self.condition = Condition(condition)
        self.offset = offset

    def _print_registers(self):
        return f"{self.condition.name} {self.offset}"
