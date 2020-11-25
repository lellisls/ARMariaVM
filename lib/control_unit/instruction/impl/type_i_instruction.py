from lib.control_unit.instruction.instruction import Instruction


class TypeIInstruction(Instruction):
    def __init__(self, id_, name, immediate):
        self.id = id_
        self.name = name
        self.immediate = immediate

    def _print_registers(self):
        return f"{self.immediate}"
