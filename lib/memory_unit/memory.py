import numpy


class Memory:
    def __init__(self, size):
        self.size = size
        self.data = numpy.zeros(size, numpy.uint32)

    def get(self, address):
        return self.data[address]

    def set(self, address, value):
        self.data[address] = value
