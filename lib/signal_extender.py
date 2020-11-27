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

        neg = int(cls._neg(value), 2)
        return - (neg + 1)

    @classmethod
    def _neg(cls, value):
        return value.replace('1', '9').replace('0', '1').replace('9', '0')
