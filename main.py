import os

from file.programLoader import ProgramLoader

if __name__ == '__main__':
    loader = ProgramLoader(os.path.join(os.path.dirname(__file__), "data", "program.txt"))
    instructions = loader.loadFile()

