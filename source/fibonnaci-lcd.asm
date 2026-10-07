.const LCD_CONTROL 0x4000
.const LCD_DATA 0x4001


.const tenthousands 0
.const thousands 1
.const hundreds 2
.const tens 3
.const units 4


.const pointer 120
.const pointer_high 121
.const digits 127

.const working_val_low 10
.const working_val_high 11

.const quotient 64
.const remainder 65

.const previous_low 66
.const previous_high 67
.const current_low 68
.const current_high 69

.const run 128

initlcd:
    LDA $0x38
    STA :LCD_CONTROL
    LDA $0x0F
    STA :LCD_CONTROL
    LDA $0x01
    STA :LCD_CONTROL


    LDA $5
    STA :digits
    LDA $0
    STA :pointer
    STA :pointer_high

    STA :tenthousands
    STA :thousands
    STA :hundreds
    STA :units
    STA :tens
    TAX


textloop:
    LDA :text-fib,X
    CMP $0x00
    BEQ :textdone
    STA :LCD_DATA

    TXA
    ADD $0x01
    TAX
    JMP :textloop

textdone:



;initialise fibonacci sequence
    LDA $0
    STA :previous_low
    STA :previous_high
    STA :current_high
    LDA $1
    STA :current_low
    ;set a flag to control when we stop printing values
    STA :run

    ;JMP :print

start:
    ;print out previous value (so we start with the initial 0)
    LDA :previous_low
    STA :working_val_low

    LDA :previous_high
    STA :working_val_high
    


;working_val_low and working_val_high contains the number to print

    LDA $0
    STA :quotient    ; Initialize quotient to 0

DIV10000:
    ;SEC         ; Set carry before 16-bit subtraction
    LDA :working_val_low
    SUB $0x10    ; Subtract 100 from low byte
    TAX         ; Temporarily save the temporary low byte
    LDA :working_val_high
    SBC $0x27      ; Subtract borrow from high byte
        
    BCC :UNDERFLOW10000 ; If carry is clear, we went below zero!
                    
    ; Successful subtraction: Save new values and increment quotient
    STA :working_val_high   ; Update high byte
    TXA         ; Pull low byte
    STA :working_val_low   ; Update low byte
    LDA :quotient
    ADD $1    ; Increase quotient
    STA :quotient
    JMP :DIV10000    ; Repeat

UNDERFLOW10000:
    ; working vals contain the remainder, quotient contains he count of hundreds
    LDA :quotient
    STA :tenthousands


    LDA $0
    STA :quotient    ; Initialize quotient to 0

DIV1000:
    ;SEC         ; Set carry before 16-bit subtraction
    LDA :working_val_low
    SUB $0xE8    ; Subtract 100 from low byte
    TAX         ; Temporarily save the temporary low byte
    LDA :working_val_high
    SBC $0x03      ; Subtract borrow from high byte
        
    BCC :UNDERFLOW1000 ; If carry is clear, we went below zero!
                    
    ; Successful subtraction: Save new values and increment quotient
    STA :working_val_high   ; Update high byte
    TXA         ; Pull low byte
    STA :working_val_low   ; Update low byte
    LDA :quotient
    ADD $1    ; Increase quotient
    STA :quotient
    JMP :DIV1000    ; Repeat

UNDERFLOW1000:
    ; working vals contain the remainder, quotient contains he count of hundreds
    LDA :quotient
    STA :thousands


    LDA $0
    STA :quotient    ; Initialize quotient to 0

DIV100:
    ;SEC         ; Set carry before 16-bit subtraction
    LDA :working_val_low
    SUB $100    ; Subtract 100 from low byte
    TAX         ; Temporarily save the temporary low byte
    LDA :working_val_high
    SBC $0      ; Subtract borrow from high byte
        
    BCC :UNDERFLOW100 ; If carry is clear, we went below zero!
                    
    ; Successful subtraction: Save new values and increment quotient
    STA :working_val_high   ; Update high byte
    TXA         ; Pull low byte
    STA :working_val_low   ; Update low byte
    LDA :quotient
    ADD $1    ; Increase quotient
    STA :quotient
    JMP :DIV100    ; Repeat

UNDERFLOW100:
    ; working vals contain the remainder, quotient contains he count of hundreds
    LDA :quotient
    STA :hundreds


;working_val_low contains value with only tens and units - max value 99 so no need to perform 16 bit maths

    LDA $0
    STA :quotient    ; Initialize quotient to 0

DIV10:
    ;SEC         ; Set carry before 16-bit subtraction
    LDA :working_val_low
    SUB $10    ; Subtract 100 from low byte
    TAX         ; Temporarily save the temporary low byte
    LDA :working_val_high
    SBC $0      ; Subtract borrow from high byte
        
    BCC :UNDERFLOW10 ; If carry is clear, we went below zero!
                    
    ; Successful subtraction: Save new values and increment quotient
    STA :working_val_high   ; Update high byte
    TXA         ; Pull low byte
    STA :working_val_low   ; Update low byte
    LDA :quotient
    ADD $1    ; Increase quotient
    STA :quotient
    JMP :DIV10    ; Repeat

UNDERFLOW10:
    ; working vals contain the remainder, quotient contains he count of hundreds
    LDA :quotient
    STA :tens

;working_val_low contains just the units

    LDA :working_val_low
    STA :units


    ;move to 2nd line, position 1
    LDA $0xC0
    STA :LCD_CONTROL

print:

    LDA $0
    STA :pointer_high ;initialise to start of the digits
printloop:
    STA :pointer
    LDA (:pointer)
    ADD $48
    STA :LCD_DATA
    LDA :pointer
    ADD $1
    CMP :digits
    BNE :printloop

;check if we need to stop
    LDA :run
    CMP $0
    BEQ :end

;perform fibonacci calculation
    LDA :previous_low
    STA :working_val_low
    LDA :previous_high
    STA :working_val_high

    LDA :current_low
    STA :previous_low
    LDA :current_high
    STA :previous_high

    LDA :current_low
    ADD :working_val_low
    STA :current_low
    LDA :current_high
    ADC :working_val_high
    STA :current_high

;continue if we didn't overflow
    BCC :start

;set flag to stop after printing next value
    LDA $0
    STA :run

    JMP :start



end:
    HLT



.org 0x3000
text-fib:
    .text "Fibonacci"
    .byte $0x00
