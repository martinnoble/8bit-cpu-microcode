
#type 0 active high, 1 active low
DIRA = 0b11110010

#decode A output lines
HLT = 0b00000001
MRI = 0b00000010
RI  = 0b00000100
RO  = 0b00001000
IRI = 0b00010000
IRO = 0b00100000
ARI = 0b01000000
ARO = 0b10000000

#type 0 active high, 1 active low
DIRB = 0b11110101

#decode B output lines
SO  = 0b00000001 << 8
SUB = 0b00000010 << 8
ORI = 0b00000100 << 8
CE  = 0b00001000 << 8
CO  = 0b00010000 << 8
JMP = 0b00100000 << 8
BRI = 0b01000000 << 8
BRO = 0b10000000 << 8

#type 0 active high, 1 active low
DIRC = 0b10000001

#decode C output lines
FRI = 0b00000001 << 16
UK1 = 0b00000010 << 16
UK2 = 0b00000100 << 16
UK3 = 0b00001000 << 16
UK4 = 0b00010000 << 16
UK5 = 0b00100000 << 16
UK6 = 0b01000000 << 16
CR  = 0b10000000 << 16

#ZP = 0
#PRI = 0

CARRY = 1
ZERO = 2


TEST = [1 | 256 | 65536, 2 | 512, 4 | 1024, 8 | 2048, 16 | 4096, 32 | 8192, 64 | 16384 , 128 | 32768 | 8388608]


''' Addressing modes

Instruction: low 4 bits of byte are the value
Immediate: following byte is the value
Aboslute: following byte is the address

LDA - Load A Register
* Instruction: values 0 to 15 direct from opcode into A register
* Immediate: values 0 to 255 from following byte into A register
* Absolute: values 0 to 255 from memory location given by following byte into A register

STA - Store A Register
* Instruction: value from A register into memory location given by low 4 bits of byte
* Absolute: value from A register into memory location given by following byte

'''

#0b00000000 : 0x00 - NOP Implied
#0b0001**** : 0x1* - JMP Instruction
#0b0010**** : 0x2* - BCS Instruction
#0b0011**** : 0x3* - BCC Instruction
#0b0100**** : 0x4* - BEQ Instruction
#0b0101**** : 0x5* - BNE Instruction
#0b0110**** : 0x6* - LDA Instruction
#0b0111**** : 0x7* - STA Instruction
#0b1000**** : 0x8* - ADD Instruction
#0b1001**** : 0x9* - SUB Instruction
#0b1010**** : 0xA* - CMP Instruction
#0b10110000 : 0xB0 - NOP
#0b10110001 : 0xB1 - JMP Immediate
#0b10110010 : 0xB2 - BCS Immediate 
#0b10110011 : 0xB3 - BCC Immediate
#0b10110100 : 0xB4 - BEQ Immediate
#0b10110101 : 0xB5 - BNE Immediate
#0b10110110 : 0xB6 - LDA Immediate
#0b10110111 : 0xB7 - NOP
#0b10111000 : 0xB8 - ADD Immediate
#0b10111001 : 0xB9 - SUB Immediate
#0b10111010 : 0xBA - CMP Immediate
#0b11000000 : 0xC0 - NOP
#0b11000001 : 0xC1 - NOP
#0b11000010 : 0xC2 - NOP
#0b11000011 : 0xC3 - NOP
#0b11000100 : 0xC4 - NOP
#0b11000101 : 0xC5 - NOP
#0b11000110 : 0xC6 - LDA Absolute
#0b11000111 : 0xC7 - STA Absolute
#0b11001000 : 0xC8 - ADD Absolute
#0b11001001 : 0xC9 - SUB Absolute
#0b11001010 : 0xCA - CMP Absolute
#0b1101**** : 0xD* - NOP
#0b1110**** : 0xE* - NOP
#0b11110000 : 0xF0 - TAO Implied
#0b11111111 : 0xFF - HLT Implied



        ### Base instructions

#NOP - No OPeration - do nothing
NOP = [ CO | MRI,   RO | IRI | CE,   CR , CR ,  CR,   CR,   CR,   CR ]
#HLT - HaLT - stop executing instructions
HLT = [ CO | MRI,   RO | IRI | CE,   HLT,   CR,   CR,   CR,   CR,  CR ]


        ### Jump instructions

#JMP - JuMP to address given by low 4 bits of instruction
JMP_IN = [CO | MRI,   RO | IRI | CE,   IRO | JMP | CR,   0,    0,   0,   0,   0 ]
#JMP - JuMP to address given by next byte
JMP_IM = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE, RO | JMP | CR,   0,   0,   0,   0 ]

        ### Branch instructions

#BCS - Branch if Carry Set to address given by low 4 bits of instruction
#BCC - Branch if Carry Clear to address given by low 4 bits of instruction
#BEQ - Branch if EQual (zero set) to address given by low 4 bits of instruction
#BNE - Branch if Not Equal (zero clear) to address given by low 4 bits of instruction

        ### Load instructions - place value into A register

