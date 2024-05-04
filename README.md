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

<opcode_without_arg> ::= "hlt"  | "inc" | "read" | "write"
<opcode_arg> ::= ("add" | "cmp" | "sub" | "input" | "output" | "mov") (" ")+ <number>
<opcode_transfer> ::= ("jmp" | "jge" | "jz") (" ")+ <label>
<opcode_addr> ::= ("add" | "cmp"| "ld" | "st" | "sub" | "input" | "output") (" ")+ (<label> | <address>)

<term> ::= <term> <term> | <number> | <letter>
<letter> ::= [a-z] | [A-Z]
<number> ::= [1-9] | <number> <number>
<comment> ::=  ";"<term>
```
- ld: загружает данные в acc, выставляет address register в указанный адрес, и data_offset в 1, чтобы указатель для read, write был на след ячейку
- write: [data_addr] <- acc, data_offset <- data_offset + 1
- read:  [data_addr] -> acc, data_offset <- data_offset + 1
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
### Hello, world

``` asm
global _start
 
section .data
message: "Hello, world", '/0'
message_ptr: 0

section .text
_start:
    loop:
        ld [message_ptr]
        cmp #0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        ld message_ptr
        inc
        st message_ptr
        jmp loop
    exit:
        hlt
        
        
; SECOND TRY WITH INC DC

section .data
message: "Hello, world", '/0'

section .text
_start:
    ld message
    loop:
        read ; inc data counter that we load earlier
        cmp #0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        jmp loop
    exit:
        hlt
        
-----------
THIRD TRY

section .data
message: "Hello, world", '/0'

section .text
_start:
    ld message
    loop:
        cmp 0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        read
        jmp loop
    exit:
        hlt
```


### cat 
``` asm
global _start

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
message: "What, is your name?" , '/0'
message_ptr: message
hello: "Hello, "
answer: res(256)
answer_ptr: answer 
hello_ptr: hello

section .text
_start:

    ld [message_ptr]
    loop_print1:
        cmp #0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        ld [message_ptr]
        inc
        st message_ptr
        jmp loop_print1

    loop_read:
        input 0
        st [answer_ptr] ; косвенная адресация
        cmp '\n'
        jmp end_read
        ld [answer_ptr]
        inc
        st answer_ptr
        jmp loop_read
        
    end_read:    
    
    ld [hello_ptr]
    
    loop_print2:
        cmp #0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        ld hello_ptr
        inc
        st hello_ptr
        jmp loop_print2
    exit:
        hlt
        
        
------------------------
message: "What, is your name?" , '/0'
message_ptr: message
hello: "Hello, "
answer: res(256)
end: "!"

section .text
_start:

    ld message
    loop_print1:
        read
        cmp #0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        jmp loop_print1
    
    ld answer
    loop_read:
        input 0
        st ; now it stores acc -> [dc] and dc + 1 -> dc
        cmp '\n'
        jmp loop_read
        
    end_read:    
    
    ld hello
    
    loop_print2:
        read ; [dc] -> acc and dc + 1 -> dc
        cmp '!'
        output 1 // вывод значения из регистра rax на 1 порт
        jz exit
        jmp loop_print2
    exit:
        hlt
        
-------------------
THIRD TRY 


message: "What, is your name?" , '/0'
hello: "Hello, "
answer: res(256)
end: '!'

section .text
_start:

    ld message
    loop_print1:
        cmp #0
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        read
        jmp loop_print1
    
    input 0
    st answer
    loop_read:
        cmp '\n'
        jmp end_read
        input 0
        write
        jmp loop_read
        
    end_read:    
    
    ld hello
    
    loop_print2:
        cmp '\n'
        jz end_loop_print2
        output 1 // вывод значения из регистра rax на 1 порт
        read
        jmp loop_print2
    
    end_loop_print2:
    ld end
    output 1
    exit:
        hlt
```

### prob1
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
**Find the sum of all the multiples of 3 or 5 below 1000.**

``` asm
global _start
number1: 3
number2: 5
number_mul: 1
result: 0
count: 0
bound: 1000

section .text
_start:
    ld #0
    loop1:
        add [number1]
        cmp [bound]
        jge end_loop1
        st result
        ld [count]
        inc
        st [count]
        ld [result]
        jmp loop1
        
    end_loop1:
    ld 0
    
    loop2:
        add [number2]
        cmp [bound]
        jge end_loop2
        st result
        ld [count]
        inc
        st [count]
        ld [result]
        jmp loop2
        
    end_loop2:
    ld [number1]
    mul [number2]
    st [number_mul]
    
    ld 0
    
    loop3:
        add [number_mul]
        cmp [bound]
        jge end_loop3
        st result
        ld [count]
        dec ; or sub 1
        st [count]
        ld [result]
        jmp loop3
        
    end_loop3:
    mov rax, rdx
    output 1
    exit:
        hlt
        
        
--------------------
global _start
number1: 3
number2: 5
number_mul: 1
result: 0
count: 0
bound: 1000

section .text
_start:
    mov 0
    loop1:
        add number1
        cmp 1000
        jge end_loop1
        ld result
        write
        ld count
        read
        inc
        ld count
        write
        ld result
        read
        jmp loop1
        
    end_loop1:
    
    mov 0
    
    loop2:
        add number2
        cmp 1000
        jge end_loop2
        ld result
        write
        ld count
        read
        inc
        st count
        write
        ld [result]
        jmp loop2
        
    end_loop2:
    ld [number1]
    mul [number2]
    st [number_mul]
    
    ld 0
    
    loop3:
        add [number_mul]
        cmp [bound]
        jge end_loop3
        st result
        ld [count]
        dec ; or sub 1
        st [count]
        ld [result]
        jmp loop3
        
    end_loop3:
    mov rax, rdx
    output 1
    exit:
        hlt
        
-----------------

THIRD TRY


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
        cmp 1000
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
        cmp 1000
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
        cmp 1000
        jge end_loop3
        st result
        ld count
        dec
        st count
        ld result
        jmp loop3
        
    end_loop3:
    ld count
    output 1
    exit:
        hlt
```