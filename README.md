# csa_lab3

## Михайлов Павел P3217

## Базовый вариант

```
asm | acc | harv | mc -> hw | instr | binary -> struct | stream | port | pstr | prob1 | cache
```

## Язык программирование

``` ebnf
<program> ::= <program> <line> | <line>

<line> ::=  <opcode_without_arg>
          | <opcode_transfer> " " <term>
          | <opcode_arg> " (" <term> ")"
          | <opcode_arg> " #" <number>
          | <opcode_arg> " " <term>
          | <label>
          | <label> " number " <number>
          | <label> ' string ' '"' <term> '"'
          | "section ." <term>
          | "\n"

<label> ::= <name> ":" (" ")* | <name> ":" (" ")* "\n"

<opcode_without_arg> ::= "hlt"
                       | "inc"
                       | "dec"
                       | "read"
                       | "write"
                       | "cntz"
                       | "setcnt"
                       | "setaddr"

<opcode_arg> ::= ("add" | "mul" | "div" | "mod" | "cmp" | "input" | "output" | "ld" | "lda" | "st")
               " " <term>

<opcode_transfer> ::= ("jmp" | "jge" | "jz" | "je")
                    " " <label>

<term> ::= <number> | <letter> | '"' <string> '"'
<letter> ::= [a-z] | [A-Z]
<number> ::= [0-9] <number>*
<string> ::= <letter>*


<name> ::= <letter> (<letter> | <number>)*

```

- `ld`: загружает данные в acc из ячейки памяти (по метке)
- `lda`: загружает в acc указанное значение
- `st`: загружает данные из acc в указанный адрес (по метке)
- `write`: [data_addr] <- [acc], [data_counter] <- [data_counter] - 1, ar <- ar + 1
- `read`:  [data_addr] -> [acc], [data_counter] <- [data_counter] - 1, ar <- ar + 1
- `jmp`: безусловный переход по указанному адресу
- `je` - условный переход по указанному адресу, если после сравнения флаги GT и LT были заполнены нулями
- `jz`: условный переход по указанному адресу, если после сравнения флаг Z был заполнен единицей
- `jge`: условный переход по указанному адресу, если после сравнения флаг GT был заполнен единицей
- `inc`: инкремент аккумулятора. [acc] <- [acc] + 1
- `dec`: декремент аккумулятора. [acc] <- [acc] - 1
- `input`: получение ввода с определенного порта (указывается номер порта)
- `output`: указание порта на вывод (выводится значение из acc)
- `add`: сумма указанного числа с [acc]
- `mul`: умножение указанного числа с [acc]
- `div`: деление значения в acc на указанное число
- `mod`: остаток от деления значения в acc на указанное число
- `hlt`: остановка процессора
- `cntz`: проверка, является ли регистр data_count равен нулю, установка соответствущего флага
- `setcnt`: загрузить значение из аккумулятора в регистр [data_count]
- `сmp`: сравнение значения из аккумулятора с указанным значением
- `setaddr`: устанавливает значение из [acc] в [ar]

### Hello, world

``` asm
section .data
message_size: 13
message: "Hello, world!"

section .text
_start:
    ld message_size
    setcnt
    lda message
    setaddr
    loop:
        read
        output 1
        cntz
        jz exit
        jmp loop
    exit:
        hlt
```

### cat

``` asm
section .data

section .text
_start:
    loop:
        input 0
        cmp '\n'
        je exit
        output 1
        jmp loop
    exit:
        hlt
```

### Hello, Alice!

