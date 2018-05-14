import datetime
from operator import methodcaller

from .entry import Entry
from .mixins import FieldsMixin, ValidateMixin
from .reader import Reader


class Options(FieldsMixin, ValidateMixin):
    __repr_fields__ = (
        'all', 'apparent_size', 'block_size', 'count_links', 'dereference',
        'dereference_args', 'exclude', 'files', 'human_readable', 'inodes',
        'max_depth', 'null', 'one_file_system', 'separate_dirs', 'si',
        'threshold', 'time', 'time_style', 'total',
    )

    def __init__(self, args):
        self._args = args
        self.validate()

    def _validate_block_size(self, value):
        if value <= 0:
            msg = '`block_size` must be greater than zero, got %d' % value
            raise ValueError(msg)

    def _validate_max_depth(self, value):
        if value < 0:
            msg = '`max_depth` must be greater than or equal to 0, got %d' % value
            raise ValueError(msg)

    def _validate_human_readable(self):
        if self.human_readable and self.si:
            msg = '`human_readable` and `si` are mutually exclusive'
            raise ValueError(msg)

    _validate_si = _validate_human_readable

    def _validate_time(self, value):
        if value not in ('atime', 'access', 'use', 'ctime', 'status', True, False):
            msg = '`time` is not an expected value, got %s' % value
            raise ValueError(msg)

    @property
    def all(self):
        '''write output for all files, not just directories

        :rtype: bool
        '''
        return self._args.all

    @property
    def apparent_size(self):
        '''print apparent sizes rather than disk usage

        :rtype: bool
        '''
        return self._args.apparent_size

    @property
    def block_size(self):
        '''if set, the amount to factor output sizes by

        :rtype: int or None
        '''
        return self._args.block_size

    @property
    def count_links(self):
        '''if set, hard links to the same file will be included

        :rtype: bool
        '''
        return self._args.count_links

    @property
    def dereference(self):
        '''follow symbolic links

        :rtype: bool
        '''
        return self._args.dereference

    @property
    def dereference_args(self):
        '''follow symbolic links on the command line

        :rtype: bool
        '''
        return self.dereference or self._args.dereference_args

    @property
    def exclude(self):
        '''exclude file patterns

        :rtype: [dirtree.pattern.FilePredicate]
        '''
        try:
            return self._exclude
        except AttributeError:
            pass

        from .pattern import exclude, exclude_from

        self._exclude = []

        if self._args.exclude:
            self._exclude.extend(map(exclude, self._args.exclude))

        if self._args.exclude_from:
            self._exclude.extend(exclude_from(self._args.exclude_from))

        return self._exclude

    @property
    def files(self):
        '''the top level files to recursively iterate over

        :rtype: [dirtree.walker.Entry]
        '''
        try:
            return self._files
        except AttributeError:
            pass

        self._files = []
        for file in self._iter_files(self._args.files0_from, *self._args.files):
            entry = Entry(file)
            self._files.append(entry)
            if self.dereference_args and entry.is_symlink:
                entry = Entry(entry.readlink)
                self._files.append(entry)

        if not self._files:
            self._files.append(Entry('.'))

        return self._files

    @property
    def human_readable(self):
        '''output sizes in a human readable format (e.g., 1K 234M 2G)

        :rtype: bool
        '''
        return self._args.human_readable

    @property
    def inodes(self):
        '''list inode usage instead of block usage

        :rtype: bool
        '''
        return self._args.inodes

    @property
    def max_depth(self):
        '''if specified, print the directory only if it is within `N` or fewer
        levels of the input argument

        :rtype: int or None
        '''
        return self._args.max_depth

    @property
    def null(self):
        '''terminate output records with a `NUL` byte instead of a newline

        :rtype: bool
        '''
        return self._args.null

    @property
    def one_file_system(self):
        '''output files only on the same device as the input argument

        :rtype: bool
        '''
        return self._args.one_file_system

    @property
    def separate_dirs(self):
        '''for directories, do not include the size of subdirectories

        :rtype: bool
        '''
        return self._args.separate_dirs

    @property
    def si(self):
        '''like `human_readable` but uses powers of 1000 instead of 1024

        :rtype: bool
        '''
        return self._args.si

    @property
    def threshold(self):
        '''include entries smaller than threshold if positive, or greater if neg

        :rtype: int or None
        '''
        return self._args.threshold

    @property
    def time(self):
        '''if set, show the last modified time or one of ('atime', 'access',
        'use', 'ctime', 'status')

        :rtype: str or bool or None
        '''
        return self._args.time

    @property
    def time_style(self):
        '''output time format

        :rtype: str
        '''
        return self._args.time_style

    @property
    def total(self):
        '''yield a total row record of the input files

        :rtype: bool
        '''
        return self._args.total

    def strftime(self, mmt=None):
        if mmt is None:
            mmt = datetime.datetime.now()

        return mmt.strftime(self.time_style)

    @classmethod
    def _iter_files(cls, files0_from=None, *files):
        yield from files

        if not files0_from:
            return

        if isinstance(files0_from, str):
            files0_from = open(files0_from, 'rb')

        with files0_from:
            reader = Reader(files0_from, b'\x00')
            yield from map(methodcaller('decode', 'utf-8'), reader)
