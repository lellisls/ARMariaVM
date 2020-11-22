import os
import re

from instruction.decoder import BytecodeDecoder


class ProgramLoader:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.data = "\n".join(self.file.readlines())

    def _loadFile(self):
        instructions = re.findall(r"(\d+) : ([0-1]+); -- (.*)", self.data)
        instructions_encoded = []
        for value in instructions:
            lineno, compressed, contexts = value
            if "size" in contexts or compressed == "0" * 16:
                continue
            context1, context2 = contexts.split("|")

            mid = int(len(compressed) / 2)
            inst1, inst2 = compressed[:mid], compressed[mid:]
            assert len(inst1) == len(inst2)

            instructions_encoded.append((lineno, inst1, context1))
            instructions_encoded.append((lineno, inst2, context2))

        return instructions_encoded

    @staticmethod
    def _decode(instruction):
        (lineno, bytecode, context) = instruction
        try:
            decoder = BytecodeDecoder(bytecode)
            result = decoder.decode()
            print(f"{result.name} : {context}")

            if str(result.id) not in context:
                raise Exception(f"Id {result.id} not in context: {context}")
            if result.name not in context.split(" "):
                raise Exception(f"Name {result.name} not in context: {context}")
            return result
        except Exception as e:
            print(f"Error while decoding {bytecode}: {e}")
            print(f"Context: {lineno}: {bytecode} -- {context}")
            raise e

    def loadFile(self):
        encoded = self._loadFile()
        return [ProgramLoader._decode(inst) for inst in encoded]


if __name__ == '__main__':
    loader = ProgramLoader(os.path.join(os.path.dirname(__file__), "..", "data", "program.txt"))
    print(len(loader.loadFile()))
