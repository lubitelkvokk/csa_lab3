from isa import write_code, read_code, read_data
from translator import translate

file = open("examples/cat.asm")
# code, translated_data_labels = translate(file.read())
# write_code("aboba.txt", code)
for i in read_code("program_file"):
    print(i)

# for i in read_data("data_file"):
#     print(i)
