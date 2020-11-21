import os

from file.programLoader import ProgramLoader
from instruction.instructionFactory import InstructionFactory
from instruction.decoder import BytecodeDecoder

if __name__ == '__main__':
    instructionFactory = InstructionFactory()

    loader = ProgramLoader(os.path.join(os.path.dirname(__file__), "data", "program.txt"))
    instructions = loader.loadFile()
    for (lineno, bytecode, context) in instructions:
        try:
            decoder = BytecodeDecoder(bytecode)
            decoder.decode()
        except Exception as e:
            print(f"Error while decoding {bytecode}: {e}")
            print(f"Context: {lineno}: {bytecode} -- {context}")
            raise e
