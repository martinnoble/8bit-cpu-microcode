import subprocess


#type 0 active high, 1 active low
DIRA = 0b11110010

#decode A output lines
HALT      = 0b00000001
ADDR_IN   = 0b00000010
WRITE     = 0b00000100 #rename to WRITE
READ      = 0b00001000 #rename to READ
I_REG_IN  = 0b00010000
I_REG_OUT = 0b00100000 
A_REG_IN  = 0b01000000
A_REG_OUT = 0b10000000

#type 0 active high, 1 active low
DIRB = 0b11110001

#decode B output lines
SUM_OUT   = 0b00000001 << 8
SUB       = 0b00000010 << 8
ADINC     = 0b00000100 << 8   #Address Increment by 1 - LED switched to active high, check this signal
COUNT_EN  = 0b00001000 << 8
JMP_LOW   = 0b00010000 << 8   #TODO: JMP_LOW for 16bit countner
JMP_HIGH  = 0b00100000 << 8  #TODO: JMP_HIGH for 16bit counter 
B_REG_IN  = 0b01000000 << 8
B_REG_OUT = 0b10000000 << 8

#type 0 active high, 1 active low
DIRC  = 0b11000111

#decode C output lines
F_REG_IN  = 0b00000001 << 16
PC_ADR   = 0b00000010 << 16  #Program counter high and low output to address bus
S_REG_IN  = 0b00000100 << 16  
F_CLEAR   = 0b00001000 << 16
F_SET     = 0b00010000 << 16 #LED added - check this signal
ZERO_PAGE = 0b00100000 << 16  #LED added - check this signal
PAGE_IN   = 0b01000000 << 16  
CYCLE_RESET = 0b10000000 << 16  


# new 4th decode block
#type 0 active high, 1 active low
DIRD  = 0b00000111

#decode D output lines
X_REG_IN  = 0b00000001 << 24  #X Reg in
X_REG_OUT = 0b00000010 << 24  #X Reg out
ADINC_X   = 0b00000100 << 24  #Address Increment by X
UD04  = 0b00001000 << 24  
UD05  = 0b00010000 << 24
UD06  = 0b00100000 << 24
UD07  = 0b01000000 << 24
RESET  = 0b10000000 << 24  



CARRY = 1
ZERO = 2


TEST = [1 | 256 | 65536, 2 | 512, 4 | 1024, 8 | 2048, 16 | 4096, 32 | 8192, 64 | 16384 , 128 | 32768 | 8388608]


''' Addressing modes

Implied: no additional data, instruction implies the operation (e.g. TAO - transfer A register to output)
Immediate Nibble: low 4 bits of byte are the value
Immediate: following byte is the value
Absolute: following byte is the address
Absolute In Place: following bytes is the address, third byte is the value to be used in the operation, and result is stored back to the original address.
Indirect: following byte is the address of a byte which contains the address to be used in the operation (eg for array operations)

LDA - Load A Register
* Immediate Nibble: values 0 to 15 low nibble of opcode into A register
* Immediate: values 0 to 255 from following byte into A register
* Absolute: values 0 to 255 from memory location given by following byte into A register
* Indirect: values 0 to 255 from memory location which is in turn given by following byte into A register

STA - Store A Register
* Instruction: value from A register into memory location given by low 4 bits of byte
* Absolute: value from A register into memory location given by following byte

'''

#0b00000000 : 0x00 - NOP
#0b00000001 : 0x01 - NOP
#0b00000010 : 0x02 - NOP
#0b00000011 : 0x03 - NOP
#0b00000100 : 0x04 - NOP
#0b00000101 : 0x05 - NOP
#0b00000110 : 0x06 - LDA Absolute Zero Page
#0b00000111 : 0x07 - STA Absolute Zero Page
#0b00001000 : 0x08 - NOP
#0b00001001 : 0x09 - NOP
#0b00001010 : 0x0A - CMP Absolute Zero Page
#0b00001011 : 0x0B - NOP
#0b00001100 : 0x0C - NOP
#0b00001101 : 0x0D - NOP
#0b00001110 : 0x0E - NOP
#0b00001111 : 0x0F - NOP

#0b0001**** : 0x1* - ADC Immediate Nibble
#0b0010**** : 0x2* - SBC Immediate Nibble
#0b0011**** : 0x3* - NOP
#0b0100**** : 0x4* - NOP
#0b0101**** : 0x5* - NOP
#0b0110**** : 0x6* - LDA Immediate Nibble
#0b0111**** : 0x7* - STA Immediate Nibble
#0b1000**** : 0x8* - ADD Immediate Nibble
#0b1001**** : 0x9* - SUB Immediate Nibble
#0b1010**** : 0xA* - CMP Immediate Nibble

