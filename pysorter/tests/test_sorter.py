from __future__ import print_function
import os

import pytest

from . import helper
from testfixtures import TempDirectory, tempdir

from ..core import pysorter


def test_noargs():
    """
    test the script when no other arguments than the directory to sort and
    the filetypes.py file are specified

    >>> assert False
    """
    with TempDirectory() as d:
        os.chdir(d.path)
        filetypes = {
            '.*\\.pdf$': 'docs/'
        }

        to_sort = 'source/'

        to_make = ['file.pdf']

        helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

        args = [to_sort, '--filetypes', 'filetypes.py']
        pysorter.main(args)

        # --- compare sorted
        expected = ['docs/',
                    'docs/file.pdf',
                    'other/',
                    'directories/']

        d.compare(expected=expected, path=to_sort)


def test_captures_1():
    with TempDirectory() as d:
        os.chdir(d.path)
        filetypes = {
            '.*\\.pdf$': 'docs/',
            '([^_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
        }

        to_sort = 'source/'

        to_make = ['file.pdf',
                   'awesome_song.mp3']

        helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

        args = [to_sort, '--filetypes', 'filetypes.py']
        pysorter.main(args)

        # --- compare sorted
        expected = ['docs/',
                    'docs/file.pdf',
                    'music/',
                    'music/awesome/',
                    'music/awesome/song.mp3',
                    'other/',
                    'directories/']
        d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_non_existing_directory(d):
    os.chdir(d.path)
    args = ['tosort']
    pysorter.main(args)


@helper.tempdir
def test_file_as_directory(d):
    with pytest.raises(OSError):
        os.chdir(d.path)
        d.write('file', b'')
        args = ['file']
        pysorter.main(args)


@helper.tempdir
def test_recursive_sort(d):
    os.chdir(d.path)
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^/_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['nested/even/deeper/file.pdf',
               'awesome_song.mp3',
               'foo/another_song.mp3', ]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-r', '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = ['foo/',
                'nested/',
                'nested/even/',
                'nested/even/deeper/',
                'docs/',
                'docs/file.pdf',
                'music/',
                'music/awesome/',
                'music/awesome/song.mp3',
                'music/another/',
                'music/another/song.mp3',
                'other/',
                'directories/']
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_recursive_sort_with_directory_processing(d):
    os.chdir(d.path)
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^/_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['nested/even/deeper/file.pdf',
               'awesome_song.mp3',
               'foo/another_song.mp3', ]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-r', '--filetypes', 'filetypes.py', '--process-dirs']
    pysorter.main(args)

    # --- compare sorted
    expected = ['foo/',
                'nested/',
                'nested/even/',
                'nested/even/deeper/',
                'docs/',
                'docs/file.pdf',
                'music/',
                'music/awesome/',
                'music/awesome/song.mp3',
                'music/another/',
                'music/another/song.mp3',
                'other/',
                'directories/']
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_clean_empty(d):
    os.chdir(d.path)
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^/_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['nested/even/deeper/file.pdf',
               'awesome_song.mp3',
               'foo/another_song.mp3', ]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-r', '-c', '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = ['docs/',
                'docs/file.pdf',
                'music/',
                'music/awesome/',
                'music/awesome/song.mp3',
                'music/another/',
                'music/another/song.mp3']
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_other_files(d):
    os.chdir(d.path)
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'files'

    to_make = ['300.mp4', ]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = [
        'directories/',
        'other/',
        'other/mp4_files/',
        'other/mp4_files/300.mp4'
    ]
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_duplicate(d):
    os.chdir(d.path)
    filetypes = {
    }

    to_sort = 's'

    to_make = ['s/300.mp4', 's/movie/300.mp4', ]

    helper.initialize_dir(d, filetypes, to_make)

    args = [to_sort, '-r', '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = [
        'directories/',
        'movie/',
        'movie/300.mp4',
        'other/',
        'other/mp4_files/',
        'other/mp4_files/300.mp4'
    ]
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_no_extension(d):
    os.chdir(d.path)
    filetypes = {
    }

    to_sort = 'files/'

    to_make = ['no_extension', ]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-r', '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = [
        'directories/',
        'other/',
        'other/no_extension'
    ]
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_no_recurse_dir(d):
    os.chdir(d.path)
    filetypes = {}

    to_sort = 'files/'

    to_make = [('movies',
                ['1.mp4', 'deep/2.mp4', '3.mp4']),
               'emptydir/'
               ]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py', '--process-dirs']
    pysorter.main(args)

    # --- compare sorted
    expected = [
                   'directories/',
                   'other/',
               ] + helper.build_path_tree(to_make, 'directories/')
    d.compare(expected=expected, path=to_sort)

def test_print_version(capsys):
    try:
        pysorter.main(['--version'])
        assert False, 'did not print out version.'
    except SystemExit:
        out, err = capsys.readouterr()
        from .. import __version__ 
        
        # Python 3.4 & 3.5 print out the version on  stdout instead
        # of stderr.
        try:
            assert err.strip() == __version__
        except AssertionError:
            assert out.strip() == __version__


@helper.tempdir
def test_write_unknown_types_correct(d):
    os.chdir(d.path)
    filetypes = {
        r'\.pdf$': 'docs/'
    }

    unknown = 'unknown.txt'
    to_sort = 'files/'

    u_files = ['movie.mp4', 'kerry.mp3', 'phantom.mp3']
    to_make = ['thesis.pdf'] + u_files

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    # --- compare sorted
    args = [to_sort, '-u', unknown, '--filetypes', 'filetypes.py']
    pysorter.main(args)

    data = set(_ for _ in d.read(unknown, encoding="utf8").split('\n') if _)

    u_exts = (os.path.splitext(_)[1] for _ in u_files if _[1])
    u_exts = set(_[1:] for _ in u_exts)


    assert len(data) == len(u_exts) and not data.difference(u_exts)
