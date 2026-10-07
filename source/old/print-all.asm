CONST char 0
CONST limit 1

LDA $32
STA .char
LDA $48
STA .limit

:print
LDA .char
STA #$0x4000
STA #$0x6000
ADD $1
STA .char
CMP .limit
BNE :print
LDA $10
STA #$0x6000
STA #$0x6000

; 00100000
; 00100000

; 00100001
; 00110000

