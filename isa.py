from enum import Enum
from typing import TypedDict, Union

WORD_SIZE = 4  # машинное слово 4 байта


class Opcode(Enum):
    ADD = 0x01
    MUL = 0x02
    INC = 0x03
    DEC = 0x04
    DIV = 0x05
    MOD = 0x06

    INPUT = 0x07
    OUTPUT = 0x08
    ST = 0x09
    LD = 0x0A
    LDA = 0x0B
    READ = 0x0C
    WRITE = 0x0D
    SETCNT = 0x0E
    SETADDR = 0x0F
    CMP = 0x10
    CNTZ = 0x11
    JMP = 0x12
    JZ = 0x13
    JGE = 0x14
    JE = 0x15
    HLT = 0x16

    def __str__(self):
        return str(self.value)


class Command(TypedDict):
    opcode: Opcode
    args_count: int


class ProgramData(TypedDict):
    addr: int
    cmd: Command
    args: Union[int, str]


class LabelUnit(TypedDict):
    arg: str
    addr: int


class DataMemory(TypedDict):
    label: LabelUnit


COMMANDS = {
    "add": {"opcode": Opcode.ADD, "args_count": 1},
    "mul": {"opcode": Opcode.MUL, "args_count": 1},
    "inc": {"opcode": Opcode.INC, "args_count": 0},
    "dec": {"opcode": Opcode.DEC, "args_count": 0},
    "div": {"opcode": Opcode.DIV, "args_count": 1},
    "mod": {"opcode": Opcode.MOD, "args_count": 1},
    "input": {"opcode": Opcode.INPUT, "args_count": 1},
    "output": {"opcode": Opcode.OUTPUT, "args_count": 1},
    "st": {"opcode": Opcode.ST, "args_count": 1},
    "ld": {"opcode": Opcode.LD, "args_count": 1},
    "lda": {"opcode": Opcode.LDA, "args_count": 1},
    "read": {"opcode": Opcode.READ, "args_count": 0},
    "write": {"opcode": Opcode.WRITE, "args_count": 0},
    "cmp": {"opcode": Opcode.CMP, "args_count": 1},
    "cntz": {"opcode": Opcode.CNTZ, "args_count": 0},
    "jmp": {"opcode": Opcode.JMP, "args_count": 1},
    "jz": {"opcode": Opcode.JZ, "args_count": 1},
    "je": {"opcode": Opcode.JE, "args_count": 1},
    "jge": {"opcode": Opcode.JGE, "args_count": 1},
    "hlt": {"opcode": Opcode.HLT, "args_count": 0},
    "setcnt": {"opcode": Opcode.SETCNT, "args_count": 0},
    "setaddr": {"opcode": Opcode.SETADDR, "args_count": 0}
}


def bytes_to_int(byte_arr: bytes) -> int:
    return int.from_bytes(byte_arr, byteorder='little')


def int_to_bytes(value: int) -> bytes:
    return value.to_bytes(WORD_SIZE, byteorder='little')


def write_code(filename: str, code: list[ProgramData]):
    with open(filename, "wb") as file:
        int_codes: list[int] = []
        for instr in code:
            if type(instr["args"]) == int:
                args = instr["args"]
            elif type(instr["args"]) == str and instr["args"]:
                args = ord(instr["args"])
            int_code = (int(instr["cmd"]["opcode"].value) << 24) | (args & 0x00FFFFFF)
            int_codes.append(int_code)
        for x in int_codes:
            file.write(int_to_bytes(x))


def write_data(filename: str, data_labels: DataMemory):
    with open(filename, "wb") as file:
        for label in data_labels.keys():
            for chunk in data_labels[label]["arg"]:
                if type(chunk) == int:
                    arg = chunk
                elif type(chunk) == str and chunk:
                    arg = ord(chunk)
                file.write(int_to_bytes(arg))


def read_data(filename: str) -> list[int]:
    with open(filename, "rb") as file:
        int_data: list[int] = []
        while True:
            chunk = file.read(WORD_SIZE)
            if not chunk:  # Если достигнут конец файла
                break
            int_data.append(bytes_to_int(chunk))
    return int_data


def read_code(filename: str) -> list[ProgramData]:
    data = read_data(filename)
    code: list[ProgramData] = []
    for pc, i in enumerate(data):
        opcode_value = i >> 24
        opcode = Opcode(opcode_value)
        args = i & 0x00FFFFFF
        if opcode in {Opcode.INPUT, Opcode.OUTPUT, Opcode.ST, Opcode.LD, Opcode.LDA, Opcode.CMP, Opcode.JMP, Opcode.JZ,
                      Opcode.JE, Opcode.JGE}:
            args = chr(args)
            arg_count = 1
        else:
            arg_count = 0
        program_data: ProgramData = {
            'addr': pc,
            'cmd': {'opcode': opcode, 'args_count': arg_count},
            'args': args
        }
        code.append(program_data)
    return code

# Пример использования:
# code = [
#     {'addr': 0, 'cmd': {'opcode': Opcode.LDA, 'args_count': 1}, 'args': 4},
#     {'addr': 1, 'cmd': {'opcode': Opcode.SETADDR, 'args_count': 0}, 'args': ''},
#     {'addr': 2, 'cmd': {'opcode': Opcode.LD, 'args_count': 1}, 'args': 0},
#     {'addr': 3, 'cmd': {'opcode': Opcode.SETCNT, 'args_count': 0}, 'args': ''},
#     {'addr': 4, 'cmd': {'opcode': Opcode.OUTPUT, 'args_count': 1}, 'args': '1'},
#     {'addr': 5, 'cmd': {'opcode': Opcode.READ, 'args_count': 0}, 'args': ''}
# ]
#
# write_code("aboba.txt", code)
# print(read_code("aboba.txt"))
