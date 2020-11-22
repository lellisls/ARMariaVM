from instruction.instruction import Instruction


class TypeIInstruction(Instruction):
    def __init__(self, id_, name, registerD):
        self.id = id_
        self.name = name
        self.registerD = registerD

    def execute(self):
        pass

