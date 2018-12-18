import argparse
from tapl.arith.parser import parser
from tapl.arith.core import evaluate

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('in_file', nargs='?')


def main():
    args = arg_parser.parse_args()
    if args.in_file is None:
        try:
            while True:
                code = input('>>> ')
                code = code.strip()
                if not code.endswith(';'):
                    code = code + ';'
                parser.file_name = '<stdin>'
                parser.file_data = code
                for term in parser.parse(code):
                    print(evaluate(term))
        except (EOFError, KeyboardInterrupt):
            print()
    else:
        with open(args.in_file) as f:
            code = f.read()
        parser.file_name = args.in_file
        parser.file_data = code
        for term in parser.parse(code):
            print(evaluate(term))


if __name__ == '__main__':
    main()
