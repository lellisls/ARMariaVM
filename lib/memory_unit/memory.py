import logging

import numpy

console = logging.getLogger(__name__)


class Memory:
    def __init__(self, size, width=32):
        self.context = dict()
        self.max_address = 0
        self.size = size
        self.width = width
        self.last_modified = -1

        if width == 32:
            self.data = numpy.zeros(size, numpy.uint32)
        else:
            self.data = numpy.zeros(size, numpy.uint16)

    @classmethod
    def _test_address(cls, address):
        if address < 0:
            raise IndexError(f"Negative index not supported: {address}")

    def get(self, address):
        self._test_address(address)
        return self.data[address]

    def set(self, address, value):
        self._test_address(address)
        self.max_address = max(self.max_address, address)
        self.last_modified = address

        self.data[address] = value

    def set_context(self, address, value: str):
        value = value.strip()
        if value != "":
            self.context[address] = value

    def get_context(self, index):
        return self.context.get(index, "")
