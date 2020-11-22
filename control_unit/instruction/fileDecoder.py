import os

from control_unit.instruction.decoder import BytecodeDecoder
from file.programLoader import ProgramLoader


class FileDecoder:
    @classmethod
    def decode(cls, instruction, print_=False):
        (line_no, bytecode, context) = instruction
        try:
            decoder = BytecodeDecoder(bytecode)
            result = decoder.decode()
            if print_:
                print(f"({result.id:2})  {result.name:6} : {context.strip()}")
            result.line_no = line_no
            result.context = context

            if str(result.id) not in context:
                raise Exception(f"Id {result.id} not in context: {context}")
            if result.name not in context.split(" "):
                raise Exception(f"Name {result.name} not in context: {context}")
            return result
        except Exception as e:
            print(f"Error while decoding {bytecode}: {e}")
            print(f"Context: {line_no}: {bytecode} -- {context}")
            raise e

    @classmethod
    def loadDecodedFile(cls, filename, print_=False):
        loader = ProgramLoader(filename)
        encoded = loader.loadFile()
        return [cls.decode(inst, print_=True) for inst in encoded]


if __name__ == '__main__':
    file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'program.txt')

    decoder = FileDecoder()
    instructions = decoder.loadDecodedFile(file)
