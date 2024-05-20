section .data

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