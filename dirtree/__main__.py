from pprint import pprint

from .cli import parser
from .options import Options


def main():
    args = Options(parser.parse_args())

    pprint(args)


if __name__ == '__main__':
    main()
