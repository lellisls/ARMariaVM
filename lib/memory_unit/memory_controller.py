from lib.control_unit.register import RegisterBank, Register
from lib.memory_unit import Memory
from lib.memory_unit.stack import Stack


class MemoryController:
    user_stack_end = 8191

    def __init__(self):
        self.main_memory = Memory(32768)  # 128k
        self.privileged_stack = Stack(self.main_memory, Register.StackPointer, 4096, 6143)
        self.user_stack = Stack(self.main_memory, Register.UserSPKeeper, 6144, 8191)

    def push_user_stack(self, value):
        self.user_stack.push(value)

    def pop_user_stack(self):
        return self.user_stack.pop()

    def push_kernel_stack(self, value):
        self.privileged_stack.push(value)
