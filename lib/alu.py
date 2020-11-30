from lib.binary_utils import BinaryUtils, min_32_bits_signed, max_32_bits_signed


class ALU:
    def __init__(self):
        self.negative = 0
        self.zero = 0
        self.carry = 0
        self.overflow = 0
        self.previous_spec_reg_carry = 0

    def _test_flags(self, a, b, result):
        self.overflow = BinaryUtils.overflow_msb(a, b, result)
        self.lt = a < b
        self.gt = a > b

    def _value_common(self, value: int) -> int:
        value = int(value)
        self.zero = value == 0
        self.negative = BinaryUtils.msb(value)
        if value > max_32_bits_signed or value < min_32_bits_signed:
            raise ValueError
        return value

    def _value_with_carry(self, a, b, value: int) -> int:
        self._reset()
        self._test_flags(a, b, value)

        # missing overflow handling
        if value > max_32_bits_signed:
            self.carry = 1
            value -= max_32_bits_signed

        if value < min_32_bits_signed:
            self.carry = 1
            value -= min_32_bits_signed

        result = self._value_common(value)
        return result

    def _value(self, value: int) -> int:
        self._reset()
        return self._value_common(value)

    def adc(self, a: int, b: int):
        """ADD with carry"""
        return self._value_with_carry(a, b, a + b + self.previous_spec_reg_carry)

    def add_or_cmn(self, a: int, b: int):
        """ADD or CMN"""
        return self._value_with_carry(a, b, a + b)

    def bitwise_and(self, a: int, b: int):
        """Bitwise AND"""
        return self._value(a & b)

    def bic(self, a: int, b: int):
        """BIC - Not working"""
        return self._value(a & ~ b)

    def sub_or_cmp(self, a: int, b: int):
        """SUB or CMP"""
        return self._value_with_carry(a, b, a - b)

    def neg(self, a: int):
        """Signal inversion"""
        return self._value(~a)

    def bitwise_or(self, a: int, b: int):
        """OR"""
        return self._value(a | b)

    def sbc(self, a: int, b: int):
        """SUB with carry"""
        return self._value_with_carry(a, b, a - b - int(not self.previous_spec_reg_carry))

    def mul(self, a: int, b: int):
        """Multiplication"""
        return self._value(a * b)

    def div(self, a: int, b: int):
        """Division"""
        self.overflow = b == 0
        if self.overflow:
            return 0
        return self._value(int(a / b))

    def rest(self, a: int, b: int):
        """Rest of division"""
        self.overflow = b == 0
        return self._value(a % b)

    def barrel_shifter_result(self, a: int):
        return self._value(a)

    def xor(self, a: int, b: int):
        """XOR"""
        return self._value(a ^ b)

    def logical_and(self, a: int, b: int):
        """Logical AND"""
        return self._value((a != 0) and (b != 0))

    def paste_special_rec(self, a: int):
        """Logical AND"""
        self.negative = int((a & 1) > 0)
        self.zero = int((a & 2) > 0)
        self.carry = int((a & 4) > 0)
        self.overflow = int((a & 8) > 0)

    def default(self, a: int):
        return self._value(a)

    def _reset(self):
        self.negative = 0
        self.zero = 0
        self.carry = 0
        self.overflow = 0
        self.lt = False
        self.gt = False
