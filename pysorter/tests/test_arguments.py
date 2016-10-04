from __future__ import print_function

import os
import pytest

from . import helper
from ..core import pysorter


@helper.tempdir
def test_bad_filetypes_file(d):
    os.chdir(d.path)
    filetypes = {}

    to_sort = 'files/'

    to_make = []
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes']

    with pytest.raises(OSError):
        pysorter.main(args)


@helper.tempdir
def test_unknown_filetypes_created(d):
    filetypes = {}

    to_sort = 'files/'

    to_make = ['']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-u', 'unknown_files', '-t', 'filetypes.py']

    expected = helper.build_path_tree([''], to_sort)
    expected += ['unknown_files', 'filetypes.py']

    pysorter.main(args)
    d.compare(expected=expected)


@helper.tempdir
def test_crash_on_nonexistent_source(d):
    with pytest.raises(OSError):
        args = ['tosort']
        pysorter.main(args)


@helper.tempdir
def test_file_as_directory(d):
    with pytest.raises(OSError):
        d.write('file', b'')
        args = ['file']
        pysorter.main(args)
