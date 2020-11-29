import logging

from lib.alu import ALU
from lib.barrel_shifter import BarrelShifter
from lib.control_unit.instruction.instruction import Instruction
from lib.control_unit.instruction.instruction_factory import InstructionFactory
from lib.control_unit.register import Register
from lib.control_unit.system_call import SystemCall
from lib.memory_unit import MemoryController, Memory
from lib.signal_extender import SignalExtender

console = logging.getLogger(__name__)


class ControlCore:
    inst: Instruction = None
    pc = None
    running = True
    next_pc = None
    is_bios = True
    is_kernel = False

    # Used for input debugging
    values = []

    def __init__(self, memory_ctrl: MemoryController, bios: Memory):
        self.instruction_factory = InstructionFactory()
        self.sig_ex = SignalExtender()
        self.bs = BarrelShifter()
        self.alu = ALU()

        self.memory_ctrl = memory_ctrl
        self.bios = bios

        self.reset()

    def reset(self):
        self.is_bios = True
        self.is_kernel = False
        self.pc = None
        self.running = True
        self.next_pc = None

        for reg in Register:
            reg.setValue(0)
        self.memory_ctrl.reset()
        self.values = [2, 4]

    def iterate(self):
        self.pc = Register.ProgramCounter.getValue()
        self.next_pc = self.pc + 1

        code_memory = self.bios if self.is_bios else self.memory_ctrl.main_memory

        inst_code = code_memory.get(self.pc)
        self.inst = self.instruction_factory.build(inst_code)

        ctx = code_memory.get_context(self.pc)
        ctx = f" - {ctx}" if ctx != "" else ""
        source = ""
        if self.is_bios:
            source = " (BIOS)"
        elif self.is_kernel:
            source = " (OS)"

        console.debug(f"\n{self.pc: 4}{source}: {self.inst}{ctx}")

        self.calculate()
        Register.ProgramCounter.setValue(self.next_pc)

    def calculate(self):
        instructions = {
            1: self.inst1_lsl,
            2: self.inst2_lsr,
            3: self.inst3_asr,
            4: self.inst4_add,
            5: self.inst5_sub,
            6: self.inst6_add,
            7: self.inst7_sub,
            8: self.inst8_mov,
            9: self.inst9_cmp,
            10: self.inst10_add,
            11: self.inst11_sub,
            12: self.inst12_and,
            13: self.inst13_exor,
            14: self.inst14_lsl,
            15: self.inst15_lsr,
            16: self.inst16_asr,
            17: self.inst17_adc,
            18: self.inst18_sbc,
            19: self.inst19_ror,
            20: self.inst20_tst,
            21: self.inst21_neg,
            22: self.inst22_cmp,
            23: self.inst23_cmn,
            24: self.inst24_orr,
            25: self.inst25_mul,
            26: self.inst26_bic,
            27: self.inst27_mvn,
            28: self.inst28_add,
            29: self.inst29_add,
            30: self.inst30_add,
            31: self.inst31_cmp,
            32: self.inst32_cmp,
            33: self.inst33_cmp,
            34: self.inst34_div,
            35: self.inst35_mov,
            36: self.inst36_mov,
            37: self.inst37_mov,
            38: self.inst38_br,
            39: self.inst39_ldr,
            40: self.inst40_str,
            41: self.inst41_strh,
            42: self.inst42_strb,
            43: self.inst43_ldrsb,
            44: self.inst44_ldr,
            45: self.inst45_ldrh,
            46: self.inst46_ldrb,
            47: self.inst47_ldrsh,
            48: self.inst48_str,
            49: self.inst49_ldr,
            50: self.inst50_strb,
            51: self.inst51_ldrb,
            52: self.inst52_strh,
            53: self.inst53_ldrh,
            54: self.inst54_str,
            55: self.inst55_ldr,
            56: self.inst56_add,
            57: self.inst57_add,
            58: self.inst58_cpxr,
            59: self.inst59_sxth,
            60: self.inst60_sxtb,
            61: self.inst61_uxth,
            62: self.inst62_uxtb,
            63: self.inst63_rev,
            64: self.inst64_rev16,
            65: self.inst65_mod,
            66: self.inst66_revsh,
            67: self.inst67_push,
            68: self.inst68_pop,
            69: self.inst69_output,
            70: self.inst70_pause,
            71: self.inst71_input,
            72: self.inst72_swi,
            73: self.inst73_b,
            74: self.inst74_nop,
            75: self.inst75_halt,
            76: self.inst76_pxr,
            77: self.inst77_pushm,
            78: self.inst78_popm,
            79: self.inst79_bl,
            80: self.inst80_bx,
        }
        handler = instructions.get(self.inst.id, self.unhandled_inst)
        handler()

    def unhandled_inst(self):
        raise RuntimeError(f"Unhandled instruction: {self.inst}")

    def inst1_lsl(self):
        rm = self.inst.registerM.getValue()
        rd = self.bs.lsl(rm, self.inst.immediate)
        self.inst.registerD.setValue(rd)

    def inst2_lsr(self):
        self.unhandled_inst()

    def inst3_asr(self):
        self.unhandled_inst()

    def inst4_add(self):
        rn = self.inst.registerN.getValue()
        rm = self.inst.registerM.getValue()
        rd = self.alu.add_or_cmn(rn, rm)
        self.inst.registerD.setValue(rd)

    def inst5_sub(self):
        rn = self.inst.registerN.getValue()
        rm = self.inst.registerM.getValue()
        rd = self.alu.sub_or_cmp(rn, rm)
        self.inst.registerD.setValue(rd)

    def inst6_add(self):
        self.unhandled_inst()

    def inst7_sub(self):
        self.unhandled_inst()

    def inst8_mov(self):
        self.inst.registerD.setValue(self.inst.immediate)

    def inst9_cmp(self):
        self.unhandled_inst()

    def inst10_add(self):
        self.inst.registerD.increment(self.inst.immediate)

    def inst11_sub(self):
        self.unhandled_inst()

    def inst12_and(self):
        self.unhandled_inst()

    def inst13_exor(self):
        self.unhandled_inst()

    def inst14_lsl(self):
        self.unhandled_inst()

    def inst15_lsr(self):
        self.unhandled_inst()

    def inst16_asr(self):
        self.unhandled_inst()

    def inst17_adc(self):
        self.unhandled_inst()

    def inst18_sbc(self):
        self.unhandled_inst()

    def inst19_ror(self):
        self.unhandled_inst()

    def inst20_tst(self):
        self.unhandled_inst()

    def inst21_neg(self):
        self.unhandled_inst()

    def inst22_cmp(self):
        lm = self.inst.registerM.getValue()
        ld = self.inst.registerD.getValue()
        self.alu.sub_or_cmp(lm, ld)

    def inst23_cmn(self):
        self.unhandled_inst()

    def inst24_orr(self):
        self.unhandled_inst()

    def inst25_mul(self):
        lm = self.inst.registerM.getValue()
        ld = self.inst.registerD.getValue()
        ld = self.alu.mul(ld, lm)
        self.inst.registerD.setValue(ld)

    def inst26_bic(self):
        self.unhandled_inst()

    def inst27_mvn(self):
        self.unhandled_inst()

    def inst28_add(self):
        self.unhandled_inst()

    def inst29_add(self):
        self.unhandled_inst()

    def inst30_add(self):
        self.unhandled_inst()

    def inst31_cmp(self):
        self.unhandled_inst()

    def inst32_cmp(self):
        self.unhandled_inst()

    def inst33_cmp(self):
        self.unhandled_inst()

    def inst34_div(self):
        lm = self.inst.registerM.getValue()
        ld = self.inst.registerD.getValue()
        ld = self.alu.div(ld, lm)
        self.inst.registerD.setValue(ld)

    def inst35_mov(self):
        self.inst.registerD.copyValueFrom(self.inst.registerM)

    def inst36_mov(self):
        self.inst.registerD.copyValueFrom(self.inst.registerM)

    def inst37_mov(self):
        self.inst.registerD.copyValueFrom(self.inst.registerM)

    def inst38_br(self):  # RELATIVE INDIRECT BRANCH
        condition = self.inst.condition.getResult(self.alu)
        rd = self.inst.registerD.getValue()

        if condition:
            console.debug(f"\tTake branch {self.pc} + {rd}")
            self.next_pc = self.pc + rd
        else:
            console.debug("\tNot take branch")

    def inst39_ldr(self):
        self.unhandled_inst()

    def inst40_str(self):
        self.unhandled_inst()

    def inst41_strh(self):
        self.unhandled_inst()

    def inst42_strb(self):
        self.unhandled_inst()

    def inst43_ldrsb(self):
        self.unhandled_inst()

    def inst44_ldr(self):
        lm = self.inst.registerM.getValue()
        ln = self.inst.registerN.getValue()
        ld = self.memory_ctrl.get_data(lm + ln)
        self.inst.registerD.setValue(ld)
        self.inst.registerD.setValue(ld)

    def inst45_ldrh(self):
        self.unhandled_inst()

    def inst46_ldrb(self):
        self.unhandled_inst()

    def inst47_ldrsh(self):
        self.unhandled_inst()

    def inst48_str(self):
        ld = self.inst.registerD.getValue()
        lm = self.inst.registerM.getValue()
        self.memory_ctrl.set_data(lm + self.inst.immediate, ld)

    def inst49_ldr(self):
        lm = self.inst.registerM.getValue()
        ld = self.memory_ctrl.get_data(lm + self.inst.immediate)
        self.inst.registerD.setValue(ld)

    def inst50_strb(self):
        self.unhandled_inst()

    def inst51_ldrb(self):
        self.unhandled_inst()

    def inst52_strh(self):
        self.unhandled_inst()

    def inst53_ldrh(self):
        self.unhandled_inst()

    def inst54_str(self):
        self.unhandled_inst()

    def inst55_ldr(self):
        self.unhandled_inst()

    def inst56_add(self):
        pc = Register.ProgramCounter.getValue()
        rd = self.alu.add_or_cmn(pc, self.inst.immediate << 1)
        self.inst.registerD.setValue(rd)

    def inst57_add(self):
        sp = Register.UserSPKeeper.getValue()
        rd = self.alu.add_or_cmn(sp, self.inst.immediate << 1)
        self.inst.registerD.setValue(rd)

    def inst58_cpxr(self):
        self.inst.registerD.copyValueFrom(Register.SpecReg)

    def inst59_sxth(self):
        rm = self.inst.registerM.getValue()
        rm = self.sig_ex.extend16(rm)
        self.inst.registerD.setValue(rm)

    def inst60_sxtb(self):
        rm = self.inst.registerM.getValue()
        rm = self.sig_ex.extend8(rm)
        self.inst.registerD.setValue(rm)

    def inst61_uxth(self):
        rm = self.inst.registerM.getValue()
        self.inst.registerD.setValue(rm)

    def inst62_uxtb(self):
        rm = self.inst.registerM.getValue()
        self.inst.registerD.setValue(rm)

    def inst63_rev(self):
        self.unhandled_inst()

    def inst64_rev16(self):
        self.unhandled_inst()

    def inst65_mod(self):
        self.unhandled_inst()

    def inst66_revsh(self):
        self.unhandled_inst()

    def inst67_push(self):
        rd = self.inst.registerD.getValue()
        if self.is_kernel:
            self.memory_ctrl.push_kernel_stack(rd)
        else:
            self.memory_ctrl.push_user_stack(rd)

    def inst68_pop(self):
        if self.is_kernel:
            value = self.memory_ctrl.pop_kernel_stack()
        else:
            value = self.memory_ctrl.pop_user_stack()

        self.inst.registerD.setValue(value)

    def inst69_output(self):
        rd = self.inst.registerD.getValue()
        console.info(f"\tOUTPUT: {rd}")

    def inst70_pause(self):
        # self.running = False
        pass

    def inst71_input(self):
        # value = int(input("INPUT: "))
        value = self.values.pop()
        console.info(f"\tINPUT: {value}")

        # value = int(random() * 10)
        # console.info(f"\tINPUT: {value} (random)")
        self.inst.registerD.setValue(value)

    def inst72_swi(self):  # Software interruption
        sc = SystemCall(self.inst.immediate)

        console.info(f"\tInterruption: {sc}")
        self.is_bios = False

        if SystemCall.ProgramCompletion == sc:
            self.running = False

        if self.is_kernel:  # Exit privileged mode
            Register.StackPointer2.setValue(Register.StackPointer.getValue())
            Register.StackPointer.setValue(Register.UserSPKeeper.getValue())
            Register.ProgramCounter.setValue(Register.PCKeeper.getValue())
            self.is_kernel = False
        else:  # Enter privileged mode
            Register.UserSPKeeper.setValue(Register.StackPointer.getValue())
            Register.PCKeeper.setValue(Register.ProgramCounter.getValue())
            Register.StackPointer.setValue(Register.StackPointer2.getValue())
            self.next_pc = self.memory_ctrl.os_start
            self.is_kernel = True

        Register.SystemCallRegister.setValue(sc.value)

    def inst73_b(self):
        condition = self.inst.condition.getResult(self.alu)
        imm = self.inst.immediate

        if condition:
            console.debug(f"\tTake branch {self.pc} + {imm}")
            self.next_pc = self.pc + imm
        else:
            console.debug("\tNot take branch")

    def inst74_nop(self):
        pass

    def inst75_halt(self):
        self.unhandled_inst()

    def inst76_pxr(self):
        self.unhandled_inst()

    def inst77_pushm(self):
        if self.is_kernel:
            self.memory_ctrl.push_kernel_stack_multiple(self.inst.immediate)
        else:
            self.memory_ctrl.push_user_stack_multiple(self.inst.immediate)

    def inst78_popm(self):
        if self.is_kernel:
            self.memory_ctrl.pop_kernel_stack_multiple(self.inst.immediate)
        else:
            self.memory_ctrl.pop_user_stack_multiple(self.inst.immediate)

    def inst79_bl(self):  # RELATIVE INDIRECT BRANCH
        Register.LinkRegister.setValue(self.pc + 1)
        rd = self.inst.registerD.getValue()
        self.next_pc = self.pc + rd
        pass

    def inst80_bx(self):  # ABSOLUTE INDIRECT BRANCH
        self.next_pc = self.inst.registerD.getValue()
        pass
