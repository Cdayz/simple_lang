import io
import struct
import pathlib
import argparse
import typing

from interpreter.src.parser.parser import Parser, ParsingError
from interpreter.src.virtual_machine.byte_cc import BytecodeCompiler, MAG_NUM
from interpreter.src.virtual_machine.vm.vm_executor import execute_bytecode

META_SIZE: int = 8


def calcualte_crc(file_data: bytes) -> int:
    """Calcualte file crc.

    :param bytes file_data: Data of file

    :return: number crc of file data
    :rtype: int
    """
    result = sum(map(int, file_data)) % 100000

    return result


def compile_file(filename: str) -> bool:
    """Compile file.

    If have *.small_c file checks the file crc from bytecode and current file,
    If crc is changed recompile file else do nothing.

    :param str filename: File name to compile

    :return: True if file recompiled or False if bytecode is actual
    :rtype: bool
    """
    bytecode_file = pathlib.Path(filename + "_c")

    file_crc = None

    if bytecode_file.is_file():
        # Bytecode exists
        bytecode = bytecode_file.read_bytes()
        meta, _ = bytecode[:META_SIZE], bytecode[META_SIZE:]
        file_mag_number, file_crc = struct.unpack('hI', meta)

        if file_mag_number != MAG_NUM:
            file_crc = None

    source_code = pathlib.Path(filename).read_text()

    current_file_crc = calcualte_crc(bytes(source_code, 'utf-8'))

    if current_file_crc == file_crc:
        return False

    try:
        code_operations = Parser().parse(source_code)
    except ParsingError as pe:
        print(f"Parse error \"{pe.exception}\" at"
              f" line {pe.line_index}, {pe.line_code}")
        raise

    bytecode_gen = BytecodeCompiler(current_file_crc).compile(code_operations)
    bytecode_gen.seek(0)
    bytecode_file.write_bytes(bytecode_gen.read1())

    return True


def execute_file(filename: str) -> bool:
    """Execute bytecode of file."""
    bytecode_file = pathlib.Path(filename)

    bytecode = bytecode_file.read_bytes()

    meta, code = bytecode[:META_SIZE], bytecode[META_SIZE:]
    file_mag_number, _ = struct.unpack('hI', meta)

    if file_mag_number != MAG_NUM:
        return False

    execute_bytecode(io.BytesIO(code))

    return True


def main(config: typing.Dict[str, str]) -> int:
    """Main function for running compile of execute."""
    if 'compile' in config:
        file_to_compile = config['compile']

        try:
            updated = compile_file(file_to_compile)
        except ParsingError:
            return 1
        else:
            if updated:
                print(f'File {file_to_compile} bytecode updated.')
            else:
                print(f'File {file_to_compile} bytecode are up-to date.')

    elif 'execute' in config:
        file_to_exec = config['execute']

        exec_result = execute_file(file_to_exec)

        if not exec_result:
            print('Unable to execute bytecode file.')
            return 1

    return 0


def parse_args(args):
    """Parser for command line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--compile',
        '-c',
        action='store',
        default=''
    )

    parser.add_argument(
        '--execute',
        '-e',
        action='store',
        default=''
    )

    return parser.parse_args(args)


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]
    args_obj = parse_args(args)

    config = {}

    if args_obj.compile:
        config['compile'] = args_obj.compile
    elif args_obj.execute:
        config['execute'] = args_obj.execute

    sys.exit(main(config))
