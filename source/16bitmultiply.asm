CONST a_low 0
CONST b_low 2
CONST out_low 4
CONST out_high 5

;initial setup
CLF
LDA #16
STA .a_low
LDA #104
STA .b_low
LDA #0
STA .out_low
STA .out_high


:multiply
CLF
LDA .out_low
ADD .b_low
STA .out_low
LDA .out_high
ADD #0
STA .out_high

SEF
LDA .a_low
SUB #1
STA .a_low

BNE :multiply

