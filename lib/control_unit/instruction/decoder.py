from lib.control_unit.instruction.decodingHelper import DecodingHelper


class BytecodeDecoder:
    OS_START = 2048

    LINK_REGISTER = 12
    SP_REGISTER = 14
    PC_REGISTER = 15

    def __init__(self, instruction):
        self.instruction = instruction
        self.decoder = DecodingHelper(instruction)

    def _decode_inst1_2(self):
        self.decoder.get_opbit()
        id_ = 2 if self.decoder.op else 1
        return self.decoder.decode_typeA(id_)

    def _decode_inst3_7(self):
        self.decoder.get_opbit()
        if not self.decoder.op:
            return None

        self.decoder.get_func1()
        id_ = self.decoder.func1 + 4

        if id_ == 4 or id_ == 5:
            return self.decoder.decode_typeB(id_)
        elif id_ == 6 or id_ == 7:
            return self.decoder.decode_typeC(id_)

    def _decode_inst8_9(self):
        self.decoder.get_opbit()
        id_ = 9 if self.decoder.op else 8
        return self.decoder.decode_typeD(id_)

    def _decode_inst10_11(self):
        self.decoder.get_opbit()
        id_ = 11 if self.decoder.op else 10
        return self.decoder.decode_typeD(id_)

    def _decode_inst12_39(self):
        self.decoder.get_func2()
        if self.decoder.func2 < 4:  # <= 27
            self.decoder.get_func1()
            id_ = 12 + self.decoder.func2 * 4 + self.decoder.func1
            return self.decoder.decode_typeE(id_)
        elif self.decoder.func2 == 6:  # 34~37
            self.decoder.get_func1()
            id_ = 34 + self.decoder.func1
            return self.decoder.decode_typeE(id_)
        elif self.decoder.func2 == 7:  # 38 - BX
            id_ = 38
            cond = self.decoder.get_value(4)
            decoded = self.decoder.decode_typeF(id_, cond)
            decoded.registerA = self.PC_REGISTER
            return decoded
        return None

    def _decode_inst40_47(self):
        self.decoder.get_opbit()
        self.decoder.get_func1()
        aux = self.decoder.op * 4 + self.decoder.func1
        id_ = 40 + aux
        return self.decoder.decode_typeB(id_)

    def _decode_inst48_49(self):
        self.decoder.get_opbit()
        id_ = 49 if self.decoder.op else 48
        return self.decoder.decode_typeA(id_)

    def _decode_inst50_51(self):
        pass

    def _decode_inst52_53(self):
        pass

    def _decode_inst54_55(self):
        pass

    def _decode_inst56_57(self):
        self.decoder.get_opbit()
        id_ = 57 if self.decoder.op else 56
        return self.decoder.decode_typeD(id_)

    def _decode_inst58_71(self):  # 76
        self.decoder.get_func2()
        if self.decoder.func2 == 0:
            self.decoder.get_func1()
            id_ = 76 if self.decoder.func1 == 1 else 58
            return self.decoder.decode_typeH(id_)
        if self.decoder.func2 == 1:  # 79 BL - 80 BX
            self.decoder.get_opbit()

            if self.decoder.op:
                id_ = 80
                decoded = self.decoder.decode_typeI(id_)
            else:
                id_ = 79
                decoded = self.decoder.decode_typeK(id_)

            decoded.registerA = self.PC_REGISTER
            decoded.registerB = self.LINK_REGISTER
            return decoded
        elif self.decoder.func2 == 2:  # 59~62
            self.decoder.get_func1()
            id_ = 59 + self.decoder.func1
            return self.decoder.decode_typeE(id_)
        elif self.decoder.func2 == 4:  # 67 - PUSH
            self.decoder.get_opbit()
            if self.decoder.op:
                id_ = 77
                return self.decoder.decode_typeI(id_)
            else:
                id_ = 67
                return self.decoder.decode_typeJ(id_)
        elif self.decoder.func2 == 13:  # 68 - POP
            self.decoder.get_opbit()
            if self.decoder.op:
                id_ = 78
                return self.decoder.decode_typeI(id_)
            else:
                id_ = 68
                return self.decoder.decode_typeJ(id_)
        elif self.decoder.func2 == 14:
            self.decoder.get_func1()
            if self.decoder.func1 == 0:  # 69 - OUTPUT
                id_ = 69
                return self.decoder.decode_typeE(id_)
            elif self.decoder.func1 == 1:  # 70 - PAUSE
                id_ = 70
                return self.decoder.decode_typeE(id_)
            elif self.decoder.func1 == 2:  # 71 - INPUT
                id_ = 71
                return self.decoder.decode_typeE(id_)

    def _decode_inst72(self):  # 72 - SWI
        id_ = 72
        self.decoder.get_opbit()  # Fills the System Call Register ?
        return self.decoder.decode_typeD(id_)

    def _decode_inst73(self):  # 73 - B immediate
        id_ = 73
        decoded = self.decoder.decode_typeG(id_)
        decoded.registerA = self.PC_REGISTER
        return decoded

    def _decode_inst74_75(self):
        self.decoder.get_opbit()
        id_ = 75 if self.decoder.op else 74
        return self.decoder.decode_typeD(id_)

    def decode_default(self):
        raise Exception(f"Unhandled opcode: {self.decoder.opcode} - {self.instruction}!")

    def decode(self):
        opcode_switcher = {
            0: self._decode_inst1_2,
            1: self._decode_inst3_7,
            2: self._decode_inst8_9,
            3: self._decode_inst10_11,
            4: self._decode_inst12_39,
            5: self._decode_inst40_47,
            6: self._decode_inst48_49,
            7: self._decode_inst50_51,
            8: self._decode_inst52_53,
            9: self._decode_inst54_55,
            10: self._decode_inst56_57,
            11: self._decode_inst58_71,
            12: self._decode_inst72,
            13: self._decode_inst73,
            14: self._decode_inst74_75,
        }
        opcode_decoder = opcode_switcher.get(self.decoder.opcode, self.decode_default)
        result = opcode_decoder()
        if result is None:
            raise Exception("Unhandled instruction error: " + self.instruction)
        if len(self.decoder.instruction) > 0:
            raise Exception("Instruction not fully processed: " + self.instruction)
        if result.name is None:
            raise Exception(f"Name not found for id {result.id}")
        return result
