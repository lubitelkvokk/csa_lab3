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

<transfer_command> ::= ("jmp" | "jz" | "jnz" | "je" | "jge" | "jne") (" ")+ <label>

<number_arg_command> ::= ("inc" | "cmp" | "input" | "output"| "add" | "sub" | "mul" | "div" | "mov" ) (" ")+ <number>
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
- jnz - условный переход по указанному адресу, если содержимое аккумулятора не равно 0, иначе осуществляется переход к следующей инструкции.
- je - условный переход по указанному адресу, если содержимое аккумулятора равно указанному значению
