from enum import Enum


class SystemCall(Enum):
    StandardPreemptionFlow = 0
    IORequest = 1
    ProgramCompletion = 2
    UserPreemption = 3
    BiosCompletion = 4
