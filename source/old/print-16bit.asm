;divisors low 0-4
;divisors high 5-9
;output - 10-14
;working-low 15
;working-high 16


CONST div_pointer_low 32
CONST div_pointer_low-page 33
CONST div_pointer_high 34
CONST div_pointer_high-page 35
CONST output_pointer 36
CONST output_pointer-page 37

CONST working_low 128
CONST working_high 129

LDA $0
STA .div_pointer_low-page
STA .div_pointer_high-page
STA .output_pointer-page

STA .div_pointer_low
LDA $5
STA .div_pointer_high

LDA $64
STA .output_pointer

;10,000 - 0x2710
LDA $0x10
STA $0
LDA $0x27
STA $5

;1000 - 0x03E8
LDA $0xE8
STA $1
LDA $0x03
STA $6

;100 - 0x0064
LDA $0x64
STA $2
LDA $0
STA $7

;10 - 0x000A
LDA $0x0A
STA $3
LDA $0
STA $8

;1 - 0x0001
LDA $0x01
STA $4
LDA $0
STA $9

;working val set to 43,981 - OxABCD
LDA $0xCD
STA .working_low
LDA $0xAB
STA .working_high



:loopstart
LDA $0
STA (.output_pointer)
LDA (.div_pointer_low)
CMP $1
BEQ :unitcopy 

:subloop
LDA (.output_pointer)
STA #$0x4000
LDA .working_low
SUB (.div_pointer_low)
STA .working_low
LDA .working_high
SBC (.div_pointer_high)
BCC :underflow ;if carry was cleared, this indicates a borrow, so we underflowed on the high byte
STA .working_high
LDA (.output_pointer)
ADD $1
STA (.output_pointer)
JMP :subloop
:underflow ;need to add back the low value
LDA .working_low
ADD (.div_pointer_low)
STA .working_low

;LDA .working_low
;STA #$0x4000
;LDA .working_high
;TAS
;HLT

;increment the pointers
LDA .div_pointer_low
ADD $1
STA .div_pointer_low

LDA .div_pointer_high
ADD $1
STA .div_pointer_high

LDA .output_pointer
ADD $1
STA .output_pointer

JMP :loopstart

:unitcopy
LDA .working_low
STA (.output_pointer)

LDA #$64
TAS
LDA #$65
STA #$0x4000


;now print it out
LDA $64
:printloop
STA .output_pointer
LDA (.output_pointer)
ADD $48
STA #$0x6000
LDA .output_pointer
ADD $1
CMP $69
BNE :printloop


LDA '\n'
STA #$0x6000
STA #$0x6000