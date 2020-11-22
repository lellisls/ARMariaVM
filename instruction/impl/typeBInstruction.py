from instruction.instruction import Instruction


class TypeBInstruction(Instruction):
    def __init__(self, id, name, registerM, registerN, registerD):
        self.id = id
        self.name = name
        self.registerM = registerM
        self.registerN = registerN
        self.registerD = registerD

    def execute(self):
        pass
