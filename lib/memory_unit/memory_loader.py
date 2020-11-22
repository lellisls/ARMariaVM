from lib.file.file_reader import FileReader
from lib.memory_unit import Memory


class MemoryLoader:
    def __init__(self, memory: Memory):
        self.memory = memory

    def loadFile(self, filename):
        fileReader = FileReader(filename)
        data = fileReader.loadFileRaw()
        super().__init__(len(data))
        for (address, instruction, context) in data:
            instruction = int(instruction, 2)
            self.set(address, instruction)

