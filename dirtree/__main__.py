from pprint import pprint

from .cli import parser
from .options import Options
from .walker import EntryWalker


def main():
    args = Options(parser.parse_args())

    # pprint(args)

    for file in args.files:
        for entry in EntryWalker(args, file):
            pprint(entry)


if __name__ == '__main__':
    main()
