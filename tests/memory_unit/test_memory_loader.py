import os

import pytest

from lib.file.file_reader import FileReader
from lib.memory_unit import Memory, MemoryLoader

instructions_path = os.path.join(os.path.dirname(__file__), 'data', 'instructions.txt')


@pytest.fixture
def memory():
    return Memory(3000)


@pytest.fixture
def file_loader():
    return FileReader(instructions_path)


def test_memory_loader(memory: Memory, file_loader: FileReader):
    instructions = file_loader.loadFileRaw()

    memory_loader = MemoryLoader(memory)
    memory_loader.loadFile(instructions_path)

    for address, inst, comment in instructions:
        assert int(inst, 2) == memory.get(address)
