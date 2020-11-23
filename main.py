import os

from lib.memory_unit import Memory
from lib.memory_unit.memory_loader import MemoryLoader

main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, 'data')
bios_path = os.path.join(data_dir, 'bios.txt')
# program_path = os.path.join(data_dir, 'program.txt')

if __name__ == '__main__':
    main_memory = Memory(32768)  # 128 K
    memory_loader = MemoryLoader(main_memory)
    memory_loader.loadFile(bios_path)
    # memory_loader.loadFile(program_path)

    print(main_memory)
