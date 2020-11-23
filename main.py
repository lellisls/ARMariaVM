import os

from lib.memory_unit import Memory
from lib.memory_unit.memory_loader import MemoryLoader

main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, 'data')
bios_path = os.path.join(data_dir, 'bios.txt')
# program_path = os.path.join(data_dir, 'program.txt')

if __name__ == '__main__':
    bios = Memory(pow(2, 9), 16)  # 512b
    # main_memory = Memory(32768)  # 128k
    bios_loader = MemoryLoader(bios)
    bios_loader.loadBios(bios_path)
    # memory_loader.loadFile(program_path)

    print("BIOS:")
    print(bios)
