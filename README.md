# 8bit breadboard CPU

The project contains the microcode generator and related assembler to enable writing programs for my custom "Ben Eater" style breadboad computer.

It consists of an 8-bit data bus and 16-bit address bus.

Control logic is split across 4 ROMs enabling a total of 16 control lines.  

Each instruction is broken down into a maximum of 8 sub instructions, the first of which is always reading the next instruction from the address currently in the 16-bit program counter.

The following modules exist:

* A register
  * 8-bit register which supports explicit load and store operations
  * Input from data bus
  * Output to data bus
* B register
  * 8-bit register which is used by specific insturctions to store data and perform calculations
  * Input from data bus
  * Output to data bus
* Accumulator
  * 8-bit arithmetic logic unit which performs ADD or SUBTRACT operations on A and B and stores the result in A. Also includes CARRY and ZERO flag registers which are exposed to the control logic to support branching instructions.
  * Input from A and B
  * Output to data bus
* Status Register
  * 8-bit register which only supports "transfer A to S" operations to enable status output.
  * This board also includes the reset circuit
  * Input from data bus
* X Register
  * 8-bit register which supports "transfer A to X" and "transfer X to A" operations
  * Input from data bus
  * Output to data bus and Address offset unit
* Clock
  * 555 timer with variable speed which supports clocks between around 10 Hz and 1kHz.
  * Also supports pausing the clock and manually single stepping
  * Output to clock line
* Program Counter - LOW
  * 8-bit counter which holds the low byte of the program counter
  * Supports set and reset operations
  * Counter overflow chains to Program Counter - HIGH
  * Input from data bus
  * Output to address bus low byte to read instructions
* Program Counter - HIGH
  * 8-bit counter which holds the high byte of the program counter
  * Supports set and reset operations
  * Input from data bus
  * Output to address bus high byte to read instructions
* Address Register
  * Physically combined with Page register
  * Holds low byte of address for read and write operations
  * Input from data bus
  * Outputs to Address Offset Unit (not directly to address bus)
* Page Register
  * Physically combined with Address register
  * Holds high byte of address for read and write operations
  * Asserting the Zero Page control line causes zero to be output to the address bus huigh byte without affecting the stored page value
  * Defaults to driving address bus high byte when insturctions not being read using Program counter
  * Input from data bus
  * Outputs to high byte of address
* Address Offset Unit
  * Three modes of operation controlled by control lines:
    * Pass through (default)
    * Add One - outputs the address value plus one, wrapping around (does not overflow to page)
    * Add X - outputs the address value plus the value in the X register, wrapping around (does not overflow to page)
  * Defaults to driving address bus low byte when insturctions not being read using Program counter
  * Input from Address and X registers
  * Outputs to low byte of address
* Address Decode
  * Takes top 3 bits and bottom bit of the 16-bit address along with the read and write control lines to generate device specific control lines
  * Outputs Read signal for ROM and RAM
  * Outputs Write signals for RAM and Output (low and high)
  * This unit handles mapping of 8K or ROM and 8K of RAM into the full possible 64K address space as detailed below
* RAM
  * SRAM supporting 13-bit addresses (8192 bytes)
  * Supports read and write operations controlled by the Address Decode unit
  * Inputs from data bus
  * Outputs to data bus
  * Address from address bus low 13 bits
* ROM
  * ROM supporting 13-bit addresses (8192 bytes)
  * Supports read perations controlled by the Address Decode unit
  * Outputs to data bus
  * Address from address bus low 13 bits
* Instruction Register
  * 8-bit register to hold the current instruction
  * Input from data bus
  * Output low 4-bits to data bus for "nibble" instructions
* Control Logic
  * Instruction register value, zero, carry and reset flags, and sub-instruction counter combine to generate a 14-bit address
  * 4 * 16K ROM chips output control lines based on this address as defined by the microcode configuration
  * Each clock tick increments the sub-insturction counter allowing complex multi-step instructions
  * Clock ticks can be saved for simple instructions by asseting the Cycle-Reset flag which causes the sub-instruction counter to reset on the next clock tick and trigger a new instruction fetch.
* Reset logic
  * When the reset line is asseted by the press of the reset button, this triggers the control logic to reset to sub-instruction zero with the reset line asserted.
  * A special reset instruction is then run which forces the program counter to address 0x2000 (bottom or ROM) before de-asserting the reset line
  * This address is hardcoded so all ROM code must begin at the stary of the ROM, after which is can perform a jump to any other location in ROM or RAM as needed.


# 8bit-cpu-microcode


program rom:  minipro -p W27C512@DIP28 -w output/16bitadd.bin -s

program microcode: minipro  -p AT28C64B -w microcode/CODEA.bin 




## 16 bit addressing enhancement

To implement 16 bit addressing, a rewrite of the microcode and addressing modes is necessary.

