import io
import struct

import pytest

from interpreter.src.virtual_machine.vm.jumps_and_labels import (
    generate_jump,
    vm_label,
    vm_nop,
    vm_cmp,
    VmState
)

from interpreter.src.virtual_machine.test.vm.test_binary_ops import (
    gen_bytecode
)


def test_generate_jump():
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("JMP LABEL")),
        vm_code_pointer=0,
        vm_labels={1: 100500}
    )

    jmp_code = generate_jump("JMP", lambda x: True)

    assert jmp_code.__name__ == 'vm_jmp'

    state = jmp_code(base_state)

    assert state.vm_code_pointer == 100500 + 12


def test_generate_jump_bad_label():
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("JMP LABEL")),
        vm_code_pointer=0,
        vm_labels={2: 100500}
    )

    jmp_code = generate_jump("JMP", lambda x: True)

    with pytest.raises(Exception):
        jmp_code(base_state)


def test_vm_label():
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("LABEL main")),
        vm_code_pointer=0,
        vm_labels={2: 100500}
    )

    state = vm_label(base_state)

    assert state.vm_labels == {2: 100500, 1: 0}


def test_vm_nop():
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("NOP")),
        vm_code_pointer=0,
    )

    state = vm_nop(base_state)

    assert state.vm_code_pointer == 12


def test_vm_cmp():
    # In-place
    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("CMP 3, 7")),
        vm_code_pointer=0,
    )

    state = vm_cmp(base_state)

    assert not state.vm_registers[5].value
    assert not state.vm_registers[7].value
    assert state.vm_registers[6]
    assert state.vm_registers[8]

    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("CMP r1, r2")),
        vm_code_pointer=0,
    )
    base_state.vm_registers[0].value = 7
    base_state.vm_registers[1].value = 3

    state = vm_cmp(base_state)

    assert not state.vm_registers[5].value
    assert not state.vm_registers[6].value
    assert state.vm_registers[7].value
    assert state.vm_registers[8].value

    base_state = VmState(
        vm_code_buffer=io.BytesIO(gen_bytecode("CMP @r1, @r2")),
        vm_code_pointer=0,
    )

    base_state.vm_registers[0].value = 7
    base_state.vm_registers[1].value = 7

    state = vm_cmp(base_state)

    assert state.vm_registers[5].value
    assert not state.vm_registers[6].value
    assert not state.vm_registers[7].value
    assert not state.vm_registers[8].value


def test_vm_cmp_error_1_arg():
    bcode = gen_bytecode("CMP r1, 11")

    op_code = struct.unpack('=hbibi', bcode)
    op_code = list(op_code)
    op_code[1] = 0

    bcode = struct.pack('=hbibi', *op_code)

    base_state = VmState(
        vm_code_buffer=io.BytesIO(bcode),
        vm_code_pointer=0,
    )

    with pytest.raises(Exception):
        vm_cmp(base_state)


def test_vm_cmp_error_2_arg():
    bcode = gen_bytecode("CMP r1, 11")

    op_code = struct.unpack('=hbibi', bcode)
    op_code = list(op_code)
    op_code[-2] = 0

    bcode = struct.pack('=hbibi', *op_code)

    base_state = VmState(
        vm_code_buffer=io.BytesIO(bcode),
        vm_code_pointer=0,
    )

    with pytest.raises(Exception):
        vm_cmp(base_state)