#LDA - LoaD A register with value from low 4 bits of instruction 
LDA_IN = [CO | MRI,   RO | IRI | CE,   IRO | ARI | CR,   0,    0,   0,   0,   0 ]
#LDA - LoaD A register with value from next byte
LDA_IM = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | ARI | CR,   0,    0,   0,   0 ]
#LoaD A register with value from memory address in next byte 
LDA_AB = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | MRI,   RO | ARI | CR,    0,   0,   0 ]


        ### Store instructions - place value from A register into memory

#STA - STore value from A register into memory address given by low 4 bits of instruction
STA_IN = [CO | MRI,   RO | IRI | CE,   IRO | MRI, ARO | RI | CR,   0,    0,   0,   0]
#STA - STore value from A register into memory address given by next byte
STA_AB = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | MRI ,  ARO | RI | CR,    0,   0,   0 ]                  

        ### Math instructions

        ## Add instructions - add value to A register and place result in A register

#ADD - ADD value from low 4 bits of instruction to A register
ADD_IN = [CO | MRI,   RO | IRI | CE,   IRO | BRI,   SO | ARI | FRI | CR,    0,    0,   0,   0 ]
#ADD - ADD value from next byte to A register
ADD_IM = [ CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | BRI,   SO | ARI | FRI | CR,    0,   0,   0 ]
#ADD - ADD value from memory address in next byte to A register
ADD_AB = [ CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | MRI,   RO | BRI,  SO | ARI | FRI | CR,    0,   0 ]   

        ## Subtract instructions - subtract value from A register and place result in A register

#SUB - SUBtract value from low 4 bits of instruction from A register
SUB_IN = [CO | MRI,   RO | IRI | CE,   IRO | BRI,   SO | SUB | ARI | FRI | CR,    0,    0,   0,   0 ]
#SUB - SUBtract value from next byte from A register
SUB_IM = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | BRI,   SO | SUB | ARI | FRI | CR,   0,   0,   0 ]
#SUB - SUBtract value from memory address in next byte from A register
SUB_AB = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | MRI,   RO | BRI,  SO | SUB | ARI | FRI | CR,   0,   0 ]

        ### Compare operations - same as subtract but don't store result in A register
        # set flags (carry and zero) as if A register was subtracted by value but don't store result in A register

#CMP - CoMPare value from low 4 bits of instruction with A register
CMP_IN = [CO | MRI,   RO | IRI | CE,   IRO | BRI,   SUB | FRI | CR,    0,    0,   0,   0 ]
#CMP - CoMPare value from next byte with A register
CMP_IM = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | BRI,   SUB | FRI | CR,    0,    0,   0,   0 ]
#CMP - CoMPare value from memory address in next byte with A register
CMP_AB = [CO | MRI,   RO | IRI | CE,   CO | MRI | CE,   RO | MRI,   RO | BRI,  SUB | FRI | CR,    0,    0,   0 ]

        ### Transfer instructions - transfer value from one register to another

#TAO - Transfer A register to Output register
TAO = [CO | MRI,   RO | IRI | CE,   ARO | ORI | CR , 0 ,  0,   0,   0,   0 ]



CODEA = [None] * 8192
CODEB = [None] * 8192
CODEC = [None] * 8192

