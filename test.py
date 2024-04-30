from translator import translate_stage_1, translate_stage_2

file = open("examples/hello.asm")
data_labels, text_labels, code = translate_stage_1(file.read())
translate_stage_2(data_labels, text_labels, code)
