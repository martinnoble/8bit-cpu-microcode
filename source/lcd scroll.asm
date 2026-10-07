
.const LCD_CONTROL 0x4000 
.const LCD_DATA 0x4001

LCD_INIT:
    LDA $0x38
    STA :LCD_CONTROL
    LDA $0x0F
    STA :LCD_CONTROL
    LDA $0x01
    STA :LCD_CONTROL

OUTPUT:
    LDA $0
    TAX
OUTPUT_LOOP:
    LDA :MESSAGE,X
    CMP $0x00
    BEQ :SCROLL
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :OUTPUT_LOOP

SCROLL:
    LDA $0x18
SCROLL_LOOP:
    STA :LCD_CONTROL
    NOP
    NOP
    NOP
    JMP :SCROLL_LOOP

END:
    HLT

.org 0x3F00
MESSAGE:
    .text "Testing LCD scrolling of long text!     "
    .byte $0x00
