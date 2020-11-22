from instruction.instruction import Instruction


class TypeGInstruction(Instruction):
    def __init__(self, id_, name, cond, offset):
        self.id = id_
        self.name = name
        self.cond = cond
        self.offset = offset

    def execute(self):
        pass

