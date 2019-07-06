"""Module with bytecode compiler."""

import io
import typing
import struct
import itertools

from interpreter.src.parser.operation import Operation

from interpreter.src.virtual_machine.bytecode import BYTECODES, Keyword
from interpreter.src.virtual_machine.errors import BadOperationSize

OP_SIZE: int = 12
MAG_NUM: int = 0x1235


class BytecodeCompiler:
    """Bytecode compiler.

    Compiles operations to bytecode.
    """

    def __init__(self, file_crc: int):
        """Initialize compiler with current file crc."""
        self.file_crc = file_crc

    def compile(self, code: typing.List[Operation]) -> io.BytesIO:
        """Compile list of operations in a single byte-code.

        :param code: List of operations to compile
        :type code: List[Operation]

        :raise BadOperationSize: If bad operation size will be generated

        :return: BytesIO with written bytecode
        :rtype: io.BytesIO
        """
        bytecode_buffer = io.BytesIO(self.generate_metadata(self.file_crc))

        for operation in code:
            encoded_operation = self.encode_operation(operation)

            op_writed = bytecode_buffer.write(encoded_operation)

            if op_writed != OP_SIZE:
                raise BadOperationSize(operation, op_writed)

        return bytecode_buffer

    def generate_metadata(self, file_crc: int) -> bytes:
        """Generate bytecode-file metadata.

        :param int file_crc: CRC sum of file to compile

        :return: Bytes of metadata
        :rtype: bytes
        """
        return struct.pack('hI', MAG_NUM, file_crc)

    def encode_operation(self, operation: Operation) -> bytes:
        """Encode operation to bytes in byte-code.

        :param operation: Operation to encode
        :type operation: :class:`~.Operation`

        :return: Encoded bytes of operation
        :rtype: bytes
        """
        op_word = operation.op_word

        op_code = BYTECODES[Keyword(op_word)]

        arguments = list(
            itertools.chain(
                *[(arg.arg_type.value, arg.arg_word)
                  for arg in operation.op_args]
            )
        )

        operation_code = struct.pack(
            '=hbibi',
            op_code, *arguments
        )

        return operation_code
