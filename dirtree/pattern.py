import collections
import fnmatch
import re

from .mixins import FieldsMixin


def exclude(pattern):
    return FilePredicate(pattern, fnmatch.translate(pattern))


def exclude_from(file):
    if isinstance(file, (str, bytes)):
        file = open(file, 'rt')

    with file:
        it = (line.strip() for line in file)
        return [exclude(line) for line in it if line and not line.startswith('#')]


class FilePredicate(collections.Callable, FieldsMixin):
    __repr_fields__ = ('fn_pattern', 're_pattern')

    def __init__(self, fn_pattern, re_pattern):
        self.fn_pattern = fn_pattern
        self.re_pattern = re_pattern

        self._re = re.compile(re_pattern, re.I)

    def __call__(self, entry):
        if '/' in self.fn_pattern:
            return bool(self._re.search(entry.path))

        return bool(self._re.search(entry.name))
