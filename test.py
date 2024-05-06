from translator import translate_stage_1, translate_stage_2

file = open("examples/hello_io.asm")
data_labels, text_labels, code = translate_stage_1(file.read())
# print(data_labels)
# print(text_labels)
# print(code)
data = [0] * 1024
translate_stage_2(data_labels, text_labels, code, data)
print(data)
