
; test or writing and reading a single address repeatedly
; alternates between 0xAA and 0xBB as values.
; A register to changed to different values between write and read
; to ensure it is actually getting the data back from RAM

CONST data-zeropage-one 0x2D
CONST data-zeropage-two 0xA5

:start
; store in one location, load from another to check both operations work
LDA $0x0A
STA .data-zeropage-one
LDA $0x00
TAS
STA .data-zeropage-two
LDA .data-zeropage-one
CMP $0x0A
BNE :error

; store in one location, compare with that location immediately - A -> RAM -> B -> SUB = 0
LDA $0x01
TAS
LDA $0xFA
STA .data-zeropage-one
CMP .data-zeropage-one
BNE :error


LDA $0x0B
STA .data-zeropage-one
LDA $0x02 ;change value in A reg before loading back
TAS
LDA .data-zeropage-one
CMP $0x0B
BNE :error

LDA $0x0B
STA .data-zeropage-two
LDA $0x03 ;change value in A reg before loading back
TAS
LDA .data-zeropage-two
CMP $0x0B
BNE :error

LDA $0x0C
STA .data-zeropage-one
LDA $0x04 ;change value in A reg before loading back
TAS
LDA .data-zeropage-one
CMP $0x0C
BNE :error

LDA $0x0D
STA .data-zeropage-two
LDA $0x05 ;change value in A reg before loading back
TAS
LDA .data-zeropage-two
CMP $0x0D
BNE :error

; now do it on a higher page


NOP
NOP
NOP
NOP

LDA $0xFA
STA #$0x0140
LDA $0x06 ;change value in A reg before loading back
TAS
LDA #$0x0140
CMP $0xFA
BNE :error

LDA $0xFB
STA #$0x1A80
LDA $0x07 ;change value in A reg before loading back
TAS
LDA #$0x1A80
CMP $0xFB
BNE :error

LDA $0xFC
STA #$0x0140
LDA $0x08 ;change value in A reg before loading back
TAS
LDA #$0x0140
CMP $0xFC
BNE :error

LDA $0xFD
STA #$0x1A80
LDA $0x09 ;change value in A reg before loading back
TAS
LDA #$0x1A80
CMP $0xFD
BNE :error

JMP :start

:error
HLT