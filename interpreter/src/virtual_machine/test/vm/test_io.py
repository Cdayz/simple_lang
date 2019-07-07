import io
import struct

import mock
import pytest

from interpreter.src.virtual_machine.vm.io_ops import (
    vm_input,
    vm_print,
    VmState
)

from interpreter.src.virtual_machine.test.vm.test_binary_ops import (
    gen_bytecode
)


def test_vm_print():
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("PRINT r1")),
        vm_code_pointer=0,
    )

    with mock.patch('interpreter.src.virtual_machine.vm.io_ops.print') as p:
        p.return_value = 1
        state = vm_print(base_state)

        p.assert_called_with("VM PRINT: 0")

    assert state.vm_code_pointer == 12

    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("PRINT @r1")),
        vm_code_pointer=0,
    )

    with mock.patch('interpreter.src.virtual_machine.vm.io_ops.print') as p:
        p.return_value = 1
        state = vm_print(base_state)

        p.assert_called_with("VM PRINT: 0")

    assert state.vm_code_pointer == 12

    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("PRINT 12")),
        vm_code_pointer=0,
    )

    with mock.patch('interpreter.src.virtual_machine.vm.io_ops.print') as p:
        p.return_value = 1
        state = vm_print(base_state)

        p.assert_called_with("VM PRINT: 12")

    assert state.vm_code_pointer == 12


def test_vm_print_error():
    bcode = gen_bytecode("PRINT r1")

    op_code = struct.unpack('=hbibi', bcode)
    op_code = list(op_code)
    op_code[1] = 0

    bcode = struct.pack('=hbibi', *op_code)

    base_state = VmState(
        vm_code_buffer=io.BytesIO(bcode),
        vm_code_pointer=0,
    )

    with pytest.raises(Exception):
        vm_print(base_state)


def test_vm_input():
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("INPUT r1")),
        vm_code_pointer=0,
    )

    with mock.patch('interpreter.src.virtual_machine.vm.io_ops.input') as inp:
        inp.side_effect = ['a', 1]
        state = vm_input(base_state)

    assert state.vm_code_pointer == 12
    assert state.vm_registers[0].value == 1

    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("INPUT @r1")),
        vm_code_pointer=0,
    )

    with mock.patch('interpreter.src.virtual_machine.vm.io_ops.input') as inp:
        inp.side_effect = ['a', 1]
        state = vm_input(base_state)

    assert state.vm_code_pointer == 12
    mem_addr = state.vm_registers[0].value
    assert state.vm_memory[mem_addr] == 1


def test_vm_input_error():
    bcode = gen_bytecode("INPUT r1")

    op_code = struct.unpack('=hbibi', bcode)
    op_code = list(op_code)
    op_code[1] = 0

    bcode = struct.pack('=hbibi', *op_code)

    base_state = VmState(
        vm_code_buffer=io.BytesIO(bcode),
        vm_code_pointer=0,
    )

    with mock.patch('interpreter.src.virtual_machine.vm.io_ops.input') as inp:
        inp.side_effect = ['a', 1]
        with pytest.raises(Exception):
            vm_input(base_state)
