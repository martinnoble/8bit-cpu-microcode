
;output digits in 1,2,3

CONST working_val 10

CONST pointer 32
CONST pointer_high 33

CONST quotient 64
CONST remainder 65

CONST previous 66
CONST current 67

CONST run 128

LDA 'F'
STA #$0x6000
LDA 'i'
STA #$0x6000
LDA 'b'
STA #$0x6000
LDA 'o'
STA #$0x6000
LDA 'n'
STA #$0x6000
LDA 'a'
STA #$0x6000
LDA 'c'
STA #$0x6000
LDA 'c'
STA #$0x6000
LDA 'i'
STA #$0x6000
LDA '\n'
STA #$0x6000
STA #$0x6000


;initialise fibonacci sequence
LDA $0
STA .previous
LDA $1
STA .current
;set a flag to control when we stop printing values
STA .run

:start
;print out previous value (so we start with the initial 0)
LDA .previous
STA .working_val
STA #$0x4000

;initialise pointer to start of digits array
LDA $1
STA .pointer
TAS

:loop
LDA $0
STA .quotient
LDA .working_val
STA .remainder
:divstart
SUB $10
BCC :divcomplete
STA .remainder
LDA .quotient
ADD $1
STA .quotient
LDA .remainder
JMP :divstart
:divcomplete

LDA .remainder
STA (.pointer)
LDA .quotient
STA .working_val
LDA .pointer
ADD $1
STA .pointer
TAS

CMP $4
BNE :loop

:zeroskip
LDA .pointer
SUB $1
STA .pointer
CMP $1
BEQ :printit
LDA (.pointer)
CMP $0
BNE :printit
JMP :zeroskip

:printloop
LDA .pointer
SUB $1
STA .pointer
CMP $0
BEQ :newline
:printit
LDA (.pointer)
ADD $48
STA #$0x6000
TAS
JMP :printloop

:newline
LDA '\n'
STA #$0x6000

;check if we need to stop
LDA .run
CMP $0
BEQ :end

;perform fibonacci calculation
LDA .previous
STA .working_val
LDA .current
STA .previous
ADD .working_val
STA .current
;continue if we didn't overflow
BCC :start

;set flag to stop after printing next value
LDA $0
STA .run

JMP :start

:end
LDA '\n'
STA #$0x6000

LDA 'D'
STA #$0x6000
LDA 'O'
STA #$0x6000
LDA 'N'
STA #$0x6000
LDA 'E'
STA #$0x6000
LDA '\n'
STA #$0x6000
STA #$0x6000

HLT