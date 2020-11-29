import logging
from enum import Enum

console = logging.getLogger(__name__)


class Condition(Enum):
    EQ = 0  # Equal
    NE = 1  # NOT EQUAL
    HS = 2  # Unsigned Greater than or equal
    LO = 3  # Unsigned Lower then
    MI = 4  # Negative
    PL = 5  # Positive or zero
    VS = 6  # Overflow
    VC = 7  # No overflow
    HI = 8  # Unsigned greater than
    LS = 9  # Unsgined lower than or equal
    GE = 10  # Signed greater than or equal
    LT = 11  # Signed lower than
    GT = 12  # Signed greater than
    LE = 13  # Signed lower than
    AL = 14  # Always
    CS = 2  # Unsigned Greater than or equal
    CC = 3  # Unsigned Lower THan

    def getResult(self, alu):
        zero = bool(alu.zero)
        carry = bool(alu.carry)
        overflow = bool(alu.overflow)
        negative = bool(alu.negative)

        condition_result = dict({
            Condition.EQ: zero,
            Condition.NE: not zero,
            Condition.CS: carry,
            Condition.HS: carry,
            Condition.CC: not carry,
            Condition.LO: not carry,
            Condition.MI: negative,
            Condition.PL: not negative,
            Condition.VS: overflow,
            Condition.VC: not overflow,
            Condition.HI: (not zero) and carry,
            Condition.LS: zero or (not carry),
            Condition.GE: zero == overflow,
            Condition.LT: zero != overflow,
            Condition.GT: (negative == overflow) and zero,
            Condition.LE: zero or (negative != overflow),
            Condition.AL: True,
        })
        result = condition_result.get(self)
        console.debug(f"\tCondition {self.name} (Z={zero}, C={carry}, V={overflow}, N={negative}) = {result}")
        return result
