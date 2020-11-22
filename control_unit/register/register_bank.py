from control_unit.register.register import Register


class RegisterBank:
    def __init__(self):
        self.bank = dict({
            Register.HeapArrayRegister: 0,
            Register.AccumulatorRegister: 0,
            Register.TemporaryRegister: 0,
            Register.SecondRegister: 0,
            Register.FramePointer: 0,
            Register.GlobalPointer: 0,
            Register.UserSPKeeper: 0,
            Register.SystemCallRegister: 0,
            Register.StoredSpecReg: 0,
            Register.LinkRegister: 0,
            Register.PCKeeper: 0,
            Register.StackPointer: 0,
            Register.ProgramCounter: 0,
        })

    def setRegister(self, reg: Register, value):
        self.bank[reg] = value

    def getRegister(self, reg: Register):
        return self.bank[reg]
