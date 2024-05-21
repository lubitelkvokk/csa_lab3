from enum import Enum

from isa import ProgramData, Opcode


class Signal(Enum):
    LATCH_PM = 1

    SEL_MPC_ZERO = 1 << 1
    SEL_MPC_OPC = 1 << 1 | 1 << 2

    LATCH_MC = 1 << 3

    SEL_PC_NEXT = 1 << 4
    SEL_JMP = 1 << 4 | 1 << 7
    SEL_JZ = 1 << 4 | 1 << 6
    SEL_JE = 1 << 4 | 1 << 6 | 1 << 7
    SEL_JGE = 1 << 4 | 1 << 5

    SEL_AR_NEXT = 1 << 8
    SEL_AR_ADDR = 1 << 8 | 1 << 9

    LATCH_DATA_MEM = 1 << 10

    SEL_ACC_DATA_MEM = 1 << 11
    SEL_ACC_IO = 1 << 11 | 1 << 13
    SEL_ACC_VAL = 1 << 11 | 1 << 12

    LATCH_WRITE_IO = 1 << 14
    LATCH_BUFF = 1 << 15

    # 15 bit: flag, 16-18 bits: operations
    SEL_ALU_INC = 1 << 16
    SEL_ALU_DEC = 1 << 16 | 1 << 19
    SEL_ALU_ADD = 1 << 16 | 1 << 18
    SEL_ALU_SUB = 1 << 16 | 1 << 18 | 1 << 19
    SEL_ALU_MUL = 1 << 16 | 1 << 17
    SEL_ALU_DIV = 1 << 16 | 1 << 17 | 1 << 19
    SEL_ALU_MOD = 1 << 16 | 1 << 17 | 1 << 18

    SEL_DC_DEC = 1 << 20
    SEL_DC_ACC = 1 << 20 | 1 << 21

    SEL_CMP_ACC = 1 << 22
    SEL_CMP_DC = 1 << 22 | 1 << 23

    def __str__(self):
        return str(self.value)


microinstructions = {
    Opcode.LD: [
        0b0000000000000011,  # latch_pm, inc_pc
        0b0000000110100100,  # sel_ar_control_unit, latch_addr, sel_acc_data_mem, latch_data_mem
    ],

    Opcode.ADD: [
        0b1000001110000000,
        # sel_ar_control_unit, latch_br, sel_acc_data_mem, latch_alu_re, latch_alu_le, alu_add, sel_acc_alu
    ],

    Opcode.MUL: [
        0b1000011110000000,
        # sel_ar_control_unit, latch_br, sel_acc_data_mem, latch_alu_re, latch_alu_le, alu_mul, sel_acc_alu
    ],

    Opcode.INC: [
        0b0010100010000000,  # latch_alu_re, alu_inc, sel_acc_alu, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.DEC: [
        0b0010101010000000,  # latch_alu_re, alu_dec, sel_acc_alu, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.OUTPUT: [
        0b0100100000000010,  # write_io, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.INPUT: [
        0b0000111000000001,  # sel_acc_io, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.ST: [
        0b0010100110000000,
        # sel_ar_control_unit, latch_addr, latch_data_mem, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.LDA: [
        0b0000000110001001,  # sel_acc_control_unit, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.READ: [
        0b0110001010000000,
        # latch_addr, sel_acc_data_mem, dec_data_count, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.WRITE: [
        0b0010001010000000,
        # latch_addr, latch_data_mem, dec_data_count, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.SETCNT: [
        0b0000110000001001,  # sel_data_count_acc, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.SETADDR: [
        0b0000000010001001,  # sel_ar_control_unit, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.CMP: [
        0b1000110000001001,  # sel_acc_cmp, compare, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.CNTZ: [
        0b1100110000001001,  # sel_dc_cmp, compare, inc_pc, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.JMP: [
        0b0000000000001001,  # sel_pc_addr, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.JZ: [
        0b0010000000001001,  # sel_pc_addr, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.JGE: [
        0b0100000000001001,  # sel_pc_addr, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.JE: [
        0b0110000000001001,  # sel_pc_addr, latch_pm, latch_opcode, sel_mpc_opc, latch_mc
    ],

    Opcode.HLT: [
        0b0000000000000001,  # пример placeholder (нужны подробные микроинструкции)
    ],
}

opcodeToMp = {Opcode.ADD: 1,

              }


def assert_sel_error(sel: Signal):
    return "internal error, incorrect selector: {}".format(sel)


