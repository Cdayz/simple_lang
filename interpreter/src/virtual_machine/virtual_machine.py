"""Module with virtual machine state and some vm-related functional."""

import io
import copy
import struct
import typing
import functools
import dataclasses

from interpreter.src.virtual_machine.bytecode import BYTECODES

VM_OPERATION_TO_BYTECODE = {
    bytecode: operation
    for operation, bytecode in BYTECODES.items()
}

VM_MEM_SIZE = 1024
VM_OP_SIZE = 12


@dataclasses.dataclass
class VmState:
    """Virtual Machine State representation."""

    # Registers
    A: int = 0
    r1: int = 0
    r2: int = 0
    r3: int = 0
    r4: int = 0
    EQ: int = 0
    GT: int = 0
    LT: int = 0
    NE: int = 0
    # Memory
    vm_memory: typing.List[int] = [0 for _ in range(VM_MEM_SIZE)]
    # Code execution
    vm_code_pointer: int = 0
    vm_code_buffer: io.BytesIO = dataclasses.field(default_factory=io.BytesIO)


def vm_operation(func):
    """Decorator around operations on VmState."""

    @functools.wraps(func)
    def wrapper(vm_state, *args, **kwargs):
        new_state: VmState = copy.deepcopy(vm_state)
        operation_bytecode = struct.unpack(
            '=hbibi',
            new_state.vm_code_buffer.read1(12)
        )

        kwargs['op_bytecode'] = operation_bytecode

        new_state = func(new_state, *args, **kwargs)

        new_state.vm_code_pointer += 12

        return new_state

    return wrapper


@vm_operation
def vm_mov(vm_state: VmState, *args, op_bytecode=None) -> VmState:
    """MOV function for virtual machine."""
    op_code, arg1_type, arg1, arg2_type, arg2 = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == 'MOV'

    # get input
    if arg2_type == 2:  # Register
        pass
    elif arg2_type == 3:  # Register pointer
        pass
    elif arg2_type == 4:  # In-place value
        pass
    else:
        raise Exception("Bad argument for mov")

    # Write to output
    if arg1_type == 2:  # Register
        pass
    elif arg1_type == 3:  # RegisterPointer
        pass
    else:
        raise Exception("Bad argument to Mov")

    return vm_state