#0b10110000 : 0xB0 - NOP
#0b10110001 : 0xB1 - NOP
#0b10110010 : 0xB2 - NOP 
#0b10110011 : 0xB3 - NOP
#0b10110100 : 0xB4 - NOP
#0b10110101 : 0xB5 - NOP
#0b10110110 : 0xB6 - LDA Immediate
#0b10110111 : 0xB7 - NOP
#0b10111000 : 0xB8 - ADD Immediate
#0b10111001 : 0xB9 - SUB Immediate
#0b10111010 : 0xBA - CMP Immediate
#0b10111011 : 0xBB - NOP
#0b10111100 : 0xBC - ADC Immediate
#0b10111101 : 0xBD - SBC Immediate
#0b10111110 : 0xBE - NOP
#0b10111111 : 0xBF - NOP

#0b11000000 : 0xC0 - NOP
#0b11000001 : 0xC1 - JMP Absolute
#0b11000010 : 0xC2 - BCS Absolute
#0b11000011 : 0xC3 - BCC Absolute
#0b11000100 : 0xC4 - BEQ Absolute
#0b11000101 : 0xC5 - BNE Absolute
#0b11000110 : 0xC6 - LDA Absolute
#0b11000111 : 0xC7 - STA Absolute
#0b11001000 : 0xC8 - ADD Absolute
#0b11001001 : 0xC9 - SUB Absolute
#0b11001010 : 0xCA - CMP Absolute
#0b11001011 : 0xCB - CPY Absolute
#0b11001100 : 0xCC - ADC Absolute
#0b11001101 : 0xCD - SBC Absolute
#0b11001110 : 0xCE - NOP
#0b11001111 : 0xCF - NOP

#0b11010000 : 0xD0 - NOP
#0b11010001 : 0xD1 - NOP
#0b11010010 : 0xD2 - NOP
#0b11010011 : 0xD3 - NOP
#0b11010100 : 0xD4 - NOP
#0b11010101 : 0xD5 - NOP
#0b11010110 : 0xD6 - NOP
#0b11010111 : 0xD7 - NOP
#0b11011000 : 0xD8 - ADD Absolute In Place
#0b11011001 : 0xD9 - SUB Absolute In Place
#0b11011010 : 0xDA - NOP
#0b11011011 : 0xDB - NOP
#0b11011100 : 0xDC - ADC Absolute In Place
#0b11011101 : 0xDD - SBC Absolute In Place
#0b11011110 : 0xDE - NOP
#0b11011111 : 0xDF - NOP

#0b11100000 : 0xE0 - NOP
#0b11100001 : 0xE1 - NOP
#0b11100010 : 0xE2 - NOP
#0b11100011 : 0xE3 - NOP
#0b11100100 : 0xE4 - NOP
#0b11100101 : 0xE5 - NOP
#0b11100110 : 0xE6 - LDA Indirect Zero Page
#0b11100111 : 0xE7 - STA Indirect Zero Page
#0b11101000 : 0xE8 - ADD Indirect
#0b11101001 : 0xE9 - SUB Indirect
#0b11101010 : 0xEA - NOP
#0b11101011 : 0xEB - NOP
#0b11101100 : 0xEC - ADC Indirect Zero Page
#0b11101101 : 0xED - SBC Indirect Zero Page
#0b11101110 : 0xEE - NOP
#0b11101111 : 0xEF - NOP

#0b11110000 : 0xF0 - NOP
#0b11110001 : 0xF1 - TAS Implied
#0b11110010 : 0xF2 - CLF Implied
#0b11110011 : 0xF3 - SEF Implied
#0b11110100 : 0xF4 - TAX Implied
#0b11110101 : 0xF5 - TXA Implied
#0b11110110 : 0xF6 - LDA Indirect
#0b11110111 : 0xF7 - STA Indirect
#0b11111000 : 0xF8 - NOP
#0b11111001 : 0xF9 - NOP
#0b11111010 : 0xFA - NOP
#0b11111011 : 0xFB - NOP
#0b11111100 : 0xFC - ADC Indirect
#0b11111101 : 0xFD - SBC Indirect
#0b11111110 : 0xFE - NOP
#0b11111111 : 0xFF - HALT Implied



        ### Base instructions

