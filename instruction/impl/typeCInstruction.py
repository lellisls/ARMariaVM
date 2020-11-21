from instruction.instruction import Instruction


class TypeCInstruction(Instruction):
    def __init__(self, id, name, immediate, registerN, registerD):
        self.id = id
        self.name = name
        self.immediate = immediate
        self.registerN = registerN
        self.registerD = registerD
