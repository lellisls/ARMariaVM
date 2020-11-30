import logging
from enum import Enum

console = logging.getLogger(__name__)


class Condition(Enum):
    EQ = 0  # Equal
    NE = 1  # NOT EQUAL
    HS_CS = 2  # Unsigned Greater than or equal
    LO_CC = 3  # Unsigned Lower then
    MI = 4  # Negative
    PL = 5  # Positive or zero
    VS = 6  # Overflow
    VC = 7  # No overflow
    HI = 8  # Unsigned greater than
    LS = 9  # Unsigned lower than or equal
    GE = 10  # Signed greater than or equal
    LT = 11  # Signed lower than
    GT = 12  # Signed greater than
    LE = 13  # Signed lower than or equal
    AL = 14  # Always

    def getResult(self, alu) -> bool:
        zero = bool(alu.zero)
        carry = bool(alu.carry)
        overflow = bool(alu.overflow)
        negative = bool(alu.negative)

        condition_result = dict({
            Condition.EQ: zero,
            Condition.NE: not zero,
            Condition.HS_CS: carry,
            Condition.LO_CC: not carry,
            Condition.MI: negative,
            Condition.PL: not negative,
            Condition.VS: overflow,
            Condition.VC: not overflow,
            Condition.HI: carry and (not zero),
            Condition.LS: (not carry) and zero,
            Condition.GE: negative == overflow,
            Condition.LT: negative != overflow,
            Condition.GT: (negative == overflow) and not zero,
            Condition.LE: zero or (negative != overflow),
            Condition.AL: True,
        })
        result = condition_result.get(self)
        console.debug(f"\tCondition {self.name} (Z={zero}, C={carry}, V={overflow}, N={negative}) = {result}")
        return result
