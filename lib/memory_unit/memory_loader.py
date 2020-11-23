from lib.file.file_reader import FileReader
from lib.memory_unit import Memory


class MemoryLoader:
    def __init__(self, memory: Memory):
        self.memory = memory

    def loadFile(self, filename, split=False):
        fileReader = FileReader(filename)
        data = fileReader.loadFileRaw()
        for (address, instruction, context) in data:
            address = int(address)
            mid = int(len(instruction) / 2)
            inst1, inst2 = int(instruction[:mid], 2), int(instruction[mid:], 2)
            if split:
                self.memory.set(address * 2, inst1)
                self.memory.set(address * 2 + 1, inst2)
            else:
                instruction = int(instruction, 2)
                self.memory.set(address, instruction)
