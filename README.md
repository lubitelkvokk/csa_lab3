# csa_lab3

## Вариант без усложнения

```
asm | acc | harv | mc -> hw | instr | binary -> struct | stream | port | pstr | prob1 | cache
```

## Язык программирование
``` ebnf
<program> ::= <section_data> <section_text> | <section_text> <section_data> | <section_text>

<section_data> ::= "section .data\n" <declaration>*
<section_text> ::= "section .text\n" (<label> | <instruction>)*

<declaration> ::= <label> (<array> | <reserve>)
<instruction> ::= <label_arg_command> | <number_arg_command> | <without_arg_command>

<label> ::= (<name> ":" (" ")*) | (<name> ":" (" ")* "\n")

<array> ::= (<array_element> "," (" ")*)* <array_element>+
<reserve> ::= "res" (" ")+ <number>
<array_element> ::= ("\"" <any_ascii> "\"" | <number>)

<transfer_command> ::= ("jmp" | "jz" | "jge") (" ")+ <label>

<number_arg_command> ::= ("inc" | "cmp" | "input" | "output"| "add" | "sub" | "mul" | "mov" ) (" ")+ <number>
<without_arg_command> ::= ( "hlt")

<number> ::= [-2^64; 2^64 - 1]
<name> ::= (<letter_or_>)+
<letter_or_> ::= <letter> | ("_")
<letter> ::= [a-z] | [A-Z]
```

### Описание языка
- section .text - секция, в которой содержимое интерпретируется как инструкция
- section .data - секция, в которой содержимое интерпретируется как данные
- label - метка, после которой указывается ее название. Является указателем на адрес памяти. Может быть указана строка, числа через запятую

- jmp - безусловный переход по указанному адресу (для упрощения только по метке).
- jz - условный переход по указанному адресу, если содержимое аккумулятора равно 0, иначе осуществляется переход к следующей инструкции.
- jge - условный переход по указанному адресу, если содержимое аккумулятора равно больше определенного числа, иначе осуществляется переход к следующей инструкции.
- inc - инкремент указанного регистра
- input - получение ввода с определенного порта (рядом указывается номер порта, например input 0). Запись осуществляется в регистр rax
- output - указание порта на вывод. Вывод осуществляется из регистра rax
- add - прибавление числа к регистру и сохранение результата в этот же регистр (вместо числа может быть представлен другой регистр, данные из памяти)
- sub - вычитания числа из регистра и сохранение результата в этот же регистр (-||-)
- mul - умножение числа на регистр и сохранение результата в этот же регистр (-||-)
- mov - помещение числа, символа, данных из памяти, регистра в регистр.
- 
### Hello, world

``` asm
global _start
 
section .data
message "Hello, world"
 
section .text
_start:
    mov rdx, 0 // смещение в строке
    loop:
        mov rax, [message + rdx] // загрузка в rax символа из памяти
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        inc rdx // инкремент rdx
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
        jz exit
        output 1
        jmp loop
    exit:
        hlt
```

### cat
``` asm
global _start
message: "What is your name?" , /0
answer: res(256)

section .text
_start:
    mov rdx, 0
    loop_read:
        input 0
        mov [answer + rdx], rax
        cmp '\n'
        jmp end_read
        inc rdx
        jmp loop_read
        
    end_read:    
    mov rdx, 0
    loop_print:
        mov rax, [answer + rdx]
        output 1
        cmp '\n'
        jmp exit
        inc rdx
        jmp loop_print
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
bound: 1000

section .text
_start:
    mov rax, [number1]
    mov rdx, 0
    loop1:
        add rdx, rax
        add rax, [number1]
        jge [bound], end_loop1 ??????
        jmp loop1
    end_loop1:
    
    mov rax, [number2]
    loop2:
        add rdx, rax
        add rax, [number2]
        cmp rax, [bound]
        jge end_loop2
        jmp loop2
        
    end_loop2:
    mov rcx, [number1]
    mul rcx, [number2]
    mov rax, rcx
    
    loop3:
        sub rdx, rax
        add rax, rcx
        jge [bound], end_loop3
        jmp loop3
        
    end_loop3:
    mov rax, rdx
    output 1
    exit:
        hlt
```
