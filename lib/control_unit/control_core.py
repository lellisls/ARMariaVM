import time
from random import random

from lib.alu import ALU
from lib.barrel_shifter import BarrelShifter
from lib.control_unit.instruction.instruction import Instruction
from lib.control_unit.instruction.instruction_factory import InstructionFactory
from lib.control_unit.register import RegisterBank, Register
from lib.control_unit.register.system_call import SystemCall
from lib.memory_unit import MemoryController
from lib.signal_extender import SignalExtender


class ControlCore:
    inst: Instruction = None

    def __init__(self, reg_bank: RegisterBank, memory_ctrl: MemoryController):
        self.instruction_factory = InstructionFactory()
        self.sig_ex = SignalExtender()
        self.bs = BarrelShifter()
        self.alu = ALU()

        self.pc = None
        self.running = True
        self.next_pc = None
        self.reg_bank = reg_bank
        self.memory_ctrl = memory_ctrl

    def iterate(self):
        self.pc = self.reg_bank.getRegister(Register.ProgramCounter)
        self.next_pc = self.pc + 1

        inst_code = self.memory_ctrl.main_memory.get(self.pc)
        self.inst = self.instruction_factory.build(inst_code)
        print(f"{self.pc: 4}: {self.inst}")
        self.calculate()
        self.reg_bank.setRegister(Register.ProgramCounter, self.next_pc)

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
        rm = self.reg_bank.getRegister(self.inst.registerM)
        rd = self.bs.lsl(rm, self.inst.immediate)
        self.reg_bank.setRegister(self.inst.registerD, rd)

    def inst2_lsr(self):
        self.unhandled_inst()

    def inst3_asr(self):
        self.unhandled_inst()

    def inst4_add(self):
        rn = self.reg_bank.getRegister(self.inst.registerN)
        rm = self.reg_bank.getRegister(self.inst.registerM)
        rd = self.alu.add_or_cmn(rn, rm)
        self.reg_bank.setRegister(self.inst.registerD, rd)

    def inst5_sub(self):
        rn = self.reg_bank.getRegister(self.inst.registerN)
        rm = self.reg_bank.getRegister(self.inst.registerM)
        rd = self.alu.sub_or_cmp(rn, rm)
        self.reg_bank.setRegister(self.inst.registerD, rd)

    def inst6_add(self):
        self.unhandled_inst()

    def inst7_sub(self):
        self.unhandled_inst()

    def inst8_mov(self):
        self.reg_bank.setRegister(self.inst.registerD, self.inst.immediate)

    def inst9_cmp(self):
        self.unhandled_inst()

    def inst10_add(self):
        self.reg_bank.increment(self.inst.registerD, self.inst.immediate)

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
        lm = self.reg_bank.getRegister(self.inst.registerM)
        ld = self.reg_bank.getRegister(self.inst.registerD)
        self.alu.sub_or_cmp(lm, ld)

    def inst23_cmn(self):
        self.unhandled_inst()

    def inst24_orr(self):
        self.unhandled_inst()

    def inst25_mul(self):
        lm = self.reg_bank.getRegister(self.inst.registerM)
        ld = self.reg_bank.getRegister(self.inst.registerD)
        ld = self.alu.mul(ld, lm)
        self.reg_bank.setRegister(self.inst.registerD, ld)

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
        lm = self.reg_bank.getRegister(self.inst.registerM)
        ld = self.reg_bank.getRegister(self.inst.registerD)
        ld = self.alu.div(ld, lm)
        self.reg_bank.setRegister(self.inst.registerD, ld)

    def inst35_mov(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst36_mov(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst37_mov(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst38_br(self):  # RELATIVE INDIRECT BRANCH
        # TODO: use self.inst.condition
        self.next_pc = self.pc + self.reg_bank.getRegister(self.inst.registerD)
        pass

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
        self.unhandled_inst()

    def inst45_ldrh(self):
        self.unhandled_inst()

    def inst46_ldrb(self):
        self.unhandled_inst()

    def inst47_ldrsh(self):
        self.unhandled_inst()

    def inst48_str(self):
        ld = self.reg_bank.getRegister(self.inst.registerM)
        lm = self.reg_bank.getRegister(self.inst.registerM)
        self.memory_ctrl.main_memory.set(lm + self.inst.immediate, ld)

    def inst49_ldr(self):
        lm = self.reg_bank.getRegister(self.inst.registerM)
        ld = self.memory_ctrl.main_memory.get(lm + self.inst.immediate)
        self.reg_bank.setRegister(self.inst.registerD, ld)

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
        pc = self.reg_bank.getRegister(Register.ProgramCounter)
        rd = self.alu.add_or_cmn(pc, self.inst.immediate << 1)
        self.reg_bank.setRegister(self.inst.registerD, rd)

    def inst57_add(self):
        sp = self.reg_bank.getRegister(Register.StackPointer)
        rd = self.alu.add_or_cmn(sp, self.inst.immediate << 1)
        self.reg_bank.setRegister(self.inst.registerD, rd)

    def inst58_cpxr(self):
        self.unhandled_inst()

    def inst59_sxth(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        rm = self.sig_ex.extend16(rm)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst60_sxtb(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        rm = self.sig_ex.extend8(rm)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst61_uxth(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst62_uxtb(self):
        rm = self.reg_bank.getRegister(self.inst.registerM)
        self.reg_bank.setRegister(self.inst.registerD, rm)

    def inst63_rev(self):
        self.unhandled_inst()

    def inst64_rev16(self):
        self.unhandled_inst()

    def inst65_mod(self):
        self.unhandled_inst()

    def inst66_revsh(self):
        self.unhandled_inst()

    def inst67_push(self):
        rd = self.reg_bank.getRegister(self.inst.registerD)
        self.memory_ctrl.push_user_stack(rd)

    def inst68_pop(self):
        value = self.memory_ctrl.pop_user_stack()
        self.reg_bank.setRegister(self.inst.registerD, value)

    def inst69_output(self):
        self.unhandled_inst()

    def inst70_pause(self):
        # time.sleep(1)
        pass

    def inst71_input(self):
        # value = int(input("INPUT: "))
        value = int(random() * 10)
        print(f"INPUT: {value} (random)")
        self.reg_bank.setRegister(self.inst.registerD, value)

    def inst72_swi(self):  # Software interruption
        print(f"Interruption: {SystemCall(self.inst.immediate)}")
        if SystemCall.ProgramCompletion == SystemCall(self.inst.immediate):
            self.running = False
            self.next_pc = -1

    def inst73_b(self):
        self.unhandled_inst()

    def inst74_nop(self):
        pass

    def inst75_halt(self):
        self.unhandled_inst()

    def inst76_pxr(self):
        self.unhandled_inst()

    def inst77_pushm(self):
        self.reg_bank.increment(Register.StackPointer, self.inst.immediate)

    def inst78_popm(self):
        self.reg_bank.decrement(Register.StackPointer, self.inst.immediate)

    def inst79_bl(self):  # RELATIVE INDIRECT BRANCH
        self.reg_bank.setRegister(Register.LinkRegister, self.pc)
        rd = self.reg_bank.getRegister(self.inst.registerD)
        self.next_pc = self.pc + rd
        pass

    def inst80_bx(self):  # ABSOLUTE INDIRECT BRANCH
        self.next_pc = self.reg_bank.getRegister(self.inst.immediate)
        pass
