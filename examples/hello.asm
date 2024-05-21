section .data
message_size: 13
message: "Hello, world!"

section .text
_start:
    ld message_size
    setcnt
    ld message
    loop:
        read
        output 1
        cntz
        jz exit
        jmp loop
    exit:
        hlt