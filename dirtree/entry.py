import os
import stat

from .constants import STAT_FMT_TYPE
from .mixins import FieldsMixin
from .utils import local_timestamp, strftime


class Entry(FieldsMixin):
    __repr_fields__ = (
        'name', 'path', 'exists', 'type', 'is_dir', 'is_file', 'is_symlink',
        'readlink', ('mode', stat.filemode), ('device', hex), ('inode', hex),
        'num_links', 'uid', 'gid', 'size', ('atime', strftime),
        ('mtime', strftime), ('ctime', strftime),
    )

    def __init__(self, dir_entry):
        if isinstance(dir_entry, (Entry, os.DirEntry)):
            self.name = dir_entry.name
            self.path = dir_entry.path
            st = dir_entry.stat
            if callable(st):
                self.stat = st()
            else:
                self.stat = st
        else:
            self.name = os.path.basename(dir_entry)
            self.path = dir_entry
            try:
                self.stat = os.lstat(dir_entry)
            except OSError:
                self.stat = None

    def __bool__(self):
        return bool(self.stat)

    exists = property(__bool__)

    @property
    def type(self):
        if self:
            fmt = stat.S_IFMT(self.mode)
            return STAT_FMT_TYPE[fmt]

    @property
    def is_dir(self):
        return self.exists and stat.S_ISDIR(self.mode)

    @property
    def is_file(self):
        return self.exists and stat.S_ISREG(self.mode)

    @property
    def is_symlink(self):
        return self.exists and stat.S_ISLNK(self.mode)

    @property
    def readlink(self):
        try:
            return self._readlink
        except AttributeError:
            if self.is_symlink:
                link = os.readlink(self.path)
                self._readlink = os.path.join(self.path, link)
            else:
                self._readlink = None

            return self._readlink

    def __len__(self):
        if self.is_dir:
            return self.num_links

        if self.is_file:
            return self.size

        return 0

    def __hash__(self):
        return hash((self.device, self.inode))

    def __eq__(self, other):
        return (self.device, self.inode) == (other.device, other.inode)

    @property
    def mode(self):
        return self.exists and self.stat.st_mode

    @property
    def inode(self):
        return self.exists and self.stat.st_ino

    @property
    def device(self):
        return self.exists and self.stat.st_dev

    @property
    def num_links(self):
        return self.exists and self.stat.st_nlink

    @property
    def uid(self):
        return self.exists and self.stat.st_uid

    @property
    def gid(self):
        return self.exists and self.stat.st_gid

    @property
    def size(self):
        return self.exists and self.stat.st_size

    @property
    def atime(self):
        return self.exists and local_timestamp(self.stat.st_atime)

    @property
    def mtime(self):
        return self.exists and local_timestamp(self.stat.st_mtime)

    @property
    def ctime(self):
        return self.exists and local_timestamp(self.stat.st_ctime)
