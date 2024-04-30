import json
from collections import namedtuple
from enum import Enum


class Opcode(str, Enum):
    ADD = "add"
    INC = "inc"
    DEC = "dec"
    INPUT = "input"
    OUTPUT = "output"
    ST = "st"
    LD = "ld"

    CMP = "cmp"
    JMP = "jmp"
    JZ = "jz"
    JGE = "jge"

    HLT = "hlt"

    def __str__(self):
        return str(self.value)


COMMANDS = {
    "add": {"opcode": Opcode.ADD, "args_count": 1},
    "inc": {"opcode": Opcode.INC, "args_count": 0},
    "dec": {"opcode": Opcode.DEC, "args_count": 0},
    "input": {"opcode": Opcode.INPUT, "args_count": 1},
    "output": {"opcode": Opcode.OUTPUT, "args_count": 1},
    "store": {"opcode": Opcode.ST, "args_count": 1},
    "load": {"opcode": Opcode.LD, "args_count": 1},
    "cmp": {"opcode": Opcode.CMP, "args_count": 1},
    "jmp": {"opcode": Opcode.JMP, "args_count": 1},
    "jz": {"opcode": Opcode.JZ, "args_count": 1},
    "jge": {"opcode": Opcode.JGE, "args_count": 1},
    "hlt": {"opcode": Opcode.HLT, "args_count": 0}
}


class Term(namedtuple("Term", "line pos symbol")):
    """Описание выражения из исходного текста программы.

    Сделано через класс, чтобы был docstring.
    """


def write_code(filename, code):
    with open(filename, "w", encoding="utf-8") as file:
        # Почему не: `file.write(json.dumps(code, indent=4))`?
        # Чтобы одна инструкция была на одну строку.
        buf = []
        for instr in code:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")


def read_code(filename):
    with open(filename, encoding="utf-8") as file:
        code = json.loads(file.read())

    for instr in code:
        # Конвертация строки в Opcode
        instr["opcode"] = Opcode(instr["opcode"])

        # Конвертация списка term в класс Term
        if "term" in instr:
            assert len(instr["term"]) == 3
            instr["term"] = Term(instr["term"][0], instr["term"][1], instr["term"][2])

    return code
