#!/usr/bin/python3
"""Транслятор Asm в машинный код.
"""

import sys

from isa import Opcode, Term, write_code

TEXT_ADDR = 0
DATA_ADDR = 300000


def get_meaningful_token(line):
    """Извлекаем из строки содержательный токен (метка или инструкция), удаляем
    комментарии и пробелы в начале/конце строки.
    """
    return line.split(";", 1)[0].strip()


def translate_stage_1(text):
    datasec = text.split("section .data")[1].split("section .text")[0]
    textsec = text.split("section .text")[1]

    labels = {}
    code = []
    data_ptr = DATA_ADDR
    # data section in address space started with #00030000
    for data in datasec.splitlines():
        data.strip()
        if data:
            label_name, args = data.split(":")
            labels[label_name] = data_ptr

            data_ptr += len(
                args)  # возможно сделать обработку массива данных (разделение по запятой и тд) / корректный адрес для данных

    for line_num, raw_line in enumerate(text.splitlines(), 1):
        token = get_meaningful_token(raw_line)
        if token == "":
            continue
        print(token)
        pc = len(code)
        cmd, arg = token.split()
        # code.append({Opcode.})
    return

def translate_stage_2(labels, code):
    """Второй проход транслятора. В уже определённые инструкции подставляются
    адреса меток."""
    for instruction in code:
        if "arg" in instruction:
            label = instruction["arg"]
            assert label in labels, "Label not defined: " + label
            instruction["arg"] = labels[label]
    return code


def translate(text):
    """Трансляция текста программы на Asm в машинный код.

    Выполняется в два прохода:

    1. Разбор текста на метки и инструкции.

    2. Подстановка адресов меток в операнды инструкции.
    """
    labels, code = translate_stage_1(text)
    code = translate_stage_2(labels, code)

    # ruff: noqa: RET504
    return code


def main(source, target):
    """Функция запуска транслятора. Параметры -- исходный и целевой файлы."""
    with open(source, encoding="utf-8") as f:
        source = f.read()

    code = translate(source)

    write_code(target, code)
    print("source LoC:", len(source.split("\n")), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator_asm.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)