``` asm
section .data
message_size: 19
message: "What, is your name?"
endl: 10
hello_size: 7
hello: "Hello, "
answer_size: 0
answer: res(15)
answer_end: "!"
answer_ptr: answer


section .text
_start:
    ld message_size
    setcnt
    lda message
    setaddr
    loop_print1:
        read
        output 1
        cntz
        jz end_loop_print1
        jmp loop_print1

    end_loop_print1:
      ld endl
      output 1
      lda answer
      setaddr

    loop_write:
        input 0
        write
        cmp '\n'
        je end_write
        ld answer_size
        inc
        st answer_size
        ld answer_ptr
        add 4
        st answer_ptr
        setaddr
        jmp loop_write

    end_write:

    ld hello_size
    setcnt
    lda hello
    setaddr
    loop_print2:
        read
        output 1
        cntz
        jz loop_print2_end
        jmp loop_print2

    loop_print2_end:

    ld answer_size
    setcnt
    lda answer
    setaddr
    loop_print3:
        read
        output 1
        cntz
        jz print_answer_end
        jmp loop_print3

    print_answer_end:
        ld answer_end
        output 1
    exit:
        hlt
```

### prob1

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these
multiples is 23.
**Find the sum of all the multiples of 3 or 5 below 1000.**

``` asm
section .data
    result: 0
    count: 0

section .text
_start:

main_loop:
    ld result
    inc
    st result
    cmp 1000
    jge exit

    mod3:
    ld result
    mod 3
    cmp 0
    je div3_found

    mod5:
    ld result
    mod 5
    cmp 0
    je div5_found
    jmp main_loop

div3_found:
    ld count
    inc
    st count
    jmp main_loop

div5_found:
    ld count
    inc
    st count
    jmp main_loop

exit:
    hlt
```

## Организация памяти


- Гарвардская архитектура
- Размер машинного слова
    - Память данных - 32 бит. Один символ - 1 машинное слово.
    - Память команд - 32 бит.
- Адресация
    - Прямая (ld <label>)
    - Косвенная. Аналог только для команд write/read, где мы заранее помещаем значение адреса в ar и производим
      последовательное чтение.

## Система команд


- Особенности процессора
    - Машинное слово - беззнаковое 32 битное;
    - Доступ к памяти осуществляется через address register;
    - Устройство ввода/вывода: port-mapped;
    - Поток управления:
        - Инкрементирование PC,
        - Условный/безусловный переход,
        - Адрес из аккумулятора при выполнении команды setaddr

| Номер | Команда | Последовательность сигналов               |
|-------|---------|-------------------------------------------|
| 0     | start   | latch_mpc_zero, latch_mc, sel_pc          |
| 1     | ld      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_ar_addr                               |
|       |         | sel_acc_data_mem, sel_pc_next             |
| 2     | st      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_ar_addr                               |
|       |         | latch_data_mem, sel_pc_next               |
| 3     | lda     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_acc_val, sel_pc_next                  |
| 4     | write   | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_data_mem, sel_dc_dec                |
|       |         | sel_ar_next, sel_pc_next                  |
| 5     | read    | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_acc_data_mem, sel_dc_dec              |
|       |         | sel_ar_next, sel_pc_next                  |
| 6     | setcnt  | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_dc_acc, sel_pc_next                   |
| 7     | setaddr | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_ar_addr, sel_pc_next                  |
| 8     | jmp     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_jmp                                   |
| 9     | jz      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_jz                                    |
| 10    | jge     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_jge                                   |
| 11    | je      | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_je                                    |
| 12    | inc     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_alu_inc, sel_pc_next                  |
| 13    | dec     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_alu_dec, sel_pc_next                  |
| 14    | output  | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_write_io, sel_pc_next               |
| 15    | input   | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_acc_io, sel_pc_next                   |
| 16    | add     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_add |
|       |         | sel_pc_next                               |
| 17    | sub     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_sub |
|       |         | sel_pc_next                               |
| 18    | mul     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_mul |
|       |         | sel_pc_next                               |
| 19    | div     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_div |
|       |         | sel_pc_next                               |
| 20    | mod     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_mod |
|       |         | sel_pc_next                               |
| 21    | cmp     | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_cmp_acc, sel_pc_next                  |
| 22    | cntz    | latch_pm, sel_mpc_opc, latch_mc           |
|       |         | sel_cmp_dc, sel_pc_next                   |

