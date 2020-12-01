from lib.binary_utils import BinaryUtils


class SignalExtender:
    @classmethod
    def extend16(cls, value):
        binary = f"{value:016b}"
        compl = binary[0] * 16
        return cls._from_binary(compl + binary)

    @classmethod
    def extend8(cls, value):
        binary = f"{value:08b}"
        compl = binary[0] * 24
        return cls._from_binary(compl + binary)

    @classmethod
    def _from_binary(cls, value):
        if value[0] == '0':
            return int(value, 2)

        neg = int(BinaryUtils.neg(value), 2)
        return - (neg + 1)
