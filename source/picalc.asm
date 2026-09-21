CONST num_array 0
CONST num_array_end 9
CONST den_array 16
CONST den_array_end 25
CONST rem_array 32
CONST rem_array_end 41
CONST tens_array 48
CONST tens_array_end 57
CONST quot_array 64
CONST quot_array_end 73

CONST num_pointer 80
CONST den_pointer 81
CONST rem_pointer 82
CONST tens_pointer 83
CONST quot_pointer 84
CONST loop_count 85
CONST counter 86
CONST working_val 88
CONST output_pointer 89

; clear output reg
LDA #0
TAO

; state 1 - initial setup
LDA #128
TAS

LDA #253
STA .output_pointer

LDA #10                 ; 10 items in numerator array
STA .loop_count

LDA #0                  ; set starting value
STA .working_val 
LDA .num_array          ; initialise numerator array pointer       could use CPY here
STA .num_pointer

:numerator_init
LDA .working_val
STA (.num_pointer)
ADD .working_val,#1
ADD .num_pointer,#1
SUB .loop_count,#1
BNE :numerator_init

;first check above works
HLT

LDA .den_array          ; initialise denominator array pointer       
STA .den_pointer
LDA #10                 ; hard code first denominator to 10
STA (.den_pointer)
ADD .den_pointer,#1


LDA #9                 ; 9 more items to fill in
STA .loop_count

LDA #3                  ; next denominator is 3
STA .working_val 

:denominator_init
LDA .working_val
STA (.den_pointer)
ADD .working_val,#2     ; increase by 2 each time
ADD .den_pointer,#1
SUB .loop_count,#1
BNE :denominator_init




LDA #10                     ;10 items in array to process
STA .loop_count
LDA .rem_array             ; reset all pointers
STA .rem_pointer

:rems_init
LDA #2
STA (.rem_pointer)
ADD .rem_pointer,#1
SUB .loop_count,#1
BNE :rems_init

:start

LDA .num_array_end          ; reset all pointers
STA .num_pointer
LDA .den_array_end
STA .den_pointer
LDA .rem_array_end
STA .rem_pointer
LDA .tens_array_end          
STA .tens_pointer
LDA .quot_array_end
STA .quot_pointer


LDA #10                     ;10 items in array to process
STA .loop_count

:array_loop

; multiple by 10
LDA .tens_pointer
SUB .tens_array
ADD #64
TAS


LDA #10                     ;multiply by 10
STA .counter
LDA #0
STA (.tens_pointer)         ;initialise the sum

:loop
LDA (.tens_pointer)
ADD (.rem_pointer)
STA (.tens_pointer)
SUB .counter,#1
BNE :loop

SUB .tens_pointer,#1          ;move to next tens item
SUB .rem_pointer,#1           ;move to next remainder item
SUB .loop_count,#1
BNE :array_loop            ;loop till end of array


; dividing
LDA #32
TAS

LDA #9                     ;9 items in array to process
STA .loop_count

LDA .tens_array_end           ; reset tens pointer
STA .tens_pointer

LDA .rem_array_end              ; reset rem pointer
STA .rem_pointer

:divloop
LDA (.num_pointer)
ADD #32
TAS

LDA #0
STA (.quot_pointer)
LDA (.tens_pointer)
STA (.rem_pointer)
:divstart
SUB (.den_pointer)
BCC :divcomplete
STA (.rem_pointer)
LDA (.quot_pointer)
ADD #1
STA (.quot_pointer)
LDA (.rem_pointer)
JMP :divstart
:divcomplete

SUB .tens_pointer,#1           ; move to next 10s

LDA (.quot_pointer)
STA .counter
:quotadd
LDA (.tens_pointer)
ADD (.num_pointer)
STA (.tens_pointer)
SUB .counter,#1
BNE :quotadd

SUB .quot_pointer,#1           ; move to next quot
SUB .num_pointer,#1           ; move to next numerator
SUB .den_pointer,#1           ; move to next denominator
SUB .rem_pointer,#1           ; move to next remainder

SUB .loop_count,#1
BNE :divloop            ;loop till end of array

; final division
LDA (.num_pointer)
ADD #32
TAS

LDA #0
STA (.quot_pointer)
LDA (.tens_pointer)
STA (.rem_pointer)
:findivstart
SUB #10
BCC :findivcomplete
STA (.rem_pointer)
LDA (.quot_pointer)
ADD #1
STA (.quot_pointer)
LDA (.rem_pointer)
JMP :findivstart
:findivcomplete

LDA (.quot_pointer)
TAO

STA (.output_pointer)
ADD .output_pointer,#1

BCC :start

LDA #255
TAS

HLT
