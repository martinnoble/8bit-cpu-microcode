
;initialise pointer to start of digits array
LDA #1
STA .pointer
TAS

:loop
LDA #0
STA .quotient
LDA .working_val
STA .remainder
:divstart
SUB #10
BCC :divcomplete
STA .remainder
ADD .quotient,#1
LDA .remainder
JMP :divstart
:divcomplete

LDA .remainder
STA (.pointer)
LDA .quotient
STA .working_val
ADD .pointer,#1
TAS

CMP #4
BNE :loop

:zeroskip
SUB .pointer,#1
CMP #1
BEQ :printit
LDA (.pointer)
CMP #0
BNE :printit
JMP :zeroskip

:printloop
SUB .pointer,#1
CMP #0
BEQ :newline
:printit
LDA (.pointer)
ADD #48
TAP
TAS
JMP :printloop

:newline
LDA #10
TAP


JMP :start

:end

LDA 'D'
TAP
LDA 'O'
TAP
LDA 'N'
TAP
LDA 'E'
TAP
LDA #10
TAP
LDA #10
TAP

HLT