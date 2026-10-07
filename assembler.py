import opcode
import sys
import os
import subprocess
from hexdump import hexdump

filename = sys.argv[1]
if len(sys.argv) > 2:
    outfilename = sys.argv[2]
else:
    outfilename = "output/" + os.path.basename(filename).replace("asm", "bin")


print("Source: " + filename)
print("Output: " + outfilename)
print()



OPCODES = {
    "JMP" : { "IN": None, "IM": None, "ABS": 0xC1, "ABS_X": None, "ABS_ZP": None},
    "BCS" : { "IN": None, "IM": None, "ABS": 0xC2, "ABS_X": None, "ABS_ZP": None},
    "BCC" : { "IN": None, "IM": None, "ABS": 0xC3, "ABS_X": None, "ABS_ZP": None},
    "BEQ" : { "IN": None, "IM": None, "ABS": 0xC4, "ABS_X": None, "ABS_ZP": None},
    "BNE" : { "IN": None, "IM": None, "ABS": 0xC5, "ABS_X": None, "ABS_ZP": None},
    "LDA" : { "IN": 0x60, "IM": 0xB6, "ABS": 0xC6, "ABS_X": 0xD6, "ABS_ZP": 0x06, "IND": 0xF6, "IND_ZP": 0xE6},
    "STA" : { "IN": 0x70, "IM": None, "ABS": 0xC7, "ABS_X": 0xD7, "ABS_ZP": 0x07, "IND": 0xF7, "IND_ZP": 0xE7},
    "ADD" : { "IN": 0x80, "IM": 0xB8, "ABS": 0xC8, "ABS_X": None, "ABS_ZP": None, "ABS_IP": 0xD8, "IND": 0xE8, "IND_ZP": None},
    "SUB" : { "IN": 0x90, "IM": 0xB9, "ABS": 0xC9, "ABS_X": None, "ABS_ZP": None, "ABS_IP": 0xD9, "IND": 0xE9, "IND_ZP": None},
    "ADC" : { "IN": 0x10, "IM": 0xBC, "ABS": 0xCC, "ABS_X": None, "ABS_ZP": None, "ABS_IP": 0xDC, "IND": 0xEC, "IND_ZP": None},
    "SBC" : { "IN": 0x20, "IM": 0xBD, "ABS": 0xCD, "ABS_X": None, "ABS_ZP": None, "ABS_IP": 0xDD, "IND": 0xED, "IND_ZP": None},
    "CMP" : { "IN": 0xA0, "IM": 0xBA, "ABS": 0xCA, "ABS_X": None, "ABS_ZP": 0x0A},
    "CPY" : { "IN": None, "IM": None, "ABS": 0xCB, "ABS_X": None, "ABS_ZP": None},
    "TAS" : { "IN": 0xF0, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "INX" : { "IN": 0xF1, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "CLF" : { "IN": 0xF2, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "SEF" : { "IN": 0xF3, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "TAX" : { "IN": 0xF4, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "TXA" : { "IN": 0xF5, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "HLT" : { "IN": 0xFF, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
    "NOP" : { "IN": 0x00, "IM": None, "ABS": None, "ABS_X": None, "ABS_ZP": None},
}

PROGRAM = [OPCODES["HLT"]["IN"]] * 8192
LOCATIONS = {}

ROMSTART = 0x2000

def parse_instruction(line, counter, linenumber):
    parts = line.split(" ", 1)


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
            addr_str, mode = parts[1].split(",")
            if mode != "X":
                print("Invalid indexed addressing: " + parts[1])
            
            num = int(addr_str[2:],0)
            if num <= 255 and opcode["ABS_ZP"] is not None:
                #zero page addressing
                return [opcode["ABS_ZP_X"], num]
            else:
                #full 16 bit address
                if opcode["ABS_X"] is not None:
                    numlow = num & 0xFF
                    numhigh = (num & 0xFF00) >> 8
                    #little endian format
                    return [opcode["ABS_X"], numlow, numhigh]
                else:
                    print("Instruction does not support absolute,X addressing: " + parts[0])
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
        if ',' in parts[1]:
            label, mode = parts[1].split(",")
            if mode != "X":
                print("Invalid indexed addressing: " + parts[1])
            
            if label[1:] not in LOCATIONS:
                print("Undefined label: " + label)
                return [opcode["ABS_X"], label, None]

            num = LOCATIONS[label]
            #full 16 bit address
            if opcode["ABS_X"] is not None:
                numlow = num & 0xFF
                numhigh = (num & 0xFF00) >> 8
                #little endian format
                return [opcode["ABS_X"], numlow, numhigh]
            else:
                print("Instruction does not support absolute,X addressing: " + parts[0])
                exit(1)
        else:
            label = parts[1][1:]
            if label not in LOCATIONS:
                print("Undefined label: " + label)
                return [opcode["ABS"], parts[1], None]
            num = LOCATIONS[label]
            numlow = num & 0xFF
            numhigh = (num & 0xFF00) >> 8
            #little endian format
            return [opcode["ABS"], numlow, numhigh]
        
    #Indirect addressing
    #TODO add support for Indirect X indexed
    elif parts[1].startswith("("):
        if not parts[1].endswith(")"):
            print("Invalid indirect addressing: " + parts[1])
            exit(1)
        if opcode["IND"] is not None:
            inner = parts[1][1:-1]
            print("Parsing indirect addressing: " + inner)
            if inner.startswith("#$"):
                num = int(inner[1:])
                if num <= 255 and opcode["IND_ZP"] is not None:
                    return [opcode["IND_ZP"], num]
                else:
                    numlow = num & 0xFF
                    numhigh = (num & 0xFF00) >> 8
                    #little endian format
                    return [opcode["IND"], numlow, numhigh]
            elif inner.startswith(":"):
                location = inner[1:]
                if location not in LOCATIONS:
                    #TODO: ensure this works for 16 bit addresses we don't know about yet
                    print("WARN: location not defined: " + location)
                    return [opcode["IND"], inner, None]
                else:
                    num = LOCATIONS[location]
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
        print("ERROR: Invalid operand: " + parts[1])
        exit(1)
        
         

def load_lines(filepath, seen=None):
    """Return a flat list of (line_text, filepath, lineno) tuples,
    recursively expanding .include directives."""
    if seen is None:
        seen = set()
    filepath = os.path.realpath(filepath)
    if filepath in seen:
        print("ERROR: circular .include detected: " + filepath)
        exit(1)
    seen.add(filepath)
    result = []
    with open(filepath, 'r') as f:
        for lineno, line in enumerate(f, 1):
            stripped = line.split(";")[0].strip()
            if stripped.startswith(".include"):
                parts = stripped.split(None, 1)
                if len(parts) != 2:
                    print(f"ERROR: {filepath}:{lineno}: Invalid .include syntax: {stripped}")
                    exit(1)
                include_path = parts[1].strip().strip('"').strip("'")
                # resolve relative to the directory of the including file
                include_path = os.path.join(os.path.dirname(filepath), include_path)
                print(f"Line {lineno} - Including file: {include_path}")
                result.extend(load_lines(include_path, seen))
            else:
                result.append((line, filepath, lineno))
    seen.discard(filepath)
    return result


with open(outfilename,"wb") as outfile:
    print("Compiling source code...")


    counter = 0

    print("Inserting NOPs at start of program")
    PROGRAM[0] = OPCODES["NOP"]["IN"]
    PROGRAM[1] = OPCODES["NOP"]["IN"]
    PROGRAM[2] = OPCODES["NOP"]["IN"]
    counter += 3

    all_lines = load_lines(filename)

    for (line, sourcefile, linenumber) in all_lines:
        line = line.split(";")[0] #remove comments
        line = line.strip() #remove whitespace
        if line == "" or line.startswith(";"): #skip empty lines and comment lines
            continue
       
        if line.startswith(".const"):
            print("Line " + str(linenumber) + " - Processing CONST: " + line + " at counter " + str(counter))
            parts = line.split(" ")
            if len(parts) != 3:
                print("ERROR: Invalid CONST syntax: " + line)
                exit(1)
            constant = parts[1]
            num = int(parts[2], 0)
            if constant in LOCATIONS:
                print("ERROR: Duplicate location: " + constant)
                exit(1)
            LOCATIONS[constant] = num
            continue


        if line.startswith(".org"):
            #set location counter
            print("Line " + str(linenumber) + " - Processing ORG: " + line + " at counter " + str(counter))
            line = line.replace("org", "")
            parts = line.split(" ")
            num = int(parts[1], 0)
            counter = num - ROMSTART
            print(" - New counter: " + str(counter))
            continue

        if line.startswith(".text"):
            print("Line " + str(linenumber) + " - Processing TEXT: " + line + " at counter " + str(counter))
            parts = line.replace(".text ", "")
            
            text = parts[1:-1]
            print(" - Inserting text: " + text)
            for char in text:
                byte = ord(char)
                PROGRAM[counter] = byte
                counter = counter + 1

            continue

        if line.startswith(".byte"):
            print("Line " + str(linenumber) + " - Processing BYTE: " + line + " at counter " + str(counter))
            parts = line.split(" ")

            byte = int(parts[1][1:],0)
            PROGRAM[counter] = byte
            counter = counter + 1
            continue

        if line.startswith(".word"):
            print("Line " + str(linenumber) + " - Processing WORD: " + line + " at counter " + str(counter))
            parts = line.split(" ")

            num = int(parts[1][1:],0)
            numlow = num & 0xFF
            numhigh = (num & 0xFF00) >> 8
            #little endian format

            PROGRAM[counter] = numlow
            PROGRAM[counter+1] = numhigh
            counter = counter + 2
            continue

        if line.endswith(":"):
            label = line[0:-1]
            LOCATIONS[label] = counter + ROMSTART
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
                #locations should only appear in absolute calls, so can directly insert the 2 bytes
                PROGRAM[i] = num & 0xFF
                PROGRAM[i+1] = (num & 0xFF00) >> 8


    print()
    print("Known labels:")

    print("-" * 34)
    for key, value in LOCATIONS.items():
        print(f'{key:15}|{str(value):^10}|{hex(value):>7}')
    print("-" * 34)


    
    print()
    print(hexdump(PROGRAM))
    print()

    print("Program compiled successfully, writing output...")
    print("Program size: " + str(counter) + " bytes")

    print("Writing program: " + outfilename)
    outfile.write(bytes(PROGRAM))

answer = input("Program ROM?")
if answer.upper() in ["Y", "YES"]:
    ret = subprocess.run(["minipro", "-p", "AT28C64B", "-w", outfilename, "-u", "-P"])
