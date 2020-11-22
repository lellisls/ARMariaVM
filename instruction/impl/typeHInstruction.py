from instruction.instruction import Instruction


class TypeHInstruction(Instruction):
    def __init__(self, id_, name, registerD):
        self.id = id_
        self.registerD = registerD
