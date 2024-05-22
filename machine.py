import logging
import sys
from enum import Enum
from typing import Union

from isa import ProgramData, read_code, read_data, DataMemory
from microcode import *


def assert_sel_error(sel: Signal):
    return "internal error, incorrect selector: {}".format(sel)


class DataPath:
    # data_memory_size: int = None
    data_memory: list[int] = None
    data_address: int = None
    buff: int = None
    ports: list[list[int]] = None
    flag_zero: bool
    flag_lt: bool
    flag_gt: bool
    dc: int = None

    def __init__(self, data: list[int], input_data: list[Union[str, int]]):
        # assert data_memory_size > 0, "Data_memory size should be non-zero"
        # self.data_memory_size = data_memory_size
        self.data_memory = data
        self.data_address = 0
        self.acc = 0
        self.buff = 0
        self.ports = [[0] * 256, [0] * 256]
        if input_data:
            self.ports[0] = input_data
        self.flag_zero = False
        self.flag_lt = False
        self.flag_gt = False
        self.dc = 0

    def sel_address_register(self, sel: Signal, addr: int = None):
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

    def sel_acc(self, sel: Signal, arg: int = None):
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
        self.mcProgram = microprogram_addresses
        self.pc = 0
        self._tick = 0

    def tick(self):
        self._tick += 1

    def current_tick(self):
        return self._tick

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
            self.mpc = microprogram_addresses[
                self.program_mem[self.pc]["cmd"]["opcode"]]

    def exec_mp(self):
        microinstruction_count = microprogram_lengths[self.mpc]
        arg = self.program_mem[self.pc]["args"]
        for microinstruction in microinstructions[self.mpc:self.mpc + microinstruction_count]:
            if microinstruction & Signal.SEL_MPC_ZERO.value:
                self.sel_mpc(Signal.SEL_MPC_ZERO)
            if microinstruction & Signal.SEL_MPC_OPC.value:
                self.sel_mpc(Signal.SEL_MPC_OPC)
            if microinstruction & Signal.SEL_PC_NEXT.value:
                self.sel_pc(Signal.SEL_PC_NEXT)
            if microinstruction & Signal.SEL_JMP.value:
                self.sel_pc(Signal.SEL_JMP)
            if microinstruction & Signal.SEL_JZ.value:
                self.sel_pc(Signal.SEL_JZ)
            if microinstruction & Signal.SEL_JGE.value:
                self.sel_pc(Signal.SEL_JGE)
            if microinstruction & Signal.SEL_JE.value:
                self.sel_pc(Signal.SEL_JE)
            if microinstruction & Signal.SEL_AR_NEXT.value:
                self.datapath.sel_address_register(Signal.SEL_AR_NEXT)
            if microinstruction & Signal.SEL_AR_ADDR.value:
                self.datapath.sel_address_register(Signal.SEL_AR_ADDR, arg)
            if microinstruction & Signal.LATCH_DATA_MEM.value:
                self.datapath.latch_data_mem()
            if microinstruction & Signal.SEL_ACC_DATA_MEM.value:
                self.datapath.sel_acc(Signal.SEL_ACC_DATA_MEM)
            if microinstruction & Signal.SEL_ACC_IO.value:
                self.datapath.sel_acc(Signal.SEL_ACC_IO, arg)
            if microinstruction & Signal.SEL_ACC_VAL.value:
                self.datapath.sel_acc(Signal.SEL_ACC_VAL, arg)
            if microinstruction & Signal.LATCH_WRITE_IO.value:
                self.datapath.latch_write_io()
            if microinstruction & Signal.LATCH_BUFF.value:
                self.datapath.latch_buff()
            if microinstruction & Signal.SEL_ALU_INC.value:
                self.datapath.sel_alu(Signal.SEL_ALU_INC)
            if microinstruction & Signal.SEL_ALU_DEC.value:
                self.datapath.sel_alu(Signal.SEL_ALU_DEC)
            if microinstruction & Signal.SEL_ALU_ADD.value:
                self.datapath.sel_alu(Signal.SEL_ALU_ADD)
            if microinstruction & Signal.SEL_ALU_SUB.value:
                self.datapath.sel_alu(Signal.SEL_ALU_SUB)
            if microinstruction & Signal.SEL_ALU_MUL.value:
                self.datapath.sel_alu(Signal.SEL_ALU_MUL)
            if microinstruction & Signal.SEL_ALU_DIV.value:
                self.datapath.sel_alu(Signal.SEL_ALU_DIV)
            if microinstruction & Signal.SEL_ALU_MOD.value:
                self.datapath.sel_alu(Signal.SEL_ALU_MOD)
            if microinstruction & Signal.SEL_DC_DEC.value:
                self.datapath.sel_dc(Signal.SEL_DC_DEC)
            if microinstruction & Signal.SEL_DC_ACC.value:
                self.datapath.sel_dc(Signal.SEL_DC_ACC)
            if microinstruction & Signal.SEL_CMP_ACC.value:
                self.datapath.sel_cmp(Signal.SEL_CMP_ACC, arg)
            if microinstruction & Signal.SEL_CMP_DC.value:
                self.datapath.sel_cmp(Signal.SEL_CMP_DC, arg)
            self.tick()

    def __repr__(self):
        state_repr = "TICK: {:3} PC: {:3} ADDR: {:3} MEM_OUT: {} ACC: {}".format(
            self._tick,
            self.pc,
            self.datapath.data_address,
            self.datapath.data_memory[self.datapath.data_address],
            self.datapath.acc,
        )

        instr = self.program_mem[self.pc]
        opcode = instr["cmd"]["opcode"]
        instr_repr = str(opcode)

        instr_repr += " {}".format(instr["args"])

        return "{} \t{}".format(state_repr, instr_repr)


def simulation(code: list[ProgramData], data: list[int],
               input_tokens: Union[str, int], limit: int):
    data_path = DataPath(data, input_tokens)
    control_unit = ControlUnit(code, data_path)
    instr_counter = 0

    logging.debug("%s", control_unit)
    try:
        while instr_counter < limit:
            control_unit.exec_mp()
            instr_counter += 1
            control_unit.tick()
            logging.debug("%s", control_unit)
    except EOFError:
        logging.warning("Input buffer is empty!")
    except StopIteration:
        pass

    if instr_counter >= limit:
        logging.warning("Limit exceeded!")
    logging.info("output_buffer: %s", repr("".join(*data_path.ports[0])))
    return "".join(*data_path.ports[1]), instr_counter, control_unit.current_tick()


def main(code_file, data_file, input_file):
    code = read_code(code_file)
    data = read_data(data_file)
    with open(input_file, encoding="utf-8") as file:
        input_text = file.read()
        input_token = []
        for char in input_text:
            input_token.append(char)

    output, instr_counter, ticks = simulation(code, data, input_token, 1000)

    print("".join(output))
    print("ticks:", ticks)


if __name__ == "__main__":
    assert len(sys.argv) == 4, "Wrong arguments: machine.py <data_file> <code_file> <input_file>"
    _, data_file, code_file, input_file = sys.argv
    main(code_file, data_file, input_file)
