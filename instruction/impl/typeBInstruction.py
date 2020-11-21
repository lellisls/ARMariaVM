from instruction.instruction import Instruction


class TypeBInstruction(Instruction):
    def __init__(self, id, name, immediate, registerM, registerN, registerD):
        self.id = id
        self.name = name
        self.immediate = immediate
        self.registerM = registerM
        self.registerN = registerN
        self.registerD = registerD
