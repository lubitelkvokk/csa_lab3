﻿# csa_lab3

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

<label_arg_command> ::= ("push" | "jmp" 
| "jz" | "jnz" | "js" | "jns" | "call") (" ")+ <label>

<number_arg_command> ::= ("push" | "cmp" | "input" | "output") (" ")+ <number>
<without_arg_command> ::= ("inc" | "hlt" | "pop" | "swap" | "add" | "sub" | "mul" | "div" | "ret" | "load" | "store")

<number> ::= [-2^64; 2^64 - 1]
<name> ::= (<letter_or_>)+
<letter_or_> ::= <letter> | ("_")
<letter> ::= [a-z] | [A-Z]
```

