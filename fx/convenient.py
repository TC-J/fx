from typing import Any, AnyStr


def fexists(fpath: AnyStr) -> bool:
    """
    -
    returns true if fpath exists and is a
    file.
    """
    import os

    return os.path.exists(fpath) and os.path.isfile(fpath)


def dexists(dpath: AnyStr) -> bool:
    """
    -
    returns true if dpath exists and is a
    directory.
    """
    import os

    return os.path.exists(dpath) and os.path.isdir(dpath)


def touch(path):
    """
    -
    create an empty file.
    """
    import os

    if not os.path.exists(path):
        open(path, "w").close()


# FIXME: remove links as well
def rm(path):
    """
    -
    remove file or directory.
    """
    import os
    import shutil

    if fexists(path):
        os.remove(path)
    elif dexists(path):
        shutil.rmtree(path)


def cut(fpath, __slice: slice):
    """
    -
    cut data from file.
    """
    data = []
    prev = []

    # read the target file
    with open(fpath) as fh:
        prev = fh.readlines()

    data = prev[__slice]

    # overwrite the file without the specified
    # sliced lines.
    with open(fpath, "w") as fh:
        for i, line in enumerate(prev):
            if i >= __slice.start and i < __slice.stop:
                continue
            fh.write(line)

        fh.truncate()

        fh.flush()

    return data
