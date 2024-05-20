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

    LATCH_ALU_LE = 1 << 15
    LATCH_ALU_RE = 1 << 16
    # 16 bit: flag, 17-19 bits: operations
    SEL_ALU_INC = 1 << 17
    SEL_ALU_DEC = 1 << 17 | 1 << 20
    SEL_ALU_ADD = 1 << 17 | 1 << 19
    SEL_ALU_SUB = 1 << 17 | 1 << 19 | 1 << 20
    SEL_ALU_MUL = 1 << 17 | 1 << 18
    SEL_ALU_DIV = 1 << 17 | 1 << 18 | 1 << 20
    SEL_ALU_MOD = 1 << 17 | 1 << 18 | 1 << 19

    SEL_DC_DEC = 1 << 21
    SEL_DC_ACC = 1 << 21 | 1 << 22

    SEL_CMP_ACC = 1 << 23
    SEL_CMP_DC = 1 << 23 | 1 << 24


    def __str__(self):
        return str(self.value)


SIGNALS = {
    LATCH_PM:
}


class DataPath:
    data_memory_size: int = None
    data_memory: list[int] = None
    address_register: int = None
    buffer_register: int = None

    def __init__(self, data_memory_size):
        assert data_memory_size > 0, "Data_memory size should be non-zero"
        self.data_memory_size = data_memory_size
        self.data_memory = [0] * data_memory_size
        self.data_address = 0
        self.acc = 0
        self.buffer_register = 0

    def latch_address_register(self, sel_addr:):
        self.address_register = addr
