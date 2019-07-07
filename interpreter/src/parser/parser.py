"""Module with Parser for code."""

import typing
import itertools

from interpreter.src.lexer.keywords import (
    LANGUAGE_OPTYPES,
    LANGUAGE_REGISTERS,
    Keyword,
    Register
)
from interpreter.src.parser.errors import (
    BadOperationIdentifier,
    BadOperationArgument,
    BadInPlaceValue,
    ParsingError
)
from interpreter.src.parser.operation import (
    Operation,
    OperationType,
    OperationArgument,
    OperationArgumentType,
)

LABELS_OR_JUMPS = (
    "LABEL",
    "JMP",
    "JMP_NE",
    "JMP_EQ",
    "JMP_GT",
    "JMP_LT"
)

NOP_ARG = OperationArgument(
    arg_word=0,
    arg_type=OperationArgumentType.Nop
)


class Parser:
    """Code parser class.

    Provides parse method wich parses code string into list of operations
    which need to perform.
    """

    def __init__(self):
        """Initialize labels table used for normal jumps."""
        self.labels_table: typing.Dict[str, int] = {}

    def parse(self, code: str) -> typing.List[Operation]:
        """Parse code into list of line by line operations to execute.

        Split code line by line, parse line into Operation object and add
        to all operations list.

        :param str code: Source code for parsing into Operations

        :raise ParserError: If any parser errors occured

        :return: List of Operations parsed from code
        :rtype: List[Operation]
        """
        operations = []

        for line_index, line in enumerate(code.split('\n')):

            line_unindented = itertools.dropwhile(str.isspace, line)
            line_without_comments = ''.join(
                itertools.takewhile(
                    lambda symbol: symbol != ';',
                    line_unindented
                )
            )

            if not line_without_comments:
                continue

            try:
                operation = self.parse_line(line_without_comments)
            except Exception as e:
                raise ParsingError(line_index, line, e)

            operations.append(operation)

        return operations

    def parse_line(self, line: str) -> Operation:
        """Parse line of code with one operation into Operation object.

        Split line by spaces, we assume that operation everything is first.

        Check the operation and if it if available operations parse arguments.

        :param str line: Line of code

        :raise BadOperationIdentifier: if operation is not in allowed
        :raise BadOperationArgument: If any argument not in argument types
        :raise BadInPlaceValue: If argument is not an integer

        :return: Operation object builded from code line
        :rtype: :class:`~.Operation`
        """
        words = line.replace(',', '').split(' ')

        operation, *args = words

        if Keyword(operation) not in LANGUAGE_OPTYPES:
            raise BadOperationIdentifier(operation)

        op_type = LANGUAGE_OPTYPES[Keyword(operation)]

        if op_type is OperationType.Nop:
            return Operation(
                op_type=op_type,
                op_word=operation,
                op_args=[NOP_ARG, NOP_ARG]
            )

        elif op_type is OperationType.Unary:
            argument = args[0]
            is_label_or_jump = operation in LABELS_OR_JUMPS
            arg1 = self.parse_argument(argument, is_label_or_jump)

            if operation == 'NOT':
                op_args = [arg1, arg1]
            else:
                op_args = [arg1, NOP_ARG]

            return Operation(
                op_type=op_type,
                op_word=operation,
                op_args=op_args
            )

        # Binary operation
        arguments = [args[0], args[1]]

        arg12 = [
            self.parse_argument(arg)
            for arg in arguments
        ]

        return Operation(
            op_type=op_type,
            op_word=operation,
            op_args=arg12
        )

    def parse_argument(self, argument: str, is_label_or_jump: bool = False):
        """Parse argument for operation.

        Check the argument type and build OperationArgument object.

        :param str argument: Argument string from code

        :raise BadOperationArgument: If argument not in allowed argument types
        :raise BadInPlaceValue: If argument is not an integer

        :return: OperationArgument object builded from argument string
        :rtype: :class:`~.OperationArgument`
        """
        is_reference = '@' in argument

        if is_reference:
            argument = argument[1:]

        if Register(argument) in LANGUAGE_REGISTERS:
            arg_type = (
                OperationArgumentType.RegisterPointer
                if is_reference
                else OperationArgumentType.Register
            )
            arg_word = LANGUAGE_REGISTERS.index(Register(argument))

        elif is_inplace(argument):
            arg_type = OperationArgumentType.InPlaceValue

            try:
                arg_word = int(argument)
            except ValueError:
                raise BadInPlaceValue(argument)

        elif is_label_or_jump:
            arg_type = OperationArgumentType.Label

            if argument in self.labels_table:
                label_index = self.labels_table[argument]
            else:
                label_index = max(self.labels_table.values() or [0, ]) + 1
                self.labels_table[argument] = label_index

            arg_word = label_index

        else:
            raise BadOperationArgument(argument)

        return OperationArgument(
            arg_type=arg_type,
            arg_word=arg_word
        )


def is_inplace(argument: str) -> bool:
    """Check that argument is in-place value.

    :param str argument: argument string

    :return: True if argument is a digit of decimal else False
    :rtype: bool
    """
    checks = [
        str.isdigit,
        str.isdecimal,
    ]

    return any(check(argument) for check in checks)
