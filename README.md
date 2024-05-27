# csa_lab3

ВОПРОС
Было принято решение использовать для взаимодействия с памятью команду загрузки адреса в dc и write, read на замену
привычной
загрузки данных из указанного адреса, т.к. не имеется возможности не используя косвенную адресацию осуществлять
последовательный ввод
и вывод в память.
Оставить ли реализацию такой, вернуть косвенную адресацию, или сделать привычной ld по адресу с учетом того, что мы
сделаем отдельные
команды для инкремента, декремента data counter и загрузки без указания адреса?
Введение команды инкремента dc, загрузки без адреса, записи без адреса

сделал служебный регистр Offset data pointer,
Который позволяет увеличивать его на 1 при выполнении команды write и read,
которые не принимают аргументов и читают/записывают значение с учетом адреса в data address + offset и увеличивают
Offset на 1
для следующих данных. Также отдельно есть команда ld <addr>, которая загружает данные в аккумулятор,
запписывает адрес в address register и устанавливает offset в ноль для дальнейшего чтения с помощью read,
write (чтобы выполнять последовательное чтение, т.к. я не могу из программы напрямую увеличить offset register)

Вопросы на защиту:

1) MUX(INC) - является сочетанием шины и комбинационной схемы инкрементирует значение
2) Как происходит выбор jmp, cmp, порта на вывод (на основании чего делается выбор)
3) Шины на вход в мультиплексор имеют одинаковую размерность
4) Контроль тактов (пытаться избежать излишних, например доступ к адресу памяти за 2 такта - излишне)

## Вариант без усложнения

```
asm | acc | harv | mc -> hw | instr | binary -> struct | stream | port | pstr | prob1 | cache
```

## Язык программирование

``` ebnf
<program> ::= <program> <line> | <line>
<line> ::=  <opcode_without_arg> | <opcode_transfer> " ."<term> 
    | <opcode_arg> " (" <term> ")" | <opcode_arg> " #"<number> 
    | <opcode_arg> <term>
    | <label> | <comment> | <line> <comment>
    |  <label> " number " <number> | <label> ' string ' '"' <term> '"'
    | "section ."<term> | "\n" 

<label> ::= (<name>":" (" ")*) | (<name>":" (" ")* "\n")
<address> ::= #<number>

<opcode_without_arg> ::= "hlt"  | "inc" | "read" | "write" | "cntz" | "setcnt"
<opcode_arg> ::= ("add" | "cmp" | "sub" | "input" | "output") (" ")+ <number>
<opcode_transfer> ::= ("jmp" | "jge" | "jz") (" ")+ <label>
<opcode_addr> ::= ("add" | "cmp"| "ld" | "lda" | st" | "sub" | "input" | "output") (" ")+ (<label> | <address>)

<term> ::= <term> <term> | <number> | <letter>
<letter> ::= [a-z] | [A-Z]
<number> ::= [1-9] | <number> <number>
<comment> ::=  ";"<term>
```

- ld: загружает данные в acc из ячейки памяти
- lda: загрузить в acc непосредственно значение
- write: [data_addr] <- acc, data_counter <- data_counter - 1
- read:  [data_addr] -> acc, data_counter <- data_counter - 1
- jmp: безусловный переход по указанному адресу (для упрощения только по метке). pc <- addr
- je - условный переход по указанному адресу, если после сравнения флаги GT и LT были заполнены нулями
- jz: условный переход по указанному адресу, если после сравнения флаг Z был заполнен единицей
- jge: условный переход по указанному адресу, если после сравнения флаг GT был заполнен единицей
- jle: условный переход по указанному адресу, если после сравнения флаг LT был заполнен единицей
- inc: инкремент аккумулятора. acc <- acc + 1
- dec: декремент аккумулятора. acc <- acc - 1
- input: получение ввода с определенного порта (рядом указывается номер порта, например input 0). Запись осуществляется
  в регистр rax
- output: указание порта на вывод. Вывод осуществляется из регистра rax
- add: прибавление числа к регистру и сохранение результата в этот же регистр (вместо числа может быть представлен
  другой регистр, данные из памяти)
- mul: умножение числа на регистр и сохранение результата в этот же регистр (-||-)
- hlt: остановка процессора
- cntz - count data zero, проверка, является ли регистр data count равен нулю, установка соответствущего флага
- setcnt - загрузить значение из аккумулятора в регистр счетчика данных

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
        jz exit
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
hello_size: 7
hello: "Hello, "
answer_size: 0
answer: res(255)
answer_end: "!"

section .text
_start:


    ld message_size
    setcnt
    lda message
    setaddr
    loop_print1:
        output 1
        read
        cntz
        jz end_loop_print1
        jmp loop_print1

    end_loop_print1:
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
        lda answer
        add answer_size
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
        je loop_print2_end
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
        je print_answer_end
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

null: 0
number1: 3
number2: 5
number15: 15
result: 0
count: 0
bound: 1000

section .text

_start:
    ld null
    st count
    ld null
    st result

main_loop:
    ld result
    inc
    st result
    
    ld result
    cmp bound
    jge end_loop

    ld result
    mod number15
    cmp null
    je div15_found

    ld result
    mod number1
    cmp null
    je div3_found

    ld result
    mod number2
    cmp null
    je div5_found

    jmp main_loop

div15_found:
    ld count
    dec
    st count
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

end_loop:
    ld count
    output 1
    
exit:
    hlt
