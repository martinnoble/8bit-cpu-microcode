CONST counter 0
CONST number 1
CONST pointer_low 2
CONST pointer_high 3

:beginning
LDA $0x04
STA .pointer_low
STA .number
LDA $0x00
STA .pointer_high

LDA $0

:start
STA .counter
TAS
LDA .number

:loop
STA (.pointer_low)
LDA (.pointer_low)
;write to output
STA #$0x4000

CMP .number
BNE :end ;error out if we fail to read back what we wrote

;increment the pointer
LDA .pointer_low
ADD $1
STA .pointer_low
BCC :continue
LDA .pointer_high
ADD $1
STA .pointer_high
CMP $0x20
BEQ :beginning
:continue

LDA .number
ADD $1
STA .number
BCC :loop

LDA .counter
ADD $1
JMP :start
:end
LDA .pointer_low
STA #$0x4000
LDA .pointer_high
TAS
HLT