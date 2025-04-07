import re
import random

if_counter = 0
while_counter = 0
forever_counter = 0
# Get code from the file
with open("main.tl", "r") as f:
    data = f.read()
    data = re.split(r'(\n)', data)
    data = [line.lstrip() for line in data]
    data = [line for line in data if line != '']

class Compiler:
    def getValue(self, value, register):
        ree = list(value)

        if ree[0] == "$":
            ree.remove(ree[0])
            try:
                info = self.variables["".join(ree)]
                vartype = info['type']
                if not vartype in ["int", "char"]:
                    raise ImportError("Can't call String variable.")
            except KeyError:
                raise KeyError(f"Undefined variable -> {''.join(ree)}")
            print(info)
            self.addCode(f"LDI r4 {info['adr']}")
            self.addCode(f"LOD r4 r{register}")
        elif ree[0] == "#":
            combinedRee = "".join(ree)
            if combinedRee == "#random":
                self.addCode(f"LDI r{register} {random.randint(0, 255)}")
                vartype = "int"
            elif combinedRee[:-1] == "#par":
                adrmap = {"a": 0, "b": 1, "c": 2, "d": 3}
                adr = 236 + adrmap[combinedRee[4:]]
                self.addCode(f"LDI r4 {adr}")
                self.addCode(f"LOD r4 {register}")
                vartype = "any"
            elif combinedRee == "#controls":
                self.addCode("LDI r15 255")
                self.addCode(f"LOD r15 r{register}")
                vartype = "int"
            elif combinedRee == "#returnval":
                self.addCode("LDI r15 231")
                self.addCode(f"LOD r15 r{register}")
                vartype = "any"
            else:
                raise NameError(f"Systemvar {combinedRee} not found!")
        else:
            self.addCode(f"LDI r{register} {value}")
            vartype = "any"

        return vartype

    def addCode(self, code):  
        self.program.append(code + "\n")


    def __init__(self, variables, functions, program):
        self.variables = variables
        self.functions = functions
        self.program = program
        self.freeram = list(range(231))
        self.moduleCode = []
        self.modules = []
        self.ongoingInternalGroups = []

    def addReserveCode(self, code):
        self.reserveAdd.append(code + "\n")
    
    def compileLine(self, line):
            global if_counter
            global forever_counter
            global while_counter
            linedata = line.split(" ")
    
            keyword = linedata[0]
            

            if keyword == "return":
                self.addCode("RET")
    
            if keyword == "var":
                vartype = linedata[1]
                if not vartype in ["int", "char", "String"]:
                    raise TypeError(f"Invalid type -> {vartype}")

                varname = linedata[2]
                if varname in self.variables:
                    raise KeyError(f"Variable {varname} already defined")
                varvalue = linedata[4]

                temp_cache = varvalue
                print(list(varvalue)[1:])
                print(vartype)
                if list(varvalue)[1:] != "$" and vartype == "int":
                    try:
                        temp_cache = int(varvalue)
                    except Exception as e:
                        pass
                        # raise ValueError(f"Error: couldn't compile {varvalue} as an integer (assigned value is int)")
                if list(varvalue)[1:] != "$" and vartype == "char" and len(list(varvalue)) > 3:
                    raise ValueError(f"Can't compile {varvalue} as a single character (assigned as char)")
                

                if vartype == "int" or vartype == "char":
                    adr = self.freeram[0]
                    self.freeram.pop(0)

                    self.getValue(varvalue, 1)
                    self.addCode(f"LDI r4 {adr}")
                    self.addCode(f"STR r4 r1")

                    self.variables[varname] = {"adr": adr, "type": vartype}
                else:
                    if list(varvalue)[0] == "$":
                        varvaluename = varvalue[1:]
                        try:
                            info = self.variables[varvaluename]
                            if info['type'] != 'String':
                                raise ValueError(f"Type {info['type']} can't store in a String variable")
                        except KeyError:
                            raise KeyError(f"Variable (string) with name {varvaluename} not found")
                        raise ImportError("Can't call String variable.")
                        # Feel free to code this, idc
                    splitVarValue = list(varvalue)
                    splitVarValue = [item for item in splitVarValue if item != '"']
                    if len(self.freeram) < len(splitVarValue) + 1:
                        raise MemoryError("Too little memory left over for variable " + varname)
                    startAdr = self.freeram.pop(0)
                    for i, char in enumerate(splitVarValue):
                        self.addCode(f"LDI r4 '{char}'")
                        self.addCode(f"LDI r15 {startAdr + i}")
                        self.freeram.pop(0)
                        self.addCode(f"STR r15 r4")
                        endAdr = startAdr + i
                    endAdr += 1
                    
                    self.variables[varname] = {"adr": startAdr, "type": "String", "endAdr": endAdr}
            
            if keyword == "mutate":
                varname = linedata[1]
                operation = list(linedata[2])[0]

                operationvalue = linedata[3]
                vardata = self.variables[varname]
                vartype = vardata['type']
                self.addCode(f"LDI r7 {vardata['adr']}") # Pointer in r4
                self.addCode(f"LOD r7 r5") 
                valuetype = self.getValue(operationvalue, 4)
                if valuetype != "any" and valuetype != vartype:
                    raise TypeError(f"Setting a var with type {vartype} to type {valuetype} is not allowed")
                if operation == "+":
                    if vartype != "int":
                        raise ValueError(f"Can't add with invalid var type {vartype}")
                    self.addCode(f"ADD r4 r5 r5")
                elif operation == "-":
                    if vartype != "int":
                        raise ValueError(f"Can't add with invalid var type {vartype}")
                    self.addCode(f"SUB r5 r4 r5")
                elif operation == "=":
                    self.getValue(operationvalue, "5")
                else:
                    raise ValueError(f"Invalid operation -> {operation}")
                self.addCode(f"STR r7 r5")
            if keyword == "call":
                
                functionname = linedata[1]
                try:
                    info = self.functions[functionname]
                except KeyError:
                    try:
                        info = self.modules.index(functionname)
                    except ValueError:
                        raise KeyError(f"Undefined function -> {functionname}")
                if functionname == "txtdisplay.set":
                    if functionname == "txtdisplay.set":
                        varname = linedata[2]
                        vardata = self.variables[varname]
                        if vardata['type'] != "String":
                            raise SyntaxError("Must use a variable of type String when using txtdisplay.set!")
                        self.addCode(f"LDI r15 232")
                        self.addCode(f"LDI r4 {vardata['adr']}")
                        self.addCode(f"STR r15 r4")
                        self.addCode(f"LDI r15 233")
                        self.addCode(f"LDI r4 {vardata['endAdr']}")
                        self.addCode(f"STR r15 r4")
                        self.addCode(f"CAL .{functionname}")
                else:
                    linedata = linedata[2:]
                    adr = 235
                    reg = 3
                    for value in linedata:
                        reg += 1
                        adr += 1
                        self.getValue(value, reg)
                        self.addCode(f"LDI r3 {adr}")
                        self.addCode(f"STR r3 r{reg}")
                    self.addCode(f"CAL .{functionname}")
            if keyword == "include":
                import json
                with open("modules.json", 'r') as f:
                    modulesdata = json.load(f)
                    try:
                        for func in modulesdata[linedata[1]]:
                            self.moduleCode.append(func)
                            self.modules.append(func[0][1:-1])
                        print(self.moduleCode)
                        print(self.modules)
                    except KeyError:
                        raise KeyError(f"Module not found -> {linedata[1]}")
            if keyword == "free":
                varname = linedata[1]
                info = self.variables[varname]
                
                # If it's a string, free its allocated memory
                if info['type'] == "String":
                    # Start address of the string
                    startAdr = info['adr']
                    # End address of the string
                    endAdr = info['endAdr']
                    
                    # Iterate over the memory used by the string and return it to freeram
                    for addr in range(startAdr, endAdr):
                        self.freeram.append(addr)
                    
                    # Ensure the addresses are in order (optional but makes it more organized)
                    self.freeram.sort()
                else:
                    # For non-String types, just return the variable's address to freeram
                    self.freeram.append(info['adr'])
                
                # Remove the variable from the dictionary
                del self.variables[varname]
            if line.startswith("!"):
                tagname = line[1:]
                self.addCode(f".{tagname}")
            if keyword == "goto":
                self.addCode(f"JMP .{linedata[1]}")
            if keyword == "if":
                valA = linedata[1]
                condition = linedata[2]
                condMap = {"==": "NE", "!=": "EQ"}
                valB = linedata[3]

                if_counter += 1
                label = f".if_{str(if_counter)}"
                self.ongoingInternalGroups.insert(0, {'type': "if", 'label': label})

                self.getValue(valA, 6)
                self.getValue(valB, 7)
                self.addCode(f"CMP r6 r7")
                self.addCode(f"BRH {condMap[condition]} {label}")
            if keyword == "forever":
                forever_counter += 1
                label = f".forever_{str(forever_counter)}"
                self.addCode(label)
                self.ongoingInternalGroups.insert(0, {'type': "forever", 'label': label})

            if keyword == "while":
                valA = linedata[1]
                condition = linedata[2]
                valB = linedata[3]
                condMap = {"==": "EQ", "!=": "NE"}
                while_counter += 1
                label = f".while_{str(while_counter)}"
                self.ongoingInternalGroups.insert(0, {'type': "while", 'label': label, 'cond': condMap[condition], 'vala': valA, 'valb': valB})
                self.addCode(label)
            
            if keyword == "}":
                if len(self.ongoingInternalGroups) == 0:
                    raise MemoryError("No open {")
                data = self.ongoingInternalGroups.pop(0)
                if data['type'] == "if":
                    self.addCode(data['label'])
                elif data['type'] == "forever":
                    self.addCode(f"JMP {data['label']}")
                elif data['type'] == "while":
                    print(data)
                    self.getValue(data['vala'], 6)
                    self.getValue(data['valb'], 7)
                    self.addCode(f"CMP r6 r7")
                    self.addCode(f"BRH {data['cond']} {data['label']}")



# Parse the code
name = ""
functions = {}
temp = []
scanningFunction = False
scanningNestedCode = 0

for line in data:
    words = line.split()
    if line == "}":
        if scanningNestedCode > 0:
            scanningNestedCode -= 1
        else:
            scanningFunction = False
            functions[name] = temp
            temp = []
            name = ""

    if scanningFunction:
        temp.append(line)
    # hi!    
    if words[0] == "fn":
        scanningFunction = True
        name = words[1]
    
    if words[len(words) - 1] == "{":
        if not words[0] == "fn":
            scanningNestedCode += 1


print(functions)


program = ["CAL .Main\n", "HLT\n"]
c = Compiler({}, functions, program)

# Compiling
variables = {}
for function in functions.keys():
    hasRet = False
    c.program.append("." + function + "\n")
    lines = functions[function]
    for line in lines:
        c.compileLine(line)
        if "return" in line.split(" "):
            hasRet = True
    if not hasRet:
        raise BufferError("No return!")


# Add RET statements
for module in c.moduleCode:
    c.program.extend(module)

print("Program:" + "".join(c.program))
with open("main.as", "w") as f:
    f.write("".join(c.program))