#NOP - No OPeration - do nothing
NOP    = [ PC_ADR | READ | I_REG_IN | COUNT_EN,     CYCLE_RESET,         CYCLE_RESET,  0,  0,  0,  0,  0 ]
NOP_IM = [ PC_ADR | READ | I_REG_IN | COUNT_EN,     COUNT_EN | CYCLE_RESET,    0,  0,  0,  0,  0,  0 ]
NOP_ABS = [ PC_ADR | READ | I_REG_IN | COUNT_EN,     COUNT_EN,  COUNT_EN | CYCLE_RESET,  0,  0,  0,  0,  0 ]

#HLT - HaLT - stop executing instructions
HLT = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   HALT ,   HALT,   HALT,   HALT,   HALT,  HALT , 0 ]


        ### Jump instructions

#JUMP - JuMP to address given by low 4 bits of instruction
#JMP_IN = [PC_ADR | READ | I_REG_IN | COUNT_EN,   I_REG_OUT | JUMP | CYCLE_RESET,   0,    0,   0,   0,   0, 0 ]
#JUMP - JuMP to address given by next byte
JMP_AB = [PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | B_REG_IN | COUNT_EN,   PC_ADR | READ | JMP_HIGH | COUNT_EN, B_REG_OUT | JMP_LOW | CYCLE_RESET,  0,   0, 0, 0 ]

        ### Branch instructions

#BCS - Branch if Carry Set to address given by low 4 bits of instruction
#BCC - Branch if Carry Clear to address given by low 4 bits of instruction
#BEQ - Branch if EQual (zero set) to address given by low 4 bits of instruction
#BNE - Branch if Not Equal (zero clear) to address given by low 4 bits of instruction

        ### Load instructions - place value into A register

#LDA - LoaD A register with value from low 4 bits of instruction 
LDA_IN  = [PC_ADR | READ | I_REG_IN | COUNT_EN,  I_REG_OUT | A_REG_IN | CYCLE_RESET,   0,    0,   0,   0,   0, 0 ]
#LDA - LoaD A register with value from next byte
LDA_IM  = [PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | A_REG_IN | COUNT_EN | CYCLE_RESET,   0,    0,   0,   0, 0,0 ]

#LoaD A register with value from memory address in next byte (zero page)
LDA_AB_ZP  = [PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   ZERO_PAGE | READ | A_REG_IN | CYCLE_RESET,    0,   0,   0, 0, 0 ]

#LoaD A register with value from memory address in next two bytes (little endian)
LDA_AB  = [PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ | PAGE_IN | COUNT_EN, READ | A_REG_IN | CYCLE_RESET,   0,   0, 0, 0 ]


#LoaD A register using 16bit memory address stored in zero page (indirect)
LDA_IND_ZP = [PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   ZERO_PAGE | READ | B_REG_IN,  ADINC | ZERO_PAGE | READ | PAGE_IN,   B_REG_OUT | ADDR_IN,   READ | A_REG_IN | CYCLE_RESET, 0, 0 ]

#LoaD A register indirect - next two bytes point to an address which contains the address of the byte to read
LDA_IND = [PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ | PAGE_IN | COUNT_EN, READ | B_REG_IN,  ADINC | READ | PAGE_IN,   B_REG_OUT | ADDR_IN,   READ | A_REG_IN | CYCLE_RESET, 0 ]



        ### Store instructions - place value from A register into memory

#STA - STore value from A register into memory address given by low 4 bits of instruction - implies zero page
#TODO: is this actually used in the assembler / necessary?
STA_IN  = [PC_ADR | READ | I_REG_IN | COUNT_EN,   I_REG_OUT | ADDR_IN,  ZERO_PAGE | A_REG_OUT | WRITE | CYCLE_RESET,    0,   0,   0, 0 ,0]

#STA - STore value from A register into memory address given by next byte (zero page)
STA_AB_ZP  = [PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | ADDR_IN | COUNT_EN ,  ZERO_PAGE | A_REG_OUT | WRITE | CYCLE_RESET,   0, 0, 0 ,0, 0]  

#STA - STore value from A register into memory address given by next type bytes (little endian)
STA_AB  =    [PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | ADDR_IN | COUNT_EN ,  PC_ADR | READ | PAGE_IN | COUNT_EN, A_REG_OUT | WRITE | CYCLE_RESET, 0, 0, 0, 0 ]  

