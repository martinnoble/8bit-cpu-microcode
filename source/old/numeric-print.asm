

CONST digits_array 1
CONST pointer 4

CONST quotient 5
CONST remainder 6
CONST initial 7

CONST previous_low 8
CONST previous_high 9
CONST current_low 10
CONST current_high 11

CONST working_val_low 20
CONST working_val_high 21

;initialise fibonacci sequence
LDA #0
STA .previous_low
STA .previous_high
STA .current_high
LDA #1
STA .current_low

:start
;perform fibonacci calculation
;move previous value to working value
LDA .previous_low
STA .working_val_low
LDA .previous_high
STA .working_val_high

;move current value to previous value
LDA .current_low
STA .previous_low
LDA .current_high
STA .previous_high

LDA .current_low
ADD .working_val_low
STA .current_low
TAO
TAS
BCS :end
LDA .current_high
ADC .working_val_high
STA .current_high
BCS :end

JMP :start

;print out previous value
LDA .previous_low
STA .working_val_low
TAO
LDA .previous_high
STA .working_val_high
TAS

JMP :start

:end
HLT