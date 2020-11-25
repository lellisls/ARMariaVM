from lib.control_unit.register import RegisterBank, Register


class Stack:
    def __init__(self, main_memory, reg_bank: RegisterBank, register: Register, start: int, end: int):
        self.main_memory = main_memory
        self.reg_bank = reg_bank
        self.register = register
        self.start = start
        self.end = end
        self.size = end - start + 1
        self.reg_bank.setRegister(self.register, end)

    def push(self, value: int):
        next_idx = self.pushM(1)
        self.main_memory.set(self.end - next_idx, value)

    def pushM(self, increment):
        next_idx = self.reg_bank.increment(self.register, increment)
        if next_idx > self.size or next_idx < 0:
            raise RuntimeError(f"Stack overflow: 0 <= {next_idx} <= {self.end}")
        return next_idx

    def pop(self):
        value = self.main_memory.get(self.reg_bank.getRegister(self.register))
        self.popM(1)
        return value

    def popM(self, increment):
        next_idx = self.reg_bank.decrement(self.register, increment)
        if next_idx > self.size or next_idx < 0:
            raise RuntimeError(f"Stack overflow: 0 <= {next_idx} <= {self.end}")
        return next_idx

