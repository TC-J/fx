import os

import difflib

from typing import *

from .convenient import *


class file:
    """
    -
        API
    append - append string
    appendf - append other file
    insert - insert string at line
    remove - remove file
    sync - flush file
    close - close file handle
    __add__ - append other file
    __lshift__ - append string
    __(get/set)item__ - array style access

    """

    def __init__(self, path, mode="rt+"):
        touch(path)

        self.mode = mode

        self.path = path

        self.handle = open(path, mode)

        self.buffer = self.handle.readlines()

        self.modified = False

    def __len__(self):
        return len(self.buffer)

    def __str__(self):
        return "".join(self.buffer)

    def __getitem__(self, key):
        return self.buffer[key]

    def __setitem__(self, key, value):
        lines = len(self.buffer)

        if (key + 1) >= lines:
            self.linefill(key - lines)

        if value[-1] != "\n":
            value += "\n"

        self.buffer[key] = value

    def __lshift__(self, rhs: str):
        """
        -
        this appends a string to the file.
        """
        return self.append(rhs)

    def __add__(self, rhs):
        return self.appendf(rhs)

    def linefill(self, count):
        """
        -
        this appends newlines to the
        end of the buffer. this is used
        to avoid index-out-of-range errors.
        """
        lines = len(self.buffer)

        total = lines + count

        while lines <= total:
            self.buffer.append("\n")

            lines += 1

        return self

    def sync(self):
        """
        -
        flush the inner-buffers. writes
        are often unseen by reads of the
        file until the file is closed.
        this function eliminates that concern.

        """
        self.handle.seek(0)

        self.handle.writelines(self.buffer)

        self.handle.truncate()

        self.handle.flush()

        return self

    def remove(self):
        """
        -
        remove the file from the operating
        system.
        """
        os.remove(self.path)

    def close(self):
        """
        -
        close the file for the program.
        """
        self.handle.close()

    def append(self, value):
        """
        -
        append to the end of the file.
        """
        if value[-1] != "\n":
            value += "\n"
        self.buffer.append(value)

        return self

    def __check_key(self, key) -> int:
        """
        -
        check the size of the key. if the
        internal buffer is not the right
        size, fill empty lines to accommodate.
        """
        lines = len(self)
        if key >= lines - 1:
            self.linefill(key - lines)
        return len(self)

    # TODO: array scooting
    def scoot(self, __range: range):
        """
        -
        scoots the elements. what that means
        precisely is TBA
        """
        pass

    def cut(self, region: slice) -> List[str]:
        """
        -
        cut removes & returns a slice
        of lines from the file.
        """
        return cut(self.path, region)

    def insert(self, key, value):
        """
        -
        insert at the index via the key.
        """
        lines = self.__check_key(key)
        for i in range(lines, key, -1):
            self[i] = self[i - 1]

        self[key] = value

        return self

    def appendf(self, rhs):
        """
        this appends the file on the right,
        to this file.
        """
        for l in rhs:
            self << l

        return self

    # TODO: file::__sub__ => file diff
    # TODO: file::__inv__ => SHA checksum
    # TODO: file::__mod__ => regex substitution line by line
