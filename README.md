# csa_lab3

ВОПРОС
Было принято решение использовать для взаимодействия с памятью команду загрузки адреса в dc и write, read на замену привычной
загрузки данных из указанного адреса, т.к. не имеется возможности не используя косвенную адресацию осуществлять последовательный ввод
и вывод в память. 
Оставить ли реализацию такой, вернуть косвенную адресацию, или сделать привычной ld по адресу с учетом того, что мы сделаем отдельные
команды для инкремента, декремента data counter и загрузки без указания адреса?
Введение команды инкремента dc, загрузки без адреса, записи без адреса

сделал служебный регистр Offset data pointer, 
Который позволяет увеличивать его на 1 при выполнении команды write и read, 
которые не принимают аргументов и читают/записывают значение с учетом адреса в address register + offset и увеличивают Offset на 1
для следующих данных. Также отдельно есть команда ld <addr>, которая загружает данные в аккумулятор, 
запписывает адрес в address register и устанавливает offset в ноль для дальнейшего чтения с помощью read, 
write (чтобы выполнять последовательное чтение, т.к. я не могу из программы напрямую увеличить offset register)

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
<opcode_arg> ::= ("add" | "cmp" | "sub" | "input" | "output" | "mov") (" ")+ <number>
<opcode_transfer> ::= ("jmp" | "jge" | "jz") (" ")+ <label>
<opcode_addr> ::= ("add" | "cmp"| "ld" | "lda" | st" | "sub" | "input" | "output") (" ")+ (<label> | <address>)

<term> ::= <term> <term> | <number> | <letter>
<letter> ::= [a-z] | [A-Z]
<number> ::= [1-9] | <number> <number>
<comment> ::=  ";"<term>
```
- ld: загружает данные в acc, выставляет address register в указанный адрес, и data_offset в 1, чтобы указатель для read, write был на след ячейку
- lda: загрузить адрес метки
- write: [data_addr] <- acc, data_counter <- data_counter - 1
- read:  [data_addr] -> acc, data_counter <- data_counter - 1
- jmp: безусловный переход по указанному адресу (для упрощения только по метке). pc <- addr
- jz: условный переход по указанному адресу, если содержимое аккумулятора равно 0, иначе осуществляется переход к следующей инструкции.
- jge: условный переход по указанному адресу, если содержимое аккумулятора равно больше определенного числа, иначе осуществляется переход к следующей инструкции.
- inc: инкремент аккумулятора. acc <- acc + 1
- dec: декремент аккумулятора. acc <- acc - 1
- input: получение ввода с определенного порта (рядом указывается номер порта, например input 0). Запись осуществляется в регистр rax
- output: указание порта на вывод. Вывод осуществляется из регистра rax
- add: прибавление числа к регистру и сохранение результата в этот же регистр (вместо числа может быть представлен другой регистр, данные из памяти)
- mul: умножение числа на регистр и сохранение результата в этот же регистр (-||-)
- mov: помещение числа, символа, данных из памяти, регистра в регистр.
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
section .text
_start:
    loop:
        input 0
        cmp 0
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
hello: "Hello, "
answer_size: 0
answer: res(255)
answer_end: "!"

section .text
_start:

    lda message
    setaddr
    ld message_size
    setcnt
    loop_print1:
        output 1
        read
        cntz
        jz loop_read
        jmp loop_print1
    
    lda answer
    setaddr
    
    loop_read:
        input 0
        write
        cmp '\n'
        je end_read
        ld answer_size
        inc
        st answer_size
        lda answer
        add answer_size
        setaddr
        jmp loop_read
    answer_size
    
    end_read:    
    
    lda hello
    setaddr
    ld hello_size
    setcnt
    
    loop_print2:
        read
        output 1
        cntz
        je loop_print2_end
        jmp loop_print2
        
    loop_print2_end:    
    lda answer_size
    setaddr
    ld answer
    setcnt
    
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
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
**Find the sum of all the multiples of 3 or 5 below 1000.**

``` asm
global _start
null: 0
number1: 3
number2: 5
number_mul: 1
result: 0
count: 0
bound: 1000

section .text
_start:
    ld null
    loop1:
        add number1
        cmp bound
        jge end_loop1
        st result
        ld count
        inc
        st count
        ld result
        jmp loop1
        
    end_loop1:
    ld null
    
    loop2:
        add number2
        cmp bound
        jge end_loop2
        st result
        ld count
        inc
        st count
        ld result
        jmp loop2
        
    end_loop2:
    ld number1
    mul number2
    st number_mul
    
    ld null
    
    loop3:
        add number_mul
        cmp bound
        jge end_loop3
        st result
        ld count
        dec ; or sub 1
        st count
        ld result
        jmp loop3
        
    end_loop3:
    ld count
    output 1
    exit:
        hlt
```