#STA - STore value from A register into memory address which is in turn given by next byte (indirect zero page) 
STA_IND_ZP = [PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | ADDR_IN | COUNT_EN ,  ZERO_PAGE | READ | B_REG_IN,  ADINC | ZERO_PAGE | READ | PAGE_IN,   B_REG_OUT | ADDR_IN,  A_REG_OUT | WRITE | CYCLE_RESET, 0 ,0]

#STA - STore value from A register into memory address which is in turn given by next two byte (indirect) 
STA_IND = [PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | ADDR_IN | COUNT_EN ,  PC_ADR | READ | PAGE_IN | COUNT_EN, READ | B_REG_IN,  ADINC | READ | PAGE_IN,   B_REG_OUT | ADDR_IN,   A_REG_OUT | WRITE | CYCLE_RESET, 0]

        ### Math instructions

        ## Add instructions - add value to A register and place result in A register

#ADD - resets carry flag before add

#ADD - ADD INstruction - add value from low 4 bits of instruction to A register
ADD_IN  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  I_REG_OUT | F_CLEAR | F_REG_IN | B_REG_IN,   SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,    0,   0,   0, 0 ]

#ADD - ADD IMmediate - add value from next byte to A register
ADD_IM  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_CLEAR | F_REG_IN | B_REG_IN | COUNT_EN,   SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,   0,   0, 0, 0 ]

#TODO: implement ADD_AB_ZP
#ADD - ADD ABsolute - add value from memory address in next byte to A register
ADD_AB  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_CLEAR | F_REG_IN | ADDR_IN | COUNT_EN,   PC_ADR | READ | PAGE_IN | COUNT_EN, READ | B_REG_IN,  SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,   0, 0]  

#TODO: implement ADD_AB_IP_ZP
#ADD - ADD ABsolute In Place - equivalent of a LDA, ADD and STA all in one. LDA value from memory address in next two bytes, ADD the value in the third byte, and Store the result back to the original location.
ADD_AB_IP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_CLEAR | F_REG_IN | ADDR_IN | COUNT_EN,  PC_ADR | READ | PAGE_IN | COUNT_EN, READ | A_REG_IN,  PC_ADR | READ | B_REG_IN | COUNT_EN, SUM_OUT | A_REG_IN | F_REG_IN, A_REG_OUT | WRITE | CYCLE_RESET, 0]

#ADD - ADD INDirect - add value from memory address which is in turn given by next byte (indirect zero page) to A register
ADD_IND_ZP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_CLEAR | F_REG_IN | ADDR_IN | COUNT_EN,   ZERO_PAGE | READ | B_REG_IN,  ADINC | ZERO_PAGE | READ | PAGE_IN, B_REG_OUT | ADDR_IN,   READ | B_REG_IN,  SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET, 0 ]

#ADD - ADD INDirect - add value from memory address which is in turn given by next two bytes (indirect) to A register
ADD_IND = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_CLEAR | F_REG_IN | ADDR_IN | COUNT_EN,   PC_ADR | READ | PAGE_IN | COUNT_EN,  READ | B_REG_IN,  ADINC | READ | PAGE_IN, B_REG_OUT | ADDR_IN,   READ | B_REG_IN,  SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET]


#ADC - ADd with Carry - respects carry flag to support multi byte maths

#ADC - ADd with Carry INstruction - add value from low 4 bits of instruction to A register
ADC_IN  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  I_REG_OUT | B_REG_IN,   SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,    0,   0,   0, 0 ]

#ADC - ADd with Carry IMmediate - add value from next byte to A register
ADC_IM  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | B_REG_IN | COUNT_EN,   SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,   0,   0, 0, 0 ]

#TODO: implement ADC_AB_ZP
#ADC - ADd with Carry ABsolute - add value from memory address in next byte to A register
ADC_AB  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ |  ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | B_REG_IN,  SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,   0, 0, 0 ]  

#TODO: implement ADC_AB_IP_ZP
#ADC - ADd with Carry ABsolute In Place - equivalent of a LDA, ADD and STA all in one. LDA value from memory address in next byte, ADD the value in the byte after, and Store the result back to the original location.
ADC_AB_IP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | A_REG_IN,  PC_ADR | READ | B_REG_IN | COUNT_EN, SUM_OUT | A_REG_IN | F_REG_IN, A_REG_OUT | WRITE | CYCLE_RESET, 0,    0, 0 ,0]

