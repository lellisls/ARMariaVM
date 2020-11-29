import logging

from lib.control_unit.instruction.instruction_factory import InstructionFactory
from lib.control_unit.register import Register
from lib.memory_unit import Memory
from lib.memory_unit.stack import Stack

console = logging.getLogger(__name__)


class MemoryController:
    user_stack_end = 8191

    def __init__(self):
        self.inst_factory = InstructionFactory()
        self.main_memory = Memory(32768)  # 128k
        self.kernel_stack = Stack(self.main_memory, Register.StackPointer, 4096, 6143)
        self.user_stack = Stack(self.main_memory, Register.StackPointer, 6144, 8191)
        self.code_start = 0
        self.code_end = 2047
        self.os_start = 2048
        self.os_end = 4095

    def set_data(self, address, value):
        console.debug(f"\tMEMORY[{address}] = {value}")
        self.main_memory.set(address, value)

    def get_data(self, address):
        return self.main_memory.get(address)

    def push_user_stack(self, value):
        console.debug(f"\tPUSH USER >>s {value}")
        self.user_stack.push(value)

    def push_user_stack_multiple(self, increment):
        console.debug(f"\tPUSH USER by {increment}")
        self.user_stack.pushM(increment)

    def pop_user_stack(self):
        value = self.user_stack.pop()
        console.debug(f"\tPOP USER << {value}")
        return value

    def pop_user_stack_multiple(self, increment):
        self.user_stack.popM(increment)
        console.debug(f"\tPOP USER by {increment}")

    def push_kernel_stack(self, value):
        console.debug(f"\tPUSH KERNEL << {value}")
        self.kernel_stack.push(value)

    def push_kernel_stack_multiple(self, increment):
        console.debug(f"\tPUSH KERNEL by {increment}")
        self.kernel_stack.pushM(increment)

    def pop_kernel_stack(self):
        value = self.kernel_stack.pop()
        console.debug(f"\tPOP KERNEL >> {value}")
        return value

    def pop_kernel_stack_multiple(self, increment):
        self.kernel_stack.popM(increment)
        console.debug(f"\tPOP KERNEL by {increment}")

    def reset(self):
        self.user_stack.reset()
        self.kernel_stack.reset()

    def __str__(self):
        output = ""
        last = 0
        count = 0
        index = 0

        for index, value in enumerate(self.main_memory.data):
            flags = self.print_flags(index)
            mark = self.print_mark(index)

            output += mark

            if last == value == 0 and len(flags) == 0:
                count += 1
                continue

            if count > 1:
                output += self.print_text(index, f"{count: 5} empty words")

            elif count == 1:
                output += self.display_value(index - 1, 0)

            last = value
            count = 0

            output += self.display_value(index, value)

        if count > 1:
            output += self.print_text(index, f"{count: 5} empty words")

        return output

    def display_value(self, index, value):
        if index <= self.os_end:
            return self.display_inst(index, value)
        if self.main_memory.width == 32:
            return f"{index: 6}: {value :032b} = {value : 6}{self.print_flags(index)}\n"
        else:
            return f"{index: 6}: {value :016b} = {value : 6}{self.print_flags(index)}\n"

    def print_mark(self, index):
        result = ""
        if index == self.code_start:
            result += self.print_text(index, "CODE - START")
        if index == (self.code_end + 1):
            result += self.print_text(index, "CODE - END")
        if index == self.os_start:
            result += self.print_text(index, "OS - START")
        if index == (self.os_end + 1):
            result += self.print_text(index, "OS - END")
        if index == self.kernel_stack.start:
            result += self.print_text(index, "KERNEL STACK - START")
        if index == (self.kernel_stack.end + 1):
            result += self.print_text(index, "KERNEL STACK - END")
        if index == self.user_stack.start:
            result += self.print_text(index, "USER STACK - START")
        if index == (self.user_stack.end + 1):
            result += self.print_text(index, "USER STACK - END")
        return result

    @classmethod
    def print_text(cls, index, text):
        return f"{index: 6}: =========== {text :^17} ===========\n"

    def print_flags(self, index):
        reg = ""
        memory_address_regs = [Register.ProgramCounter, Register.StackPointer]

        for register in memory_address_regs:
            if index == register.getValue():
                reg = f"${register.shortName()}"

        if index == self.main_memory.last_modified:
            return ' <<< ' + reg

        if reg != "":
            return " <- " + reg

        return ""

    def display_inst(self, index, value):
        ctx = self.main_memory.get_context(index)
        ctx = f" - {ctx}" if ctx != "" else ""
        decoded = self.inst_factory.build(value)
        return f"{index: 6}: {str(decoded) :^20} {self.print_flags(index):10}{ctx}\n"
