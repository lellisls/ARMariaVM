import os

from lib.control_unit.control_core import ControlCore
from lib.control_unit.instruction.instruction_factory import InstructionFactory
from lib.control_unit.register import RegisterBank, Register
from lib.memory_unit import Memory, MemoryController
from lib.memory_unit.memory_loader import MemoryLoader

factory = InstructionFactory()
main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, 'data')
bios_path = os.path.join(data_dir, 'bios.txt')
program_path = os.path.join(data_dir, 'program.txt')

if __name__ == '__main__':
    bios = Memory(pow(2, 9), 16)  # 512b
    bios_loader = MemoryLoader(bios)
    bios_loader.loadBios(bios_path)
    controller = MemoryController()
    memory_loader = MemoryLoader(controller.main_memory)
    memory_loader.loadFile(program_path, split=True)

    Register.ProgramCounter.setValue(0)
    core = ControlCore(controller)

    while core.running:
        core.iterate()

    # print("RUNNING BIOS:")
    # for idx, inst in enumerate(bios.data):
    #     inst = f"{inst:016b}"
    #     inst = factory.build(inst)
    #     print(f"{idx: 4}: {inst}")
    #     code.inst = inst
    #     core.calculate()
