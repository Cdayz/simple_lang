"""Module with virtual machine state and some vm-related functional."""

import io
import typing
import dataclasses

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
