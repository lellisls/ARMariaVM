import logging
import os

from lib.control_unit.instruction.decoder import BytecodeDecoder
from lib.file.file_reader import FileReader

console = logging.getLogger(__name__)


class FileDecoder:
    @classmethod
    def decode(cls, instruction, print_=False):
        (line_no, bytecode, context) = instruction
        try:
            decoder = BytecodeDecoder(bytecode)
            result = decoder.decode()
            if print_:
                console.info(f"({result.id:2})  {result.name:6} : {context.strip()}")
            result.line_no = line_no
            result.context = context

            if str(result.id) not in context:
                raise RuntimeError(f"Id {result.id} not in context: {context}")
            if result.name not in context.split(" "):
                raise RuntimeError(f"Name {result.name} not in context: {context}")
            return result
        except RuntimeError as e:
            console.info(f"Error while decoding {bytecode}: {e}")
            console.info(f"Context: {line_no}: {bytecode} -- {context}")
            raise e

    @classmethod
    def loadDecodedFile(cls, filename, print_=False):
        loader = FileReader(filename)
        encoded = loader.loadFile()
        return [cls.decode(inst, print_) for inst in encoded]


if __name__ == '__main__':
    file = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data', 'program.txt')

    decoder = FileDecoder()
    instructions = decoder.loadDecodedFile(file)
