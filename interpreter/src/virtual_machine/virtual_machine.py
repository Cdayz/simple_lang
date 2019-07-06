"""Module with virtual machine state and some vm-related functional."""

import io
import copy
import struct
import typing
import operator
import functools
import dataclasses

from interpreter.src.virtual_machine.bytecode import BYTECODES
from interpreter.src.lexer.keywords import LANGUAGE_REGISTERS

VM_OPERATION_TO_BYTECODE = {
    bytecode: operation
    for operation, bytecode in BYTECODES.items()
}

VM_MEM_SIZE = 1024
VM_OP_SIZE = 12


@dataclasses.dataclass
class VmRegister:
    """Register representation of virtual machine."""

    name: str
    value: int


@dataclasses.dataclass
class VmState:
    """Virtual Machine State representation."""

    # Registers
    vm_registers: typing.Dict[int, VmRegister] = {
        reg_index: VmRegister(name=name, value=0)
        for reg_index, name in enumerate(LANGUAGE_REGISTERS)
    }
    # Memory
    vm_memory: typing.List[int] = [0 for _ in range(VM_MEM_SIZE)]
    # Code execution
    vm_code_pointer: int = 0
    vm_code_buffer: io.BytesIO = dataclasses.field(default_factory=io.BytesIO)
    # Labels map, key - label, value label position
    vm_labels: typing.Dict[int, int] = dataclasses.field(default_factory=dict)


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


def gen_binary_operation(operation_name: str, func: typing.Callable):
    """Generate function for binary operations."""

    @vm_operation
    def gen(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
        op_code, arg1_type, arg1, arg2_type, arg2 = op_bytecode

        assert VM_OPERATION_TO_BYTECODE[op_code] == operation_name

        if arg2_type == 2:  # Register
            input_value = vm_state.vm_registers[arg2].value

        elif arg2_type == 3:  # Register pointer
            input_value_addr = vm_state.vm_registers[arg2].value
            input_value = vm_state.vm_memory[input_value_addr]

        elif arg2_type == 4:  # In-place value
            input_value = arg2

        else:
            raise Exception(f"Bad argument for {operation_name}")

        if arg1_type == 2:  # Register
            output_val = vm_state.vm_registers[arg1].value
            vm_state.vm_registers[arg1].value = func(output_val, input_value)

        elif arg1_type == 3:  # RegisterPointer
            mem_index = vm_state.vm_registers[arg1].value
            output_val = vm_state.vm_memory[mem_index]
            vm_state.vm_memory[mem_index] = func(output_val, input_value)

        else:
            raise Exception(f"Bad argument on {operation_name}")

        return vm_state

    return gen


def generate_jump(jmp_name: str, cond: typing.Callable):
    """Generate function for conditional jumps."""

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


# Binary operations
vm_add = gen_binary_operation("ADD", operator.add)
vm_sub = gen_binary_operation("SUB", operator.sub)
vm_mul = gen_binary_operation("MUL", operator.mul)
vm_div = gen_binary_operation("DIV", operator.truediv)
vm_and = gen_binary_operation("AND", operator.and_)
vm_or = gen_binary_operation("OR", operator.or_)
vm_xor = gen_binary_operation("XOR", operator.xor)
vm_mov = gen_binary_operation("MOV", lambda _, x: x)
# NOT operation works because it's a parser dependent hack
vm_not = gen_binary_operation("NOT", lambda _, y: ~y)

# Jumps
vm_jmp = generate_jump("JMP", lambda _: True)
vm_jump_eq = generate_jump("JMP_EQ", lambda state: state.vm_registers[5].value)
vm_jump_lt = generate_jump("JMP_LT", lambda state: state.vm_registers[6].value)
vm_jump_gt = generate_jump("JMP_GT", lambda state: state.vm_registers[7].value)
vm_jump_ne = generate_jump("JMP_NE", lambda state: state.vm_registers[8].value)


@vm_operation
def vm_nop(vm_state: VmState, *args, op_bytecode=None, **kwargs) -> VmState:
    """NOP operation for virtual machine."""
    op_code, _, _, _, _ = op_bytecode

    assert VM_OPERATION_TO_BYTECODE[op_code] == "NOP"

    return vm_state


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

    elif arg1_type == 4: # In-place value
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
