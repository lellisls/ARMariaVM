from instruction.instruction import Instruction


class TypeDInstruction(Instruction):
    def __init__(self, id, name, immediate, registerD):
        self.id = id
        self.name = name
        self.immediate = immediate
        self.registerD = registerD
