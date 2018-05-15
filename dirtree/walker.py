import os
from itertools import chain

from .entry import Entry


class EntryWalker:
    '''Recursively walks down a path rooted at `entry` with `options`

    :type options: dirtree.options.Options
    :type entry: dirtree.entry.Entry
    '''

    def __init__(self, options, entry):
        self.options = options
        self.entry = entry
        self.queue = self.__descend(entry, options.dereference_args)

    def __iter__(self):
        return self

    def __same_device(self, entry):
        if not self.options.one_file_system:
            return True

        if entry is self.entry:
            return True

        return self.entry.device == entry.device

    def __excluded(self, entry):
        for pred in self.options.exclude:
            if pred(entry):
                return True

        return False

    def __threshold(self, entry):
        thresh = self.options.threshold
        if thresh is None:
            return True

        if thresh == 0:
            return entry.size == 0

        if thresh < 0:
            return entry.size <= -thresh

        return thresh <= entry.size

    def __descend(self, entry, dereference=None):
        if dereference is None:
            dereference = self.options.dereference

        if not self.__same_device(entry):
            return ()

        result = (entry, )

        if dereference and entry.is_symlink:
            ref = Entry(entry.readlink)
            result = chain(self.__descend(ref), result)

        if not entry.is_dir:
            return result

        sub = os.scandir(entry.path)
        sub = map(Entry, sub)
        sub = map(self.__descend, sub)
        sub = chain.from_iterable(sub)

        result = chain(sub, result)
        return result

    def __next__(self):
        while True:
            entry = next(self.queue)
            assert isinstance(entry, Entry)
            if not self.__excluded(entry) and self.__threshold(entry):
                return entry
