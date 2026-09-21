
CONST previous_low 0
CONST previous_high 1
CONST current_low 2
CONST current_high 3

CONST next_low 4
CONST next_high 5

LDA $0
STA .previous_low
STA .previous_high
STA .current_high
LDA $1
STA .current_low

:loop
; output the current value to output and status
LDA .previous_low
STA #$0x4000
LDA .previous_high
TAS

;perform 16-bit add or operand
LDA .previous_low
ADD .current_low
STA .next_low
LDA .previous_high
ADC .current_high
STA .next_high

;shuffle down
LDA .current_low
STA .previous_low
LDA .current_high
STA .previous_high
LDA .next_low
STA .current_low
LDA .next_high
STA .current_high

JMP :loop