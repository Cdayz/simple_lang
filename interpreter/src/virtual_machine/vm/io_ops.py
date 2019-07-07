"""Module with IO operations for VmState execution."""

from interpreter.src.virtual_machine.vm.vm_def import (
    VmState,
    VM_OPERATION_TO_BYTECODE
)
from interpreter.src.virtual_machine.vm.helpers import vm_operation


@vm_operation
def vm_input(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
    """Input value from stdin and write it to memory or register."""
    op_code, arg1_type, arg1, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "INPUT"

    while True:
        try:
            input_value = int(input("VM INPUT: "))
        except ValueError:
            continue
        else:
            break

    if arg1_type == 2:  # Register
        vm_state.vm_registers[arg1].value = input_value

    elif arg1_type == 3:  # Register pointer
        mem_address = vm_state.vm_registers[arg1].value
        vm_state.vm_memory[mem_address] = input_value

    else:
        raise Exception("Bad input destination")

    return vm_state


@vm_operation
def vm_print(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
    """Read value from register or memory and print it to stdout."""
    op_code, arg1_type, arg1, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "PRINT"

    if arg1_type == 2:  # Register
        value_for_print = vm_state.vm_registers[arg1].value

    elif arg1_type == 3:  # Register pointer
        mem_address = vm_state.vm_registers[arg1].value
        value_for_print = vm_state.vm_memory[mem_address]

    elif arg1_type == 4:  # In-place value
        value_for_print = arg1

    else:
        raise Exception("Bad print source")

    print(f'VM PRINT: {value_for_print}')

    return vm_state