#ADC - ADd with Carry INDirect - add value from memory address which is in turn given by next byte (indirect) to A register
ADC_IND = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | B_REG_IN, ADINC | READ | PAGE_IN, B_REG_OUT | ADDR_IN,  READ | B_REG_IN,  SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET]

ADC_IND_ZP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   ZERO_PAGE | READ | B_REG_IN,  ADINC | ZERO_PAGE | READ | PAGE_IN, B_REG_OUT | ADDR_IN,   READ | B_REG_IN,  SUM_OUT | A_REG_IN | F_REG_IN | CYCLE_RESET, 0 ]

        ## Subtract instructions - subtract value from A register and place result in A register

#SUB - SUBtract value from low 4 bits of instruction from A register
SUB_IN  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  I_REG_OUT | F_SET | F_REG_IN | B_REG_IN,   SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,    0,   0,   0, 0 ]
#SUB - SUBtract value from next byte from A register
SUB_IM  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_SET | F_REG_IN | B_REG_IN | COUNT_EN,   SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET,   0,   0, 0, 0, 0, 0 ]
#TODO: implement SUB_AB_ZP
#SUB - SUBtract value from memory address in next byte from A register
SUB_AB  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_SET | F_REG_IN | ADDR_IN | COUNT_EN,    PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | B_REG_IN,  SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET,   0,   0, 0 ]
#TODO: implement SUB_AB_IP_ZP
#SUB - SUBtract Absolute In Place - equivalent of a LDA, SUB and STA all in one. LDA value from memory address in next byte, SUB the value in the byte after, and Store the result back to the original location.
SUB_AB_IP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_SET | F_REG_IN | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | A_REG_IN,  PC_ADR | READ | B_REG_IN | COUNT_EN, SUM_OUT | SUB | A_REG_IN | F_REG_IN, A_REG_OUT | WRITE | CYCLE_RESET,0,   0 ]
#TODO: implement SUB_IND_ZP
#SUB - SUBtract value from memory address which is in turn given by next byte (indirect) from A register
SUB_IND = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | F_SET | F_REG_IN | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | B_REG_IN, ADINC | READ | PAGE_IN, B_REG_OUT | ADDR_IN,  READ | B_REG_IN,  SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET ]


#SBC - SuBtract with Carry value from low 4 bits of instruction from A register
SBC_IN  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  I_REG_OUT | B_REG_IN,   SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET,    0,    0,   0,   0, 0 ]
#SBC - SuBtract with Carry value from next byte from A register
SBC_IM  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | B_REG_IN | COUNT_EN,   SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET,   0,   0,   0, 0, 0 ]
#TODO: implement SBC_AB_ZP
#SBC - SuBtract with Carry value from memory address in next byte from A register
SBC_AB  = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | B_REG_IN,  SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET,   0,   0, 0 ]
#TODO: implement SBC_AB_IP_ZP
#SBC - SuBtract with Carry Absolute In Place - equivalent of a LDA, SUB and STA all in one. LDA value from memory address in next byte, SUB the value in the byte after, and Store the result back to the original location.
SBC_AB_IP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | A_REG_IN,  PC_ADR | READ | B_REG_IN | COUNT_EN, SUM_OUT | SUB | A_REG_IN | F_REG_IN, A_REG_OUT | WRITE | CYCLE_RESET, 0,   0 ]
#TODO: implement SBC_IND_ZP
#SBC - SuBtract with Carry value from memory address which is in turn given by next byte (indirect) from A register
SBC_IND = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,   PC_ADR | READ |  PAGE_IN | COUNT_EN, READ | B_REG_IN, ADINC | READ | PAGE_IN, B_REG_OUT | ADDR_IN,  READ | B_REG_IN,  SUM_OUT | SUB | A_REG_IN | F_REG_IN | CYCLE_RESET ]

        ### Compare operations - same as subtract but don't store result in A register
        # set flags (carry and zero) as if A register was subtracted by value but don't store result in A register
#CMP - CoMPare value from low 4 bits of instruction with A register
CMP_IN = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   F_SET | F_REG_IN | I_REG_OUT | B_REG_IN,   SUB | F_REG_IN | CYCLE_RESET,    0,    0,   0,   0, 0 ]
#CMP - CoMPare value from next byte with A register
CMP_IM = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | F_SET | F_REG_IN | B_REG_IN | COUNT_EN,   SUB | F_REG_IN | CYCLE_RESET,    0,    0,   0,   0, 0 ]

