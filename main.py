import os

from memory_unit import Bios, Memory

main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, 'data')

if __name__ == '__main__':
    bios = Bios(os.path.join(data_dir, 'bios.txt'))
    storage = Memory()
    main_memory = Memory()
