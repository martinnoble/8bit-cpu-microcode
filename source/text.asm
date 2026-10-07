
.const OUTPUT 0x4000
.const PRINTER 0x6000


    LDA 0x40
    STA 
    LDA $0x00
    TAX
    LDA 
setupheartloop:
    LDA :message,X
    CMP $0x00
    BEQ :end
    STA :OUTPUT
    STA :PRINTER

    TXA
    ADD $0x01
    TAX
    JMP :readloop


LDA $0x00
TAX
readloop:
    LDA :message,X
    CMP $0x00
    BEQ :end
    STA :OUTPUT
    STA :PRINTER

    TXA
    ADD $0x01
    TAX
    JMP :readloop

end:
    HLT

.org 0x2100
message:
    .text "Hello World!"
    .byte $0x0A
    .byte $0x00


