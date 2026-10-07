

;write value to fixed ram location
LDA $0x00
LDA $0xCD
STA #$0x1482


; loop reading value over and over to ensure it remains stable
loop:
    LDA $0xAA
    STA #$0x1482
    LDA #$0x1482
    CMP $0xAA
    BNE :end

    LDA $0xBB
    STA #$0x1482
    LDA #$0x1482
    CMP $0xBB
    BEQ :loop

end:
    HLT