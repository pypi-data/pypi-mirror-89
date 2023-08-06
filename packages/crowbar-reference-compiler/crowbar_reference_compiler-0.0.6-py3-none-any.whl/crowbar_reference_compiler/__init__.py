from .ast import build_ast
from .parser import parse_header, parse_implementation
from .scanner import scan
from .ssagen import build_ssa


def main():
    import argparse
    import subprocess
    import sys

    args = argparse.ArgumentParser(description='The reference compiler for the Crowbar programming language')
    args.add_argument('-V', '--version', action='version', version='%(prog)s 0.0.5')
    args.add_argument('-g', '--include-debug-info', action='store_true')
    args.add_argument('--stop-at-parse-tree', action='store_true')
    args.add_argument('--stop-at-qbe-ssa', action='store_true')
    args.add_argument('-S', '--stop-at-assembly', action='store_true')
    args.add_argument('-c', '--stop-at-object', action='store_true')
    args.add_argument('-D', '--define-constant', action='append', help='define a constant with some literal value')
    args.add_argument('-I', '--include-dir', action='append', help='folder to look for included headers within')
    args.add_argument('-o', '--out', help='output file')
    args.add_argument('input', help='input file')

    args = args.parse_args()
    with open(args.input, 'r', encoding='utf-8') as input_file:
        input_code = input_file.read()
    tokens = scan(input_code)
    parse_tree = parse_implementation(tokens)
    if args.stop_at_parse_tree:
        if args.out is None:
            args.out = args.input.replace('.cro', '.cro.txt')
        with open(args.out, 'w', encoding='utf-8') as output_file:
            output_file.write(str(parse_tree))
        return

    full_ast = build_ast(parse_tree, args.include_dir)

    ssa = build_ssa(full_ast)
    if args.stop_at_qbe_ssa:
        if args.out is None:
            args.out = args.input.replace('.cro', '.ssa')
        with open(args.out, 'w', encoding='utf-8') as output_file:
            output_file.write(ssa)
        return
    # TODO bundle the qbe binary or something
    qbe_result = subprocess.run(['qbe', '-'], input=ssa, capture_output=True, text=True)
    if qbe_result.returncode != 0:
        print(qbe_result.stderr, file=sys.stderr)
        sys.exit(1)
    asm = qbe_result.stdout
    if args.stop_at_assembly:
        if args.out is None:
            args.out = args.input.replace('.cro', '.s')
        with open(args.out, 'w', encoding='utf-8') as output_file:
            output_file.write(asm)
        return
    if args.out is None:
        args.out = args.input.replace('.cro', '.out')
    # TODO don't assume gcc is always the right thing
    extra_gcc_flags = []
    if args.stop_at_object:
        if args.out is None:
            args.out = args.input.replace('.cro', '.o')
        extra_gcc_flags.append('-c')
    gcc_result = subprocess.run(['gcc', '-x', 'assembler', '-o', args.out, *extra_gcc_flags, '-'], input=asm, text=True)
    sys.exit(gcc_result.returncode)


if __name__ == '__main__':
    main()
