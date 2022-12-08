from fx.file import file
import os


def example_file(name, content):
    with open(name, mode="w") as fh:
        fh.write(content)


def test_file_create_and_delete():
    fname = "a.txt"

    assert not os.path.exists(fname)

    f = file(fname)
    assert os.path.exists(fname)

    f.close()
    assert f.handle.closed

    f.remove()
    assert not os.path.exists(fname)


def test_file_read():
    example_file("b.txt", "abc\ndef\nghi")
    f = file("b.txt")
    assert str(f) == "abc\ndef\nghi"
    os.remove("b.txt")


def test_file_write():
    f = file("c.txt", "wt+")
    f[0] = "1"
    f[9] = "10"
    f[99] = "100"
    f[999] = "1000"
    f.sync()

    with open("c.txt", "rt+") as fh:
        data = fh.readlines()
        for i in range(0, 1000):
            if i == 0:
                assert f[0] == data[i]
            elif i == 9:
                assert f[9] == data[i]
            elif i == 99:
                assert f[99] == data[i]
            elif i == 999:
                assert f[999] == data[i]
            else:
                assert data[i] == "\n"

    f.remove()


def test_file_append():
    example_file("a.txt", "abc\n")

    f = file("a.txt")

    f.append("def")

    f.append("ghi")

    f.sync()

    with open("a.txt") as fh:
        data = fh.read()

        assert data[0:4] == "abc\n"

        assert data[4:8] == "def\n"

        assert data[8:12] == "ghi\n"

    f.close()

    f.remove()


def test_file_insert():
    example_file("a.txt", "a=00\nb=01\nd=03")

    f = file("a.txt")

    f.insert(2, "c=02")

    f.sync()

    with open("a.txt") as fh:
        data = fh.readlines()

        assert data[0] == "a=00\n"

        assert data[1] == "b=01\n"

        assert data[2] == "c=02\n"

        assert data[3] == "d=03\n"

    f.close()

    f.remove()


def test_file_lshift_ops():
    f = file("a.txt")

    f << "a"

    f << "b"

    f.sync()

    assert f[0] == "a\n"

    assert f[1] == "b\n"

    f.close()

    f.remove()


def test_file_or_ops():
    f0 = file("a.txt")
    f0 << "a"
    f0 << "b"

    f1 = file("b.txt")
    f1 << "c"
    f1 << "d"

    f0 | f1

    assert f0[2] == f1[0]

    assert f0[3] == f1[1]
