"""Golden тесты транслятора ассемблера и машины.

Конфигурационнфе файлы: "golden/*_asm.yml"
"""

import contextlib
import io
import logging
import os
import tempfile

import isa
import machine
import pytest
import translator


@pytest.mark.golden_test("golden/*_asm.yml")
def test_translator_asm_and_machine(golden, caplog):
    """Почти полная копия test_translator_and_machine из golden_bf_test. Детали
    см. там."""
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.asm")
        input_stream = os.path.join(tmpdirname, "input.txt")
        target_code = os.path.join(tmpdirname, "target_code.o")
        target_data = os.path.join(tmpdirname, "target_data.o")
        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["in_source"])
        with open(input_stream, "w", encoding="utf-8") as file:
            file.write(golden["in_stdin"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main(source, target_code, target_data)
            print("============================================================")
            machine.main(target_code, target_data, input_stream)

        with open(target_code, encoding="utf-8") as file:
            code = file.read()

        with open(target_data, encoding="utf-8") as file:
            data = file.read()

        assert code == golden.out["out_code"]
        assert data == golden.out["out_data"]
        assert stdout.getvalue() == golden.out["out_stdout"]
        assert caplog.text == golden.out["out_log"]
