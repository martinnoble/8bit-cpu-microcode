

;byte level march-c- style algorithm

; March-C Minus test algorithm is executed in below 6 steps:
; Step-1: Ascending(W0)
; Step-2: Ascending(r0, w1)
; Step-3: Ascending(r1, w0)
; Step-4: Descending(r0, w1)
; Step-5: Descending(r1, w0)
; Step-6: Ascending(r0)


CONST page 1
CONST address 0
CONST counter 10

;do all on page 1 to begin with


; ----- Step-1: Ascending(W0)
LDA $0x01
TAS

LDA $0x01
STA .page

LDA $0x00
STA .address

:step1-loop
LDA $0x00
STA (.address)

LDA .address
ADD $0x01
STA .address
BCC :step1-loop


; ----- Step-2: Ascending(r0, w1)
LDA $0x02
TAS

LDA $0x01
STA .page

LDA $0x00
STA .address

:step2-loop
LDA (.address)
CMP $0x00
BNE :error
LDA $0xff
STA (.address)

LDA .address
ADD $0x01
STA .address
BCC :step2-loop

:error
HLT