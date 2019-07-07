import io

from interpreter.src.virtual_machine.vm.vm_executor import (
    initialize_vm,
    execute_bytecode,
)

from interpreter.src.virtual_machine.test.vm.test_binary_ops import (
    gen_bytecode
)


def test_initialize():
    bcode = io.BytesIO(b"")

    vm = initialize_vm(bcode)

    assert vm.vm_code_buffer is bcode
    assert vm.vm_code_pointer == 0


def test_execute():
    bcode_lines = [
        gen_bytecode("MOV r1, 3"),
        gen_bytecode("MOV r2, 3"),
        gen_bytecode("ADD r1, r2"),
    ]
    bcode = io.BytesIO(b"".join(bcode_lines))

    end_state = execute_bytecode(bcode)

    assert end_state.vm_code_pointer == 12*3
    assert end_state.vm_registers[0].value == 6
