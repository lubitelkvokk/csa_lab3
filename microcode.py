from enum import Enum

from isa import Opcode


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


# Объединенные микроинструкции
microinstructions = [
    # start
    Signal.SEL_MPC_ZERO.value | Signal.LATCH_MC.value | Signal.SEL_PC_NEXT.value,  # latch_mpc_zero, latch_mc, sel_pc

    # ld
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_PM.value,  # sel_ar_addr, latch_addr
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_PC_NEXT.value,  # sel_acc_data_mem, sel_pc_next

    # st
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_PM.value,  # sel_ar_addr, latch_addr
    Signal.LATCH_DATA_MEM.value | Signal.SEL_PC_NEXT.value,  # latch_data_mem, sel_pc_next

    # lda
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ACC_VAL.value | Signal.SEL_PC_NEXT.value,  # sel_acc_val, sel_pc_next

    # write
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_DATA_MEM.value | Signal.SEL_DC_DEC.value,  # latch_data_mem, sel_dc_dec
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # read
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_DATA_MEM.value | Signal.SEL_DC_DEC.value,  # latch_data_mem, sel_dc_dec
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # setcnt
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_DC_ACC.value | Signal.SEL_PC_NEXT.value,  # sel_dc_acc, sel_pc_next

    # setaddr
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.SEL_PC_NEXT.value,  # sel_ar_addr, sel_pc_next

    # jmp
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JMP.value,  # sel_jmp

    # jz
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JZ.value,  # sel_jz

    # jge
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JGE.value,  # sel_jge

    # je
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_JE.value,  # sel_je

    # inc
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ALU_INC.value | Signal.SEL_PC_NEXT.value,  # sel_alu_inc, sel_pc_next

    # dec
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ALU_DEC.value | Signal.SEL_PC_NEXT.value,  # sel_alu_dec, sel_pc_next

    # output
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.LATCH_WRITE_IO.value | Signal.SEL_PC_NEXT.value,  # latch_write_io, sel_pc_next

    # input
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_ACC_IO.value | Signal.SEL_PC_NEXT.value,  # sel_acc_io, sel_pc_next

    # add
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_BUFF.value,  # latch_ar_addr, latch_buff
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_ALU_ADD.value,  # sel_acc_data_mem, sel_alu_add
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # sub
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_BUFF.value,  # latch_ar_addr, latch_buff
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_ALU_SUB.value,  # sel_acc_data_mem, sel_alu_sub
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # mul
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_BUFF.value,  # latch_ar_addr, latch_buff
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_ALU_MUL.value,  # sel_acc_data_mem, sel_alu_mul
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # div
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_BUFF.value,  # latch_ar_addr, latch_buff
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_ALU_DIV.value,  # sel_acc_data_mem, sel_alu_div
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # mod
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_AR_ADDR.value | Signal.LATCH_BUFF.value,  # latch_ar_addr, latch_buff
    Signal.SEL_ACC_DATA_MEM.value | Signal.SEL_ALU_MOD.value,  # sel_acc_data_mem, sel_alu_mod
    Signal.SEL_PC_NEXT.value,  # sel_pc_next

    # cmp
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_CMP_ACC.value | Signal.SEL_PC_NEXT.value,  # sel_cmp_acc, sel_pc_next

    # cntz
    Signal.LATCH_PM.value | Signal.SEL_MPC_OPC.value | Signal.LATCH_MC.value,  # latch_pm, sel_mpc_opc, latch_mc
    Signal.SEL_CMP_DC.value | Signal.SEL_PC_NEXT.value,  # sel_cmp_dc, sel_pc_next
]

# Словарь сопоставления Opcode к адресу в массиве микроинструкций
microprogram_addresses = {
    Opcode.START: 0,
    Opcode.LD: 1,
    Opcode.ST: 4,
    Opcode.LDA: 7,
    Opcode.WRITE: 9,
    Opcode.READ: 12,
    Opcode.SETCNT: 15,
    Opcode.SETADDR: 17,
    Opcode.JMP: 19,
    Opcode.JZ: 21,
    Opcode.JGE: 23,
    Opcode.JE: 25,
    Opcode.INC: 27,
    Opcode.DEC: 29,
    Opcode.OUTPUT: 31,
    Opcode.INPUT: 33,
    Opcode.ADD: 35,
    Opcode.SUB: 38,
    Opcode.MUL: 41,
    Opcode.DIV: 44,
    Opcode.MOD: 47,
    Opcode.CMP: 50,
    Opcode.CNTZ: 52,
}

microprogram_lengths = {
    Opcode.START: 1,
    Opcode.LD: 3,
    Opcode.ST: 3,
    Opcode.LDA: 2,
    Opcode.WRITE: 3,
    Opcode.READ: 3,
    Opcode.SETCNT: 2,
    Opcode.SETADDR: 2,
    Opcode.JMP: 1,
    Opcode.JZ: 1,
    Opcode.JGE: 1,
    Opcode.JE: 1,
    Opcode.INC: 2,
    Opcode.DEC: 2,
    Opcode.OUTPUT: 2,
    Opcode.INPUT: 2,
    Opcode.ADD: 4,
    Opcode.SUB: 4,
    Opcode.MUL: 4,
    Opcode.DIV: 4,
    Opcode.MOD: 4,
    Opcode.CMP: 2,
    Opcode.CNTZ: 2,
}