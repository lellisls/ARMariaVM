import numpy

class Memory:
    def __init__(self, size, width=32):
        self.max_address = 0
        self.size = size
        self.width = width

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
        self.data[address] = value

    def __str__(self):
        output = ""
        for index, value in enumerate(self.data[:self.max_address]):
            if self.width == 32:
                output += f"{index: 4}: {value :032b}\n"
            else:
                output += f"{index: 4}: {value :016b}\n"
        return output
