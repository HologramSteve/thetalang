from parser import Parser
from compiler import Compiler

with open("main.tl", 'r') as f:
    data = f.read()
    lines = data.split('\n')
    processed_lines = []
    for line in lines:
        if line.strip():
            processed_lines.append(line + ';')
        else:
            processed_lines.append(line)
    data = '\n'.join(processed_lines)
    # data = [line.strip() for line in data]
    # data = data.split("\n")

p = Parser(data)
print("Parsed program:")
print(p.finalParsed)


c = Compiler(p.finalParsed, addComments=True)
print("Finished Compiling")