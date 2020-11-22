from abc import abstractmethod


class Instruction:
    name = None
    id = None

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def _print_registers(self):
        raise NotImplementedError

    def __str__(self):
        return f"({self.id}) {self.name} {self._print_registers()}"
