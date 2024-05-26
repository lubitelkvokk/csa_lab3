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