import io
import struct

import pytest

from interpreter.src.parser.parser import Parser
from interpreter.src.virtual_machine.byte_cc import BytecodeCompiler
from interpreter.src.virtual_machine.vm.binary_ops import (
    gen_binary_operation,
    VmState
)


def gen_bytecode(line: str) -> bytes:
    operation = Parser().parse_line(line)

    return BytecodeCompiler(file_crc=123).encode_operation(operation)


def test_gen_binary_ops_reg_reg():
    start_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("ADD r1, r2")),
        vm_code_pointer=0
    )

    start_state.vm_registers[0].value = 1
    start_state.vm_registers[1].value = 2

    bin_add = gen_binary_operation("ADD", lambda x, y: x+y)

    assert bin_add.__name__ == 'vm_add'

    result_state: VmState = bin_add(start_state)

    x = start_state.vm_registers[0].value
    y = start_state.vm_registers[1].value

    expected_sum = x + y

    assert result_state.vm_registers[0].value == expected_sum


def test_gen_binary_ops_point_reg():
    start_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("ADD @r1, r2")),
        vm_code_pointer=0
    )

    start_state.vm_registers[0].value = 1
    x_mem = start_state.vm_registers[0].value
    start_state.vm_memory[x_mem] = 1
    start_state.vm_registers[1].value = 2

    bin_add = gen_binary_operation("ADD", lambda x, y: x+y)

    result_state: VmState = bin_add(start_state)

    x_mem = start_state.vm_registers[0].value
    x = start_state.vm_memory[x_mem]
    y = start_state.vm_registers[1].value

    expected_sum = x + y

    assert result_state.vm_memory[x_mem] == expected_sum


def test_gen_binary_ops_point_point():
    start_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("ADD @r1, @r2")),
        vm_code_pointer=0
    )

    start_state.vm_registers[0].value = 1
    x_mem = start_state.vm_registers[0].value
    start_state.vm_memory[x_mem] = 1
    start_state.vm_registers[1].value = 2
    y_mem = start_state.vm_registers[1].value
    start_state.vm_memory[y_mem] = 12

    bin_add = gen_binary_operation("ADD", lambda x, y: x+y)

    result_state: VmState = bin_add(start_state)

    x_mem = start_state.vm_registers[0].value
    x = start_state.vm_memory[x_mem]
    y_mem = start_state.vm_registers[1].value
    y = start_state.vm_memory[y_mem]

    expected_sum = x + y

    assert result_state.vm_memory[x_mem] == expected_sum


def test_gen_binary_ops_reg_in_place():
    start_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("ADD r1, 12")),
        vm_code_pointer=0
    )

    start_state.vm_registers[0].value = 1

    bin_add = gen_binary_operation("ADD", lambda x, y: x+y)

    result_state: VmState = bin_add(start_state)

    x = start_state.vm_registers[0].value
    y = 12

    expected_sum = x + y

    assert result_state.vm_registers[0].value == expected_sum


def test_gen_binary_ops_error_1_arg():
    start_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("ADD 12, @r1")),
        vm_code_pointer=0
    )

    bin_add = gen_binary_operation("ADD", lambda x, y: x+y)

    with pytest.raises(Exception):
        bin_add(start_state)


def test_gen_binary_ops_error_2_arg():
    bcode = gen_bytecode("ADD r1, 11")

    op_code = struct.unpack('=hbibi', bcode)
    op_code = list(op_code)
    op_code[-2] = 0

    bcode = struct.pack('=hbibi', *op_code)

    start_state = VmState(
        vm_code_buffer=io.BytesIO(bcode),
        vm_code_pointer=0
    )

    bin_add = gen_binary_operation("ADD", lambda x, y: x+y)

    with pytest.raises(Exception):
        bin_add(start_state)
