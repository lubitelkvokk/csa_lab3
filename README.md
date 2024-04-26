# csa_lab3

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

<label> ::= <term>":"
<opcode_without_arg> ::= "in" | "out_int" | "hlt" | "out_char"
<opcode_arg> ::= "add" | "div" | "mul" | "mod"| "cmp" | "st" | "ld" | "sub"
<opcode_transfer> ::= "jmp" | "je" | "jge" | "jne"

<term> ::= <term> <term> | <number> | <letter>
<letter> ::= [a-z] | [A-Z]
<number> ::= [1-9] | <number> <number>
<comment> ::=  ";"<term>
```


### Hello, world

``` asm
global _start
 
section .data
message "Hello, world", '/0'
message_ptr message

section .text
_start:
    ld [message_ptr]
    loop:
        ld [acc]
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        ld [message_ptr]
        inc
        st message_ptr
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
message "What is your name?" , /0
message_ptr message
answer res(256)
answer_ptr answer 

section .text
_start:

    ld [message_ptr]
    loop_print1:
        ld [acc]
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
    
    ld answer
    st answer_ptr
    
    loop_print2:
        ld [acc]
        jz exit
        output 1 // вывод значения из регистра rax на 1 порт
        ld [answer_ptr]
        inc
        st answer_ptr
        jmp loop_print2
    exit:
        hlt
```

### prob1
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
**Find the sum of all the multiples of 3 or 5 below 1000.**

```
global _start
number1 3
number2 5
number_mul 1
result 0
count 0
bound: 1000

section .text
_start:
    ld 0
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
```