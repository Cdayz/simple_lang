import io
from interpreter.src.parser.parser import Parser
from interpreter.src.virtual_machine.byte_cc import BytecodeCompiler
from interpreter.src.virtual_machine.vm.vm_executor import execute_bytecode

with open('test_examples/input.small', 'r') as inp_file:
    code = inp_file.read()


parsed_ops = Parser().parse(code)

bytecode = BytecodeCompiler(file_crc=12345).compile(parsed_ops)

bytecode.seek(0)

with open('test_examples/output.small_c', 'wb') as bytecode_file:
    bytecode_file.write(
        bytecode.read1()
    )


with open('test_examples/output.small_c', 'rb') as bcode_file:
    file_bcode = bcode_file.read()

meta_pos = 8
meta, bcode = file_bcode[:meta_pos], file_bcode[meta_pos:]

_end_state = execute_bytecode(io.BytesIO(bcode))
# print(_end_state)