class DataPath:
    data_memory_size: int = None
    data_memory: list[int] = None
    data_address: int = None
    buff: int = None
    ports: list[list[int]] = None
    flag_zero: bool
    flag_lt: bool
    flag_gt: bool
    dc: int = None

    def __init__(self, data_memory_size):
        assert data_memory_size > 0, "Data_memory size should be non-zero"
        self.data_memory_size = data_memory_size
        self.data_memory = [0] * data_memory_size
        self.data_address = 0
        self.acc = 0
        self.buff = 0
        self.ports = [[0] * 256, [0] * 256]
        flag_zero = False
        flag_lt = False
        flag_gt = False
        self.dc = 0

    def sel_address_register(self, sel: Signal, addr: int):
        assert sel in {Signal.SEL_AR_NEXT, Signal.SEL_AR_ADDR}, \
            assert_sel_error(sel)
        if sel == Signal.SEL_AR_NEXT:
            self.data_address += 1
        elif sel == Signal.SEL_AR_ADDR:
            assert addr > 0, "address register mustn't be negative"
            self.data_address = addr

    def latch_data_mem(self):
        self.data_memory[self.data_address] = self.acc

    def latch_buff(self):
        self.buff = self.acc

    def sel_acc(self, sel: Signal, arg: int):
        assert sel in {Signal.SEL_ACC_IO,
                       Signal.SEL_ACC_VAL,
                       Signal.SEL_ACC_DATA_MEM}, \
            assert_sel_error(sel)
        if sel == Signal.SEL_ACC_IO:
            self.acc = self.ports[arg].pop(0)
        elif sel == Signal.SEL_ACC_VAL:
            self.acc = arg
        elif sel == Signal.SEL_ACC_DATA_MEM:
            self.acc = self.data_memory[self.data_address]

    def sel_alu(self, sel: Signal):
        assert sel in {Signal.SEL_ALU_ADD,
                       Signal.SEL_ALU_DEC,
                       Signal.SEL_ALU_DIV,
                       Signal.SEL_ALU_MOD,
                       Signal.SEL_ALU_SUB,
                       Signal.SEL_ALU_INC,
                       Signal.SEL_ALU_MUL}, \
            assert_sel_error(sel)
        if sel == Signal.SEL_ALU_INC:
            self.acc += 1
        elif sel == Signal.SEL_ALU_DEC:
            self.acc -= 1
        elif sel == Signal.SEL_ALU_SUB:
            self.acc = self.buff - self.acc
        elif sel == Signal.SEL_ALU_ADD:
            self.acc = self.buff + self.acc
        elif sel == Signal.SEL_ALU_MUL:
            self.acc = self.buff * self.acc
        elif sel == Signal.SEL_ALU_DIV:
            self.acc = self.buff // self.acc
        elif sel == Signal.SEL_ALU_MOD:
            self.acc = self.buff % self.acc

    def sel_dc(self, sel: Signal):
        assert sel in {Signal.SEL_DC_ACC,
                       Signal.SEL_DC_DEC}, \
            assert_sel_error(sel)
        if sel == Signal.SEL_DC_ACC:
            self.dc = self.acc
        elif sel == Signal.SEL_DC_DEC:
            self.dc -= 1

    def __compare(self, left: int, right: int):
        self.flag_lt = False
        self.flag_gt = False
        self.flag_zero = False
        if left > right:
            self.flag_gt = True
        elif left < right:
            self.flag_lt = True
        if left == 0:
            self.flag_zero = True

    def sel_cmp(self, sel: Signal, value: int):
        # decoded value from CU
        assert sel in {Signal.SEL_CMP_DC,
                       Signal.SEL_CMP_ACC}, \
            assert_sel_error(sel)
        if sel == Signal.SEL_CMP_DC:
            self.__compare(self.dc, value)
        elif sel == Signal.SEL_CMP_ACC:
            self.__compare(self.acc, value)


class ControlUnit:
    pc: int = None
    program_mem = list[ProgramData]
    mpc: int = None
    mcProgram = None
    datapath: DataPath = None
    _tick: int = None

    def __init__(self, program_mem: list[ProgramData], datapath: DataPath):
        self.program_mem = program_mem
        self.datapath = datapath
        self.mpc = 0
        self.mcProgram = mProgram
        self.pc = 0
        self._tick = 0

    def tick(self):
        self._tick += 1

    def sel_pc(self, sel_pc: Signal):
        assert sel_pc in {Signal.SEL_PC_NEXT,
                          Signal.SEL_JMP,
                          Signal.SEL_JGE,
                          Signal.SEL_JZ}, \
            assert_sel_error(sel_pc)
        addr: int
        if sel_pc == Signal.SEL_PC_NEXT:
            addr = self.program_mem[self.pc]["args"] + 1
        elif sel_pc == Signal.SEL_JMP:
            addr = self.program_mem[self.pc]["args"]
        elif sel_pc == Signal.SEL_JE:
            if not (self.datapath.flag_lt or self.datapath.flag_gt):
                addr = self.program_mem[self.pc]["args"]
        elif sel_pc == Signal.SEL_JGE:
            if self.datapath.flag_gt:
                addr = self.program_mem[self.pc]["args"]
        elif sel_pc == Signal.SEL_JZ:
            if self.datapath.flag_zero:
                addr = self.program_mem[self.pc]["args"]

        self.pc = addr

    def sel_mpc(self, sel: Signal):
        assert sel in {Signal.SEL_MPC_OPC,
                       Signal.SEL_MPC_ZERO}, assert_sel_error(sel)
        if sel == Signal.SEL_MPC_ZERO:
            self.mpc = 0
        elif sel == Signal.SEL_MPC_OPC:
            self.mpc =
