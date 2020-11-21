import logging

from instruction.impl.typeAInstruction import TypeAInstruction
from instruction.impl.typeBInstruction import TypeBInstruction
from instruction.impl.typeCInstruction import TypeCInstruction
from instruction.impl.typeDInstruction import TypeDInstruction
from instruction.impl.typeEInstruction import TypeEInstruction
from instruction.impl.typeFInstruction import TypeFInstruction
from instruction.impl.typeGInstruction import TypeGInstruction
from instruction.impl.typeJInstruction import TypeJInstruction

names = {
    1: "LSL",
    2: "LSR",
    4: "ADD",
    6: "ADD",
    7: "SUB",
    8: "MOV",
    10: "ADD",
    11: "SUB",
    22: "CMP",
    35: "MOV",
    36: "MOV",
    38: "B",
    40: "STR",
    44: "LDR",
    48: "STR",
    49: "LDR",
    56: "ADD",
    57: "ADD",
    59: "SXTH",
    61: "UXTH",
    67: "PUSH",
    68: "POP",
    69: "OUTPUT",
    70: "PAUSE",
    72: "SWI",
    73: "B",
    74: "NOP",
    75: "HLT",
    77: "PUSHM",
    78: "POPM",  # unhandled
    79: "BL",  # unhandled
    80: "BX"  # unhandled
}


