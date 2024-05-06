section .data
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