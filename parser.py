def isInt(value):
    try:
        temp = int(value)
    except ValueError:
        return False
    return True

def extract_parameters(s):
    open_paren = s.find('(')
    close_paren = s.rfind(')')
    
    if open_paren == -1 or close_paren == -1 or close_paren <= open_paren:
        return []
    
    inner = s[open_paren + 1 : close_paren].strip()
    
    if not inner:
        return []
    
    return [param.strip() for param in inner.split(',') if param.strip()]

def getType(value):
    itemArray = list(value)
    if isInt(value):
        return "int"
    elif itemArray[len(itemArray)-1] == "'" and len(itemArray) == 3 and itemArray[0] == "'":
        return "char"
    elif itemArray[0] == "[" and itemArray[len(itemArray)-1] == "]":
        return "array"
    elif itemArray[len(itemArray)-1] == '"' and itemArray[0] == '"':
        return "String"
    else:
        return "None"

def isFunctionCall(value):
    itemArray = list(value)
    
    if itemArray[len(itemArray) - 1] == ")" and "(" in itemArray and len(value.split("(")) == 2 and value.split("(")[0] != "":
        return True
    
    # if "(" in itemArray and 

    return False
# print(isFunctionCall("test(1, 5)"))
class Parser:
    def __init__(self, data, forceMainFunction=True):
        self.forceMainFunction = forceMainFunction
        data = data.replace("\n", "")
        data = data.split(";")
        data = [item.strip() for item in data]
        self.parseProgram(data)

    def parseProgram(self, data):
        self.parsed = []
        self.finalParsed = {}
        currentFuncName = ""

        openBracketCount = 0
        readingFunc = False
        for line in data:
            if line.strip() == "" or line.strip().startswith("//"):
                continue
            lineList = line.split(" ")
            if lineList[0] == "fn" and len(lineList) == 3 and lineList[len(lineList)-1] == "{":
                if readingFunc:
                    raise SyntaxError("Cannot have nested functions")
                readingFunc = True
                currentFuncName = lineList[1]
            elif line == "}":
                if readingFunc and openBracketCount == 0:
                    readingFunc = False
                    self.finalParsed[currentFuncName] = self.parsed
                    self.parsed = []

                else:
                    openBracketCount -= 1
            
                    if openBracketCount < 0:
                        raise SyntaxError("Uknown closing bracket")
                    self.parsed.append(self.parseLine(line))
                
            elif line.split(" ")[len(line.split(" "))-1] == "{":
                openBracketCount += 1
                self.parsed.append(self.parseLine(line))
            else:
                if not readingFunc:
                    if len(lineList) == 2 and lineList[0] == "include":
                        
                        with open(f"tl_modules/{lineList[1]}.tl", 'r') as mf:
                            mfdata = mf.read()
                            # mfdata = mfdata.split("\n")
                            # mfdata = [line.strip() for line in mfdata]
                        moduleParser = Parser(mfdata, False)
                        self.finalParsed = moduleParser.finalParsed | self.finalParsed
                    else:
                        raise SyntaxError("Can't read code outside of functions. If you have an empty function, make sure to split the brackets with a new line.\n" + line)
                self.parsed.append(self.parseLine(line))
        
        if not "Main" in self.finalParsed.keys():
            if self.forceMainFunction:
                raise SyntaxError("No Main function found!")
        if openBracketCount > 0 or readingFunc:
            raise SyntaxError("Brackets not closed!")

    def parseLine(self, line):
        if line.strip() == "":
            return
        parsedLine = {}
        expression = ""


        a = ""
        def parseItem(item):
            itemArray = list(item)
            if item in ["String", "int", "char", 'array']:
                a = "t"
            elif item == "=":
                a = "d"
            elif "[" in list(item) and item.endswith("]") and "," not in list(item):
                a = "l"
            elif getType(item) != "None":
                a = "v"
            elif item == "+=" or item == "-=":
                a = "m"
            elif item == "{":
                a = "{"
            elif item == "while":
                a = "w"
            elif item == "to":
                a = ">"
            elif item == "write":
                a = "*"
            elif item == "forever":
                a = "f"
            elif item == "if":
                a = "s"
            elif item in ["==", "!=", ">", "<", ">=", "<="]:
                a = "c"
            elif item == "}":
                a = "}"
            elif item == "return":
                a = "r"
            elif isFunctionCall(item):
                a = "b"

            else:
                a = "i"
                
            
            return a
        
        def isAbrMatch(item, comparison):
            matchingChars = 0
            for i, char in enumerate(list(item)):
                # When the item is longer than the comparison:
                try:
                    comparisonChar = comparison[i]
                except IndexError:
                    return
                
                if (char == comparisonChar) or (comparisonChar == "v" and (char == "i" or char == "b")) or (comparisonChar == "m" and char == "d"):
                    matchingChars += 1
            
            if matchingChars != len(list(item)):
                return False
            
            return True

        lineParsed = []
        lineAbr = ""
        lineList = line.split(" ")
        for item in line.split(" "):
            parsedItem = parseItem(item)

            lineParsed.append({"abr": parsedItem, "posVal": parsedItem == "v" or parsedItem == "i"})
            lineAbr = lineAbr + parsedItem

        try:
            if isAbrMatch(lineAbr, "tidv"):
                expression = "VARDECL"
                parsedLine['ta'] = lineList[0]
                parsedLine['ia'] = lineList[1]
                if len(lineList) == 2:
                    parsedLine['va'] = 0
                else:
                    parsedLine['va'] = lineList[3]
            elif isAbrMatch(lineAbr, "ti"):
                expression = "VARDECL"
                parsedLine['ta'] = lineList[0]
                parsedLine['ia'] = lineList[1]
                parsedLine['va'] = 0
            elif isAbrMatch(lineAbr, "imv"):
                expression = "VARMUTATION"
                parsedLine['ia'] = lineList[0]
                parsedLine['ma'] = lineList[1]
                parsedLine['va'] = lineList[2]
            elif isAbrMatch(lineAbr, "ldv"):
                expression = "LISTMUTATION"
                list_access = lineList[0]
                list_name = list_access.split('[')[0]
                index = list_access.split('[')[1].rstrip(']')
                parsedLine['ia'] = list_name
                parsedLine['idx'] = index
                parsedLine['va'] = lineList[2]
                print(parsedLine)
            elif isAbrMatch(lineAbr, "r"):
                expression = "NULLRETURN"
            elif isAbrMatch(lineAbr, "rv"):
                expression = "DATARETURN"
                parsedLine['va'] = lineList[1]
            elif isAbrMatch(lineAbr, "svcv{"):
                expression = "IFSTATEMENT"
                parsedLine['va'] = lineList[1]
                parsedLine['ca'] = lineList[2]
                parsedLine['vb'] = lineList[3]
            elif lineAbr == "}":
                expression = "CLOSINGBRACKET" 
            elif isAbrMatch(lineAbr, "*v>v"):
                expression = "WRITETO"
                parsedLine['va'] = lineList[1]
                parsedLine['vb'] = lineList[3]
            elif isAbrMatch(lineAbr, "f{"):
                expression = "FOREVERLOOP"
            elif isAbrMatch(lineAbr, "wvcv{"):
                expression = "WHILELOOP"
                parsedLine['va'] = lineList[1]
                parsedLine['ca'] = lineList[2]
                parsedLine['vb'] = lineList[3]
            elif isAbrMatch(lineAbr, "b"):
                expression = "FUNCCALL"
                parsedLine['ia'] = line.split("(")[0]
                
                parameters = extract_parameters(line)
                
                letterMap = ["a", "b", "c", "d"]
                letterI = 0
                
                for parameter in parameters:
                    parsedLine[f'p{letterMap[letterI]}'] = parameter
                    letterI += 1
                
                


            else:
                print(lineAbr)
                if not (len(lineList) == 2 and lineList[0] == "include"):
                    raise SyntaxError(f"Invalid syntax ->\n{line}")
                else:
                    expression = "INCLUDESTATEMENT"
        except Exception as e:
            print(f"Error '{e}' on line {line}")
        parsedLine["expression"] = expression
        parsedLine['raw'] = line
        return parsedLine