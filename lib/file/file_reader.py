import os
import re


class FileReader:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.data = "\n".join(self.file.readlines())

    def loadFileRaw(self):
        rows = re.findall(r"(\d+) : ([0-1]+); -- (.*)", self.data)
        return [(int(address), compressed, contexts) for address, compressed, contexts in rows]

    def loadFile(self):
        instructions = self.loadFileRaw()
        decompressed_inst = []
        for value in instructions:
            address, compressed, contexts = value
            if "size" in contexts or compressed == "0" * 16:
                continue
            context1, context2 = contexts.split("|")

            mid = int(len(compressed) / 2)
            inst1, inst2 = compressed[:mid], compressed[mid:]
            assert len(inst1) == len(inst2)

            decompressed_inst.append((address, inst1, context1))
            decompressed_inst.append((address, inst2, context2))

        return decompressed_inst


if __name__ == '__main__':
    loader = FileReader(os.path.join(os.path.dirname(__file__), "..", '..', "data", "program.txt"))
    print(loader.loadFile())
    print(loader.loadFileRaw())