for instruction in range(0, 256):

    if instruction % 16 == 0:
        print(instruction)

    for subinst in range(0, 8):

        for flags in range(0, 4):

            address = instruction << 5 | flags << 3 | subinst

            #default all instructions to NOP
            value = NOP[subinst]

            ### Instruction addressed opcodes

            #Jump  
            if (((instruction & 0b11110000) == 0b00010000)                                  #0b0001**** : 0x1* - JMP Instruction
                or ((instruction & 0b11110000) == 0b00100000 and (flags & CARRY) == CARRY)  #0b0010**** : 0x2* - BCS Instruction
                or ((instruction & 0b11110000) == 0b00110000 and (flags & CARRY) == 0)      #0b0011**** : 0x3* - BCC Instruction
                or ((instruction & 0b11110000) == 0b01000000 and (flags & ZERO) == ZERO)    #0b0100**** : 0x4* - BEQ Instruction
                or ((instruction & 0b11110000) == 0b01010000 and (flags & ZERO) == 0)       #0b0101**** : 0x5* - BNE Instruction
                ):
                value = JMP_IN[subinst]

            #0b0110**** : 0x6* - LDA Instruction
            if ((instruction & 0b11110000) == 0b01100000):
                #0b0110**** : 0x6* - LDA Instruction
                value = LDA_IN[subinst]

            #0b0111**** : 0x7* - STA Instruction
            if ((instruction & 0b11110000) == 0b01110000):
                #0b0111**** : 0x7* - STA Instruction
                value = STA_IN[subinst]

            #0b1000**** : 0x8* - ADD Instruction
            if ((instruction & 0b11110000) == 0b10000000):
                #0b1000**** : 0x8* - ADD Instruction
                value = ADD_IN[subinst]

            #0b1001**** : 0x9* - SUB Instruction
            if ((instruction & 0b11110000) == 0b10010000):
                #0b1001**** : 0x9* - SUB Instruction
                value = SUB_IN[subinst]

            #0b1010**** : 0xA* - CMP Instruction
            if ((instruction & 0b11110000) == 0b10100000):
                #0b1010**** : 0xA* - CMP Instruction
                value = CMP_IN[subinst]


            ### Immediate addressed opcodes

            #Jump Immediate instructions
            if ((instruction  == 0b10110001)                                                #0b10110001 : 0xB1 - JMP Immediate
                or ((instruction == 0b10110010) and (flags & CARRY) == CARRY)               #0b10110010 : 0xB2 - BCS Immediate
                or ((instruction == 0b10110011) and (flags & CARRY) == 0)                   #0b10110011 : 0xB3 - BCC Immediate
                or ((instruction == 0b10110100) and (flags & ZERO) == ZERO)                 #0b10110100 : 0xB4 - BEQ Immediate
                or ((instruction == 0b10110101) and (flags & ZERO) == 0)                    #0b10110101 : 0xB5 - BNE Immediate
                ):                                            
                value = JMP_IM[subinst]


            #0b10110001 : 0xB1 - JMP Immediate
            if (instruction == 0b10110001):
                #0b10110001 : 0xB1 - JMP Immediate
                value = JMP_IM[subinst]

            #0b10110010 : 0xB2 - BCS Immediate
            if (instruction == 0b10110010 and (flags & CARRY) == CARRY):
                #0b10110010 : 0xB2 - BCS Immediate
                value = JMP_IM[subinst]

            #0b10110011 : 0xB3 - BCC Immediate
            if (instruction == 0b10110011 and (flags & CARRY) == 0):
                #0b10110011 : 0xB3 - BCC Immediate
                value = JMP_IM[subinst]

            #0b10110100 : 0xB4 - BEQ Immediate
            if (instruction == 0b10110100 and (flags & ZERO) == ZERO):
                #0b10110100 : 0xB4 - BEQ Immediate
                value = JMP_IM[subinst]

            #0b10110101 : 0xB5 - BNE Immediate
            if (instruction == 0b10110101 and (flags & ZERO) == 0):
                #0b10110101 : 0xB5 - BNE Immediate
                value = JMP_IM[subinst] 

            #0b10110110 : 0xB6 - LDA Immediate
            if (instruction == 0b10110110):
                #0b10110110 : 0xB6 - LDA Immediate
                value = LDA_IM[subinst]

            #0b10111000 : 0xB8 - ADD Immediate
            if (instruction == 0b10111000):
                #0b10111000 : 0xB8 - ADD Immediate
                value = ADD_IM[subinst]

            #0b10111001 : 0xB9 - SUB Immediate
            if (instruction == 0b10111001):
                #0b10111001 : 0xB9 - SUB Immediate
                value = SUB_IM[subinst]

            #0b10111010 : 0xBA - CMP Immediate
            if (instruction == 0b10111010):
                #0b10111010 : 0xBA - CMP Immediate
                value = CMP_IM[subinst]


            ### Absolute addressed opcodes

            #0b11000110 : 0xC6 - LDA Absolute
            if (instruction == 0b11000110):
                #0b11000110 : 0xC6 - LDA Absolute
                value = LDA_AB[subinst]

            #0b11000111 : 0xC7 - STA Absolute
            if (instruction == 0b11000111):
                #0b11000111 : 0xC7 - STA Absolute
                value = STA_AB[subinst]

            #0b11001000 : 0xC8 - ADD Absolute
            if (instruction == 0b11001000):
                #0b11001000 : 0xC8 - ADD Absolute
                value = ADD_AB[subinst]

            #0b11001001 : 0xC9 - SUB Absolute
            if (instruction == 0b11001001):
                #0b11001001 : 0xC9 - SUB Absolute
                value = SUB_AB[subinst]

            #0b11001010 : 0xCA - CMP Absolute
            if (instruction == 0b11001010):
                #0b11001010 : 0xCA - CMP Absolute
                value = CMP_AB[subinst]


            ### Implied addressed opcodes

            #0b11110000 : 0xF0 - TAO Implied
            if (instruction == 0b11110000):
                #0b11110000 : 0xF0 - TAO Implied
                value = TAO[subinst]

            #0b11111111 : 0xFF - HLT Implied
            if (instruction == 0b11111111):
                #0b11111111 : 0xFF - HLT Implied
                value = HLT[subinst]

            CODEA[address] = (value & 0xFF) ^ DIRA
            CODEB[address] = ((value >> 8) & 0xFF) ^ DIRB
            CODEC[address] = ((value >> 16) & 0xFF) ^ DIRC


f=open("output/CODEA.bin","wb")
f.write(bytearray(CODEA))
f.close()

f=open("output/CODEB.bin","wb")
f.write(bytearray(CODEB))
f.close()

f=open("output/CODEC.bin","wb")
f.write(bytearray(CODEC))
f.close()
