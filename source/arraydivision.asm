&0
:num_array
&10
:den_array
&20
:rem_array
&30
:tens_array
&40
:quot_array

&50
.den_pointer
.num_pointer
.tens_pointer
.rem_pointer
.quot_pointer
.loop_count
.counter
.output_pointer

&1
CPY $0,#0



&190 ;locate data at this starting point
%0
%1
%2
%3
%4
%5
%6
%7
%8
:num_array
%9
%10
%3
%5
%7
%9
%11
%13
%15
%17
:den_array
%19
%2
%2
%2
%2
%2
%2
%2
%2
%2
:rem_array
%2
%0
%0
%0
%0
%0
%0
%0
%0
%0
:tens_array
%0
%0
%0
%0
%0
%0
%0
%0
%0
%0
:quot_array
%0

&240
.den_pointer
*den_array
.num_pointer
*num_array
.tens_pointer
*tens_array
.rem_pointer
*rem_array
.quot_pointer
*quot_array
.loop_count
%0
.counter
%0
.output_pointer
%253

&0
:start
LDA #10                     ;10 items in array to process
STA .loop_count
LDA :tens_array             ; reset all pointers
STA .tens_pointer
LDA :rem_array
STA .rem_pointer
LDA :num_array
STA .num_pointer
LDA :quot_array
STA .quot_pointer
LDA :den_array
STA .den_pointer

:array_loop
;TAO
LDA #10                     ;multiply by 10
STA .counter
LDA #0
STA (.tens_pointer)         ;initialise the sum

:loop
LDA (.tens_pointer)
ADD (.rem_pointer)
STA (.tens_pointer)
LDA .counter
SUB #1
STA .counter
BNE :loop

LDA .tens_pointer           ;move to next tens item
SUB #1
STA .tens_pointer
LDA .rem_pointer           ;move to next remainder item
SUB #1
STA .rem_pointer
LDA .loop_count
SUB #1
STA .loop_count
BNE :array_loop            ;loop till end of array


LDA :tens_array           ; reset tens pointer
STA .tens_pointer

LDA :rem_array
STA .rem_pointer


LDA #9                     ;10 items in array to process
STA .loop_count

:divloop
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

;LDA .loop_count
;CMP #1
;BEQ :end

LDA .tens_pointer           ; move to next 10s
SUB #1
STA .tens_pointer


LDA (.quot_pointer)
STA .counter
:quotadd
LDA (.tens_pointer)
ADD (.num_pointer)
STA (.tens_pointer)
LDA .counter
SUB #1
STA .counter
BNE :quotadd

;LDA (.tens_pointer)
;TAO

LDA .quot_pointer           ; move to next quot
SUB #1
STA .quot_pointer
LDA .num_pointer           ; move to next numerator
SUB #1
STA .num_pointer
LDA .den_pointer           ; move to next denominator
SUB #1
STA .den_pointer
LDA .rem_pointer           ; move to next remainder
SUB #1
STA .rem_pointer

LDA .loop_count
SUB #1
STA .loop_count
BNE :divloop            ;loop till end of array

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
LDA .output_pointer
ADD #1
STA .output_pointer
BCC :start`


HLT







