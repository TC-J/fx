from fx.convenient import *

import os


def test_cut():
    rm("a.txt")

    # dummy data
    with open("a.txt", "w") as fh:
        fh.write("a\nb\nc\n")

    # cut operation
    data = cut("a.txt", slice(1, 2))

    # extracted the correct item
    assert data == ["b\n"]

    # ensure the lines were removed
    with open("a.txt") as fh:
        assert fh.read() == "a\nc\n"
