section .data
message: "Hello, world", "\0"
message_ptr: message

section .text
    ld [message_ptr]
    loop:
        ld [acc]
        jz exit
        output 1 ; вывод значения из регистра rax на 1 порт
        ld [message_ptr]
        inc
        st message_ptr
        jmp loop
    exit:
        hlt