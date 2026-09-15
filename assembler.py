import opcode
import sys
import os
import subprocess


filename = sys.argv[1]
if len(sys.argv) > 2:
    outfilename = sys.argv[2]
else:
    outfilename = "output/" + os.path.basename(filename).replace("asm", "bin")


print("Source: " + filename)
print("Output: " + outfilename)
print()



OPCODES = {
    "JMP" : { "IN": None, "IM": 0xB1, "ABS": None, "ABS_ZP": None},
    "BCS" : { "IN": None, "IM": 0xB2, "ABS": None, "ABS_ZP": None},
    "BCC" : { "IN": None, "IM": 0xB3, "ABS": None, "ABS_ZP": None},
    "BEQ" : { "IN": None, "IM": 0xB4, "ABS": None, "ABS_ZP": None},
    "BNE" : { "IN": None, "IM": 0xB5, "ABS": None, "ABS_ZP": None},
    "LDA" : { "IN": 0x60, "IM": 0xB6, "ABS": 0xC6, "ABS_ZP": 0x06, "IND": 0xF6, "IND_ZP": 0xE6},
    "STA" : { "IN": 0x70, "IM": None, "ABS": 0xC7, "ABS_ZP": 0x07, "IND": 0xF7, "IND_ZP": 0xE7},
    "ADD" : { "IN": 0x80, "IM": 0xB8, "ABS": 0xC8, "ABS_ZP": None, "ABS_IP": 0xD8, "IND": 0xE8, "IND_ZP": None},
    "SUB" : { "IN": 0x90, "IM": 0xB9, "ABS": 0xC9, "ABS_ZP": None, "ABS_IP": 0xD9, "IND": 0xE9, "IND_ZP": None},
    "ADC" : { "IN": 0x10, "IM": 0xBC, "ABS": 0xCC, "ABS_ZP": None, "ABS_IP": 0xDC, "IND": 0xEC, "IND_ZP": None},
    "SBC" : { "IN": 0x20, "IM": 0xBD, "ABS": 0xCD, "ABS_ZP": None, "ABS_IP": 0xDD, "IND": 0xED, "IND_ZP": None},
    "CMP" : { "IN": 0xA0, "IM": 0xBA, "ABS": 0xCA, "ABS_ZP": 0x0A},
    "CPY" : { "IN": None, "IM": None, "ABS": 0xCB, "ABS_ZP": None},
    "TAS" : { "IN": 0xF1, "IM": None, "ABS": None, "ABS_ZP": None},
    "CLF" : { "IN": 0xF2, "IM": None, "ABS": None, "ABS_ZP": None},
    "SEF" : { "IN": 0xF3, "IM": None, "ABS": None, "ABS_ZP": None},
    "HLT" : { "IN": 0xFF, "IM": None, "ABS": None, "ABS_ZP": None},
    "NOP" : { "IN": 0x00, "IM": None, "ABS": None, "ABS_ZP": None},
}

PROGRAM = [OPCODES["HLT"]["IN"]] * 8192
LOCATIONS = {}
VARIABLES = {}

