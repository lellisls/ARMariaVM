import logging
import os

from lib.control_unit.control_core import ControlCore
from lib.control_unit.instruction.instruction_factory import InstructionFactory
from lib.control_unit.register import Register
from lib.memory_unit import Memory, MemoryController
from lib.memory_unit.memory_loader import MemoryLoader
from ui.log_handler import LogHandler
from ui.main_window import MainWindow

format_ = '%(message)s'

logging.basicConfig(level=logging.DEBUG, format=format_)
logger = logging.getLogger()

factory = InstructionFactory()
main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, 'data')
bios_path = os.path.join(data_dir, 'bios.mif')
program_path = os.path.join(data_dir, 'program.mif')

if __name__ == '__main__':
    window = MainWindow()
    log_handler = LogHandler(window.print_console)
    log_handler.setLevel(level=logging.DEBUG)
    logger.addHandler(log_handler)

    bios = Memory(pow(2, 9), 16)  # 512b
    bios_loader = MemoryLoader(bios)
    bios_loader.loadFile(bios_path)
    controller = MemoryController()
    memory_loader = MemoryLoader(controller.main_memory)
    memory_loader.loadFile(program_path, split=False)

    Register.ProgramCounter.setValue(0)

    core = ControlCore(controller, bios)

    window.run(core)

    core.running = False

    # console.debug("RUNNING BIOS:")
    # for idx, inst in enumerate(bios.data):
    #     inst = f"{inst:016b}"
    #     inst = factory.build(inst)
    #     console.debug(f"{idx: 4}: {inst}")
    #     code.inst = inst
    #     core.calculate()
