import os

from file.programLoader import ProgramLoader
from instruction.decoder import BytecodeDecoder
from instruction.instructionFactory import InstructionFactory

if __name__ == '__main__':
    instructionFactory = InstructionFactory()

    loader = ProgramLoader(os.path.join(os.path.dirname(__file__), "data", "program.txt"))
    instructions = loader.loadFile()
    for (lineno, bytecode, context) in instructions:
        try:
            decoder = BytecodeDecoder(bytecode)
            result = decoder.decode()
            print(f"{result.name} : {context}")

            if str(result.id) not in context:
                raise Exception(f"Id {result.id} not in context: {context}")
            if result.name not in context.split(" "):
                raise Exception(f"Name {result.name} not in context: {context}")
        except Exception as e:
            print(f"Error while decoding {bytecode}: {e}")
            print(f"Context: {lineno}: {bytecode} -- {context}")
            raise e
