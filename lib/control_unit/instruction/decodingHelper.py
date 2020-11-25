from lib.control_unit.instruction.impl import *

names = {
    1: "LSL",
    2: "LSR",
    4: "ADD",
    5: "SUB",
    6: "ADD",
    7: "SUB",
    8: "MOV",
    10: "ADD",
    11: "SUB",
    22: "CMP",
    25: "MUL",
    34: "DIV",
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
    71: "INPUT",
    72: "SWI",
    73: "B",
    74: "NOP",
    75: "HLT",
    77: "PUSHM",
    78: "POPM",  # unhandled
    79: "BL",  # unhandled
    80: "BX"  # unhandled
}


class DecodingHelper:
    opcode = None
    func1 = 0
    func2 = None
    op = 0
    aux = 0
    value_raw = None

    def __init__(self, instruction):
        self.instruction = instruction
        self.func2 = instruction[8:11]
        self.get_opcode()

    def get_value(self, bits: int) -> int:
        value = self.get_value_raw(bits)
        return int(value, 2)

    def get_value_raw(self, bits: int) -> str:
        length = len(self.instruction)
        assert length >= bits
        self.value_raw = value = self.instruction[:bits]
        # print(f"{self.instruction} : {length} - {bits} : {value}")
        self.instruction = self.instruction[bits:]
        assert len(self.instruction) == (length - bits)
        return value

    def get_opcode(self):
        self.opcode = self.get_value(4)

    def get_opbit(self):
        self.op = self.get_value(1)

    def get_func2(self):
        self.func2 = self.get_value(4)

    def get_func1(self):
        self.func1 = self.get_value(2)

    def decode_typeA(self, id_):
        offset = self.get_value(5)
        RegM = self.get_value(3)
        RegD = self.get_value(3)
        return TypeAInstruction(id_, names.get(id_), offset, RegM, RegD)

    def decode_typeB(self, id_):
        RegM = self.get_value(3)
        RegN = self.get_value(3)
        RegD = self.get_value(3)
        return TypeBInstruction(id_, names.get(id_), RegM, RegN, RegD)

    def decode_typeC(self, id_):
        offset = self.get_value(3)
        RegN = self.get_value(3)
        RegD = self.get_value(3)
        return TypeCInstruction(id_, names.get(id_), offset, RegN, RegD)

    def decode_typeD(self, id_):
        RegD = self.get_value(3)
        immediate = self.get_value(8)
        return TypeDInstruction(id_, names.get(id_), immediate, RegD)

    def decode_typeE(self, id_):
        RegM = self.get_value(3)
        RegD = self.get_value(3)

        if id_ in [29, 30, 32, 36, 37]:
            RegD = RegD + 8

        if id_ in [28, 30, 31, 33, 35, 37]:
            RegM = RegM + 8

        if id_ == 33:
            RegD = RegD & 7

        return TypeEInstruction(id_, names.get(id_), RegM, RegD)

    def decode_typeF(self, id_, cond):
        RegD = self.get_value(4)
        return TypeFInstruction(id_, names.get(id_), cond, RegD)

    def decode_typeG(self, id_):
        cond = self.get_value(4)
        offset = self.get_value(8)
        return TypeGInstruction(id_, names.get(id_), cond, offset)

    def decode_typeH(self, id_):
        self.get_value(2)
        RegD = self.get_value(4)
        return TypeHInstruction(id_, names.get(id_), RegD)

    def decode_typeJ(self, id_):
        self.get_value(4)  # 00000
        RegD = self.get_value(3)
        return TypeJInstruction(id_, names.get(id_), RegD)

    def decode_typeK(self, id_):
        self.get_value(3)  # 00000
        RegD = self.get_value(4)
        return TypeKInstruction(id_, names.get(id_), RegD)

    def decode_typeI(self, id_):
        immediate = self.get_value(7)
        return TypeIInstruction(id_, names.get(id_), immediate)
