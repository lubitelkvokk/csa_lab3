#!/usr/bin/python3
"""Транслятор Asm в машинный код.
"""

import sys
import re

from isa import Opcode, COMMANDS, WORD_SIZE, write_code, write_data, ProgramData

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
    for data in datasec.splitlines():
        data.strip()
        if data:
            label_name, arg = data.split(":")

            if '"' in arg:
                arg = arg.split('"')[1]
                data_labels[label_name.strip()] = arg
            else:
                data_labels[label_name.strip()] = arg.strip()

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
            arg = ""
            if len(token) == 1:
                cmd = token[0]
                code.append({"addr": pc, "cmd": COMMANDS[cmd]})
            else:
                cmd = token[0]
                arg = token[1]
                if "'" in arg:
                    arg = arg.replace("'", "")
                    arg = arg.replace("\\n", "\n")

                code.append({"addr": pc, "cmd": COMMANDS[cmd], "args": arg})

    return data_labels, text_labels, code


def translate_data_labels_to_addr(data_labels: dict[str]):
    translated_data_labels = {}
    addr_ptr = DATA_ADDR
    for label in data_labels.keys():
        translated_data_labels[label] = {"arg": data_labels[label], "addr": addr_ptr}
        element: str = data_labels[label]
        if re.search("res\([0-9]+\)", element):
            addr_ptr += int(element.split("(")[1].split(")")[0]) * WORD_SIZE
        elif not element.isdigit():
            # 1 символ - 1 машинное слово
            if element in data_labels:
                translated_data_labels[label]["arg"] = str(translated_data_labels[element]["addr"])
            for i in range(len(element)):
                addr_ptr += WORD_SIZE
        else:
            # Число - смещение на 1 машинное слово
            addr_ptr += WORD_SIZE
    return translated_data_labels


def translate_stage_2(data_labels: dict, text_labels: dict, code: list[ProgramData]):
    """Второй проход транслятора. В уже определённые инструкции подставляются
    адреса меток."""

    translated_data_labels = translate_data_labels_to_addr(data_labels)

    for instruction in code:
        if instruction["cmd"]["args_count"]:
            label = instruction["args"]
            if label.isdigit():
                instruction["args"] = int(label)
            elif label.strip() in data_labels:
                instruction["args"] = translated_data_labels[label]["addr"]
            elif label in text_labels:
                instruction["args"] = text_labels[label]

    return code, translated_data_labels


def translate(text):
    """Трансляция текста программы на Asm в машинный код.

    Выполняется в два прохода:

    1. Разбор текста на метки и инструкции.

    2. Подстановка адресов меток в операнды инструкции.
    """
    data_labels, text_labels, code = translate_stage_1(text)
    code, translated_data_labels = translate_stage_2(data_labels, text_labels, code)
    return code, translated_data_labels


def main(source, program_file, data_file):
    """Функция запуска транслятора. Параметры -- исходный и целевой файлы."""
    with open(source, encoding="utf-8") as f:
        source = f.read()

    code, translated_data_labels = translate(source)
    # for i in code:
    #     print(i)
    write_code(program_file, code)
    write_data(data_file, translated_data_labels)
    print("source LoC:", len(source.split("\n")), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 4, "Wrong arguments: translator_asm.py <input_file> <program_file> <data_file> "
    _, input_file, program_file, data_file = sys.argv
    # main(input_file, program_file, data_file)
    main("examples/prob1.asm", "program_file", "data_file")
