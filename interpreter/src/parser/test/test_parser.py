import pytest

from interpreter.src.parser.parser import (
    Parser,
    is_inplace,
    Operation,
    OperationArgument,
    OperationArgumentType,
    OperationType,
    NOP_ARG,
    BadOperationArgument,
    BadOperationIdentifier,
    ParsingError
)


def test_is_inplace():
    in_place = "100500"

    assert is_inplace(in_place)

    no_in_place = "12+4"

    assert not is_inplace(no_in_place)


def test_parser_ok():
    code = """
    LABEL abc
        MOV A, 1
        CMP A,2
        MOV @r1, A
        JMP abc
    """

    operations = Parser().parse(code)

    assert operations

    expected_ops = [
        Operation(
            op_word="LABEL",
            op_type=OperationType.Unary,
            op_args=[
                OperationArgument(arg_type=OperationArgumentType.Label,
                                  arg_word=1),
                NOP_ARG
            ]
        ),
        Operation(
            op_word="MOV",
            op_type=OperationType.Binary,
            op_args=[
                OperationArgument(arg_type=OperationArgumentType.Register,
                                  arg_word=4),
                OperationArgument(arg_type=OperationArgumentType.InPlaceValue,
                                  arg_word=1)
            ]
        ),
        Operation(
            op_word="CMP",
            op_type=OperationType.Binary,
            op_args=[
                OperationArgument(arg_type=OperationArgumentType.Register,
                                  arg_word=4),
                OperationArgument(arg_type=OperationArgumentType.InPlaceValue,
                                  arg_word=2)
            ]
        ),
        Operation(
            op_word="MOV",
            op_type=OperationType.Binary,
            op_args=[
                OperationArgument(
                    arg_type=OperationArgumentType.RegisterPointer,
                    arg_word=0),
                OperationArgument(arg_type=OperationArgumentType.Register,
                                  arg_word=4)
            ]
        ),
        Operation(
            op_word="JMP",
            op_type=OperationType.Unary,
            op_args=[
                OperationArgument(arg_type=OperationArgumentType.Label,
                                  arg_word=1),
                NOP_ARG
            ]
        ),
    ]

    assert operations == expected_ops


def test_parser_error():
    code = """
    LABEL L
    MOV error, error
    """

    with pytest.raises(ParsingError):
        Parser().parse(code)


def test_parser_hack_not():
    code = "NOT r1"

    parsed_ops = Parser().parse(code)

    expected = [
        Operation(
            op_word="NOT",
            op_type=OperationType.Unary,
            op_args=[
                OperationArgument(arg_type=OperationArgumentType.Register,
                                  arg_word=0),
                OperationArgument(arg_type=OperationArgumentType.Register,
                                  arg_word=0),
            ]
        )
    ]

    assert parsed_ops == expected


def test_parser_parse_arg():
    parser = Parser()

    # No label in LUT

    argument = "abc"  # label

    arg = parser.parse_argument(argument, is_label_or_jump=True)

    expected_arg = OperationArgument(
        arg_type=OperationArgumentType.Label,
        arg_word=1
    )

    assert arg == expected_arg

    # Label in LUT
    parser.labels_table = {"abc": 4}

    arg = parser.parse_argument(argument, is_label_or_jump=True)

    expected_arg = OperationArgument(
        arg_type=OperationArgumentType.Label,
        arg_word=4
    )

    assert arg == expected_arg

    parser.labels_table = {}

    # Register argument

    argument = "r1"

    arg = parser.parse_argument(argument)

    expected_arg = OperationArgument(
        arg_type=OperationArgumentType.Register,
        arg_word=0
    )

    assert arg == expected_arg

    # Register pointer

    argument = "@r1"

    arg = parser.parse_argument(argument)

    expected_arg = OperationArgument(
        arg_type=OperationArgumentType.RegisterPointer,
        arg_word=0
    )

    assert arg == expected_arg

    # In-place

    argument = "100"

    arg = parser.parse_argument(argument)

    expected_arg = OperationArgument(
        arg_type=OperationArgumentType.InPlaceValue,
        arg_word=100
    )

    assert arg == expected_arg

    # Bad argument

    argument = "a"

    with pytest.raises(BadOperationArgument):
        arg = parser.parse_argument(argument)


def test_parser_parse_line():
    # Bad keyword
    line = "MVO r1, 14"

    with pytest.raises(BadOperationIdentifier):
        Parser().parse_line(line)

    # Nop operation

    line = "NOP"

    parsed_op = Parser().parse_line(line)

    expected_op = Operation(
        op_type=OperationType.Nop,
        op_args=[NOP_ARG, NOP_ARG],
        op_word="NOP"
    )

    assert parsed_op == expected_op

    # Unary op

    line = "INPUT r1"

    parsed_op = Parser().parse_line(line)

    expected_op = Operation(
        op_type=OperationType.Unary,
        op_args=[
            OperationArgument(
                arg_type=OperationArgumentType.Register,
                arg_word=0),
            NOP_ARG],
        op_word="INPUT"
    )

    assert parsed_op == expected_op

    # Binary op

    line = "CMP r1, 10"

    parsed_op = Parser().parse_line(line)

    expected_op = Operation(
        op_type=OperationType.Binary,
        op_args=[
            OperationArgument(
                arg_type=OperationArgumentType.Register,
                arg_word=0),
            OperationArgument(
                arg_type=OperationArgumentType.InPlaceValue,
                arg_word=10)
            ],
        op_word="CMP"
    )

    assert parsed_op == expected_op
