"""Module with predefined bytecodes."""

from typing import Dict

from interpreter.src.lexer.keywords import Keyword, LANGUAGE_OPTYPES


BYTECODES: Dict[Keyword, int] = {
    # Pack every operation code to 2 bytes integer (short)
    keyword: code
    for code, keyword in enumerate(LANGUAGE_OPTYPES.keys())
}
