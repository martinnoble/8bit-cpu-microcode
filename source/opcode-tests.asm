.const COUNTER 10
.const STATE 11

LDA $0x00
STA :COUNTER


start:
    STA #$0x4000

; subtraction, no underflow
    LDA $1
    STA :STATE
    TAS

    LDA $64
    SUB $32
    BCC :flag-error
    CMP $32
    BNE :maths-error


; subtraction, with underflow
    LDA $2
    STA :STATE
    TAS

    LDA $64
    SUB $128
    BCS :flag-error
    CMP $192
    BNE :maths-error

;16-bit subtraction, no underflow on low or high
    LDA $3
    STA :STATE
    TAS

    LDA $0xCD
    SUB $0x70
    LDA $0xAB
    SBC $0x12
    BCC :flag-error ;should not underflow on high byte
    CMP $0x99
    BNE :maths-error

;16-bit subtration, no underflow on low, underflow on high
    LDA $4
    STA :STATE
    TAS

    LDA $0xCD
    SUB $0x70
    LDA $0xAB
    SBC $0xBA
    BCS :flag-error ;should underflow on high byte
    CMP $0xF1
    BNE :maths-error


;16-bit subtration, underflow on low, no underflow on high
    LDA $5
    STA :STATE
    TAS

    LDA $0x70
    SUB $0xCD
    LDA $0xAB
    SBC $0x12
    BCC :flag-error ;should not underflow on high byte
    CMP $0x98
    BNE :maths-error


;16-bit subtration, underflow on low, underflow on high
    LDA $6
    STA :STATE
    TAS

    LDA $0x70
    SUB $0xCD
    LDA $0x12
    SBC $0xAB
    BCS :flag-error ;should not underflow on high byte
    CMP $0x66
    BNE :maths-error


; -------- memory tests below --------;


;basic memory operations
; all done against single memory location - set to AA initially, all tests then use different values
    .const data-zeropage 0x2D
    .const data-highpage 0x0545 
    LDA $0xAA
    STA :data-zeropage
    STA :data-highpage


;store and load absolute zero page
    LDA $7
    STA :STATE
    TAS

    LDA $0xBB
    STA :data-zeropage
    LDA :data-zeropage
    CMP $0xBB
    BNE :memory-error

;store and load absolute
    LDA $8
    STA :STATE
    TAS

    LDA $0xBB
    STA :data-highpage
    LDA :data-highpage
    CMP $0xBB
    BNE :memory-error


;store absolute, load indirect zero page
    LDA $9
    STA :STATE
    TAS

    LDA $45
    STA $0 ;low byte of address
    LDA $0
    STA $1 ;high byte of address

    LDA $0xCC
    STA :data-zeropage
    LDA ($0)
    CMP $0xCC
    BNE :memory-error

;store indirect zero page, load absolute
    LDA $10
    STA :STATE
    TAS

    LDA $45
    STA $0 ;low byte of address
    LDA $0
    STA $1 ;high byte of address

    LDA $0xDD
    STA ($0)
    LDA #$45
    CMP $0xDD
    BNE :memory-error

;store and load indirect
    LDA $11
    STA :STATE
    TAS

    LDA $0x45
    STA $0 ;low byte of address
    LDA $0x5
    STA $1 ;high byte of address

    LDA $0xAA
    STA ($0)
    LDA ($0)
    CMP $0xAA
    BNE :memory-error

;store and load indirect inverted bits
    LDA $12
    STA :STATE
    TAS

    LDA $0x45
    STA $0 ;low byte of address
    LDA $0x5
    STA $1 ;high byte of address

    LDA $0x55
    STA ($0)
    LDA ($0)
    CMP $0x55
    BNE :memory-error

increment:
;ADD .counter,$1 ;seeing some issues with add in place
    LDA :COUNTER
    ADD $1
    STA :COUNTER

    JMP :start


.org 0x2200
flag-error: ; D4
    HLT


.org 0x2300
maths-error: ; D8
    HLT

.org 0x2400
memory-error: ; DB
    HLT



