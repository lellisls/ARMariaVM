min_32_bits_signed = -2 ** 31
max_32_bits = 2 ** 32 - 1
max_32_bits_signed = 2 ** 31 - 1


class BinaryUtils:

    @classmethod
    def to_2cb(cls, value, size=32):
        if value >= 0:
            result = f"{value:0{size}b}"[-size:]
        else:
            value = - value - 1
            result = cls.neg(f"{value:0{size}b}")[-size:]
        assert len(result) == size
        return result

    @classmethod
    def add_2cb(cls, a, b, c=0, size=32):
        a = cls.to_2cb(a)
        b = cls.to_2cb(b)
        c = cls.to_2cb(c)

        result, carry = cls.add_binary_nums(a, b, size)
        result, carry2 = cls.add_binary_nums(result, c, size)

        is_negative = result[0] == '1'

        if is_negative:
            result = - int(cls.neg(result), 2) - 1
        else:
            result = int(result, 2)

        return carry or carry2, result

    @classmethod
    def add_binary_nums(cls, x, y, max_len=32):
        x = x.zfill(max_len)
        y = y.zfill(max_len)

        assert len(x) == max_len
        assert len(y) == max_len

        # initialize the result
        result = ''

        # initialize the carry
        carry = 0

        # Traverse the string
        for i in range(max_len - 1, -1, -1):
            r = carry
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
            carry = 0 if r < 2 else 1  # Compute the carry.

        assert len(result) == max_len
        return result, bool(carry)

    @classmethod
    def neg(cls, value: str):
        return value.replace('1', '9').replace('0', '1').replace('9', '0')

    @classmethod
    def msb(cls, value):
        msb = BinaryUtils.to_2cb(value)
        return bool(int(msb[0]))

    @classmethod
    def overflow(cls, result):
        return result >= (2 ** 31) or result < (-2 ** 31)

    @classmethod
    def overflow_msb(cls, a, b, result):
        result_msb = cls.msb(result)
        a_msb = cls.msb(a)
        b_msb = cls.msb(b)

        if result_msb is True:  # If the result is negative
            return (not a_msb) and (not b_msb)  # And both inputs are positive, then overflow
        else:  # If the result is positive
            return a_msb and b_msb  # And both inputs are negative, then overflow
