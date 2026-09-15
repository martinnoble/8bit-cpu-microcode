LDA #0
STA $0


:start
LDA $0
TAS

LDA #255
STA $1  ; set the array pointer
:clearloop
TAO
LDA #0
STA ($1)
SUB $1,#1
LDA $1
CMP #1
BNE :clearloop

LDA #2
STA $1  ; set the array pointer
:arrayloop2
STA ($1)
LDA ($1)
TAO
ADD $1,#1
BCC :arrayloop2

ADD $0,#1

JMP :start

:error
