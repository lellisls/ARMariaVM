from abc import abstractmethod


class Instruction:
    @abstractmethod
    def execute(self):
        pass

