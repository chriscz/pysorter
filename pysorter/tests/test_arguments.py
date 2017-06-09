from __future__ import print_function

import pytest

from . import helper
from .. import commandline


def test_bad_filetypes_file(tempdir):
    filetypes = {}

    to_sort = 'files/'

    to_make = []
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes']

    with pytest.raises(OSError):
        commandline.main(args)


def test_unknown_filetypes_created(tempdir):
    filetypes = {}

    to_sort = 'files/'

    to_make = ['']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-u', 'unknown_files', '-t', 'filetypes.py']

    expected = helper.build_path_tree([''], to_sort)
    expected += ['unknown_files', 'filetypes.py']

    commandline.main(args)
    tempdir.compare(expected=expected)


def test_crash_on_nonexistent_source(tempdir):
    with pytest.raises(OSError):
        args = ['tosort']
        commandline.main(args)


def test_file_as_directory(tempdir):
    with pytest.raises(OSError):
        tempdir.write('file', b'')
        args = ['file']
        commandline.main(args)