class BytecodeDecoder:
    opcode = None
    func1 = 0
    func2 = None
    op = 0
    aux = 0

    def __init__(self, instruction):
        self.original = instruction
        self.instruction = instruction
        self.func2 = instruction[8:11]
        self.get_opcode()

    def _get_value(self, bits: int) -> int:
        value = self._get_value_raw(bits)
        return int(value, 2)

    def _get_value_raw(self, bits: int) -> str:
        length = len(self.instruction)
        # print(f"{self.instruction} : {length} - {bits}")
        value = self.instruction[:bits]
        print(value)
        self.instruction = self.instruction[bits:]
        assert len(self.instruction) == (length - bits)
        return value

    def get_opcode(self):
        self.opcode = self._get_value(4)

    def get_opbit(self):
        self.op = self._get_value(1)

    def get_func2(self):
        self.func2 = self._get_value(4)

    def get_func1(self):
        self.func1 = self._get_value(2)

    def decode(self):
        opcode_switcher = {
            0: self.decode_inst1_2,
            1: self.decode_inst3_7,
            2: self.decode_inst8_9,
            3: self.decode_inst10_11,
            4: self.decode_inst12_39,
            5: self.decode_inst40_47,
            6: self.decode_inst48_49,
            7: self.decode_inst50_51,
            8: self.decode_inst52_53,
            9: self.decode_inst54_55,
            10: self.decode_inst56_57,
            11: self.decode_inst58_71,
            12: self.decode_inst72,
            13: self.decode_inst73,
            14: self.decode_inst74_75,
        }
        opcode_decoder = opcode_switcher.get(self.opcode, self.decode_default)
        result = opcode_decoder()
        if result is None:
            raise Exception("Unhandled instruction error: " + self.original)
        if len(self.instruction) > 0:
            raise Exception("Instruction not fully processed" + self.original)
        print(result.name)
        return result

    def decode_default(self):
        raise Exception(f"Unhandled opcode: {self.opcode}!")

    def _decode_typeA(self, id_):
        offset = self._get_value(5)
        RegM = self._get_value(3)
        RegD = self._get_value(3)
        return TypeAInstruction(id_, names.get(id_), offset, RegM, RegD)

    def _decode_typeB(self, id_):
        RegM = self._get_value(3)
        RegN = self._get_value(3)
        RegD = self._get_value(3)
        return TypeBInstruction(id_, names.get(id_), RegM, RegN, RegD)

    def _decode_typeC(self, id_):
        offset = self._get_value(3)
        RegN = self._get_value(3)
        RegD = self._get_value(3)
        return TypeCInstruction(id_, names.get(id_), offset, RegN, RegD)

    def _decode_typeD(self, id_):
        RegD = self._get_value(3)
        offset = self._get_value(8)
        return TypeDInstruction(id_, names.get(id_), offset, RegD)

    def _decode_typeE(self, id_):
        RegM = self._get_value(3)
        RegD = self._get_value(3)
        return TypeEInstruction(id_, names.get(id_), RegM, RegD)

    def _decode_typeF(self, id_, cond):
        RegD = self._get_value(4)
        return TypeFInstruction(id_, names.get(id_), cond, RegD)

    def __decode_typeG(self, id_):
        cond = self._get_value(4)
        offset = self._get_value(8)
        return TypeGInstruction(id_, names.get(id_), cond, offset)

    def _decode_typeJ(self, id_):
        self._get_value(5)  # 00000
        RegD = self._get_value(3)
        return TypeJInstruction(id_, names.get(id_), RegD)

    def decode_inst1_2(self):
        self.get_opbit()
        id_ = 2 if self.op else 1
        return self._decode_typeA(id_)

    def decode_inst3_7(self):
        self.get_opbit()
        if not self.op:
            return None

        self.get_func1()
        id_ = self.func1 + 4

        if id_ == 4 or id_ == 5:
            return self._decode_typeB(id_)
        elif id_ == 6 or id_ == 7:
            return self._decode_typeC(id_)

    def decode_inst8_9(self):
        self.get_opbit()
        id_ = 9 if self.op else 8
        return self._decode_typeD(id_)

    def decode_inst10_11(self):
        self.get_opbit()
        id_ = 11 if self.op else 10
        return self._decode_typeD(id_)

    def decode_inst12_39(self):
        self.get_opbit()
        self.get_func1()
        self.get_func2()
        if self.op:  # 39
            return None

        if self.func2 < 4:  # <= 27
            id_ = 12 + self.func2 * 4 + self.func1
            return self._decode_typeE(id_)
        elif self.func2 == 6:  # 34~37
            id_ = 34 + self.func1
            return self._decode_typeE(id_)
        elif self.func2 == 7:
            id_ = 38
            cond = self._get_value(4)
            if cond == 7:
                id_ = 77  # TODO CHECK PUSHM
                return self._decode_typeF(id_, cond)

            return self._decode_typeF(id_, cond)
        return None

    def decode_inst40_47(self):
        self.get_opbit()
        self.get_func1()
        aux = self.op * 4 + self.func1
        id_ = 40 + aux
        return self._decode_typeB(id_)

    def decode_inst48_49(self):
        self.get_opbit()
        id_ = 48 if self.op else 49
        return self._decode_typeA(id_)

    def decode_inst50_51(self):
        pass

    def decode_inst52_53(self):
        pass

    def decode_inst54_55(self):
        pass

    def decode_inst56_57(self):
        self.get_opbit()
        id_ = 56 if self.op else 57
        return self._decode_typeD(id_)

    def decode_inst58_71(self):
        self.get_func2()
        if self.func2 == 2:  # 59~62
            self.get_func1()
            id_ = 59 + self.func1
            return self._decode_typeE(id_)
        elif self.func2 == 4:  # 67 - PUSH
            id_ = 67
            return self._decode_typeJ(id_)
        elif self.func2 == 13:  # 68 - POP
            id_ = 68
            return self._decode_typeJ(id_)
        elif self.func2 == 14:
            self.get_func1()
            if self.func1 == 0:  # 69 - OUTPUT
                id_ = 69
                return self._decode_typeE(id_)
            if self.func1 == 1:  # 70 - PAUSE
                id_ = 70
                return self._decode_typeE(id_)

    def decode_inst72(self):  # 72 - SWI
        id_ = 72
        self.get_opbit()
        return self._decode_typeD(id_)

    def decode_inst73(self):  # 73 - B
        id_ = 73
        return self.__decode_typeG(id_)

    def decode_inst74_75(self):
        self.get_opbit()
        id_ = 75 if self.op else 74
        return self._decode_typeD(id_)
