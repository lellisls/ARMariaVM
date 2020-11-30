import logging
from enum import Enum

console = logging.getLogger(__name__)


class Condition(Enum):
    EQ = 0  # Equal
    NE = 1  # NOT EQUAL
    # HS = 2  # Unsigned Greater than or equal
    # LO = 3  # Unsigned Lower then
    MI = 4  # Negative
    PL = 5  # Positive or zero
    # VS = 6  # Overflow
    # VC = 7  # No overflow
    # HI = 8  # Unsigned greater than
    # LS = 9  # Unsigned lower than or equal
    GE = 10  # Signed greater than or equal
    LT = 11  # Signed lower than
    GT = 12  # Signed greater than
    LE = 13  # Signed lower than or equal
    AL = 14  # Always
    # CS = 2  # Unsigned Greater than or equal
    # CC = 3  # Unsigned Lower THan

    def getResult(self, alu) -> bool:
        zero = equal = bool(alu.zero)
        carry = bool(alu.carry)
        overflow = bool(alu.overflow)
        negative = bool(alu.negative)
        less_signed = bool(alu.lt)
        greater_signed = bool(alu.gt)

        condition_result = dict({
            Condition.EQ: equal,
            Condition.NE: not equal,
            # Condition.CS: carry,
            # Condition.HS: carry,
            # Condition.CC: not carry,
            # Condition.LO: not carry,
            Condition.MI: negative,
            Condition.PL: not negative,
            # Condition.VS: overflow,
            # Condition.VC: not overflow,
            # Condition.HI: carry and (not zero),
            # Condition.LS: (not carry) and zero,
            Condition.GE: greater_signed or equal,
            Condition.LT: less_signed,
            Condition.GT: greater_signed,
            Condition.LE: less_signed or equal,
            Condition.AL: True,
        })
        result = condition_result.get(self)
        console.debug(f"\tCondition {self.name} (Z={zero}, C={carry}, V={overflow}, N={negative}) = {result}")
        return result
