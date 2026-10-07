JMP :start
.opera
%6
.operb
%7
.counter
%0
.result
%0
:start
LDA #0
STA .result
LDA .opera
CMP #0
BEQ :end
LDA .operb
CMP #0
BEQ :end
STA .counter
:loop
LDA .result
ADD .opera
STA .result
LDA .counter
SUB #1
STA .counter
BNE :loop
:end
LDA .result
TAO