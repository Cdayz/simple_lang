"""Module with basic language keywords."""

from typing import NewType, List

Keyword = NewType('Keyword', str)


LANGUAGE_KEYWORDS: List[Keyword] = [
    # MATH
    "ADD",
    "SUB",
    "DIV",
    "MUL",
    # Pointers, Equations
    "MOV",
    "CMP",
    # JUMPS
    "JMP",
    "JMP_EQ",
    "JMP_GT",
    "JMP_LT",
    "JMP_NE",
    # Labeling
    "LABEL"
]
