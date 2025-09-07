from parser import Parser
from compiler import Compiler

with open("main.tl", 'r') as f:
    data = f.read()
    # data = data.split("\n")
    # data = [line.strip() for line in data]

p = Parser(data)
print("Parsed program:")
print(p.finalParsed)


c = Compiler(p.finalParsed, addComments=True)
print("Finished Compiling")