def parse_instruction(line, counter, linenumber):
    parts = line.split(" ", 1)

    #% store a number in the program (for data)
    if parts[0].startswith("%"):
         num = int(parts[0][1:])
         return num

    if parts[0].startswith(":"):
        label = parts[0][1:]
        LOCATIONS[label] = counter
        return None
    
    #if parts[0].startswith("*"):
    #    label = parts[0][1:]
    #    if label not in LOCATIONS:
    #        print("Undefined label: " + label)
    #        exit(1)
    #    num = LOCATIONS[label]
    #    return num
    
    #if parts[0].startswith("."):
    #    varname = parts[0][1:]
    #    if varname in VARIABLES:
    #        print("Duplicate variable: " + varname)
    #        exit(1)
    #    VARIABLES[varname] = counter
    #    return None

    opcode = OPCODES.get(parts[0], None)
    print("Line " + str(linenumber) + " - Processing opcode: " + parts[0])
    if opcode is None:
        print("Unknown instruction: " + parts[0])
        exit(1)
    
    #handle Implied instructions which have no operand
    if len(parts) == 1:
        return opcode["IN"]
    
    #handle chars as operands - forces immediate addressing mode
    if parts[1].startswith("'"):
        print("operand: " + parts[1])
        char = parts[1][1]
        num = ord(char)
        if char == '\\':
            char = parts[1][2]
            if char == 'n':
                num = 10
            if char == 'r':
                num = 13
            if char == '\\':
                num = ord(char)
        
        if opcode["IM"] is not None:
            return [opcode["IM"], num]
        else:
            print("Chars are only supported for opcodes with Immediate addressing mode")

    #Absolute addressing with a variable
    #TODO: make this work with potential 16 bit variable values, especially when not yet defined
    if parts[1].startswith("."):
        if ',' in parts[1]:
            varname, num_str = parts[1].split(",")
            if not varname.startswith(".") or not num_str.startswith("$"):
                print("Invalid ABS,IMM addressing: " + parts[1])
                exit(1)
            varname = varname[1:]
            num = int(num_str[1:])
            if varname not in VARIABLES:
                print("Undefined variable: " + varname)
                return [opcode["ABS_IP"], parts[1]]
            if opcode["ABS_IP"] is not None:
                address = VARIABLES[varname]
                numlow = address & 0xFF
                numhigh = (address & 0xFF00) >> 8
                #little endian format
                return [opcode["ABS_IP"], numlow, numhigh, num]
            else:
                print("Instruction does not support ABS IP addressing: " + parts[0])
                exit(1)
        else:
            varname = parts[1][1:]
            if varname not in VARIABLES:
                print("Undefined variable: " + varname)
                return [opcode["ABS"], parts[1]]
            num = VARIABLES[varname]
            if num <= 255 and opcode["ABS_ZP"] is not None:
                #zero page addressing
                return [opcode["ABS_ZP"], num]
            else:
                #full 16 bit address
                if opcode["ABS"] is not None:
                    numlow = num & 0xFF
                    numhigh = (num & 0xFF00) >> 8
                    #little endian format
                    return [opcode["ABS"], numlow, numhigh]
                else:
                    print("Instruction does not support absolute addressing: " + parts[0])
                    exit(1)
            #if num < 16 and opcode["IN"] is not None:
            #    return opcode["IN"] | num
            #else:
            #    if opcode["IM"] is not None:
            #        return [opcode["IM"], num]
            #    else:
            #        return [opcode["ABS"], num]


    #Immediate addressing modes
    #operand is a number, either hex ($0xAB) or int ($171)
    if parts[1].startswith("$"):
        num = int(parts[1][1:],0)
        #use immediate nibble if available for this opcode
        if num < 16 and opcode["IN"] is not None:
            return opcode["IN"] | num
        #otherwise use immediate mode
        elif opcode["IM"] is not None:
            return [opcode["IM"], num]
        else:
            print("Invalid Immediate addressing: " + parts[1])
            exit(1)
        
    #Absolute addressing
    elif parts[1].startswith("#$"):
        #TODO: fix this up to work with X indexed
        #currently won't work correctly with 16 bit addressing
        if ',' in parts[1]:
            addr_str, num_str = parts[1].split(",")
            if not addr_str.startswith("$") or not num_str.startswith("#"):
                print("Invalid ABS,IMM addressing: " + parts[1])
                exit(1)
            addr = int(addr_str[1:])
            num = int(num_str[1:])
            if opcode["ABS_IP"] is not None:
                return [opcode["ABS_IP"], addr, num]
            else:
                print("Instruction does not support ABS IP addressing: " + parts[0])
                exit(1)

        #non-indexed
        else:
            num = int(parts[1][2:],0)
            if num <= 255 and opcode["ABS_ZP"] is not None:
                #zero page addressing
                return [opcode["ABS_ZP"], num]
            else:
                #full 16 bit address
                if opcode["ABS"] is not None:
                    numlow = num & 0xFF
                    numhigh = (num & 0xFF00) >> 8
                    #little endian format
                    return [opcode["ABS"], numlow, numhigh]
                else:
                    print("Instruction does not support absolute addressing: " + parts[0])
                    exit(1)

    elif parts[1].startswith(":"):
        label = parts[1][1:]
        if label not in LOCATIONS:
            print("Undefined label: " + label)
            return [opcode["IM"], parts[1]]
        num = LOCATIONS[label]
        if num < 16 and opcode["IN"] is not None:
            return opcode["IN"] | num
        else:
            return [opcode["IM"], num]
        
    #Indirect addressing
    #TODO add support for Indirect X indexed
    elif parts[1].startswith("("):
        if not parts[1].endswith(")"):
            print("Invalid indirect addressing: " + parts[1])
            exit(1)
        if opcode["IND"] is not None:
            inner = parts[1][1:-1]
            print("Parsing indirect addressing: " + inner)
            if inner.startswith("$"):
                num = int(inner[1:])
                if num <= 255 and opcode["IND_ZP"] is not None:
                    return [opcode["IND_ZP"], num]
                else:
                    numlow = num & 0xFF
                    numhigh = (num & 0xFF00) >> 8
                    #little endian format
                    return [opcode["IND"], numlow, numhigh]
            elif inner.startswith("."):
                varname = inner[1:]
                if varname not in VARIABLES:
                    #TODO: ensure this works for 16 bit addresses we don't know about yet
                    print("WARN: variable not defined: " + varname)
                    return [opcode["IND"], inner]
                else:
                    num = VARIABLES[varname]
                    if num <= 255 and opcode["IND_ZP"] is not None:
                        return [opcode["IND_ZP"], num]
                    else:
                        numlow = num & 0xFF
                        numhigh = (num & 0xFF00) >> 8
                        #little endian format
                        return [opcode["IND"], numlow, numhigh]
        else:
            print("Instruction does not support indirect addressing: " + parts[0])
            exit(1)

    else:
        print("Invalid operand: " + parts[1])
        exit(1)
        
         

