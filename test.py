from isa import write_code, read_code, read_data
from translator import translate

file = open("examples/cat.asm")
# code, translated_data_labels = translate(file.read())
# write_code("input.txt", code)
# print(read_code("program_file"))
# for i in read_code("program_file"):
#     print(i)
# print(read_data("data_file"))
# for i in read_data("data_file"):
#     print(i)

with open("program_file", "rb") as file1:
    for i in file1.read():
        print()
