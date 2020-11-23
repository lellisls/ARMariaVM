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

    def shortName(self):
        names = {
            self.HeapArrayRegister: "$H0",
            self.AccumulatorRegister: "$A0",
            self.TemporaryRegister: "$T1",
            self.SecondRegister: "$SXR",
            self.FramePointer: "$FP",
            self.GlobalPointer: "$GP",
            self.UserSPKeeper: "$USPK",
            self.SystemCallRegister: "$SC",
            self.StoredSpecReg: "$SXR",
            self.LinkRegister: "$LR",
            self.PCKeeper: "$PCK",
            self.StackPointer: "$SP",
            self.ProgramCounter: "$PC",
        }
        return names.get(self)

    def __str__(self):
        return f"{self.shortName()}"