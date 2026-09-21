CONST working_pointer_low 0
CONST working_pointer_low-high 1
CONST working_pointer_high 2
CONST working_pointer_high-high 3

CONST div_pointer_low 4
CONST div_pointer_low-high 5
CONST div_pointer_high 6
CONST div_pointer_high-high 7

LDA $0
STA .working_pointer_low-high
STA .working_pointer_high-high
STA .div_pointer_low-high
STA .div_pointer_high-high

LDA $10
STA .div_pointer_low
LDA $11
STA .div_pointer_high

LDA $12
STA .working_pointer_low
LDA $13
STA .working_pointer_high



;10,000 - 0x2710
LDA $0x10
STA (.div_pointer_low)
LDA $0x27
STA (.div_pointer_high)



;working val set to 43,981 - OxABCD
LDA $0xCD
STA (.working_pointer_low)
LDA $0xAB
STA (.working_pointer_high)

LDA (.working_pointer_low)
STA #$0x4000
LDA (.working_pointer_high)
TAS

LDA (.working_pointer_low)
SUB (.div_pointer_low)
STA (.working_pointer_low)
LDA (.working_pointer_high)
SBC (.div_pointer_high)
STA (.working_pointer_high)

LDA (.working_pointer_low)
STA #$0x4000
LDA (.working_pointer_high)
TAS