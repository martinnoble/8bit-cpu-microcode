CONST pointer 0
CONST pointer_high 1

CONST counter 10
CONST state 11

CONST dataval 16

; writing a fixed value across all RAM works
; writing counter values across all RAM doesn't work
LDA $0x55
STA .dataval

LDA $0
STA .counter

LDA $0x1
STA .pointer_high ;high byte of address

:writing
STA #$0x4000

LDA .counter
STA .pointer ;low byte of address

LDA .dataval
STA (.pointer)
LDA (.pointer)
CMP .dataval
BNE :memory-error

LDA .counter
ADD $1
STA .counter

BCC :writing


LDA $0
STA .counter

:reading
STA #$0x4000

LDA .dataval
STA .pointer ;low byte of address

LDA (.pointer)
CMP .dataval
BNE :memory-error

LDA .counter
ADD $1
STA .counter

BCC :reading

;if we overflowed, increment page
LDA .pointer_high
ADD $1
STA .pointer_high
JMP :writing

:memory-error
HLT