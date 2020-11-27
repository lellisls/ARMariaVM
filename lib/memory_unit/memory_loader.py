import re

from lib.file.file_reader import FileReader
from lib.memory_unit import Memory


class MemoryLoader:
    def __init__(self, memory: Memory):
        self.memory = memory

    def loadBios(self, filename):
        with open(filename) as file:
            for address, inst in enumerate(file.readlines()):
                self.memory.set(address, int(inst, 2))

    def loadFile(self, filename, split=False, start_address=0):
        fileReader = FileReader(filename)
        data = fileReader.loadFileRaw()
        index = 0
        for (address, instruction, context) in data:
            # print(instruction)
            mid = int(len(instruction) / 2)
            inst1, inst2 = int(instruction[:mid], 2), int(instruction[mid:], 2)

            if "size" in context:
                pass

            context = self._parse_context(context)

            if split:
                self.memory.set(start_address + index * 2, inst1)
                self.memory.set(start_address + index * 2 + 1, inst2)
                self.memory.set_context(start_address + index * 2, context)
            else:
                instruction = int(instruction, 2)
                self.memory.set(start_address + index, instruction)
                self.memory.set_context(start_address + index, context)
            index += 1

    @classmethod
    def _parse_context(cls, ctx):
        result = re.findall(r"\(\((([A-Z]|[a-z]|_| |[0-9])+)\)\)", ctx)
        if len(result) > 0:
            return f"{result[0][0]}"
        else:
            return ""
