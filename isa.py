from enum import Enum
from typing import TypedDict, Union

WORD_SIZE = 4  # машинное слово 4 байта


class Opcode(str, Enum):
    ADD = 0x01
    MUL = 0x02
    INC = 0x03
    DEC = 0x04
    INPUT = 0x05
    OUTPUT = 0x06
    ST = 0x07
    LD = 0x08
    LDA = 0x09
    READ = 0x0A
    WRITE = 0x0B
    SETCNT = 0x0C
    SETADDR = 0x0D
    CMP = 0x0E
    CNTZ = 0x0F
    JMP = 0x10
    JZ = 0x11
    JGE = 0x12
    JE = 0x13
    HLT = 0x14

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
    "input": {"opcode": Opcode.INPUT, "args_count": 1},
    "output": {"opcode": Opcode.OUTPUT, "args_count": 1},
    "st": {"opcode": Opcode.ST, "args_count": 1},
    "ld": {"opcode": Opcode.LD, "args_count": 1},
    "lda": {"opcode": Opcode.LDA, "args_count": 1},
    "read": {"opcode": Opcode.READ, "args_count": 0},
    "write": {"opcode": Opcode.WRITE, "args_count": 0},
    "cmp": {"opcode": Opcode.CMP, "args_count": 1},
    "cntz": {"opcode": Opcode.CMP, "args_count": 0},
    "jmp": {"opcode": Opcode.JMP, "args_count": 1},
    "jz": {"opcode": Opcode.JZ, "args_count": 1},
    "je": {"opcode": Opcode.JE, "args_count": 1},
    "jge": {"opcode": Opcode.JGE, "args_count": 1},
    "hlt": {"opcode": Opcode.HLT, "args_count": 0},
    "setcnt": {"opcode": Opcode.SETCNT, "args_count": 0},
    "setaddr": {"opcode": Opcode.SETADDR, "args_count": 0}
}


def bytes_to_int(byte_arr: bytes) -> int:
    return (byte_arr[3] << 24) + (byte_arr[2] << 16) + (byte_arr[1] << 8) + byte_arr[0]


def int_to_bytes(value: int) -> bytearray:
    result = []
    for _ in range(4):
        result.append(value & 0xFF)
        value = value >> 8

    return bytearray(result)


def write_code(filename, code: list[ProgramData]):
    with open(filename, "wb") as file:  # Открываем файл в бинарном режиме
        int_codes: list[int] = []
        for instr in code:
            if type(instr["args"]) == int:
                int_codes.append(instr["args"] & 0x00FFFFFF)
            elif instr["args"]:
                int_codes.append(ord(instr["args"]) & 0x00FFFFFF)
            int_codes[-1] += int(instr["cmd"]["opcode"]) << 24
        for x in int_codes:
            file.write(int_to_bytes(x))  # Записываем байты в файл


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
        opcode: Opcode = Opcode(int(i >> 24))
        args = i & 0x00FFFFFF
        arg_count = 1 if args else 0  # Определяем количество аргументов
        program_data: ProgramData = {
            'addr': pc,
            'cmd': {'opcode': opcode, 'args_count': arg_count},
            'args': args
        }
        code.append(program_data)
    return code