#CMP - CoMPare value from memory address in next byte with A register
CMP_AB_ZP = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | F_SET | F_REG_IN | ADDR_IN | COUNT_EN,  ZERO_PAGE | READ | B_REG_IN,  SUB | F_REG_IN | CYCLE_RESET,    0,    0,   0, 0 ]

#CMP - CoMPare value from memory address in next byte with A register
CMP_AB = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   PC_ADR | READ | F_SET | F_REG_IN | ADDR_IN | COUNT_EN,   PC_ADR | READ | PAGE_IN | COUNT_EN, READ | B_REG_IN,  SUB | F_REG_IN | CYCLE_RESET,    0,    0,   0 ]

        ### Transfer instructions - transfer value from one register to another

#CPY - CoPY value from ROM to RAM. Address given by the next byte, value given by 3rd byte.
CPY_AB = [ PC_ADR | READ | I_REG_IN | COUNT_EN,  PC_ADR | READ | ADDR_IN | COUNT_EN,  PC_ADR | READ | WRITE | COUNT_EN | CYCLE_RESET,    0,    0,   0, 0, 0 ]

#CPY_IND - CoPY value from ROM to RAM. Address given by the next byte, value given by 3rd byte. Indirect version where address of value is given by the next byte.

#TAO - Transfer A register to Output register
#REMOVED - output by memory mapped
#TAO = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   A_REG_OUT | ORI | CYCLE_RESET , 0 ,  0,   0,   0,   0, 0 ]

#Transfer A register to Status register
TAS = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   A_REG_OUT | S_REG_IN | CYCLE_RESET , 0 ,  0,   0,   0,   0, 0 ] 

#Tranfer A register to X register
TAX = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   A_REG_OUT | X_REG_IN | CYCLE_RESET , 0 ,  0,   0,   0,   0, 0 ] 

#Transfer X register to A register
TXA = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   X_REG_OUT | A_REG_IN | CYCLE_RESET , 0 ,  0,   0,   0,   0, 0 ] 


#CLear Flags - clear carry and zero flags
CLF = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   F_CLEAR | F_REG_IN | CYCLE_RESET , 0 ,  0,   0,   0,   0, 0 ]

#SEt Flags - set carry and zero flags
SEF = [ PC_ADR | READ | I_REG_IN | COUNT_EN,   F_SET | F_REG_IN | CYCLE_RESET , 0 ,  0,   0,   0,   0, 0 ]


#TODO: reset the instruction reg to 0x00 (NOP) as part of reset - ensures no unexpected subinstructions will run later
RST = [ JMP_LOW | I_REG_IN | RESET, JMP_HIGH | RESET, 0, 0, 0, 0, 0, 0 ]

CODEA: list[int] = [0] * 65536
CODEB: list[int] = [0] * 65536
CODEC: list[int] = [0] * 65536
CODED: list[int] = [0] * 65536

print("Generating microcode...")

