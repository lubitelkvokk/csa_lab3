from enum import Enum


class Signal(Enum):
    LATCH_PM = 1
    LATCH_OPCODE = 1 < 1

    SEL_MPC_ZERO = 1 << 2
    SEL_MPC_OPC = 1 << 2 | 1 << 3

    LATCH_MC = 1 << 4

    SEL_PC_NEXT = 1 << 5
    SEL_PC_VAL = 1 << 5 | 1 << 6

    SEL_AR_NEXT = 1 << 7
    SEL_AR_ADDR = 1 << 7 | 1 << 8

    LATCH_DATA_MEM = 1 << 9

    SEL_ACC_DATA_MEM = 1 << 10
    SEL_ACC_IO = 1 << 10 | 1 << 12
    SEL_ACC_VAL = 1 << 9 | 1 << 11

    LATCH_WRITE_IO = 1 << 13
    LATCH_BUFF = 1 << 14

    # 15 bit: flag, 16-18 bits: operations
    SEL_ALU_INC = 1 << 15
    SEL_ALU_DEC = 1 << 15 | 1 << 18
    SEL_ALU_ADD = 1 << 15 | 1 << 17
    SEL_ALU_SUB = 1 << 15 | 1 << 17 | 1 << 18
    SEL_ALU_MUL = 1 << 15 | 1 << 16
    SEL_ALU_DIV = 1 << 15 | 1 << 16 | 1 << 18
    SEL_ALU_MOD = 1 << 15 | 1 << 16 | 1 << 17

    SEL_DC_DEC = 1 << 19
    SEL_DC_ACC = 1 << 19 | 1 << 20

    SEL_CMP_ACC = 1 << 21
    SEL_CMP_DC = 1 << 21 | 1 << 22

    def __str__(self):
        return str(self.value)


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
        flag_zero = 0
        flag_lt = 0
        flag_gt = 0
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
                       Signal.SEL_ALU_MUL}
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
                       Signal.SEL_DC_DEC}
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
                       Signal.SEL_CMP_ACC}
        assert_sel_error(sel)
        if sel == Signal.SEL_CMP_DC:
            self.__compare(self.dc, value)
        elif sel == Signal.SEL_CMP_ACC:
            self.__compare(self.acc, value)
