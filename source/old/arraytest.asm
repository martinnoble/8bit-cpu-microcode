&28
.array_pointer
%32
.value
%0

&0
:start
LDA .value
STA (.array_pointer)
ADD #1
STA .value
LDA .array_pointer
ADD #1
TAO
BCS :end
STA .array_pointer
JMP :start
:end
LDA #32
STA .array_pointer
JMP :start