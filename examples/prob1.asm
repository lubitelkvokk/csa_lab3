section .data
    null: 0
    number1: 3
    number2: 5
    number15: 15
    result: 0
    count: 0
    bound: 1000

section .text

_start:
    ; Инициализация
    ld null
    st count
    ld null
    st result

    ; Основной цикл
main_loop:
    ld result
    inc
    st result

    ; Проверка, что текущий результат <= 1000
    ld result
    cmp bound
    jge end_loop

    ; Проверка на делимость на 15
    ld result
    mod number15
    cmp null
    je div15_found

    ; Проверка на делимость на 3
    ld result
    mod number1
    cmp null
    je div3_found

    ; Проверка на делимость на 5
    ld result
    mod number2
    cmp null
    je div5_found

    ; Продолжаем основной цикл
    jmp main_loop

div15_found:
    ; Уменьшить счетчик, так как число делится на 15
    ld count
    dec
    st count
    jmp main_loop

div3_found:
    ; Увеличить счетчик делителей для числа 3
    ld count
    inc
    st count
    jmp main_loop

div5_found:
    ; Увеличить счетчик делителей для числа 5
    ld count
    inc
    st count
    jmp main_loop

end_loop:
    ; Вывод результата
    ld count
    output 1

exit:
    hlt