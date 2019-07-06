"""Module with type-classes for Parser."""

import enum
import typing
import dataclasses


class OperationType(enum.Enum):
    """Enum of different types of operations."""

    Nop = 0
    Unary = 1
    Binary = 2


class OperationArgumentType(enum.Enum):
    """Enum of different types of operation arguments."""

    Nop = 0
    Register = 1
    RegisterPointer = 2
    InPlaceValue = 3


@dataclasses.dataclass
class OperationArgument:
    """Class which represents operation argument.

    :param arg_type: type of Argument
    :type arg_type: :class:`~.OperationArgumentType`

    :param str arg_word: String representation of argument
    """

    arg_type: OperationArgumentType
    arg_word: int


@dataclasses.dataclass
class Operation:
    """Class which represents operation.

    :param op_type: type of Operation
    :type op_type: :class:`~.OperationType`

    :param str op_word: String of operation word

    :param op_args: Arguments of operation
    :type op_args: List[OperationArgument]
    """

    op_type: OperationType
    op_word: str
    op_args: typing.List[OperationArgument]
