CONST pointer 0
CONST pointer_high 1

;start on page 1
LDA $1
STA .pointer_high

;start on address 0
LDA $0

TAS

:writeloop
STA .pointer
STA (.pointer)
STA #$0x4000
ADD $1
BCC :writeloop
LDA .pointer_high
ADD $1
CMP $0x02
BEQ :startreading
STA .pointer_high
LDA $0
JMP :writeloop

:startreading

;start on page 1
LDA $1
STA .pointer_high

TAS

;start on address 0
LDA $0

:readloop
STA .pointer
LDA (.pointer)
CMP .pointer
BNE :error
STA #$0x4000
ADD $1
BCC :readloop
LDA .pointer_high
ADD $1
CMP $0x02
BEQ :error
STA .pointer_high
LDA $0
JMP :readloop

:error
TAS
HLT

:end
HLT
