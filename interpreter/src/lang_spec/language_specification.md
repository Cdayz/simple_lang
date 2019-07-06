# Simple Lang Specification

SimpleLang is a subset of assembler languages implemented in virtual machine

## Language Specification

### Registers

In SimpleLang we have only 4 General-Purpose registers `r1, r2, r3, r4`.
One accumulator register `A` and 4 conditional registers `EQ`, `GT`, `LT`, `NE`

### Operations

In SimpleLang only that operations is allowed and implemented:

1) `MOV (r|a), (r|a)` - store in first operand value from second operand
2) `MOV (r|a), @r` - store in first operand value by address in second operand
3) `ADD A, r` - add value from second operand to accumulator
4) `DIV A, r` - divide value from accumulator by value in second operand
(Note: Only integer division is allowe and implemented)
5) `SUB A, r` - substract accumulator by value of second operand
6) `MUL A, r` - multiply accumulator by value of second operand
7) `LABEL lbl` - make that lbl points to that line of code
8) `JMP lbl` - jump to line that lbl points
9) `CMP A, r` - compare value of accumulator with second operand and set specific registers
10) `JMP_EQ, JMP_LT, JMP_GT, JMP_NE` - conditional jumps
11) `AND, OR, XOR, NOT` - bit operations
12) `PRINT (@|)(A|r)` - print value of register or memory by reg.pointer to stdout
13) `INPUT (@|)(A|r)` - read ONE NUMBER from stdin and write to register or to memory point


### Bytecode structure

Operation bytecode:

| 2 byte  | 1 byte | 4 byte | 1 byte | 4 byte |
-----------------------------------------------
| op_code | arg_ty | op_arg | arg_ty | op_arg |

one operation will be encoded to (2+1+4+1+4) = 12 byte

if operation doesn't have any of arguments pad_sym will be used
and arg_type will be set as pad_symbol!

1 byte before every argument is placeholder for argument type
(e.g. reference, register or in-place value)

4 byte arguments size needed for in-place values
In-place values is a 32-bit integers only!


### Bytecode invalidation

Every bytecode file have one metadata section before real code

#### Metadata section structure

|    2 byte    | 4 byte |
|magical number|   crc  |

CRC sum is used for code invalidation.
