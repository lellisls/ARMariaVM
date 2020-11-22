import os

from execution.codeExecutor import CodeExecutor
from file.programLoader import ProgramLoader

if __name__ == '__main__':
    loader = ProgramLoader(os.path.join(os.path.dirname(__file__), "data", "program.txt"))
    instructions = loader.loadFile()
    executor = CodeExecutor(instructions)
    executor.run()

