from instruction.instruction import Instruction


class TypeJInstruction(Instruction):
    def __init__(self, id_, name, registerD):
        self.id = id_
        self.name = name
        self.registerD = registerD


