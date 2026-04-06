LDA #0		; load 0 into accumulator
ADD #0		; add 0 – clears B reg
TAO			; output sum03	
:up
ADD #1		; add 1
BCS :down 	; start subtracting if carry
TAO			; output sum
JMP :up		; loop addition
:down
SUB #1		; subtract 1
TAO			; transfer A to Output
BEQ :up		; start adding if carry set
JMP :down	; loop subtraction