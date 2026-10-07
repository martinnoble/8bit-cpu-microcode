JMP :start
.dividend
%8
.divisor
%2
.quotient
%0
.remainder
%0
:start
LDA #0
STA .quotient
TAO
LDA .dividend
STA .remainder
:loop
SUB .divisor
BCC :output
STA .remainder
LDA .quotient
ADD #1
STA .quotient
LDA .remainder
JMP :loop
:output
LDA .quotient
TAO
HLT