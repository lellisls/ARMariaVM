from instruction.instruction import Instruction


class TypeEInstruction(Instruction):
    def __init__(self, id, name, registerM, registerD):
        self.id = id
        self.name = name
        self.registerM = registerM
        self.registerD = registerD
