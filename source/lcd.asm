
.include "lib/lcd_init.asm"

    LDA $0x40
    STA :LCD_CONTROL

    LDA $0
    TAX
heartsetuploop:
    LDA :heart,X
    CMP $0x80
    BEQ :heartdone
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :heartsetuploop
heartdone:

    LDA $0x48
    STA :LCD_CONTROL

    LDA $0
    TAX
pacopenloop:
    LDA :pacopen,X
    CMP $0x80
    BEQ :pacopendone
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :pacopenloop
pacopendone:

    LDA $0x50
    STA :LCD_CONTROL

    LDA $0
    TAX
pacclosedloop:
    LDA :pacclosed,X
    CMP $0x80
    BEQ :paccloseddone
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :pacclosedloop
paccloseddone:


    LDA $0x58
    STA :LCD_CONTROL
    
    LDA $0
    TAX
pelletloop:
    LDA :pellet,X
    CMP $0x80
    BEQ :pelletdone
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :pelletloop
pelletdone:

    LDA $0x60
    STA :LCD_CONTROL
    
    LDA $0
    TAX
ghostloop:
    LDA :ghost,X
    CMP $0x80
    BEQ :ghostdone
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :ghostloop
ghostdone:


LDA $0x0C
STA :LCD_CONTROL
LDA $0x01
STA :LCD_CONTROL


    LDA $0
    TAX


readloop:
    LDA :message,X
    CMP $0x00
    BEQ :done
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :readloop

done:

    LDA $0xC0
    STA :LCD_CONTROL

    LDA $0x00
    TAX
readloop2:
    LDA :message2,X
    CMP $0x00
    BEQ :end
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :readloop2

end:


.const pacmode 0x00
.const position 0x01

LDA $0x80
STA :position
LDA $0x01
STA :pacmode


playloop:
    LDA :position
    STA :LCD_CONTROL

    LDA $0x20
    STA :LCD_DATA
    LDA :pacmode
    STA :LCD_DATA

    ADD $0x01
    CMP $0x03
    BNE :continue
    LDA $0x01
continue:
    STA :pacmode

    LDA $0x0F
delay:
    SUB $0x01
    BNE :delay

    LDA :position
    ADD $0x01
    STA :position
    CMP $0x8F
    BEQ :winner
    JMP :playloop

winner:
    LDA :position
    STA :LCD_CONTROL
    LDA :pacmode
    STA :LCD_DATA

    LDA $0xCC
    STA :LCD_CONTROL
    LDA $0x39
    STA :LCD_DATA
    STA :LCD_DATA
    STA :LCD_DATA
    STA :LCD_DATA
    HLT

.org 0x3000
message:
    .byte $0x02
    .byte $0x20
    .byte $0x03
    .byte $0x20
    .byte $0x03
    .byte $0x20
    .byte $0x03
    .byte $0x20
    .byte $0x03
    .byte $0x20
    .byte $0x03
    .byte $0x20
    .byte $0x03
    .byte $0x20
    .byte $0x03
    .byte $0x04
    .byte $0x00

message2:
    .text "HIGH SCORE: 0"
    .byte $0x00




heart:
    .byte $0x00
    .byte $0x0A
    .byte $0x1F
    .byte $0x1F
    .byte $0x0E
    .byte $0x04
    .byte $0x00
    .byte $0x00
    .byte $0x80


pacclosed:
    .byte $0x0E
    .byte $0x1F
    .byte $0x1B
    .byte $0x1F
    .byte $0x1F
    .byte $0x18
    .byte $0x1F
    .byte $0x0E
    .byte $0x80

pacopen:
    .byte $0x0E
    .byte $0x1F
    .byte $0x1B
    .byte $0x1F
    .byte $0x1C
    .byte $0x18
    .byte $0x1C
    .byte $0x0F
    .byte $0x80

pellet:
    .byte $0x00
    .byte $0x00
    .byte $0x00
    .byte $0x00
    .byte $0x00
    .byte $0x06
    .byte $0x06
    .byte $0x00
    .byte $0x80

ghost:
    .byte $0x0E
    .byte $0x1F
    .byte $0x15
    .byte $0x15
    .byte $0x1F
    .byte $0x1F
    .byte $0x1F
    .byte $0x15
    .byte $0x80