```

## Система команд

| Номер | Команда | Последовательность сигналов                               |
|-------|---------|-----------------------------------------------------------|
| 0     | start   | latch_mpc_zero, latch_mc, sel_pc                          |
| 1     | ld      | latch_pm, sel_mpc_opc, latch_mc, sel_ar_addr, latch_addr  |
|       |         | sel_acc_data_mem, sel_pc_next                             |
| 2     | st      | latch_pm, sel_mpc_opc, latch_mc, sel_ar_addr, latch_addr  |
|       |         | latch_data_mem, sel_pc_next                               |
| 3     | lda     | latch_pm, sel_mpc_opc, latch_mc, sel_acc_val              |
|       |         | sel_pc_next                                               |
| 4     | write   | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | latch_data_mem, sel_dc_dec, sel_pc_next                   |
| 5     | read    | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | latch_data_mem, sel_dc_dec, sel_pc_next                   |
| 6     | setcnt  | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | sel_dc_acc, sel_pc_next                                   |
| 7     | setaddr | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | sel_ar_addr, sel_pc_next                                  |
| 7     | jmp     | latch_pm, sel_mpc_opc, latch_mc, sel_jmp                  |
| 8     | jz      | latch_pm, sel_mpc_opc, latch_mc, sel_jz                   |
| 9     | jge     | latch_pm, sel_mpc_opc, latch_mc, sel_jge                  |
| 10    | je      | latch_pm, sel_mpc_opc, latch_mc, sel_je                   |
| 10    | inc     | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | sel_alu_inc, sel_pc_next                                  |
| 11    | dec     | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | sel_alu_dec, sel_pc_next                                  |
| 12    | output  | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | latch_write_io, sel_pc_next                               |
| 13    | input   | latch_pm, sel_mpc_opc, latch_mc                           |
|       |         | sel_acc_io, sel_pc_next                                   |
| 14    | add     | latch_pm, sel_mpc_opc, latch_mc, latch_ar_addr            |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_add, sel_pc_next    |
| 15    | sub     | latch_pm, sel_mpc_opc, latch_mc, latch_ar_addr            |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_sub, sel_pc_next    |
| 16    | mul     | latch_pm, sel_mpc_opc, latch_mc,  latch_ar_addr           |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_mul, sel_pc_next    |
| 17    | div     | latch_pm, sel_mpc_opc, latch_mc, latch_ar_addr            |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_div, sel_pc_next    |
| 18    | mod     | latch_pm, sel_mpc_opc, latch_mc, latch_ar_addr            |
|       |         | latch_buff, sel_acc_data_mem, sel_alu_mod, sel_pc_next    |
| 18    | cmp     | latch_pm, sel_mpc_opc, latch_mc, sel_cmp_acc, sel_pc_next |
| 19    | cntz    | latch_pm, sel_mpc_opc, latch_mc, sel_cmp_dc, sel_pc_next  |


Описание:

| Номер бита | Сигнал         | Описание                                                                                                                                                                                       |
|------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0          | latch_pm       | Выбрать в памяти инструкции значение по указанному Program counter                                                                                                                             |
| 1          | sel_mpc_opc    | Выбрать микропрограмму по значению Opcode                                                                                                                                                      |
| 2          |                | 10 - загрузка нуля(при запуске процессора), 11 - загрузка по Opcode                                                                                                                            |
| 3          | latch_mc       | После выбранного номера микропрограммы защелкиваем для выполнения соответствующей последовательности микроинструкций                                                                           |
| 4          | sel_pc         | Выбираем следующее значение Program Counter. 1000 - SEL_NEXT, 1001 - SEL_JMP, 1010 - SEL_JZ (в зависимости от флага), 1011 - SEL_JE, 1100 - SEL_JGE                                            |
| 5          |                |                                                                                                                                                                                                |
| 6          |                |                                                                                                                                                                                                |
| 7          |                |                                                                                                                                                                                                |
| 8          | sel_ar         | Выбор адреса для последующего обращения к памяти (запись/чтение). 10 - SEL_NEXT, 11 - SEL_ADDR(декодированное значение из CU)                                                                  |
| 9          |                |                                                                                                                                                                                                |
| 10         | latch_data_mem | Выбор значения из аккумулятора в память по указанному адресу                                                                                                                                   |
| 11         | sel_acc        | Запись в аккумулятор из указанного источника. 100 - SEL_ACC_DATA_MEM, 101 - SEL_ACC_IO(из портов), 110 - SEL_ACC_VAL(декодированное значение из CU)                                            |
| 12         |                |                                                                                                                                                                                                |
| 13         |                |                                                                                                                                                                                                |
| 14         | write_io       | Запись из аккумулятора в указанный порт                                                                                                                                                        |
| 15         | latch_buff     | Запись из аккумулятора в буферный регистр                                                                                                                                                      |
| 16         | sel_alu        | Вычисление в алу и запись результата в аккумулятор. 1000 - SEL_ALU_INC, 1001 - SEL_ALU_DEC, 1010 - SEL_ALU_ADD, 1011 - SEL_ALU_SUB, 1100 - SEL_ALU_MUL, 1101 - SEL_ALU_DIV, 1110 - SEL_ALU_MOD |
| 17         |                |                                                                                                                                                                                                |
| 18         |                |                                                                                                                                                                                                |
| 19         |                |                                                                                                                                                                                                |
| 20         | sel_dc         | Выбор следующего значения для Data Count регистра. 10 - SEL_DC_DEC(декремент) 11 - SEL_DC_ACC (из аккумулятора)                                                                                |
| 21         |                |                                                                                                                                                                                                |
| 22         | sel_cmp        | Выбор левого входа для сравнения с декодированным значением из CU. 10 - SEL_CMP_ACC(значение из аккумулятора), 11 - SEL_CMP_DC(значение из data counter)                                       |
| 23         |                |                                                                                                                                                                                                |



