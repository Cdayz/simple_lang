import struct

import pytest

from interpreter.src.virtual_machine.byte_cc import (
    BytecodeCompiler,
    MAG_NUM,
    OP_SIZE,
    BadOperationSize
)

from interpreter.src.parser.parser import NOP_ARG
from interpreter.src.parser.operation import (
    Operation,
    OperationType,
    OperationArgument,
    OperationArgumentType,
)


def test_compiler_compile_ok():
    compiler = BytecodeCompiler(file_crc=1234)

    # MOV @r1, 14
    # LABEL L1
    # NOP
    operations = [
        Operation(
            op_type=OperationType.Binary,
            op_word="MOV",
            op_args=[
                OperationArgument(
                    arg_type=OperationArgumentType.RegisterPointer,
                    arg_word=0
                ),
                OperationArgument(
                    arg_type=OperationArgumentType.InPlaceValue,
                    arg_word=14
                )
            ]
        ),
        Operation(
            op_type=OperationType.Unary,
            op_word="LABEL",
            op_args=[
                OperationArgument(
                    arg_type=OperationArgumentType.Label,
                    arg_word=1
                ),
                NOP_ARG
            ]
        ),
        Operation(
            op_type=OperationType.Nop,
            op_word="NOP",
            op_args=[NOP_ARG, NOP_ARG]
        )
    ]

    bytecode = compiler.compile(operations)

    assert bytecode

    bytecode = bytecode.read1()

    meta_size = 8

    meta, code = bytecode[:meta_size], bytecode[meta_size:]

    meta_unpacked = struct.unpack('hI', meta)

    assert meta_unpacked == (MAG_NUM, 1234)

    expected_code = [
        # mov, register-pointer, r1, in-place, 14
        (8, 3, 0, 4, 14),
        # label, label-type, label, nop, nop
        (15, 1, 1, 0, 0),
        # NOP, nop, nop, nop, nop
        (18, 0, 0, 0, 0),
    ]

    ops = [
        struct.unpack('=hbibi', code[shift:shift+OP_SIZE])
        for shift in range(0, len(code), OP_SIZE)
    ]

    assert ops == expected_code


def test_compiler_compile_exception():
    compiler = BytecodeCompiler(file_crc=1234)

    # MOV @r1, 14
    # LABEL L1
    # NOP
    operations = [
        Operation(
            op_type=OperationType.Binary,
            op_word="MOV",
            op_args=[
                OperationArgument(
                    arg_type=OperationArgumentType.RegisterPointer,
                    arg_word=0
                ),
                OperationArgument(
                    arg_type=OperationArgumentType.InPlaceValue,
                    arg_word=140000000000000
                )
            ]
        ),
    ]

    with pytest.raises(BadOperationSize):
        compiler.compile(operations)

    operations = [
        Operation(
            op_type=OperationType.Binary,
            op_word="MOVABLE",
            op_args=[
                OperationArgument(
                    arg_type=OperationArgumentType.RegisterPointer,
                    arg_word=0
                ),
                OperationArgument(
                    arg_type=OperationArgumentType.InPlaceValue,
                    arg_word=140000000000000
                )
            ]
        ),
    ]

    # Bad operation key

    with pytest.raises(Exception):
        compiler.compile(operations)
