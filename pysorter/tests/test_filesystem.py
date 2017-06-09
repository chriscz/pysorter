from __future__ import print_function

import pytest

from .. import filesystem

def test_move_nondirectory(tempdir):
    tempdir.write('afile', 'some data', 'utf-8')
    with pytest.raises(OSError) as excinfo:
        filesystem.move_dir('afile', 'afile2')
    assert 'not a directory' in str(excinfo.value)

def test_move_nonfile(tempdir):
    tempdir.makedir('adir')
    with pytest.raises(OSError) as excinfo:
        filesystem.move_file('adir', 'adir2')
    assert 'not a file' in str(excinfo.value)


def test_makepath_file(tempdir):
    tempdir.write('afile', 'some data', 'utf-8')

    with pytest.raises(OSError) as excinfo:
        filesystem.make_path('afile')
    assert 'not a directory' in str(excinfo.value)

def test_paths_to_tree_bad():
    with pytest.raises(ValueError):
        filesystem.paths_to_tree(['hello/world', 'hello/world/afile'])
