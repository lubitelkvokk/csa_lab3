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