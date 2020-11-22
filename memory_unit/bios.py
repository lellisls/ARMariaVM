from file.file_reader import FileReader
from memory_unit.memory import Memory


class Bios(Memory):
    def __init__(self, filename):
        fileReader = FileReader(filename)
        data = fileReader.loadFile()
        super().__init__(len(data))
        for (address, instruction, context) in data:
            self.set(address, instruction)