Описание:

| Номер бита | Сигнал         | Описание                                                                                                             |
|------------|----------------|----------------------------------------------------------------------------------------------------------------------|
| 0          | latch_pm       | Выбрать в памяти команд значение по указанному Program counter                                                       |
| 1          | sel_mpc        | Выбрать микропрограмму по значению Opcode                                                                            |
| 2          |                | 100 - загрузка нуля(при запуске процессора), 110 - загрузка по Opcode                                                |
| 3          |                | 101 - инкремент                                                                                                      |
| 4          | latch_mc       | После выбранного номера микропрограммы защелкиваем для выполнения соответствующей последовательности микроинструкций |
| 5          | sel_pc         | Выбираем следующее значение Program Counter.                                                                         |
| 6          |                | 1000 - SEL_NEXT, 1001 - SEL_JMP,                                                                                     |
| 7          |                | 1010 - SEL_JZ (в зависимости от флага),                                                                              |
| 8          |                | 1011 - SEL_JE, 1100 - SEL_JGE                                                                                        |
| 9          | sel_ar         | Выбор адреса для последующего обращения к памяти (запись/чтение).                                                    |
| 10         |                | 100 - SEL_NEXT, 101 - SEL_ADDR(декодированное значение из CU)                                                        |
| 11         |                | 110 - SEL_AR_ACC                                                                                                     |
| 12         | latch_data_mem | Выбор значения из аккумулятора в память по адресу в AR                                                               |
| 13         | sel_acc        | Запись в аккумулятор из указанного источника.                                                                        |
| 14         |                | 100 - SEL_ACC_DATA_MEM, 101 - SEL_ACC_IO(из портов),                                                                 |
| 15         |                | 110 - SEL_ACC_VAL(декодированное значение из CU)                                                                     |
| 16         | write_io       | Запись из аккумулятора в указанный порт                                                                              |
| 17         | latch_buff     | Запись из аккумулятора в буферный регистр                                                                            |
| 18         | sel_alu        | Вычисление в алу и запись результата в аккумулятор.                                                                  |
| 19         |                | 1000 - SEL_ALU_INC, 1001 - SEL_ALU_DEC, 1010 - SEL_ALU_ADD,                                                          |
| 20         |                | 1011 - SEL_ALU_SUB, 1100 - SEL_ALU_MUL, 1101 - SEL_ALU_DIV,                                                          |
| 21         |                | 1110 - SEL_ALU_MOD                                                                                                   |
| 22         | sel_dc         | Выбор следующего значения для Data Count регистра.                                                                   |
| 23         |                | 10 - SEL_DC_DEC(декремент) 11 - SEL_DC_ACC (из аккумулятора)                                                         |
| 24         | sel_cmp        | Выбор левого входа для сравнения с декодированным значением из CU.                                                   |
| 25         |                | 10 - SEL_CMP_ACC(значение из аккумулятора), 11 - SEL_CMP_DC(значение из data counter)                                |

## Транслятор

Интерфейс командной строки: `python3 translator.py <input_file> <target_program_file> <target_data_file>`

Первый аргумент - путь до файла с исходным кодом,
второй аргумент - путь до файла, куда будет записан код в бинарном виде,
третий аргумент - путь до файла, куда будут записаны данные в бинарном виде

Трансляция секции .data:

- translate_stage1:
    - Разделяет данные на токены, возвращает данные
      в формате <label>:<addr>, а код в формате {<addr>, <command>, <args>}.
      Команды, могут не иметь аргументов, тогда <args> отсутствует.
      command представлен Enum. Также на этой стадии вернуться текстовые метки,
      которым будет соответствовать значение pc на котором они встретились.

- translate_data_labels_to_addr:
    - Вычисляет адреса для меток в памяти, выделяет необходимое адресное пространство для res(<number>)
- translate_stage2:
    - Вставляет адреса меток данных и команд в аргументы инструкций.

Правила:

