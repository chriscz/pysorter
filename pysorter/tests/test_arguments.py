from __future__ import print_function

import os
import pytest

from . import helper
from ..core import pysorter


def test_bad_filetypes_file(tempdir):
    filetypes = {}

    to_sort = 'files/'

    to_make = []
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes']

    with pytest.raises(OSError):
        pysorter.main(args)


def test_unknown_filetypes_created(tempdir):
    filetypes = {}

    to_sort = 'files/'

    to_make = ['']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-u', 'unknown_files', '-t', 'filetypes.py']

    expected = helper.build_path_tree([''], to_sort)
    expected += ['unknown_files', 'filetypes.py']

    pysorter.main(args)
    tempdir.compare(expected=expected)


def test_crash_on_nonexistent_source(tempdir):
    with pytest.raises(OSError):
        args = ['tosort']
        pysorter.main(args)


def test_file_as_directory(tempdir):
    with pytest.raises(OSError):
        tempdir.write('file', b'')
        args = ['file']
        pysorter.main(args)
