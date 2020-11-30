min_32_bits_signed = -2 ** 31
max_32_bits = 2 ** 32 - 1
max_32_bits_signed = 2 ** 31 - 1


class BinaryUtils:

    @classmethod
    def to_2cb(cls, value, size=32):
        if value >= 0:
            result = f"{value:032b}"[-size:]
        else:
            value = - value - 1
            result = cls.neg(f"{value:032b}"[-size:])
        assert len(result) == size
        return result

    @classmethod
    def neg(cls, value: str):
        return value.replace('1', '9').replace('0', '1').replace('9', '0')

    @classmethod
    def msb(cls, value):
        msb = BinaryUtils.to_2cb(value)
        return bool(int(msb[0]))

    @classmethod
    def overflow(cls, result):
        return result >= (max_32_bits_signed * 2) or result <= (min_32_bits_signed * 2)

    @classmethod
    def overflow_msb(cls, a, b, result):
        result_msb = cls.msb(result)
        a_msb = cls.msb(a)
        b_msb = cls.msb(a)

        return not (a_msb or b_msb) if result_msb else (a_msb and b_msb)
