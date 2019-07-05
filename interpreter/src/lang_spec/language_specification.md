# Simple Lang Specification

SimpleLang is a subset of assembler languages implemented in virtual machine

## Language Specification

### Registers

In SimpleLang we have only 4 General-Purpose registers `r1, r2, r3, r4`.
One accumulator register `A` and 3 conditional registers `EQ`, `GT`, `LT`

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
10) `JMP_EQ, JMP_LT, JMP_GT` - conditional jumps
