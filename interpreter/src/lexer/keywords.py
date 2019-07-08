"""Module with basic language keywords."""

from typing import NewType, List, Dict

from interpreter.src.parser.operation import OperationType


Keyword = NewType('Keyword', str)
Register = NewType('Register', str)


LANGUAGE_OPTYPES: Dict[Keyword, OperationType] = {
    # MATH
    Keyword("ADD"): OperationType.Binary,
    Keyword("SUB"): OperationType.Binary,
    Keyword("DIV"): OperationType.Binary,
    Keyword("MUL"): OperationType.Binary,
    # Binary math
    Keyword("AND"): OperationType.Binary,
    Keyword("OR"): OperationType.Binary,
    Keyword("XOR"): OperationType.Binary,
    Keyword("NOT"): OperationType.Unary,
    # Pointers, Equations
    Keyword("MOV"): OperationType.Binary,
    Keyword("CMP"): OperationType.Binary,
    # JUMPS
    Keyword("JMP"): OperationType.Unary,
    Keyword("JMP_EQ"): OperationType.Unary,
    Keyword("JMP_GT"): OperationType.Unary,
    Keyword("JMP_LT"): OperationType.Unary,
    Keyword("JMP_NE"): OperationType.Unary,
    # Labeling
    Keyword("LABEL"): OperationType.Unary,
    # IO
    Keyword("PRINT"): OperationType.Unary,
    Keyword("INPUT"): OperationType.Unary,
    # Nop
    Keyword("NOP"): OperationType.Nop,
    # End of program
    Keyword("END"): OperationType.Nop,
    # Control flow, through calls and returns used subroutins
    Keyword("CALL"): OperationType.Unary,
    Keyword("RET"): OperationType.Nop,
}


LANGUAGE_KEYWORDS: List[Keyword] = list(LANGUAGE_OPTYPES.keys())


LANGUAGE_REGISTERS: List[Register] = [
    Register("r1"),
    Register("r2"),
    Register("r3"),
    Register("r4"),
    Register("A"),
    Register("EQ"),
    Register("LT"),
    Register("GT"),
    Register("NE"),
]
