from enum import Enum


class Register(Enum):
    HeapArrayRegister = 0
    AccumulatorRegister = 1
    TemporaryRegister = 2
    SecondRegister = 3
    FramePointer = 4
    GlobalPointer = 5
    UserSPKeeper = 6
    SystemCallRegister = 7
    StoredSpecReg = 8
    LinkRegister = 12
    PCKeeper = 13
    StackPointer = 14
    ProgramCounter = 15
