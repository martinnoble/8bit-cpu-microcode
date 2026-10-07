
CONST working_val 0
CONST digits_array 1
CONST pointer 4
CONST pointer_high 5

CONST quotient 6
CONST remainder 7
CONST initial 8

CONST number 9

CONST run 10

LDA '\n'
STA #$0x6000
STA #$0x6000


;initialise fibonacci sequence
LDA $0
STA .number
STA .pointer_high
LDA $1
;set a flag to control when we stop printing values
STA .run

:start
;print out previous value (so we start with the initial 0)
LDA .number
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

;:zeroskip
;LDA .pointer
;SUB $1
;STA .pointer
;CMP $1
;BEQ :printit
;LDA (.pointer)
;CMP $0
;BNE :printit
;JMP :zeroskip

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
LDA .number
ADD $1
STA .number
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