for instruction in range(0, 256):

    for subinst in range(0, 8):

        for flags in range(0, 4):

            for reset in range(0, 2):

                address = reset << 13 | instruction << 5 | flags << 3 | subinst

                if reset == 1:
                    #when reset flag is true, all opcodes decode to a reset instruction
                    #this ensure that whatever opcode is exists in the instruction reg at time of reset, we will always actually perform the reset operations
                    value = RST[subinst]
                
                else:
                    #default all instructions to NOP
                    value = NOP[subinst]

                    ### Zero Page Absolute

                    #0b00000110 : 0x06 - LDA Absolute Zero Page
                    if (instruction == 0b00000110):
                        value = LDA_AB_ZP[subinst]

                    #0b00000111 : 0x07 - STA Absolute Zero Page
                    if (instruction == 0b00000111):
                        value = STA_AB_ZP[subinst]

                    #0b00001010 : 0x0A - CMP Absolute Zero Page
                    if (instruction == 0b00001010):
                        value = CMP_AB_ZP[subinst]

                    ### Instruction addressed opcodes

                    #0b0001**** : 0x1* - ADC Instruction
                    if ((instruction & 0b11110000) == 0b00010000):
                        value = ADC_IN[subinst]

                    #0b0010**** : 0x2* - SBC Instruction
                    if ((instruction & 0b11110000) == 0b00100000):
                        value = SBC_IN[subinst]

                    #0b0110**** : 0x6* - LDA Instruction
                    if ((instruction & 0b11110000) == 0b01100000):
                        value = LDA_IN[subinst]

                    #0b0111**** : 0x7* - STA Instruction
                    if ((instruction & 0b11110000) == 0b01110000):
                        value = STA_IN[subinst]

                    #0b1000**** : 0x8* - ADD Instruction
                    if ((instruction & 0b11110000) == 0b10000000):
                        value = ADD_IN[subinst]

                    #0b1001**** : 0x9* - SUB Instruction
                    if ((instruction & 0b11110000) == 0b10010000):
                        value = SUB_IN[subinst]

                    #0b1010**** : 0xA* - CMP Instruction
                    if ((instruction & 0b11110000) == 0b10100000):
                        value = CMP_IN[subinst]


                    ### Immediate addressed opcodes

                  

                    #0b10110110 : 0xB6 - LDA Immediate
                    if (instruction == 0b10110110):
                        value = LDA_IM[subinst]

                    #0b10111000 : 0xB8 - ADD Immediate
                    if (instruction == 0b10111000):
                        value = ADD_IM[subinst]

                    #0b10111001 : 0xB9 - SUB Immediate
                    if (instruction == 0b10111001):
                        value = SUB_IM[subinst]

                    #0b10111010 : 0xBA - CMP Immediate
                    if (instruction == 0b10111010):
                        value = CMP_IM[subinst]

                    #0b10111100 : 0xBC - ADC Immediate
                    if (instruction == 0b10111100):
                        value = ADC_IM[subinst]

                    #0b10111101 : 0xBD - SBC Immediate
                    if (instruction == 0b10111101):
                        value = SBC_IM[subinst]



                    ### Absolute addressed opcodes

                    ## for BCS, BCC, BEQ and BNE, if flag condition is not met, need to run a "long NOP" to increment the program counter twice
                    if ((instruction == 0b11000010)              #0b11000010 : 0xC2 - BCS Absolute
                        or (instruction == 0b11000011)           #0b11000011 : 0xC3 - BCC Absolute
                        or (instruction == 0b11000100)           #0b11000100 : 0xC4 - BEQ Absolute
                        or (instruction == 0b11000101)           #0b11000101 : 0xC5 - BNE Absolute
                        ):                   
                        value = NOP_ABS[subinst]
                    
                    #TODO: switch all branches to absolute
                    #Jump Immediate instructions
                    if ((instruction  == 0b11000001)                                                #0b11000001 : 0xC1 - JMP Absolute
                        or ((instruction == 0b11000010) and (flags & CARRY) == CARRY)               #0b11000010 : 0xC2 - BCS Absolute
                        or ((instruction == 0b11000011) and (flags & CARRY) == 0)                   #0b11000011 : 0xC3 - BCC Absolute
                        or ((instruction == 0b11000100) and (flags & ZERO) == ZERO)                 #0b11000100 : 0xC4 - BEQ Absolute
                        or ((instruction == 0b11000101) and (flags & ZERO) == 0)                    #0b11000101 : 0xC5 - BNE Absolute
                        ):                                            
                        value = JMP_AB[subinst]


                    #0b11000110 : 0xC6 - LDA Absolute
                    if (instruction == 0b11000110):
                        value = LDA_AB[subinst]

                    #0b11000111 : 0xC7 - STA Absolute
                    if (instruction == 0b11000111):
                        value = STA_AB[subinst]

                    #0b11001000 : 0xC8 - ADD Absolute
                    if (instruction == 0b11001000):
                        value = ADD_AB[subinst]

                    #0b11001001 : 0xC9 - SUB Absolute
                    if (instruction == 0b11001001):
                        value = SUB_AB[subinst]

                    #0b11001010 : 0xCA - CMP Absolute
                    if (instruction == 0b11001010):
                        value = CMP_AB[subinst]

                    #0b11001011 : 0xCB - CPY Absolute
                    if (instruction == 0b11001011):
                        value = CPY_AB[subinst]


                    #0b11001100 : 0xCC - ADC Absolute
                    if (instruction == 0b11001100):
                        value = ADC_AB[subinst]

                    #0b11001101 : 0xCD - SBC Absolute
                    if (instruction == 0b11001101):
                        value = SBC_AB[subinst]



                    ### Absolute In Place opcodes

                    #0b11011000 : 0xD8 - ADD Absolute In Place
                    if (instruction == 0b11011000):
                        value = ADD_AB_IP[subinst]

                    #0b11011001 : 0xD9 - SUB Absolute In Place
                    if (instruction == 0b11011001):
                        value = SUB_AB_IP[subinst]

                    #0b11011100 : 0xDC - ADC Absolute In Place
                    if (instruction == 0b11011100):
                        value = ADC_AB_IP[subinst]

                    #0b11011101 : 0xDD - SBC Absolute In Place
                    if (instruction == 0b11011101):
                        value = SBC_AB_IP[subinst]




                    ### Indirect addressed opcodes

                    #0b11100110 : 0xE6 - LDA Indirect Zero Page
                    if (instruction == 0b11100110):
                        value = LDA_IND_ZP[subinst]

                    #0b11110110 : 0xF6 - LDA Indirect
                    if (instruction == 0b11110110):
                        value = LDA_IND[subinst]

                    #0b11100111 : 0xE7 - STA Indirect Zero Page
                    if (instruction == 0b11100111):
                        value = STA_IND_ZP[subinst]

                    #0b11110111 : 0xF7 - STA Indirect
                    if (instruction == 0b11110111):
                        value = STA_IND[subinst]

                    #0b11101000 : 0xE8 - ADD Indirect
                    if (instruction == 0b11101000):
                        value = ADD_IND[subinst]

                    #0b11101001 : 0xE9 - SUB Indirect
                    if (instruction == 0b11101001): 
                        value = SUB_IND[subinst]

                    #0b11101100 : 0xEC - ADC Indirect Zerp Page
                    if (instruction == 0b11101100): 
                        value = ADC_IND_ZP[subinst]

                    #0b11111100 : 0xFC - ADC Indirect
                    if (instruction == 0b11111100): 
                        value = ADC_IND[subinst]

                    #0b11101101 : 0xED - SBC Indirect
                    if (instruction == 0b11101101): 
                        value = SBC_IND[subinst]



                    ### Implied addressed opcodes

                    #TAO REMOVED - output now memory mapped
                    #0b11110000 : 0xF0 - TAO Implied
                    #if (instruction == 0b11110000):
                    #    #0b11110000 : 0xF0 - TAO Implied
                    #    value = TAO[subinst]

                    #0b11110001 : 0xF1 - TAS Implied
                    if (instruction == 0b11110001):
                        value = TAS[subinst]

                    #0b11110010 : 0xF2 - CLF Implied
                    if (instruction == 0b11110010):
                        value = CLF[subinst]

                    #0b11110011 : 0xF3 - SEF Implied
                    if (instruction == 0b11110011):
                        value = SEF[subinst]


                    #0b11110100 : 0xF4 - TAX Implied
                    if (instruction == 0b11110100):
                        value = TAX[subinst]

                    #0b11110101 : 0xF5 - TXA Implied
                    if (instruction == 0b11110101):
                        value = TXA[subinst]


                    #0b11111111 : 0xFF - HALT Implied
                    if (instruction == 0b11111111):
                        value = HLT[subinst]


                CODEA[address] = (value & 0xFF) ^ DIRA
                CODEB[address] = ((value >> 8) & 0xFF) ^ DIRB
                CODEC[address] = ((value >> 16) & 0xFF) ^ DIRC
                CODED[address] = ((value >> 24) & 0xFF) ^ DIRD


