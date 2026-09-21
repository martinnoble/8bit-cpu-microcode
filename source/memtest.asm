&60
.array_pointer
%64
.limit
%244

&64
:array_start

&0
;loop through setting mem locations to match their location
:start
LDA :array_start
STA .array_pointer
TAO
:setloop
LDA .array_pointer
STA (.array_pointer)
TAO
ADD #1
STA .array_pointer
CMP .limit
BNE :setloop

LDA .array_pointer
SUB #1
STA .array_pointer

:getloop
LDA (.array_pointer)
TAO
CMP .array_pointer
BNE :error
SUB #1
STA .array_pointer
CMP :array_start
BNE :getloop
JMP :start

:error
LDA .array_pointer
TAO
HLT
