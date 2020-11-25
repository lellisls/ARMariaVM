from enum import Enum


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
