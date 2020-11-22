from lib.control_unit.instruction.instruction import Instruction
from lib.control_unit.register.register import Register


class TypeHInstruction(Instruction):
    def __init__(self, id_, name, register_d):
        self.id = id_
        self.name = name
        self.registerD = Register(register_d)

    def _print_registers(self):
        return f"{self.registerD}"
