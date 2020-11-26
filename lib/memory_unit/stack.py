from lib.control_unit.register import Register


class Stack:
    def __init__(self, main_memory, register: Register, start: int, end: int):
        self.main_memory = main_memory
        self.register = register
        self.start = start
        self.end = end
        self.size = end - start
        self.reset()

    def push(self, value: int):
        next_idx = self.pushM(1)
        self.main_memory.set(next_idx, value)

    def pushM(self, increment):
        next_idx = self.register.decrement(increment)
        self._check_index(next_idx)
        return next_idx

    def pop(self):
        value = self.main_memory.get(self.register.getValue())
        self.popM(1)
        return value

    def popM(self, increment):
        next_idx = self.register.increment(increment)
        self.main_memory.set(next_idx - 1, 0)
        self._check_index(next_idx)

        for idx in range(next_idx - increment, next_idx):
            self.main_memory.set(idx, 0)

        return next_idx

    def reset(self):
        for idx in range(self.start, self.end):
            self.main_memory.set(idx, 0)
        self.register.setValue(self.end)

    def _check_index(self, next_idx):
        if next_idx > self.end or next_idx < self.start:
            raise RuntimeError(f"Stack overflow: {self.start} <= {next_idx} < {self.size}")
