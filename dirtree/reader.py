class Reader:
    def __init__(self, stream, sep=None, buf_size=1024 * 4):
        self.stream = stream
        self.sep = sep
        self.buf_size = buf_size

        self.__buffer = None
        self.__eof = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__buffer:
            self.__read_block()

        if not self.__buffer and self.__eof:
            raise StopIteration

        if not self.sep:
            for blk in (b'\x00', b'\r\n', b'\r', b'\n', '\r\n', '\r', '\n'):
                try:
                    idx = self.__buffer.index(blk)
                except (ValueError, TypeError):
                    pass
                else:
                    self.sep = blk
                    break
            else:
                return self.__advance()

        if self.sep not in self.__buffer:
            return self.__advance()

        idx = self.__buffer.index(self.sep)
        value, self.__buffer = self.__buffer[:idx], self.__buffer[idx + 1:]

        if not value:
            return self.__advance()

        return value

    def __advance(self):
        if self.__eof:
            buf, self.__buffer = self.__buffer, None
            return buf

        self.__read_block()
        return next(self)

    def __read_block(self):
        if self.__eof:
            return

        block = self.stream.read(self.buf_size)

        if block is None:
            # stream isn't ready, try again
            return

        if self.__buffer is None:
            self.__buffer = type(block)()

        self.__buffer = self.__buffer + block

        if not block:
            self.__eof = True