with open(outfilename,"wb") as outfile, open(filename, 'r') as sourcefile:
    print("Compiling source code...")

    counter = 0

    print("Inserting NOPs at start of program")
    PROGRAM[0] = OPCODES["NOP"]["IN"]
    PROGRAM[1] = OPCODES["NOP"]["IN"]
    PROGRAM[2] = OPCODES["NOP"]["IN"]
    counter += 3

    linenumber = 0

    for line in sourcefile:
        linenumber += 1

        line = line.split(";")[0] #remove comments
        line = line.strip() #remove whitespace
        if line == "" or line.startswith(";"): #skip empty lines and comment lines
            continue
       
        if line.startswith("CONST"):
            print("Line " + str(linenumber) + " - Processing CONST: " + line + " at counter " + str(counter))
            parts = line.split(" ")
            if len(parts) != 3:
                print("Invalid CONST syntax: " + line)
                exit(1)
            varname = parts[1]
            num = int(parts[2], 0)
            if varname in VARIABLES:
                print("Duplicate variable: " + varname)
                exit(1)
            VARIABLES[varname] = num
            continue

        if line.startswith("&"):
            #set location counter
            num = int(line[1:])
            counter = num
            continue

        instruction = parse_instruction(line, counter, linenumber)
        if isinstance(instruction, int):
            if PROGRAM[counter] != OPCODES["HLT"]["IN"]:
                print("ERROR: overwriting instruction at address " + str(counter))
                exit(1)
            print(" - " + format(instruction, '#04x'))
            PROGRAM[counter] = instruction
            counter += 1
        elif isinstance(instruction, list):
            for byte in instruction:
                if PROGRAM[counter] != OPCODES["HLT"]["IN"]:
                    print("ERROR: overwriting instruction at address " + str(counter))
                    exit(1)
                if (isinstance(byte, int)):
                    print(" - " + format(byte, '#04x'))
                else:
                    print(" - " + str(byte))
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

    print(PROGRAM[:counter]) 

    print(LOCATIONS)
    print(VARIABLES)
    print([format(byte, '#04x') for byte in PROGRAM[:counter]])

    
    print("Program compiled successfully, writing output...")
    print("Program size: " + str(counter) + " bytes")

    print("Writing program: " + outfilename)
    outfile.write(bytes(PROGRAM))

answer = input("Program ROM?")
if answer.upper() in ["Y", "YES"]:
    ret = subprocess.run(["minipro", "-p", "AT28C64B", "-w", outfilename])
