from lib.file.file_reader import FileReader
from lib.memory_unit import Memory


class MemoryLoader:
    def __init__(self, memory: Memory):
        self.memory = memory

    def loadFile(self, filename):
        fileReader = FileReader(filename)
        data = fileReader.loadFileRaw()
        for (address, instruction, context) in data:
            address = int(address)
            instruction = int(instruction, 2)
            self.memory.set(address, instruction)