- .data и .text должны присутствовать в программе, даже если они пустые
- Одна строка - одна инструкция

## Модель процессора

Интерфейс командной строки: `python3 machine.py <data_file> <code_file> <input_file>`

DataPath
![DataPath.png](schemes%2FDataPath.png)

Регистры:

- `ACC` - аккумулятор
- `Address register` - регистр для адреса памяти данных
- `Data count` - регистр счетчика выполнения чтения/записи
- `Buffer register` - применяется как второй вход в ALU

Сигналы:

- Защелки
    - `write_io` - записать значение из acc в порт вывода
    - `latch_data_mem` - записать по указанному в ar адресу данные из acc
    - `latch_br` - защелкнуть buffer register

- Мультиплексор:
    - `sel_ar` - выбрать `sel_ar_next`, `sel_ar_addr`, `sel_ar_acc`
    - `sel_dc` - выбрать `sel_dc_next`, `sel_dc_acc`
    - `sel_acc` - выбрать `sel_acc_data_mem`, `sel_acc_io`, `sel_acc_val`, `sel_alu_*`

## Control Unit

![ControlUnit.png](schemes%2FControlUnit.png)

Регистры:

- `PC` - program counter - регистр, являющийся указателем на текущую инструкцию в Program Memory
- `mPC` - регистр, являющийся указателем на текущую микропрограммную инструкцию
- `SCP` - регистр, указывающий на верхушку стека вызовов

- Сигналы:
    - Защелки:
        - `latch_pm`
        - `latch_mc`
    - Мультиплексор:
        - sel_mpc - `sel_mpc_zero`, `sel_mpc_opcode`, `sel_mpc_next`
        - sel_pc - `sel_pc_next`, `sel_pc_jmp`, `sel_pc_jz`, `sel_je`, `sel_jge`

## Тестирование

Golden - тестирование.

Директория с тестами: `./golden`

Директория с генерацией логов тестов для отдельного просмотра-изменения `./logs`

Исполняемый файл: `golden_test.py`

## CI

```
name: Python CI

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run tests and collect coverage
        run: |
          poetry run coverage run -m pytest .
          poetry run coverage report -m
        env:
          CI: true

  lint:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Check code formatting with Ruff
        run: poetry run ruff format --check .

      - name: Run Ruff linters
        run: poetry run ruff check .
```

## Отчёт на примере Hello, world!

Исходный код:

```nasm
section .data
message_size: 19
message: "What, is your name?"
endl: 10
hello_size: 7
hello: "Hello, "
answer_size: 0
answer: res(15)
answer_end: "!"
answer_ptr: answer


section .text
_start:
    ld message_size
    setcnt
    lda message
    setaddr
    loop_print1:
        read
        output 1
        cntz
        jz end_loop_print1
        jmp loop_print1

    end_loop_print1:
      ld endl
      output 1
      lda answer
      setaddr

    loop_write:
        input 0
        write
        cmp '\n'
        je end_write
        ld answer_size
        inc
        st answer_size
        ld answer_ptr
        add 4
        st answer_ptr
        setaddr
        jmp loop_write

    end_write:

    ld hello_size
    setcnt
    lda hello
    setaddr
    loop_print2:
        read
        output 1
        cntz
        jz loop_print2_end
        jmp loop_print2

    loop_print2_end:

    ld answer_size
    setcnt
    lda answer
    setaddr
    loop_print3:
        read
        output 1
        cntz
        jz print_answer_end
        jmp loop_print3

    print_answer_end:
        ld answer_end
        output 1
    exit:
        hlt
```

Программное хранение кода:

