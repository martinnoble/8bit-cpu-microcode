LDA #0
ADD #1
JMP :jumpdest
HLT
HLT
HLT
:jumpdest
LDA #0
TAO
BNE :bnedest
HLT
HLT
HLT
:bnedest
LDA #1
TAO
BCC :bcctest
HLT
HLT
HLT
:bcctest
LDA #2
TAO
SUB #2
BEQ :beqtest
HLT
HLT
HLT
:beqtest
LDA #3
TAO
ADD #255
BCS :bcstest
HLT
HLT
HLT
:bcstest
LDA #4
TAO
SUB #4
BNE #255
LDA #5
TAO
ADD #255
BCC #255
LDA #6
TAO
BEQ #255
LDA #7
TAO
ADD #1
BCS #255
TAO
JMP #0