# 8bit-cpu-microcode


program rom:  minipro -p W27C512@DIP28 -w output/16bitadd.bin -s

program microcode: minipro  -p AT28C64B -w microcode/CODEA.bin 




## 16 bit addressing enhancement

To implement 16 bit addressing, a rewrite of the microcode and addressing modes is necessary.

16 bit addresses will be stored in memory / rom in little endian form - low byte first - this simplifies 16 bit operations by reading/writing the low byte first, then reading/writing the high byte.  In theory this could allow for pipelining, but this is unlikely to be implemented..

16 bit addressing requires the ability to increment the memory address - 2 options to do this:
1. use the increment module, routing the MAR value to it's input, then update MAR via the Bus
 - the limitation of this option is that it won't support crossing page boundaries, instead looping to the start
2. implement the MAR and PAR using 4 x 74LS163 4-bit counters.  These support pre-setting, reset and counting.
 - this would support full 16-bit increments

Addressing modes

Implied - no operand (eg NOP, HLT, TAS etc)

Immediate Nibble - 

Immediate - 1 byte operand of value to be used, eg LDA $FF

Zero Page Absolute - 1 byte operand to address page zero in RAM, eg LDA #$80 -> $0080 in RAM
Absolute - 2 byte operand to address any page in ram, in little endian form, eg LDA #$8040 -> $8040 in RAM

Indirect Zero Page - 1 byte operand pointing to a location in page zero of ram. This and the next byte contain the address in memory to operate on in little endian form.
Indirect - 2 byte operand pointing to a location in any page of ram. This and the next byte contain the address in memory to operate on in little endian form.



Immediate Nibble                - number 5 loaded into A.                                  LDA $0x5
Immediate                       - number 69 (45 hex) loaded into A.                        LDA $0x45
Absolute Zero Page              - value in $0045 in ram loaded into A.                     LDA #$0x45
Absolure                        - value in $0645 in ram loaded into A.                     LDA #$0x0645
Indirect Zero Page              - value pointed to by $0045 and $0046 loaded into A.       LDA (#$0x45)
Absolute Zero Page X Indexed    - value in $0045+X loaded into A.                          LDA #$0x45,X
Absolute X Indexed              - value in $0645+X loaded into A.                          LDA #$0x0645,X
Indirect Zero Page X indexed    - value pointed to by $0045 and $0046+X loaded into A.     LDA (#$0x45),X
Indirect X indexed              - value pointed to by $0645 and $0646+X loaded into A.     LDA (#$0x0645),X




Load A - Immediate
1. load instruction from PC address to Instruction Reg
2. load byte from ROM using PC address and store in A reg, increment PC

Load A - Absolute Zero Page
1. load instruction from PC address to Instruction Reg
2. load low byte from ROM using PC address and store in MAR, increment PC
3. set Zero page flag and load byte from RAM and store in A reg.

Load A - Absolute
1. load instruction from PC address to Instruction Reg
2. load low byte from ROM using PC address and store in MAR, increment PC
3. load high byte fron ROM using PC address and store in PAR, increment PC
4. clear zero page flag and load byte from RAM and store in A reg

Load A - Indirect Zero Page
1. load instruction from PC address to Instruction Reg
2. load low byte from PC address into MAR, increment PC
3. set zero page flag and store byte from RAM in B Reg
4. increment MAR
5. clear zero page flag and store byte from RAM in PAR
6. transfer byte from B Reg to MAR
7. clear zero page flag and load byte from RAM and store in A reg


Load A - Indirect
1. load instruction from PC address to Instruction Reg, increment PC
2. load low byte from PC address into MAR, increment PC
3. load high byte from PC address into PAR, increment PC
4. clear zero page flag and store byte from RAM in B Reg
5. increment MAR
6. clear zero page flag and store byte from RAM in PAR
7. transfer byte from B Reg to MAR
8. clear zero page flag and load byte from RAM and store in A reg


## Reset flow

Indirect jump via 3FFE / 3FFF (little endian)

1. Set page to 3F
2. Set address to FE
3. Read value to B reg
4. Increment address and Read value to Page Reg
5. B reg value to Address Reg
6. Read value to PC Low
7. Increment address and REad value to PC high

Simpler version
1. output 20 to PC high
2. output 00 to PC low
3. cycle reset

## 16 bit memory map

0x0000 0b0000 0000 0000 0000 - Zero page RAM
... - 31 pages of RAM
0x1FFF 0b0001 1111 1111 1111 - Top of RAM

0x2000 0b0010 0000 0000 0000 - Bottom of ROM
... - 31 pages of ROM
0x3FFF 0b0011 1111 1111 1111 - TOP of ROM

0x4000 0b010x xxxx xxxx xxx0 - output low byte
0x4001 0b010x xxxx xxxx xxx1 - output high byte

0x6000 0b0110 0000 0000 0000 - printer
 -spare ~48k
0xFFFF


0x0000 - 0x1FFF - RAM
0x2000 - 0x3FFF - ROM
0x4000 - output low
0x4001 - output higg
0x6000 - printer

inputs:
16bit address
Read - active high
Write - active high

outputs:
ram read - active high
ram write - active high
rom read - active low
output low write - active low
output high write - active low
printer write - active high
