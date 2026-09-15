CONST tenthousands 0
CONST thousands 1
CONST hundreds 2
CONST tens 3
CONST units 4


CONST pointer 120
CONST pointer_high 121
CONST digits 127

CONST working_val_low 10
CONST working_val_high 10

CONST quotient 64
CONST remainder 65

CONST previous_low 66
CONST previous_high 67
CONST current_low 68
CONST current_high 69

CONST run 128

LDA $5
STA .digits
LDA $0
STA .pointer
STA .pointer_high

STA .tenthousands
STA .thousands
STA .hundreds
STA .units
STA .tens


LDA 'F'
STA #$0x6000
LDA 'i'
STA #$0x6000
LDA 'b'
STA #$0x6000
LDA 'o'
STA #$0x6000
LDA 'n'
STA #$0x6000
LDA 'a'
STA #$0x6000
LDA 'c'
STA #$0x6000
LDA 'c'
STA #$0x6000
LDA 'i'
STA #$0x6000
LDA '\n'
STA #$0x6000
STA #$0x6000


;initialise fibonacci sequence
LDA $0
STA .previous_low
STA .previous_high
STA .current_high
LDA $1
STA .current_low
;set a flag to control when we stop printing values
STA .run

:start
;print out previous value (so we start with the initial 0)
LDA .previous_low
STA .working_val_low
STA #$0x4000


;working_val_low contains the number to print

;LDA $0
;STA .quotient
;:hundreds_loop
;LDA .working_val_low
;SUB $100
;BCC :hundreds_complete
;STA .working_val_low
;LDA .quotient
;ADD $1
;STA .quotient
;JMP :hundreds_loop
;:hundreds_complete
;LDA .quotient
;STA .hundreds

;working_val_low contains value with only tens

;LDA $0
;STA .quotient
;:tens_loop
;LDA .working_val_low
;SUB $10
;BCC :tens_complete
;STA .working_val_low
;LDA .quotient
;ADD $1
;STA .quotient
;JMP :tens_loop
;:tens_complete
;LDA .quotient
;STA .tens

;working_val_low contains just the units

;LDA .working_val_low
;STA .units

;LDA $0
;STA .pointer_high ;initialise to start of the digits
;:printloop
;STA .pointer
;LDA (.pointer)
;ADD $48
;STA #$0x6000
;LDA .pointer
;ADD $1
;CMP .digits
;BNE :printloop


;LDA '\n'
;STA #$0x6000

;check if we need to stop
LDA .run
CMP $0
BEQ :end

;perform fibonacci calculation
LDA .previous_low
STA .working_val_low
LDA .previous_high
STA .working_val_high

LDA .current_low
STA .previous_low
LDA .current_high
STA .previous_high

LDA .current_low
ADD .working_val_low
STA .current_low
LDA .current_high
ADC .working_val_high
STA .current_high

;continue if we didn't overflow
BCC :start

;set flag to stop after printing next value
LDA $0
STA .run

JMP :start

:end
LDA '\n'
STA #$0x6000

LDA 'D'
STA #$0x6000
LDA 'O'
STA #$0x6000
LDA 'N'
STA #$0x6000
LDA 'E'
STA #$0x6000
LDA '\n'
STA #$0x6000
STA #$0x6000

HLT