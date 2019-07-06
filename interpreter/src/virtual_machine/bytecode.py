import struct
from typing import Dict

from interpreter.src.lexer.keywords import Keyword, LANGUAGE_OPTYPES


BYTECODES: Dict[Keyword, bytes] = {
    # Pack every operation code to 2 bytes integer (short)
    keyword: struct.pack('h', code)
    for code, keyword in enumerate(LANGUAGE_OPTYPES.keys())
}
