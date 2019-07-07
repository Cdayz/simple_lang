from interpreter.src.parser.errors import ParsingError


def test_parsing_error():
    exc = Exception("test")
    parse_error = ParsingError(1, "MOV A, c", exc)

    assert parse_error.exception is exc
    assert parse_error.line_code == "MOV A, c"
    assert parse_error.line_index == 1