16 bit addresses will be stored in memory / rom in little endian form - low byte first - this simplifies 16 bit operations by reading/writing the low byte first, then reading/writing the high byte.  In theory this could allow for pipelining, but this is unlikely to be implemented..

16 bit addressing requires the ability to increment the memory address - 2 options to do this:
1. use the increment module, routing the MAR value to it's input, then update MAR via the Bus
 - the limitation of this option is that it won't support crossing page boundaries, instead looping to the start
2. implement the MAR and PAR using 4 x 74LS163 4-bit counters.  These support pre-setting, reset and counting.
 - this would support full 16-bit increments

Addressing modes

Implied - no operand (eg NOP, HLT, TAS etc)

Immediate Nibble - 

Immediate - 1 byte operand of value to be used, eg LDA $FF

Zero Page Absolute - 1 byte operand to address page zero in RAM, eg LDA #$80 -> $0080 in RAM
Absolute - 2 byte operand to address any page in ram, in little endian form, eg LDA #$8040 -> $8040 in RAM

Indirect Zero Page - 1 byte operand pointing to a location in page zero of ram. This and the next byte contain the address in memory to operate on in little endian form.
Indirect - 2 byte operand pointing to a location in any page of ram. This and the next byte contain the address in memory to operate on in little endian form.



Immediate Nibble                - number 5 loaded into A.                                  LDA $0x5
Immediate                       - number 69 (45 hex) loaded into A.                        LDA $0x45
Absolute Zero Page              - value in $0045 in ram loaded into A.                     LDA #$0x45
Absolure                        - value in $0645 in ram loaded into A.                     LDA #$0x0645
Indirect Zero Page              - value pointed to by $0045 and $0046 loaded into A.       LDA (#$0x45)
Absolute Zero Page X Indexed    - value in $0045+X loaded into A.                          LDA #$0x45,X
Absolute X Indexed              - value in $0645+X loaded into A.                          LDA #$0x0645,X
Indirect Zero Page X indexed    - value pointed to by $0045 and $0046+X loaded into A.     LDA (#$0x45),X
Indirect X indexed              - value pointed to by $0645 and $0646+X loaded into A.     LDA (#$0x0645),X




Load A - Immediate
1. load instruction from PC address to Instruction Reg
2. load byte from ROM using PC address and store in A reg, increment PC

Load A - Absolute Zero Page
1. load instruction from PC address to Instruction Reg
2. load low byte from ROM using PC address and store in MAR, increment PC
3. set Zero page flag and load byte from RAM and store in A reg.

Load A - Absolute
1. load instruction from PC address to Instruction Reg
2. load low byte from ROM using PC address and store in MAR, increment PC
3. load high byte fron ROM using PC address and store in PAR, increment PC
4. clear zero page flag and load byte from RAM and store in A reg

Load A - Indirect Zero Page
1. load instruction from PC address to Instruction Reg
2. load low byte from PC address into MAR, increment PC
3. set zero page flag and store byte from RAM in B Reg
4. increment MAR
5. clear zero page flag and store byte from RAM in PAR
6. transfer byte from B Reg to MAR
7. clear zero page flag and load byte from RAM and store in A reg


Load A - Indirect
1. load instruction from PC address to Instruction Reg, increment PC
2. load low byte from PC address into MAR, increment PC
3. load high byte from PC address into PAR, increment PC
4. clear zero page flag and store byte from RAM in B Reg
5. increment MAR
6. clear zero page flag and store byte from RAM in PAR
7. transfer byte from B Reg to MAR
8. clear zero page flag and load byte from RAM and store in A reg


## Reset flow

Indirect jump via 3FFE / 3FFF (little endian)

1. Set page to 3F
2. Set address to FE
3. Read value to B reg
4. Increment address and Read value to Page Reg
5. B reg value to Address Reg
6. Read value to PC Low
7. Increment address and REad value to PC high

Simpler version
1. output 20 to PC high
2. output 00 to PC low
3. cycle reset

## 16 bit memory map

0x0000 0b0000 0000 0000 0000 - Zero page RAM
... - 31 pages of RAM
0x1FFF 0b0001 1111 1111 1111 - Top of RAM

0x2000 0b0010 0000 0000 0000 - Bottom of ROM
... - 31 pages of ROM
0x3FFF 0b0011 1111 1111 1111 - TOP of ROM

0x4000 0b010x xxxx xxxx xxx0 - output low byte
0x4001 0b010x xxxx xxxx xxx1 - output high byte

0x6000 0b0110 0000 0000 0000 - printer
 -spare ~48k
0xFFFF


0x0000 - 0x1FFF - RAM
0x2000 - 0x3FFF - ROM
0x4000 - output low
0x4001 - output higg
0x6000 - printer

inputs:
16bit address
Read - active high
Write - active high

outputs:
ram read - active high
ram write - active high
rom read - active low
output low write - active low
output high write - active low
printer write - active high
