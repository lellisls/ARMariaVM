import os

import pytest

from lib.memory_unit import Memory, MemoryLoader

instructions_path = os.path.join(os.path.dirname(__file__), 'data', 'instructions.txt')


@pytest.fixture
def memory():
    return Memory(3000)


def test_memory_loader(memory: Memory):
    memory_loader = MemoryLoader(memory)
    memory_loader.loadFile(instructions_path)
