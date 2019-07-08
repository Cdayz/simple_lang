from interpreter.src.virtual_machine.vm.binary_ops import (
    vm_add,
    vm_sub,
    vm_mul,
    vm_div,
    vm_and,
    vm_or,
    vm_xor,
    vm_mov,
    vm_not,
)
from interpreter.src.virtual_machine.vm.jumps_and_labels import (
    vm_end,
    vm_call,
    vm_ret,
    vm_nop,
    vm_cmp,
    vm_jmp,
    vm_label,
    vm_jump_eq,
    vm_jump_lt,
    vm_jump_gt,
    vm_jump_ne,
)
from interpreter.src.virtual_machine.vm.io_ops import (
    vm_input,
    vm_print
)

from interpreter.src.virtual_machine.bytecode import BYTECODES


FUNCTIONS = (
    vm_add, vm_sub, vm_div, vm_mul,
    vm_and, vm_or, vm_xor, vm_not,
    vm_mov, vm_cmp, vm_jmp, vm_jump_eq,
    vm_jump_gt, vm_jump_lt, vm_jump_ne,
    vm_label, vm_print, vm_input, vm_nop, vm_end, vm_call, vm_ret
)


VM_BYTECODE_FUNC = {
    bytecode: func
    for bytecode, func in zip(
        [bytecode for _, bytecode in BYTECODES.items()],
        FUNCTIONS,
    )
}


VM_LABEL_FUNC = {
    bytecode: vm_nop if func.__name__ != 'vm_label' else vm_label
    for bytecode, func in VM_BYTECODE_FUNC.items()
}
