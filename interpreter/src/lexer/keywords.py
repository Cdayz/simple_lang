"""Module with basic language keywords."""

from typing import NewType, List, Dict

from interpreter.src.parser.operation import OperationType


Keyword = NewType('Keyword', str)


LANGUAGE_OPTYPES: Dict[Keyword, OperationType] = {
    # MATH
    Keyword("ADD"): OperationType.Binary,
    Keyword("SUB"): OperationType.Binary,
    Keyword("DIV"): OperationType.Binary,
    Keyword("MUL"): OperationType.Binary,
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
    # Nop
    Keyword("NOP"): OperationType.Nop
}


LANGUAGE_KEYWORDS: List[Keyword] = list(LANGUAGE_OPTYPES.keys())
