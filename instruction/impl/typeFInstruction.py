from instruction.instruction import Instruction


class TypeFInstruction(Instruction):
    def __init__(self, id, name, condition, registerD):
        self.id = id
        self.name = name
        self.condition = condition
        self.registerD = registerD
