"""Module with main executor of VM."""

import io
import struct

from interpreter.src.virtual_machine.vm.vm_def import VmState

from interpreter.src.virtual_machine.vm import VM_BYTECODE_FUNC


def initialize_vm(bytecode: io.BytesIO) -> VmState:
    """Init vm state with given bytecode.

    :param bytecode: Bytecode
    :type bytecode: io.BytesIO

    :return: Initialized VmState
    :rtype: VmState
    """
    return VmState(
        vm_code_buffer=bytecode
    )


def execute_bytecode(bytecode: io.BytesIO):
    """Execute bytecode into Virtual Machine.

    :param bytecode: Bytecode for executing
    :type bytecode: io.BytesIO
    """
    code_size = len(bytecode.read())
    bytecode.seek(0)
    vm_state = initialize_vm(bytecode)

    while vm_state.vm_code_pointer < code_size:
        vm_state.vm_code_buffer.seek(vm_state.vm_code_pointer)
        bcode = vm_state.vm_code_buffer.read1(2)
        opcode = struct.unpack('=h', bcode)[0]

        vm_state.vm_code_buffer.seek(
            vm_state.vm_code_pointer
        )

        vm_state = VM_BYTECODE_FUNC[opcode](vm_state)
