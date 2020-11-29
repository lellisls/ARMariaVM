import re

from lib.file.file_reader import FileReader
from lib.memory_unit import Memory


class MemoryLoader:
    def __init__(self, memory: Memory):
        self.memory = memory

    # def loadBios(self, filename):
    #     with open(filename) as file:
    #         for address, inst in enumerate(file.readlines()):
    #             self.memory.set(address, int(inst, 2))

    def loadFile(self, filename, split=False):
        fileReader = FileReader(filename)
        data = fileReader.loadFileRaw()
        for (address, instruction, context) in data:
            # print(f"{address}, {instruction}, {context}")
            mid = int(len(instruction) / 2)
            inst1, inst2 = int(instruction[:mid], 2), int(instruction[mid:], 2)

            if "size" in context:
                pass

            # print(context)
            context = self._parse_context(context)
            # print(context)
            if split:
                raise NotImplementedError("NOT IMPLEMENTED")
                # self.memory.set(start_address + index * 2, inst1)
                # self.memory.set(start_address + index * 2 + 1, inst2)
                # self.memory.set_context(start_address + index * 2, context)
            else:
                instruction = int(instruction, 2)
                self.memory.set(address, instruction)
                self.memory.set_context(address, context)


    @classmethod
    def _parse_context(cls, ctx):
        result = re.findall(r"\(\((.*)\)\)", ctx)
        if len(result) > 0:
            return f"{result[0]}"
        else:
            return ""
