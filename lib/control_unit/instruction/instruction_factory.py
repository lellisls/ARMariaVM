from lib.control_unit.instruction.decoder import BytecodeDecoder
from lib.control_unit.instruction.instruction import Instruction


class InstructionFactory:
    @classmethod
    def build(cls, inst) -> Instruction:
        if type(inst) != str:
            inst = f"{inst:016b}"

        decoder = BytecodeDecoder(inst)
        return decoder.decode()
