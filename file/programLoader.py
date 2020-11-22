import os
import re


class ProgramLoader:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.data = "\n".join(self.file.readlines())
        self.instructions = []

    def loadFile(self):
        instructions = re.findall(r"(\d+) : ([0-1]+); -- (.*)", self.data)
        self.instructions = []
        for value in instructions:
            lineno, compressed, contexts = value
            if "size" in contexts or compressed == "0" * 16:
                continue
            context1, context2 = contexts.split("|")

            mid = int(len(compressed) / 2)
            inst1, inst2 = compressed[:mid], compressed[mid:]
            assert len(inst1) == len(inst2)

            self.instructions.append((lineno, inst1, context1))
            self.instructions.append((lineno, inst2, context2))

        return self.instructions

    def decompress(self, value):
        return


if __name__ == '__main__':
    loader = ProgramLoader(os.path.join(os.path.dirname(__file__), "..", "data", "program.txt"))
    print(loader.loadFile())
