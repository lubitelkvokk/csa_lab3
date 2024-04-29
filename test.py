from translator import translate_stage_1

file = open("examples/hello.asm")
print(translate_stage_1(file.read()))
