from typing import List

from instruction.instruction import Instruction


class CodeExecutor:
    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions

    def run(self):
        for inst in self.instructions:
            print(inst)
