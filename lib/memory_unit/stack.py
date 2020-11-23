from lib.control_unit.register import RegisterBank, Register


class Stack:
    def __init__(self, main_memory, reg_bank: RegisterBank, register: Register, start: int, end: int):
        self.main_memory = main_memory
        self.reg_bank = reg_bank
        self.register = register
        self.start = start
        self.end = end

    def push(self, value: int):
        next_idx = self.reg_bank.increment(self.register)
        if self.start > next_idx or self.end < next_idx:
            raise RuntimeError("Stack overflow")
        self.main_memory.set(self.end - next_idx, value)

    def pushM(self, increment):
        self.reg_bank.increment(self.register, increment)

    def pop(self, value: int):
        next_idx = self.reg_bank.decrement(self.register)
        if self.start > next_idx or self.end < next_idx:
            raise RuntimeError("Stack overflow")
        self.main_memory.set(self.end - next_idx, value)

    def popM(self, increment):
        self.reg_bank.decrement(self.register, increment)

