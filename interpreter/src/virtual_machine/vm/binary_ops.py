"""Module with binary operations implementations on VmState."""

import typing
import operator

from interpreter.src.virtual_machine.vm.vm_def import (
    VmState,
    VM_OPERATION_TO_BYTECODE
)
from interpreter.src.virtual_machine.vm.helpers import vm_operation


def gen_binary_operation(operation_name: str,
                         func: typing.Callable) -> typing.Callable:
    """Generate function for binary operations.

    Every binary operation works as explained above:

        Example:
            MOV r1, r2 - it's equal to set value of r2 to r1
            and second operand can be pointer, register and in-place value
            but first operand must be register or pointer nothing else.

    :param str operation_name: Name of operation for checks and exceptions

    :param func: Function makes operations and return value for set into 1 arg
    :type func: Callable[[int, int], int]

    :return: Builded function for make that operation on VmState
    :rtype: Callable
    """
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

    # Need for easy debugging
    gen.__name__ = f"vm_{operation_name.lower()}"

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
