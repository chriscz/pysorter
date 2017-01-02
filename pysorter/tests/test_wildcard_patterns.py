"""
Tests the three defined wildcard patterns in filetypes.py
"""

from . import helper
from ..core import pysorter
from ..filetypes import DIRECTORIES, FILES_WITHOUT_EXTENSION, FILES_WITH_EXTENSION



def test_directory_pattern(tempdir):
    filetypes = {
        DIRECTORIES[0]: DIRECTORIES[1]
    }

    to_sort = 'files/'

    to_make = ['foo/', 'bar/', 'nested/directory/', 'somefile']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    to_make.remove('somefile')
    expected = helper.build_path_tree(to_make, 'directories/')
    expected += ['directories/', 'somefile']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_file_extension_pattern(tempdir):
    filetypes = {
        FILES_WITH_EXTENSION[0]: FILES_WITH_EXTENSION[1]
    }

    to_sort = 'files/'

    to_make = ['movie.mp4', 'story.doc', 'archive.tar.gz', 'noextension', ('adirectory', ['secret.txt']),
               ('directory.with.dots', [''])]
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs', '-r']

    # --- compare sorted
    expected = ['other/', 'other/mp4_files/', 'other/doc_files/', 'other/gz_files/',
                'other/mp4_files/movie.mp4', 'other/doc_files/story.doc', 'other/gz_files/archive.tar.gz',
                'other/txt_files/','other/txt_files/secret.txt',
                'noextension', 'adirectory/', 'directory.with.dots/']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_file_no_extension_pattern(tempdir):
    filetypes = {
        FILES_WITHOUT_EXTENSION[0]: FILES_WITHOUT_EXTENSION[1]
    }

    to_sort = 'files/'

    to_make = ['movie', 'story', 'archive', 'noextension', 'nested/file']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs', '-r']

    # --- compare sorted
    expected = ['other/', 'other/story', 'other/archive', 'other/movie',
                'other/noextension', 'nested/', 'other/file']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)
