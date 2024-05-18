from isa import write_code, read_code
from translator import translate

file = open("examples/hello_io.asm")
code, translated_data_labels = translate(file.read())
write_code("aboba.txt", code)
print(read_code("aboba.txt"))

