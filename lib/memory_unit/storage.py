from lib.file.file_reader import FileReader
from lib.memory_unit import Memory


class Storage(Memory):
    def __init__(self, filename):
        fileReader = FileReader(filename)
        data = fileReader.loadFileRaw()
        super().__init__(len(data))
        for (address, instruction, context) in data:
            instruction = int(instruction, 2)
            self.set(address, instruction)
