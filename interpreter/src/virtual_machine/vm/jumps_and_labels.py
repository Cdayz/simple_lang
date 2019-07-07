import typing

from interpreter.src.virtual_machine.vm.vm_def import (
    VmState,
    VM_OPERATION_TO_BYTECODE
)
from interpreter.src.virtual_machine.vm.helpers import vm_operation


def generate_jump(jmp_name: str, cond: typing.Callable):
    """Generate function for conditional jumps.

    Every jump work as explained above:

        Example:
            LABEL abc
            CMP 3, 7
            JMP_NE abc

        Jump will work only if compare operation before set NE register to True

    :param str jump_name: Name of jump operation for checks and exceptions

    :param cond: Function around VmState wich checks NE, EQ, GT, LT registers
    :type cond: Callable[[VmState], bool]

    :return: Generated function for jumps
    :rtype: Callable
    """
    @vm_operation
    def gen(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
        op_code, _, arg1, _, _ = op_bytecode

        assert VM_OPERATION_TO_BYTECODE[op_code] == jmp_name

        label_index = arg1

        if label_index not in vm_state.vm_labels:
            raise Exception(f"Bad label {label_index}")

        if cond(vm_state):
            vm_state.vm_code_pointer = vm_state.vm_labels[label_index]

        return vm_state

    return gen


# Jumps
vm_jmp = generate_jump("JMP", lambda _: True)
vm_jump_eq = generate_jump("JMP_EQ", lambda state: state.vm_registers[5].value)
vm_jump_lt = generate_jump("JMP_LT", lambda state: state.vm_registers[6].value)
vm_jump_gt = generate_jump("JMP_GT", lambda state: state.vm_registers[7].value)
vm_jump_ne = generate_jump("JMP_NE", lambda state: state.vm_registers[8].value)


@vm_operation
def vm_label(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
    """LABEL operation for virtual machine."""
    op_code, _, arg1, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "LABEL"

    label_index = arg1
    label_position = vm_state.vm_code_pointer

    if label_index not in vm_state.vm_labels:
        vm_state.vm_labels[label_index] = label_position

    return vm_state


@vm_operation
def vm_cmp(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
    """CMP operation for virtual machine."""
    op_code, arg1_type, arg1, arg2_type, arg2 = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "CMP"

    if arg2_type == 2:  # Register
        right_value = vm_state.vm_registers[arg2].value

    elif arg2_type == 3:  # Register pointer
        input_value_addr = vm_state.vm_registers[arg2].value
        right_value = vm_state.vm_memory[input_value_addr]

    elif arg2_type == 4:  # In-place value
        right_value = arg2

    else:
        raise Exception(f"Bad argument for CMP")

    if arg1_type == 2:  # Register
        left_value = vm_state.vm_registers[arg1].value

    elif arg1_type == 3:  # RegisterPointer
        mem_index = vm_state.vm_registers[arg1].value
        left_value = vm_state.vm_memory[mem_index]

    elif arg1_type == 4:  # In-place value
        left_value = arg1

    else:
        raise Exception(f"Bad argument on CMP")

    if left_value > right_value:
        vm_state.vm_registers[7].value = True
        vm_state.vm_registers[8].value = True
    elif left_value < right_value:
        vm_state.vm_registers[6].value = True
        vm_state.vm_registers[8].value = True
    elif left_value == right_value:
        vm_state.vm_registers[5].value = True
        vm_state.vm_registers[6].value = False
        vm_state.vm_registers[7].value = False
        vm_state.vm_registers[8].value = False

    return vm_state


@vm_operation
def vm_nop(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
    """NOP operation for virtual machine."""
    op_code, _, _, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "NOP"

    return vm_state
