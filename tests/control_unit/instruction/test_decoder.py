import os

from lib.control_unit.instruction.util.fileDecoder import FileDecoder

instructions_path = os.path.join(os.path.dirname(__file__), 'data', 'instructions.txt')


def test_decoder_works():
    file_decoder = FileDecoder()
    file_decoder.loadDecodedFile(instructions_path)
