"""Module with helper functions for VmState execution."""

import copy
import typing
import struct
import functools

from interpreter.src.virtual_machine.vm.vm_def import VmState


def vm_operation(func: typing.Callable):
    """Decorator around operations on VmState.

    Copies vm state, unpack operation into numbers and provide it to
    decorated function as op_bytecode keyword argument.

    :param func: Function for decorate
    :type func: Callable
    """
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
