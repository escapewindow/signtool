import os
import pytest
import subprocess

import signtool.util.archives as archives

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_bzip2(tmpdir):
    fn = "%s/foo" % tmpdir
    open(fn, "w").write("hello")
    archives.bzip2(fn)
    proc = subprocess.Popen(["bzcat", fn], stdout=subprocess.PIPE)
    assert b"hello" == proc.stdout.read()

    archives.bunzip2(fn)
    assert b"hello" == open(fn, 'rb').read()


def test_tar(tmpdir):
    tmpdir_path = str(tmpdir)
    with pytest.raises(Exception):
        archives.unpacktar(__file__, tmpdir_path)
    archives.unpacktar(
        os.path.join(DATA_DIR, "dirtree.tgz"),
        tmpdir_path
    )
    assert os.path.exists(os.path.join(tmpdir_path, "dir2", "foobar"))
    new_tarball = os.path.join(tmpdir_path, "x.tgz")
    archives.packtar(new_tarball, ["dir1_a/file1_a.tar.gz"], os.path.join(tmpdir_path, "dir1"))
    proc = subprocess.Popen(["tar", '-tzf', new_tarball], stdout=subprocess.PIPE)
    assert b"dir1_a/file1_a.tar.gz" == proc.stdout.read().rstrip()
