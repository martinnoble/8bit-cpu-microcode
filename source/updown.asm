LDA $0x00		; load 0 into accumulator
ADD $0x00		; add 0 – clears B reg

:up
ADD $0x01		; add 1
BCS :down 	    ; start subtracting if carry
STA #$0x4000    ; output sum
TAS
TAX
JMP :up		    ; loop addition
:down
SUB $0x01		; subtract 1
STA #$0x4000	; transfer A to Output
TAS
TAX
BEQ :up		    ; start adding if carry set
JMP :down	    ; loop subtraction