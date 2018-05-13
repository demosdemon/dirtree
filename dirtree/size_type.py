import argparse
import math
import os
import re

from .constants import PREFIXES


def get_default_block_size():
    '''.. function:: get_default_block_size()

        returns the default block size; which is first found value of the
        environmental variables `DU_BLOCK_SIZE`, `BLOCK_SIZE`, or `BLOCKSIZE`.
        If not found and `POSIXLY_CORRECT` is set, `512` else `1024`.
    '''
    for key in ('DU_BLOCK_SIZE', 'BLOCK_SIZE', 'BLOCKSIZE'):
        value = os.getenv(key)

        if value:
            return parse_size_type(value)

    if os.getenv('POSIXLY_CORRECT', 0):
        return 512

    return 1024


def parse_size_type(string):
    '''.. function:: parse_size_type(string)

        parses the argument `string` into a size prefix or raises an exception

            :param string: the command line argument
            :type string: str
    '''
    if not string:
        return get_default_block_size()

    match = re.match(r'(?i)^([-+]?)(\d*)\s*([KMGTPEZY]?)(B?)$', str(string).strip())
    if not match:
        raise argparse.ArgumentTypeError('"%s" is invalid' % (string, ))

    sign, sig, unit, base = match.groups()

    sign = -1 if sign == '-' else 1

    unit = unit.upper()

    if sig:
        sig = int(sig)
    else:
        sig = 1

    if base in ('b', 'B'):
        base = 1000
    else:
        base = 1024

    assert unit in PREFIXES
    unit = PREFIXES[unit]

    return sign * sig * base ** unit


def humanize_size(n_bytes, base=1024):
    n_bytes = int(n_bytes)

    for suffix, power in PREFIXES.items():
        value = n_bytes / base ** power
        value = math.trunc(value)
        fmt = '%d%s' % (value, suffix)
        if value < base:
            fmt

    return fmt
