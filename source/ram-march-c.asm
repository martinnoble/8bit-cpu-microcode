

;byte level march-c- style algorithm

; March-C Minus test algorithm is executed in below 6 steps:
; Step-1: Ascending(W0)
; Step-2: Ascending(r0, w1)
; Step-3: Ascending(r1, w0)
; Step-4: Descending(r0, w1)
; Step-5: Descending(r1, w0)
; Step-6: Ascending(r0)


    .const page 1
    .const address 0
    .const counter 10

    ;do all on page 1 to begin with

    LDA $0x01
    STA :page


start:

; ----- Step-1: Ascending(W0)
    LDA $0x01
    TAS



    LDA $0x00
    STA :address

step1-loop:
    LDA $0x00
    STA (:address)

    LDA :address
    ADD $0x01
    STA :address
    BCC :step1-loop


; ----- Step-2: Ascending(r0, w1)
    LDA $0x02
    TAS

    LDA $0x00
    STA :address

step2-loop:
    LDA (:address)
    CMP $0x00
    BNE :error
    LDA $0xFF
    STA (:address)

    LDA :address
    ADD $0x01
    STA :address
    BCC :step2-loop


; ----- Step-3: Ascending(r1, w0)
    LDA $0x03
    TAS

    LDA $0x00
    STA :address

step3-loop:
    LDA (:address)
    CMP $0xFF
    BNE :error
    LDA $0x00
    STA (:address)

    LDA :address
    ADD $0x01
    STA :address
    BCC :step3-loop


; ----- Step-4: Descending(r0, w1)

    LDA $0x04
    TAS

    LDA $0xFF
    STA :address

step4-loop:
    LDA (:address)
    CMP $0x00
    BNE :error
    LDA $0xFF
    STA (:address)

    LDA :address
    SUB $0x01
    STA :address
    BNE :step4-loop


; ----- Step-5: Descending(r1, w0)

    LDA $0x05
    TAS

    LDA $0xFF
    STA :address

step5-loop:
    LDA (:address)
    CMP $0xFF
    BNE :error
    LDA $0x00
    STA (:address)

    LDA :address
    SUB $0x01
    STA :address
    BNE :step5-loop

; Step-6: Ascending(r0)

    LDA $0x06
    TAS

    LDA $0x00
    STA :address

step6-loop:
    LDA (:address)
    CMP $0x00
    BNE :error

    LDA :address
    ADD $0x01
    STA :address
    BCC :step6-loop

; done

incrementpage:
    LDA :page
    ADD $0x01
    STA :page
    CMP $0x20
    BNE :start

end:
    LDA $0xFF
    TAS


error:
    HLT