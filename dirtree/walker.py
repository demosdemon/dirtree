from collections import Iterator

from .entry import Entry


def _get_key(obj, key, default=None):
    try:
        return obj[key]
    except (AttributeError, TypeError, KeyError):
        pass

    try:
        return getattr(obj, key)
    except AttributeError:
        pass

    return default


class DirectoryWalker(Iterator):
    def __init__(self, *paths, **kwargs):
        self.dereference = _get_key(kwargs, 'dereference', False)
        self.dereference_args = _get_key(kwargs, 'dereference_args', False)

        self._queue = []

        for path in paths:
            self.add_root(path)

    def __iter__(self):
        return self

    def __next__(self):
        return None

    def add_root(self, path):
        dereference = self.dereference or self.dereference_args
        entry = Entry(path)
        if dereference and entry.is_symlink:
            entry = Entry(entry.readlink)

        self._queue.append(entry)
