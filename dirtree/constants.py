import stat
from collections import OrderedDict

PREFIXES = OrderedDict((
    ('', 0),
    ('K', 1),
    ('M', 2),
    ('G', 3),
    ('T', 4),
    ('P', 5),
    ('E', 6),
    ('Z', 7),
    ('Y', 8),
))

DESCRIPTION = '''\
    Summarize disk usage of the set of FILEs, recursively for directories.
'''

EPILOG = '''\
    Display values are in units of the first available SIZE from --block-size,
    and the DU_BLOCK_SIZE, BLOCK_SIZE and BLOCKSIZE environment variables.
    Otherwise, units default to 1024 bytes (or 512 if POSIXLY_CORRECT is set).

    The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
    Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).

PATTERNS
    PATTERN is a shell pattern (not a regular expression). The pattern `?'
    matches any one character, whereas `*' matches any string (composed of zero,
    one, or multiple characters). For example, `*.o' will match any files whose
    names end in .o. Therefore, the command

        %(prog)s --exclude='*.o'

    will skip all files and subdirectories ending in .o (including the file .o
    itself).
'''

STAT_FMT_TYPE = {
    stat.S_IFDIR: 'directory',
    stat.S_IFCHR: 'char',
    stat.S_IFBLK: 'block',
    stat.S_IFREG: 'file',
    stat.S_IFIFO: 'fifo',
    stat.S_IFLNK: 'symlink',
    stat.S_IFSOCK: 'socket',
}
