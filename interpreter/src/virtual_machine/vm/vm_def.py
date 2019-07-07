"""Module with basic definitions for Virtual Machine."""

import io
import typing
import dataclasses

from interpreter.src.lexer.keywords import LANGUAGE_REGISTERS
from interpreter.src.virtual_machine.bytecode import BYTECODES


VM_OPERATION_TO_BYTECODE = {
    bytecode: operation
    for operation, bytecode in BYTECODES.items()
}

VM_MEM_SIZE = 1024


@dataclasses.dataclass
class VmRegister:
    """Register representation of virtual machine.

    :param str name: Name of register
    :param int value: value of register
    """

    name: str
    value: int


def get_registers_map() -> typing.Dict[int, VmRegister]:
    """Generates registers mapping."""
    return {
        reg_index: VmRegister(name=name, value=0)
        for reg_index, name in enumerate(LANGUAGE_REGISTERS)
    }


def get_default_memory() -> typing.List[int]:
    """Generates base memory."""
    return [0 for _ in range(VM_MEM_SIZE)]


@dataclasses.dataclass
class VmState:
    """Virtual Machine State representation.

    :param vm_registers: Dict[register number, register object]
    :type vm_registers: Dict[int, VmRegister]

    :param vm_memory: Memory of virtual machine
    :type vm_memory: List[int] with size=VM_MEM_SIZE

    :param int vm_code_pointer: Points to current code instruction

    :param vm_code_buffer: Buffer with code for execute in VM
    :type vm_code_buffer: io.BytesIO

    :param vm_labels: Lookup for labels and jumps throught execution
    :type vm_labels: Dict[int, int]
    """

    # Code execution
    vm_code_buffer: io.BytesIO
    vm_code_pointer: int = 0

    # Registers
    vm_registers: typing.Dict[int, VmRegister] = \
        dataclasses.field(default_factory=get_registers_map)

    # Memory
    vm_memory: typing.List[int] = \
        dataclasses.field(default_factory=get_default_memory)

    # Labels map, key - label, value label position
    vm_labels: typing.Dict[int, int] = dataclasses.field(default_factory=dict)
