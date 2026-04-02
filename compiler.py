import sys

print(sys.argv[1])

filename = sys.argv[1]
outfilename = sys.argv[2]


OPCODES = {
    "JMP" : { "IN": 0x10, "IM": 0xB1, "ABS": None},
    "BCS" : { "IN": 0x20, "IM": 0xB2, "ABS": None},
    "BCC" : { "IN": 0x30, "IM": 0xB3, "ABS": None},
    "BEQ" : { "IN": 0x40, "IM": 0xB4, "ABS": None},
    "BNE" : { "IN": 0x50, "IM": 0xB5, "ABS": None},
    "LDA" : { "IN": 0x60, "IM": 0xB6, "ABS": 0xC6, "IND": 0xD6},
    "STA" : { "IN": 0x70, "IM": None, "ABS": 0xC7, "IND": 0xD7},
    "ADD" : { "IN": 0x80, "IM": 0xB8, "ABS": 0xC8, "IND": 0xD8},
    "SUB" : { "IN": 0x90, "IM": 0xB9, "ABS": 0xC9, "IND": 0xD9},
    "CMP" : { "IN": 0xA0, "IM": 0xBA, "ABS": 0xCA},
    "TAO" : { "IN": 0xF0, "IM": None, "ABS": None},
    "HLT" : { "IN": 0xFF, "IM": None, "ABS": None},
    "NOP" : { "IN": 0x00, "IM": None, "ABS": None},
}

print(OPCODES["JMP"])

PROGRAM = [OPCODES["HLT"]["IN"]] * 8192
LOCATIONS = {}
VARIABLES = {}

def parse_instruction(line, counter):
    parts = line.split(" ")

    #% store a number in the program (for data)
    if parts[0].startswith("%"):
         num = int(parts[0][1:])
         return num

    if parts[0].startswith(":"):
        label = parts[0][1:]
        LOCATIONS[label] = counter
        return None
    
    if parts[0].startswith("*"):
        label = parts[0][1:]
        if label not in LOCATIONS:
            print("Undefined label: " + label)
            exit(1)
        num = LOCATIONS[label]
        return num
    
    if parts[0].startswith("."):
        varname = parts[0][1:]
        if varname in VARIABLES:
            print("Duplicate variable: " + varname)
            exit(1)
        VARIABLES[varname] = counter
        return None

    opcode = OPCODES.get(parts[0], None)
    print("Processing opcode: " + parts[0])
    if opcode is None:
        print("Unknown instruction: " + parts[0])
        exit(1)
    
    if len(parts) == 1:
        return opcode["IN"]
    
    if parts[1].startswith("."):
        varname = parts[1][1:]
        if varname not in VARIABLES:
            print("Undefined variable: " + varname)
            return [opcode["ABS"], parts[1]]
        num = VARIABLES[varname]
        if opcode["ABS"] is not None:
            return [opcode["ABS"], num]
        else:
            print("Instruction does not support absolute addressing: " + parts[0])
            exit(1)

    if parts[1].startswith("#"):
        num = int(parts[1][1:])
        if num < 16:
            return opcode["IN"] | num
        else:
            return [opcode["IM"], num]
        
    elif parts[1].startswith("$"):
        num = int(parts[1][1:])
        if opcode["ABS"] is not None:
            return [opcode["ABS"], num]
        else:
            print("Instruction does not support absolute addressing: " + parts[0])
            exit(1)

    elif parts[1].startswith(":"):
        label = parts[1][1:]
        if label not in LOCATIONS:
            print("Undefined label: " + label)
            return [opcode["IM"], parts[1]]
        num = LOCATIONS[label]
        if num < 16:
            return opcode["IN"] | num
        else:
            return [opcode["IM"], num]
        
    elif parts[1].startswith("("):
        if not parts[1].endswith(")"):
            print("Invalid indirect addressing: " + parts[1])
            exit(1)
        if opcode["IND"] is not None:
            inner = parts[1][1:-1]
            print("Parsing indirect addressing: " + inner)
            if inner.startswith("$"):
                num = int(inner[1:])
                return [opcode["IND"], num]
            elif inner.startswith("."):
                varname = inner[1:]
                if varname not in VARIABLES:
                    print("WARN: variable not defined: " + varname)
                    return [opcode["IND"], inner]
                else:
                    num = VARIABLES[varname]
                    return [opcode["IND"], num]
        else:
            print("Instruction does not support indirect addressing: " + parts[0])
            exit(1)

    else:
        print("Invalid operand: " + parts[1])
        exit(1)
        
         

with open(outfilename,"wb") as outfile, open(filename, 'r') as sourcefile:
    print("Compiling source code...")

    counter = 0

    for line in sourcefile:
        line = line.split(";")[0] #remove comments
        line = line.strip() #remove whitespace
        if line == "" or line.startswith(";"): #skip empty lines and comment lines
            continue

        if line.startswith("&"):
            #set location counter
            num = int(line[1:])
            counter = num
            continue

        instruction = parse_instruction(line, counter)
        if isinstance(instruction, int):
            if PROGRAM[counter] != OPCODES["HLT"]["IN"]:
                print("ERROR: overwriting instruction at address " + str(counter))
                exit(1)
            PROGRAM[counter] = instruction
            counter += 1
        elif isinstance(instruction, list):
            for byte in instruction:
                if PROGRAM[counter] != OPCODES["HLT"]["IN"]:
                    print("ERROR: overwriting instruction at address " + str(counter))
                    exit(1)
                PROGRAM[counter] = byte
                counter += 1

    #resolve labels in PROGRAM
    for i in range(0, len(PROGRAM)):
        if isinstance(PROGRAM[i], str):
            label = PROGRAM[i]
            num = None
            if label.startswith(":"):
                label = label[1:]
                if label not in LOCATIONS:
                    print("ERROR: label not defined: " + label)
                    exit(1)
                num = LOCATIONS[label]
            elif label.startswith("."):
                varname = label[1:]
                if varname not in VARIABLES:
                    print("ERROR: variable not defined: " + varname)
                    exit(1)
                num = VARIABLES[varname]

            PROGRAM[i] = num
    print(PROGRAM[0:20])
    print(LOCATIONS)
    print(VARIABLES)
    print("Writing program: " + outfilename)
    outfile.write(bytes(PROGRAM))
