#!/usr/bin/python3
"""Транслятор Asm в машинный код.
"""

import sys
import re

from isa import Opcode, Term, write_code

TEXT_ADDR = 0
DATA_ADDR = 0


# Проблема в том, чтоб непонятно на каком этапе нужно записывать данные в память


def get_meaningful_token(line: str):
    """Извлекаем из строки содержательный токен (метка или инструкция), удаляем
    комментарии и пробелы в начале/конце строки.
    """
    return line.split(";", 1)[0].strip()


def translate_stage_1(text: str):
    datasec = text.split("section .data")[1].split("section .text")[0]
    textsec = text.split("section .text")[1]
    data_labels = {}
    code = []
    data_ptr = DATA_ADDR
    # data section in address space started with #00030000
    for data in datasec.splitlines():
        data.strip()
        if data:
            label_name, args = data.split(":")
            # labels[label_name] = data_ptr
            list_args = []
            if '"' in data:
                for arg in args.split('"'):
                    if arg and arg.strip() != ",":
                        list_args.append(arg)
            else:
                for arg in args.split(','):
                    list_args.append(arg.strip())
            data_labels[label_name] = list_args
            # возможно сделать обработку массива данных (разделение по запятой и тд) / корректный адрес для данных

    text_labels = {}
    for line_num, raw_line in enumerate(textsec.splitlines(), 1):
        token = get_meaningful_token(raw_line)
        if token == "":
            continue
        pc = len(code)
        if ":" in token:
            text_labels[token.split(":")[0]] = pc
        else:
            token = token.split()
            arg = ''
            if len(token) == 1:
                cmd = token[0]
            else:
                cmd = token[0]
                arg = token[1]
            code.append({"addr": pc, "cmd": Opcode(cmd).value, "args": arg})

    return data_labels, text_labels, code


def translate_data_labels_to_addr(data_labels: dict):
    translated_data_labels = {}
    addr_ptr = DATA_ADDR
    for label in data_labels.keys():
        translated_data_labels[label] = addr_ptr
        for element in data_labels[label]:
            if re.search('[a-zA-Z]', element):
                addr_ptr += len(element)
            else:
                addr_ptr += 1
    return translated_data_labels


def translate_stage_2(data_labels: dict, text_labels: dict, code: list[dict]):
    """Второй проход транслятора. В уже определённые инструкции подставляются
    адреса меток."""

    translated_data_labels = translate_data_labels_to_addr(data_labels)

    for instruction in code:
        if "args" in instruction and re.search('[a-z]', instruction["args"]):
            left_addition = ""
            right_addition = ""
            if "[" in instruction['args']:
                label = instruction['args'].split('[')[1].split(']')[0]
                left_addition = "["
                right_addition = "]"
            else:
                label = instruction['args']

            if data_labels.get(label):
                instruction['args'] = left_addition + str(translated_data_labels[label]) + right_addition
            elif text_labels.get(label):
                instruction["args"] = left_addition + str(text_labels[label]) + right_addition
            print(instruction["args"])
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
