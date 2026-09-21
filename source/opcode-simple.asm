
:start


; subtraction, no underflow

LDA $64
SUB $16
BCC :error
CMP $48
BNE :error

JMP :start

:error
HLT
