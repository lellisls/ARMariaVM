from instruction.instruction import Instruction


class TypeAInstruction(Instruction):
    def __init__(self, id, name, immediate, registerM, registerD):
        self.id = id
        self.name = name
        self.immediate = immediate
        self.registerM = registerM
        self.registerD = registerD

    def execute(self):
        pass

