from .cli import parser
from .options import Options


def main():
    args = Options(parser.parse_args())
    print(repr(args))


if __name__ == '__main__':
    main()