```python
  {'addr': 0, 'cmd': {'opcode': < Opcode.LD: 1 >, 'args_count': 1}, 'args': 0},
{'addr': 1, 'cmd': {'opcode': < Opcode.SETCNT: 6 >, 'args_count': 0}},
{'addr': 2, 'cmd': {'opcode': < Opcode.LDA: 3 >, 'args_count': 1}, 'args': 4},
{'addr': 3, 'cmd': {'opcode': < Opcode.SETADDR: 7 >, 'args_count': 0}},
{'addr': 4, 'cmd': {'opcode': < Opcode.READ: 5 >, 'args_count': 0}},
{'addr': 5, 'cmd': {'opcode': < Opcode.OUTPUT: 14 >, 'args_count': 1}, 'args': 1},
{'addr': 6, 'cmd': {'opcode': < Opcode.CNTZ: 22 >, 'args_count': 0}},
{'addr': 7, 'cmd': {'opcode': < Opcode.JZ: 9 >, 'args_count': 1}, 'args': 9},
{'addr': 8, 'cmd': {'opcode': < Opcode.JMP: 8 >, 'args_count': 1}, 'args': 4},
{'addr': 9, 'cmd': {'opcode': < Opcode.HLT: 23 >, 'args_count': 0}}
```

Отформатированные данные

```python
  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
```

Журнал:

```
DEBUG   machine:simulation    LD 0
    TICK:   0 PC:   0 ADDR:   0 MEM_OUT: 13 ACC: 0 BUFF: 0 DC: 0 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    SETCNT 
    TICK:   4 PC:   1 ADDR:   0 MEM_OUT: 13 ACC: 13 BUFF: 0 DC: 0 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    LDA 4
    TICK:   7 PC:   2 ADDR:   0 MEM_OUT: 13 ACC: 13 BUFF: 0 DC: 13 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    SETADDR 
    TICK:  10 PC:   3 ADDR:   0 MEM_OUT: 13 ACC: 4 BUFF: 0 DC: 13 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  13 PC:   4 ADDR:   1 MEM_OUT: 72 ACC: 4 BUFF: 0 DC: 13 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  17 PC:   5 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  []
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  20 PC:   6 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 0
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  23 PC:   7 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  26 PC:   8 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  29 PC:   4 ADDR:   2 MEM_OUT: 101 ACC: 72 BUFF: 0 DC: 12 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  33 PC:   5 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  36 PC:   6 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  39 PC:   7 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  42 PC:   8 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  45 PC:   4 ADDR:   3 MEM_OUT: 108 ACC: 101 BUFF: 0 DC: 11 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  49 PC:   5 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  52 PC:   6 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  55 PC:   7 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  58 PC:   8 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  61 PC:   4 ADDR:   4 MEM_OUT: 108 ACC: 108 BUFF: 0 DC: 10 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  65 PC:   5 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  68 PC:   6 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JZ 9
    TICK:  71 PC:   7 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    JMP 4
    TICK:  74 PC:   8 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    READ 
    TICK:  77 PC:   4 ADDR:   5 MEM_OUT: 111 ACC: 108 BUFF: 0 DC: 9 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    OUTPUT 1
    TICK:  81 PC:   5 ADDR:   6 MEM_OUT: 44 ACC: 111 BUFF: 0 DC: 8 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
    ---------------------------------------
    DEBUG   machine:simulation    CNTZ 
    TICK:  84 PC:   6 ADDR:   6 MEM_OUT: 44 ACC: 111 BUFF: 0 DC: 8 FLAG_ZERO: False FLAG_LT: 0 FLAG_GT: 1
    INPUT_PORT:  []
    OUT_PORT:  ['H', 'e', 'l', 'l', 'o']
    DATA_MEM:  [13, 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
  ......
  
  ---------------------------------------
    INFO    machine:simulation    output_buffer: 'Hello, world!'
```

### Результаты

| ФИО                       | alg         | LoC | code instr | tick  |
|---------------------------|-------------|-----|------------|-------|
| Михайлов Павел Максимович | hello_world | 18  | 10         | 219   |
| Михайлов Павел Максимович | hello_alice | 76  | 46         | 944   |
| Михайлов Павел Максимович | cat         | 12  | 6          | 130   |
| Михайлов Павел Максимович | prob1       | 41  | 23         | 48493 |

