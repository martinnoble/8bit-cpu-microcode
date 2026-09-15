

;write value to fixed ram location
LDA $0x00
STA #$0x0245

; loop reading value over and over to ensure it remains stable
:loop
LDA #$0x0245
CMP $0x00
JMP :loop

HLT