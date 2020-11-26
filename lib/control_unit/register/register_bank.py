class RegisterBank:
    def __init__(self):
        self.bank = dict({})

    def setRegister(self, reg: int, value):
        self.bank[reg] = int(value)
        return int(value)

    def getRegister(self, reg: int):
        return self.bank.get(reg, 0)

    def increment(self, reg: int, value: int = 1):
        value = self.getRegister(reg) + value
        return self.setRegister(reg, value)

    def decrement(self, reg: int, value: int = 1):
        return self.setRegister(reg, self.getRegister(reg) - value)
