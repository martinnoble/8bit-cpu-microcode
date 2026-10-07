# 8-bit Breadboard CPU

A microcode generator and assembler for a custom "Ben Eater" style breadboard computer.

The CPU has an 8-bit data bus and 16-bit address bus. Control logic is split across 4 ROMs enabling a total of 16 control lines. Each instruction is broken down into a maximum of 8 micro-steps, the first of which always fetches the next instruction from the address held in the 16-bit program counter.

---

## Table of Contents

1. [Hardware Modules](#hardware-modules)
2. [Memory Map](#memory-map)
3. [Getting Started](#getting-started)
4. [Running the Assembler](#running-the-assembler)
5. [Assembly Language Reference](#assembly-language-reference)
6. [Instruction Set](#instruction-set)
7. [Generating and Programming Microcode](#generating-and-programming-microcode)
8. [Reset Flow](#reset-flow)
9. [16-bit Addressing Design Notes](#16-bit-addressing-design-notes)

---

## Hardware Modules

### A Register
- 8-bit register supporting explicit load and store operations
- Input from data bus; output to data bus

### B Register
- 8-bit register used by specific instructions to store data and perform calculations
- Input from data bus; output to data bus

### Accumulator (ALU)
- 8-bit arithmetic logic unit performing ADD or SUBTRACT on A and B, storing the result in A
- Includes CARRY and ZERO flag registers exposed to control logic to support branching
- Input from A and B registers; output to data bus

### Status Register
- 8-bit register supporting "transfer A to S" operations to enable status output
- Also hosts the reset circuit
- Input from data bus

### X Register
- 8-bit register supporting "transfer A to X" and "transfer X to A" operations
- Input from data bus; output to data bus and Address Offset Unit

### Clock
- 555 timer with variable speed supporting approximately 10 Hz to 1 kHz
- Supports pausing and manual single-stepping
- Output to clock line

### Program Counter — LOW
- 8-bit counter holding the low byte of the program counter
- Supports set and reset operations; overflow chains to Program Counter HIGH
- Input from data bus; output to address bus low byte

### Program Counter — HIGH
- 8-bit counter holding the high byte of the program counter
- Supports set and reset operations
- Input from data bus; output to address bus high byte

### Address Register
- Physically combined with Page Register
- Holds low byte of address for read/write operations
- Input from data bus; outputs to Address Offset Unit (not directly to address bus)

### Page Register
- Physically combined with Address Register
- Holds high byte of address for read/write operations
- Asserting the Zero Page control line causes zero to be output to the address bus high byte without affecting the stored page value
- Defaults to driving address bus high byte when instructions are not being read via the program counter
- Input from data bus; output to high byte of address bus

### Address Offset Unit
Three modes controlled by control lines:
- **Pass-through** (default)
- **Add One** — outputs the address value plus one, wrapping within the page (does not overflow to the next page)
- **Add X** — outputs the address value plus the value in the X register, wrapping within the page

Input from Address and X registers; output to low byte of address bus

### Address Decode
- Takes the top 3 bits and bottom bit of the 16-bit address, plus the read and write control lines, to generate device-specific control lines
- Outputs: RAM read (active high), RAM write (active high), ROM read (active low), output-low write (active low), output-high write (active low), printer write (active high)
- Handles mapping of 8 KB of ROM and 8 KB of RAM into the 64 KB address space (see [Memory Map](#memory-map))

### RAM
- SRAM with 13-bit addresses (8192 bytes)
- Supports read and write operations controlled by Address Decode
- Address from low 13 bits of address bus; data bus in and out

### ROM
- ROM with 13-bit addresses (8192 bytes)
- Supports read operations controlled by Address Decode
- Address from low 13 bits of address bus; output to data bus

### Instruction Register
- 8-bit register holding the current instruction
- Input from data bus; low 4 bits output to data bus for "nibble" instructions

### Control Logic
- Instruction register value, zero flag, carry flag, reset flag, and sub-instruction counter combine to form a 14-bit address (see [Microcode ROM Address Structure](#microcode-rom-address-structure))
- 4 × 16 KB ROM chips output control lines based on this address as defined by the microcode configuration
- Each clock tick increments the sub-instruction counter, allowing complex multi-step instructions
- Clock ticks can be saved for simple instructions by asserting the Cycle-Reset flag, which resets the sub-instruction counter on the next tick and triggers a new instruction fetch

### Reset Logic
- When the reset line is asserted (reset button pressed), the control logic resets to sub-instruction zero with the reset flag set
- A special reset instruction forces the program counter to address `0x2000` (start of ROM) before de-asserting the reset line
- This address is hardcoded; all ROM programs must begin at the start of ROM, after which a jump to any location in ROM or RAM may be performed

---

## Memory Map

| Address Range | Size | Device |
|---|---|---|
| `0x0000` – `0x1FFF` | 8 KB | RAM (zero page: `0x0000` – `0x00FF`) |
| `0x2000` – `0x3FFF` | 8 KB | ROM (program start: `0x2000`) |
| `0x4000` | 1 byte | Output — low byte |
| `0x4001` | 1 byte | Output — high byte |
| `0x6000` | 1 byte | Printer |
| `0x6001` – `0xFFFF` | ~40 KB | Spare / unmapped |

**Address decode inputs:** 16-bit address, Read (active high), Write (active high)

**Address decode outputs:**

| Signal | Active |
|---|---|
| RAM read | High |
| RAM write | High |
| ROM read | Low |
| Output low write | Low |
| Output high write | Low |
| Printer write | High |

---

## Getting Started

### Prerequisites

- Python 3.9+
- [`minipro`](https://gitlab.com/DavidGriffith/minipro) — command-line EPROM programmer tool

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### Repository layout

```
assembler.py      — assembles .asm source files into ROM binary images
microcode.py      — generates the 4 microcode ROM binary images
source/           — example and test assembly programs
microcode/        — output directory for microcode ROM binaries (CODEA–D.bin)
output/           — output directory for assembled ROM binaries
```

---

## Running the Assembler

```bash
# Assemble a source file (output written to output/<filename>.bin)
python assembler.py source/myprogram.asm

# Assemble with an explicit output path
python assembler.py source/myprogram.asm output/myprogram.bin
```

The output is always an 8192-byte image pre-filled with `HLT` (`0xFF`) bytes. The first 3 bytes are always `NOP`, followed by the assembled code. The image maps to ROM starting at `0x2000`.

After assembly the script will ask interactively whether to flash the ROM via `minipro`:

```
Program ROM? y
```

To flash manually:

```bash
minipro -p AT28C64B -w output/myprogram.bin -u -P
```

---

## Assembly Language Reference

### Comments

`;` begins a comment; everything to the right is ignored.

```asm
LDA $5   ; load the value 5 into A
```

### Labels

A line ending in `:` defines a label at the current address. Labels are referenced in instructions with a `:` prefix.

```asm
loop:
    ADD $1
    JMP :loop
```

### Directives

| Directive | Syntax | Description |
|---|---|---|
| `.const` | `.const NAME value` | Define a named constant (resolved as an address/value) |
| `.org` | `.org 0xADDR` | Set the output location counter to an absolute ROM address |
| `.text` | `.text "string"` | Insert raw ASCII bytes |
| `.byte` | `.byte $value` | Insert a single raw byte |
| `.word` | `.word $value` | Insert a 16-bit value in little-endian byte order |

**Examples:**

```asm
.const COUNTER 0x0010    ; RAM address 0x0010 aliased as COUNTER
.org 0x2100              ; place the following code at ROM address 0x2100
.text "Hello"            ; insert 5 ASCII bytes
.byte $0x0A              ; insert a newline byte
.word $0x1234            ; insert 0x34, 0x12 (little-endian)
```

### Addressing Modes

| Mode | Syntax | Notes |
|---|---|---|
| Implied | *(no operand)* | Instruction carries all information (e.g. `HLT`, `NOP`) |
| Immediate Nibble | `$value` (0 – 15) | Value encoded in low 4 bits of opcode |
| Immediate | `$value` (16 – 255) or `$0xNN` | Following byte is the value |
| Character Literal | `'c'` | Forces immediate mode; escape sequences `\n` and `\r` supported |
| Absolute Zero Page | `#$addr` (0 – 255) | One-byte address into page zero of RAM |
| Absolute | `#$addr` (> 255) | Two-byte little-endian address into any RAM/ROM location |
| Absolute X-indexed | `#$addr,X` | Absolute address with low byte offset by X register (wraps within page) |
| Indirect | `(#$addr)` or `(:label)` | Address field points to a 16-bit little-endian pointer in RAM |
| Label Reference | `:labelname` | Resolved to the 16-bit address of the label (absolute mode) |

**Examples:**

```asm
LDA $5           ; immediate nibble — load 5 into A
LDA $0xAB        ; immediate — load 0xAB into A
LDA #$0x45       ; absolute zero page — load value at RAM[0x0045]
LDA #$0x0645     ; absolute — load value at RAM[0x0645]
LDA #$0x0645,X   ; absolute X-indexed — load value at RAM[0x0645 + X]
LDA (#$0x45)     ; indirect zero page — load value pointed to by RAM[0x0045..0x0046]
LDA (#$0x0645)   ; indirect — load value pointed to by RAM[0x0645..0x0646]
LDA 'A'          ; character literal — load ASCII 65 into A
JMP :start       ; jump to label 'start'
```

The assembler automatically selects zero-page vs. full 16-bit absolute or indirect addressing based on whether the address fits in one byte and whether the instruction supports the zero-page variant.

---

## Instruction Set

### Opcode Table

| Mnemonic | Description | IN (nibble) | IM | ABS ZP | ABS | ABS,X | ABS IP | IND ZP | IND |
|---|---|---|---|---|---|---|---|---|---|
| `NOP` | No operation | `0x00` | — | — | — | — | — | — | — |
| `HLT` | Halt execution | `0xFF` | — | — | — | — | — | — | — |
| `JMP` | Jump | — | — | — | `0xC1` | — | — | — | — |
| `BCS` | Branch if carry set | — | — | — | `0xC2` | — | — | — | — |
| `BCC` | Branch if carry clear | — | — | — | `0xC3` | — | — | — | — |
| `BEQ` | Branch if equal (zero set) | — | — | — | `0xC4` | — | — | — | — |
| `BNE` | Branch if not equal (zero clear) | — | — | — | `0xC5` | — | — | — | — |
| `LDA` | Load A | `0x6n` | `0xB6` | `0x06` | `0xC6` | `0xD6` | — | `0xE6` | `0xF6` |
| `STA` | Store A | `0x7n` | — | `0x07` | `0xC7` | `0xD7` | — | `0xE7` | `0xF7` |
| `ADD` | Add (clears carry first) | `0x8n` | `0xB8` | — | `0xC8` | — | `0xD8` | — | `0xE8` |
| `SUB` | Subtract (sets carry first) | `0x9n` | `0xB9` | — | `0xC9` | — | `0xD9` | — | `0xE9` |
| `ADC` | Add with carry | `0x1n` | `0xBC` | — | `0xCC` | — | `0xDC` | `0xEC` | `0xFC` |
| `SBC` | Subtract with carry | `0x2n` | `0xBD` | — | `0xCD` | — | `0xDD` | `0xED` | `0xFD` |
| `CMP` | Compare (sets flags, does not store) | `0xAn` | `0xBA` | `0x0A` | `0xCA` | — | — | — | — |
| `CPY` | Copy ROM byte to RAM | — | — | — | `0xCB` | — | — | — | — |
| `TAS` | Transfer A to Status register | `0xF0` | — | — | — | — | — | — | — |
| `TAX` | Transfer A to X register | `0xF4` | — | — | — | — | — | — | — |
| `TXA` | Transfer X to A register | `0xF5` | — | — | — | — | — | — | — |
| `INX` | Increment X register | `0xF1` | — | — | — | — | — | — | — |
| `CLF` | Clear flags (carry and zero) | `0xF2` | — | — | — | — | — | — | — |
| `SEF` | Set flags (carry and zero) | `0xF3` | — | — | — | — | — | — | — |

**`n`** in nibble opcodes denotes the 4-bit immediate value encoded in the low nibble (e.g. `LDA $5` assembles to `0x65`).

**ABS IP (Absolute In Place):** Combines a load, arithmetic, and store in a single instruction. The operand is the target RAM address (2 bytes); the third byte in the instruction stream is the arithmetic operand. The result is written back to the original address.

**ADD vs ADC / SUB vs SBC:** `ADD`/`SUB` reset/set the carry flag before operating (for single-byte arithmetic). `ADC`/`SBC` respect the existing carry flag (for multi-byte chained arithmetic).

### Flag Behaviour

| Flag | Set when | Cleared when |
|---|---|---|
| Carry | ADD/SUB result overflows or underflows; `SEF` | No overflow/underflow; `CLF`; `ADD`/`SUB` before operation |
| Zero | Result equals zero | Result is non-zero |

Branches read the carry and zero flags at the time the instruction is decoded. The microcode ROM contains separate entries for each flag combination, so branching adds no extra clock cycles.

---

## Generating and Programming Microcode

### Generating the binaries

```bash
python microcode.py
```

This writes four files to `microcode/`:

| File | ROM | Controls |
|---|---|---|
| `CODEA.bin` | A | HALT, ADDR_IN, WRITE, READ, I_REG_IN, I_REG_OUT, A_REG_IN, A_REG_OUT |
| `CODEB.bin` | B | SUM_OUT, SUB, ADINC, COUNT_EN, JMP_LOW, JMP_HIGH, B_REG_IN, B_REG_OUT |
| `CODEC.bin` | C | F_REG_IN, PC_ADR, S_REG_IN, F_CLEAR, F_SET, ZERO_PAGE, PAGE_IN, CYCLE_RESET |
| `CODED.bin` | D | X_REG_IN, X_REG_OUT, ADINC_X, UD04, UD05, UD06, UD07, RESET |

After generation the script interactively offers to flash each ROM:

```
Program CODE A? y
Program CODE B? y
Program CODE C? y
Program CODE D? y
```

To flash manually:

```bash
minipro -p W27C512@DIP28 -w microcode/CODEA.bin
minipro -p W27C512@DIP28 -w microcode/CODEB.bin
minipro -p W27C512@DIP28 -w microcode/CODEC.bin
minipro -p W27C512@DIP28 -w microcode/CODED.bin
```

### Microcode ROM Address Structure

Each of the four 65536-byte microcode ROMs is indexed by a 16-bit address built from four fields:

```
Bit 15–14 : unused (always 0 — only lower 14 bits are meaningful)
Bit 13    : reset flag (1 = reset in progress)
Bits 12–5 : instruction opcode (8 bits)
Bits 4–3  : CPU flags  (bit 3 = carry, bit 4 = zero)
Bits 2–0  : sub-instruction step (0–7)
```

When the reset flag is set, all opcodes decode to the `RST` microprogram regardless of the instruction register value. This ensures a clean reset regardless of what instruction was executing at the time the reset button was pressed.

### Active-Low Signal Polarity

Each ROM has a direction mask (`DIRA`–`DIRD`) that is XOR'd with the computed control word before being written. This inverts the bits for control lines that are active-low, so the Python microcode definitions always use active-high logic regardless of the physical polarity of each line.

---

## Reset Flow

When the reset button is pressed:

1. The reset flag is asserted and the sub-instruction counter is forced to zero
2. The `RST` microprogram runs:
   - Loads `0x20` into Program Counter HIGH
   - Loads `0x00` into Program Counter LOW
3. The reset flag is de-asserted and normal execution resumes from `0x2000` (start of ROM)

The start address `0x2000` is hardcoded in the `RST` microprogram. All programs must begin at the start of the ROM image; a `JMP` instruction can then redirect execution anywhere in the address space.

---

## 16-bit Addressing Design Notes

> These are design/implementation notes from the development of 16-bit addressing support.

### Addressing Modes Summary

| Mode | Operand bytes | Example |
|---|---|---|
| Implied | 0 | `NOP` |
| Immediate Nibble | 0 (value in opcode) | `LDA $5` |
| Immediate | 1 | `LDA $0x45` |
| Absolute Zero Page | 1 | `LDA #$0x45` → RAM `0x0045` |
| Absolute | 2 (little-endian) | `LDA #$0x0645` → RAM `0x0645` |
| Absolute X-indexed | 2 (little-endian) | `LDA #$0x0645,X` → RAM `0x0645 + X` |
| Indirect Zero Page | 1 | `LDA (#$0x45)` → pointer at RAM `0x0045`–`0x0046` |
| Indirect | 2 (little-endian) | `LDA (#$0x0645)` → pointer at RAM `0x0645`–`0x0646` |

16-bit addresses are stored in memory in **little-endian** form (low byte first). This simplifies multi-byte operations by allowing the low byte to be read or written first, then the high byte.

### Instruction Micro-step Sequences

**Load A — Immediate**
1. Fetch instruction from PC → Instruction Register; increment PC
2. Read byte from PC → A Register; increment PC; cycle reset

**Load A — Absolute Zero Page**
1. Fetch instruction from PC → Instruction Register; increment PC
2. Read byte from PC → Address Register (MAR); increment PC
3. Assert Zero Page; read byte from RAM → A Register; cycle reset

**Load A — Absolute (16-bit)**
1. Fetch instruction from PC → Instruction Register; increment PC
2. Read low byte from PC → Address Register (MAR); increment PC
3. Read high byte from PC → Page Register (PAR); increment PC
4. Read byte from RAM → A Register; cycle reset

**Load A — Indirect Zero Page**
1. Fetch instruction from PC → Instruction Register; increment PC
2. Read byte from PC → MAR; increment PC
3. Assert Zero Page; read byte from RAM → B Register
4. Increment MAR; assert Zero Page; read byte from RAM → PAR
5. B Register → MAR
6. Read byte from RAM → A Register; cycle reset

**Load A — Indirect (16-bit)**
1. Fetch instruction from PC → Instruction Register; increment PC
2. Read low byte from PC → MAR; increment PC
3. Read high byte from PC → PAR; increment PC
4. Read byte from RAM → B Register
5. Increment MAR; read byte from RAM → PAR
6. B Register → MAR
7. Read byte from RAM → A Register; cycle reset