print("Writing microcode: CODEA.bin")
f=open("microcode/CODEA.bin","wb")
f.write(bytearray(CODEA))
f.close()

print("Writing microcode: CODEB.bin")
f=open("microcode/CODEB.bin","wb")
f.write(bytearray(CODEB))
f.close()

print("Writing microcode: CODEC.bin")
f=open("microcode/CODEC.bin","wb")
f.write(bytearray(CODEC))
f.close()

print("Writing microcode: CODED.bin")
f=open("microcode/CODED.bin","wb")
f.write(bytearray(CODED))
f.close()


answer = input("Program CODE A?")
if answer.upper() in ["Y", "YES"]:
    ret = subprocess.run(["minipro", "-p", "W27C512@DIP28", "-w", "microcode/CODEA.bin"])

answer = input("Program CODE B?")
if answer.upper() in ["Y", "YES"]:
    ret = subprocess.run(["minipro", "-p", "W27C512@DIP28", "-w", "microcode/CODEB.bin"])

answer = input("Program CODE C?")
if answer.upper() in ["Y", "YES"]:
    ret = subprocess.run(["minipro", "-p", "W27C512@DIP28", "-w", "microcode/CODEC.bin"])

answer = input("Program CODE D?")
if answer.upper() in ["Y", "YES"]:
    ret = subprocess.run(["minipro", "-p", "W27C512@DIP28", "-w", "microcode/CODED.bin"])