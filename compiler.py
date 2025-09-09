def isInt(value):
    try:
        temp = int(value)
    except ValueError:
        return False
    return True
def isFunctionCall(value):
    itemArray = list(value)
    
    if itemArray[len(itemArray) - 1] == ")" and "(" in itemArray and len(value.split("(")) == 2 and value.split("(")[0] != "":
        return True

    return False
def getType(value):
    itemArray = list(str(value))

    if isInt(value):
        return "int"
    elif itemArray[len(itemArray)-1] == "'" and len(itemArray) == 3 and itemArray[0] == "'":
        return "char"
    elif itemArray[0] == "[" and itemArray[len(itemArray)-1] == "]":
        return "array"
    elif value.startswith("enum."):
        return "enumval"
    elif itemArray[len(itemArray)-1] == '"' and itemArray[0] == '"':
        return "String"
    elif itemArray[0] == "#":
        return "sysvar"
    elif len(value.split("[")) == 2 and itemArray[len(itemArray)-1] == "]":
        return "arrayitem"
    else:
        return "None"

class Compiler:
    def __init__(self, data, ouput="main.as", addComments=False):
        self.modules = []
        self.addComments = addComments
        self.output = ouput
        self.program = []
        self.identifiers = {'a': {'adr': "236"},'b': {'adr': "237"},'c': {'adr': "238"},'d': {'adr': "239"}}
        self.freeram = list(range(228))
        self.ifcounter = 0
        self.whilecounter = 0
        self.forevercounter = 0
        self.registers = [0] * 16

        # Optimization: Collect used variables
        self.used_vars = set()
        self.collect_used_vars(data)

        self.compileProgram(data)
        print(self.identifiers)

        return None

    def collect_used_vars(self, data):
        """Collect variables that are used in the program."""
        for funcname, lines in data.items():
            for line in lines:
                expr = line.get('expression')
                if expr == "VARDECL":
                    # va might be a variable
                    if getType(str(line['va'])) == "None" and not isFunctionCall(line['va']):
                        self.used_vars.add(line['va'])
                elif expr == "VARMUTATION":
                    self.used_vars.add(line['ia'])
                    if getType(line['va']) == "None" and not isFunctionCall(line['va']):
                        self.used_vars.add(line['va'])
                elif expr in ["IFSTATEMENT", "WHILELOOP"]:
                    for key in ['va', 'vb']:
                        if key in line and getType(line[key]) == "None" and not isFunctionCall(line[key]):
                            self.used_vars.add(line[key])
                elif expr == "WRITETO":
                    for key in ['va', 'vb']:
                        if key in line and getType(line[key]) == "None" and not isFunctionCall(line[key]):
                            self.used_vars.add(line[key])
                elif expr == "DATARETURN":
                    if 'va' in line and getType(line['va']) == "None" and not isFunctionCall(line['va']):
                        self.used_vars.add(line['va'])
                elif expr == "FUNCCALL":
                    for key in ['pa', 'pb', 'pc', 'pd']:
                        if key in line and getType(line[key]) == "None" and not isFunctionCall(line[key]):
                            self.used_vars.add(line[key])

    def compileProgram(self, data):
        self.nestedBrackets = []
        for funcname in data.keys():
            self.identifiers[f"{funcname}()"] = {'type': "function"}

        self.addCode("CAL .Main")
        self.addCode("RET\n")
        self.compileFunction("Main", data["Main"])
        for funcname in data.keys():
            if funcname != "Main":
                self.compileFunction(funcname, data[funcname])
        
        self.writeCompiled()
    def addCode(self, code):
        self.program.append(f"{code}\n")


    def getValue(self, value, register):
        # Check the type
        valtype = getType(value)
        # print(valtype)

        if valtype == "None" and not isFunctionCall(value):
            # print(self.identifiers.keys())
            self.used_vars.add(value)  # Mark as used
            if not value in self.identifiers.keys():
                raise KeyError(f"Uknown identifier '{value}'")
            
            idVal = self.identifiers[value]
            if type(idVal) == dict and "type" in idVal.keys() and (idVal['type'] == "array" or idVal['type'] == "String"):
                print(idVal['type'])
                self.addCode(f"LDI r{register} {self.identifiers[value]['adr']}")
                return
            

            # print("loading var")
            adr = self.identifiers[value]['adr']
            self.addCode(f"LDI r4 {adr}")
            self.addCode(f"LOD r4 r{register}")
        else:
            if valtype == "int" or valtype == "char":
                self.addCode(f"LDI r{register} {value}")
            elif valtype == "sysvar":
                self.getValue(value[1:], "15")
                self.addCode(f"LOD r15 r{register}")
            elif valtype == "arrayitem":
                identifier = value.split("[")[0]
                self.used_vars.add(identifier)  # Mark as used
                adr = self.identifiers[identifier]['adr']
                itemIndex = value.split("[")[1][:-1]
                self.addCode(f"LDI r15 {int(adr) + int(itemIndex)}")
                self.addCode(f"LOD r15 r{register}")
            elif valtype == "enumval":
                enumval = value.split(".")[1]
                enumvalMap = {'W': "8", "A": "1", "S": "2", "D": "4", "T": "64", "Y": "128", "J": "16", "K": "32"}
                self.addCode(f"LDI r{register} {enumvalMap[enumval]}")
            elif isFunctionCall(value): 
                line = (value.split("(")[1][:-1]).split(",")
                # print(line)
                for i in range(0, 3):
                    try:
                        val = line[i]
                        self.getValue(val, "7")
                        self.addCode(f"LDI r15 {236 + i}")
                        self.addCode("STR r15 r7")

                    except (KeyError, IndexError) as e:
                        continue
                self.addCode(f"CAL .{value.split('(')[0]}")
                self.addCode("LDI r15 231")
                self.addCode(f"LOD r15 r{register}")
            else:
                raise SyntaxError("Can't load value of type String in a single register.")



    def compileFunction(self, functionname, functiondata):
        self.addCode(f".{functionname}")
        for line in functiondata:
            self.compileLine(line)

        # We'll enforce return for now, might add it as a safety feature. Double RET can't hurt I guess.
        self.addCode("RET")
    
    def compileLine(self, line):
        if line['raw'].split(' ')[0] == "include":
            return
        if self.addComments:
            self.addCode(f"; {line['raw']}")
        expression = line['expression']
        if expression == "NULLRETURN":
            self.addCode("RET")
        elif expression == "VARDECL":
            valtype = line['ta']
            if valtype in ["int", "char"]:
                if line['ia'] not in self.used_vars:
                    # Skip allocation for unused variables
                    if self.addComments:
                        self.addCode(f"; {line['raw']} - IGNORED: unused variable")
                    return
                adr = self.freeram.pop(0)
                self.identifiers[line['ia']] = {'adr': adr, 'type': valtype}
                self.getValue(line['va'], "1")
                self.addCode(f"LDI r3 {adr}")
                self.addCode(f"STR r3 r1")
            elif valtype == "array":
                ialist = list(line['ia'])
                if not ialist[len(ialist)-1] == "]" and len(ialist.split("[")) == 2 and ialist.split("[")[0] != "":
                    raise SyntaxError("No array heap given")
                arrayHeap = line['ia'].split("[")[1][:-1]

                arrayItems = line['va'][1:-1].split(",")
                try:
                    adrPointer = adr
                except Exception as e:
                    print(f"Error: {e} on line {line}")
                
                for p in range(adr, adr + len(arrayItems) + 1):
                    self.freeram.pop(0)

                while adrPointer <= adr + len(arrayItems):
                    try:
                        self.addCode(f"LDI r15 {adrPointer}")
                        self.getValue(arrayItems[adrPointer - adr], "6")
                        self.addCode("STR r15 r6")
                    except IndexError:
                        adrPointer += 1
                        continue

                    adrPointer += 1


                vardata = {'adr': adr, 'endadr': adr + int(arrayHeap), 'type': 'array'}
                self.identifiers[line['ia'].split('[')[0]] = vardata
            
            elif valtype == "String":
                arrayItems = line['va'][1:-1]
                arrayHeap = len(arrayItems)
                adrPointer = adr
                
                for p in range(adr, adr + len(arrayItems) + 1):
                    self.freeram.pop(0)

                while adrPointer <= adr + len(arrayItems):
                    try:
                        self.addCode(f"LDI r15 {adrPointer}")
                        # self.addCode(f"LDI r6 {arrayItems[adrPointer - adr]}")
                        self.getValue("'" + arrayItems[adrPointer - adr] + "'", "6")
                        self.addCode("STR r15 r6")
                    except IndexError:
                        adrPointer += 1
                        continue

                    adrPointer += 1


                vardata = {'adr': adr, 'endadr': adr + int(arrayHeap), 'type': 'String'}
                self.identifiers[line['ia'].split('[')[0]] = vardata
            else:
                raise SyntaxError("Type String not implemented yet.")
        elif expression == "VARMUTATION":
            identifier = line['ia']
            self.used_vars.add(identifier)  # Ensure marked as used
            mutationtype = line['ma']
            mutationvalue = line['va']
            adr = self.identifiers[identifier]['adr']

            self.getValue(mutationvalue, "4")
            self.addCode(f"LDI r2 {adr}")
            self.addCode(f"LOD r2 r6")
            if mutationtype == "+=":
                self.addCode(f"ADD r6 r4 r6")
            elif mutationtype == "-=":
                self.addCode(f"SUB r6 r4 r6")
            else:
                self.addCode("MOV r4 r6")
            self.addCode(f"STR r2 r6")
        elif expression == "IFSTATEMENT":
            self.getValue(line['va'], "4")
            self.getValue(line['vb'], "5")

            condmap = {"==": "NE", "!=": "EQ", ">": "LT"}
            cond = condmap[line['ca']]

            label = f".if_{self.ifcounter}"
            self.ifcounter += 1

            self.addCode("CMP r4 r5")
            self.addCode(f"BRH {cond} {label}")

            self.nestedBrackets.insert(0, {"type": expression, "label": label})
        
        elif expression == "WHILELOOP":
            self.whilecounter += 1
            label = f".while_{self.whilecounter}"
            self.addCode(label)
            # self.getValue(line['va'], "7")
            # self.getValue(line['vb'], "8")
            condmap = {"==": "EQ", "!=": "NE", "<": "LT"}
            cond = condmap[line['ca']]

            self.nestedBrackets.insert(0, {"type": expression, "label": label, "va": line['va'], "vb": line['vb'], "cond": cond})

        elif expression == "WRITETO":
            self.getValue(line['va'], "7")
            self.getValue(line['vb'], "8")
            self.addCode("STR r8 r7")

        elif expression == "DATARETURN":
            self.getValue(line['va'], "9")
            self.addCode(f"LDI r15 231")
            self.addCode("STR r15 r9")
            self.addCode("RET")

        elif expression == "FOREVERLOOP":
            self.forevercounter += 1
            label = f".forever_{self.forevercounter}"

            self.addCode(label)

            self.nestedBrackets.insert(0, {"type": expression, "label": label})

        elif expression == "FUNCCALL":
            if not "pa" in line.keys():
                self.addCode(f"CAL .{line['ia']}")
            else:
                letterMap = ["a", "b", "c", "d"]

                for i in range(0, 3):
                    try:
                        val = line[f'p{letterMap[i]}']
                        self.getValue(val, "7")
                        self.addCode(f"LDI r15 {236 + i}")
                        self.addCode("STR r15 r7")

                    except KeyError:
                        continue
                self.addCode(f"CAL .{line['ia']}")
                    

        elif expression == "CLOSINGBRACKET":
            if len(self.nestedBrackets) < 1:
                raise SyntaxError("Unexpected closing bracket")

            data = self.nestedBrackets.pop(0)
            if data['type'] == "IFSTATEMENT":
                self.addCode(data['label'])
            elif data['type'] == "WHILELOOP":
                self.getValue(data['va'], "7")
                self.getValue(data['vb'], "8")

                self.addCode("CMP r7 r8")
                self.addCode(f"BRH {data['cond']} {data['label']}")
            elif data['type'] == "FOREVERLOOP":
                self.addCode(f"JMP {data['label']}")
        else:
            raise SyntaxError(f"Not implemented expression found: {expression}")
            

    
    def writeCompiled(self):
        data = "".join(self.program)
        with open(self.output, 'w') as f:
            f.write(data)

        return True