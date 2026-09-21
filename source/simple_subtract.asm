;initialise and clear down
LDA #0
ADD #0
TAO
TAS

;set carry flag for subtraction
SEF

;start with 64
LDA #64
;subtract 128
SUB #128

;output low byte
TAO
;carry flag should be clear - borrow occurred

;start with 128
LDA #128
;subtract 64
SUB #64

;output result
TAS