import os

from testfixtures import TempDirectory, tempdir

from helper import initialize_dir

import helper
from pysorter.core import pysorter

import pytest


@tempdir()
def test_bad_filetypes(d):
    os.chdir(d.path)
    filetypes = {}

    to_sort = 'files/'

    to_make = []
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes']

    with pytest.raises(OSError):
        pysorter.main(args)


@tempdir()
def test_unknown_filetypes_created(d):
    os.chdir(d.path)
    filetypes = {}

    to_sort = 'files/'

    to_make = []
    initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-u', 'unknown_files']

    # --- compare sorted
    expected = helper.build_path_tree(['',
                                       'other/',
                                       'directories/'],
                                      to_sort) + \
               ['unknown_files',
                'filetypes.py']

    pysorter.main(args)
    d.compare(expected=expected)

if __name__ == '__main__':
    # test_noargs()
    pass
