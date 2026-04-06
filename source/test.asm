:start
LDA #1
:loop
STA .storage
ADD .storage
TAO
BEQ :start
JMP :loop
.storage
%5