import argparse

from .constants import DESCRIPTION, EPILOG
from .size_type import parse_size_type


class MetaAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        kwargs['nargs'] = 0
        kwargs['dest'] = argparse.SUPPRESS
        super().__init__(*args, **kwargs)


class SetBytesAction(MetaAction):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'apparent_size', True)
        setattr(namespace, 'block_size', 1)


def parse_time_style(string):
    if string.startswith('+'):
        return string[1:]

    if string == 'full-iso':
        return '%F %T.%f %z'

    if string == 'long-iso':
        return '%F %R'

    if string == 'iso':
        return '%F'

    raise argparse.ArgumentTypeError('Invalid style "%s"' % (string, ))


parser = argparse.ArgumentParser(
    description=DESCRIPTION,
    epilog=EPILOG,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    add_help=False,
)

parser.add_argument(
    '-0', '--null',
    action='store_true',
    help='end each output line with NUL, not newline',
)

parser.add_argument(
    '-a', '--all',
    action='store_true',
    help='write counts for all files, not just directories',
)

parser.add_argument(
    '--apparent-size',
    action='store_true',
    help='print apparent sizes, rather than disk usage; although the apparent '
    "size is usually smaller, it may be larger due to holes in ('sparse') "
    'files, internal fragmentation, indirect blocks, and the like'
)

parser.add_argument(
    '-B', '--block-size',
    type=parse_size_type,
    default='',
    help="scale sizes by SIZE before printing them; e.g., '-BM' prints sizes in "
    'units of 1,048,576 bytes; see SIZE format below',
    metavar='SIZE',
)

parser.add_argument(
    '-b', '--bytes',
    action=SetBytesAction,
    help="equivalent to '--apparent-size --block-size=1'",
)

parser.add_argument(
    '-c', '--total',
    action='store_true',
    help='produce a grand total',
)

parser.add_argument(
    '-H', '-D', '--dereference-args',
    action='store_true',
    help='dereference only symlinks that are listed on the command line',
)

parser.add_argument(
    '-d', '--max-depth',
    type=int,
    help='print the total for a directory (or file, with --all) only if it is '
    'in N or fewer levels below the command line argument; --max-depth=0 is the '
    'same as --summarize',
    metavar='N',
)

parser.add_argument(
    '--files0-from',
    type=argparse.FileType('rb'),
    help='summarize disk usage of the NUL-terminated file names specified in '
    'file F; if F is -, then read names from standard input',
    metavar='F',
)

parser.add_argument(
    '-h', '--human-readable',
    action='store_true',
    help='print sizes in human readable format (e.g., 1K 234M 2G)'
)

parser.add_argument(
    '--inodes',
    action='store_true',
    help='list inode usage information instead of block usage'
)

parser.add_argument(
    '-k',
    action='store_const',
    const=parse_size_type('1K'),
    dest='block_size',
    help='like --block-size=1K',
)

parser.add_argument(
    '-L', '--dereference',
    action='store_true',
    help='dereference all symbolic links',
)

parser.add_argument(
    '-l', '--count-links',
    action='store_true',
    help='count sizes many times if hard linked',
)

parser.add_argument(
    '-m',
    action='store_const',
    const=parse_size_type('1M'),
    dest='block_size',
    help='like --block-size=1M',
)

parser.add_argument(
    '-P', '--no-dereference',
    action='store_false',
    default=False,
    dest='dereference',
    help="don't follow any symbolic links (this is the default)",
)

parser.add_argument(
    '-S', '--separate-dirs',
    action='store_true',
    help='for directories, do not include size of subdirectories',
)

parser.add_argument(
    '--si',
    action='store_true',
    help='like -h, but uses powers of 1000 not 1024',
)

parser.add_argument(
    '-s', '--summarize',
    action='store_const',
    const=0,
    dest='max_depth',
    help='display only a total for each argument',
)

parser.add_argument(
    '-t', '--threshold',
    type=parse_size_type,
    help='exclude entries smaller than SIZE if positive, or entries greater than '
    'SIZE if negative',
    metavar='SIZE',
)

parser.add_argument(
    '--time',
    nargs='?',
    const=True,
    choices=('atime', 'access', 'use', 'ctime', 'status'),
    help='show time of the last modification of any file in the directory, or '
    'any of its subdirectories; show time as WORD instead of modification time: '
    'atime, access, use, ctime, or status',
    metavar='WORD'
)

parser.add_argument(
    '--time-style',
    type=parse_time_style,
    default='long-iso',
    help='show times using STYLE, which can be: full-iso, long-iso, iso, or '
    '+FORMAT; FORMAT is interpreted as in `strftime`',
    metavar='STYLE',
)

parser.add_argument(
    '-X', '--exclude-from',
    type=argparse.FileType(),
    help='exclude files that match any pattern in FILE',
    metavar='FILE',
)

parser.add_argument(
    '--exclude',
    action='append',
    help='exclude files that match PATTERN',
    metavar='PATTERN',
)

parser.add_argument(
    '-x', '--one-file-system',
    action='store_true',
    help='skip directories on a different file system',
)

parser.add_argument(
    'files',
    nargs='*',
    metavar='FILE',
)

parser.add_argument(
    '--help',
    action='help',
    help='display this help and exit'
)
