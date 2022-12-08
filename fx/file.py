import os


def touch(path):
    """
    -
    create an empty file.
    """
    if not os.path.exists(path):
        open(path, "w").close()


class file:
    """
    -
    load and operate on files.
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

    def insert(self, key, value):
        """
        -
        insert at the index via the key.
        """
        lines = len(self)

        if key >= lines:
            self.linefill(key - lines)

        for i in range(lines, key, -1):
            self[i] = self[i - 1]

        self[key] = value

    def __lshift__(self, rhs):
        self.append(rhs)

    def __or__(self, rhs):
        for l in rhs:
            self << l
