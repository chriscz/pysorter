from __future__ import print_function
import os

import pytest

from . import helper
from testfixtures import TempDirectory, tempdir

from ..core import pysorter


@helper.tempdir
def test_sort_only_filetypes_arg(d):
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
                'docs/file.pdf']

    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_recursive_sort(d):
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
                'music/another/song.mp3']
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_recursive_sort_with_directory_processing(d):
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
                'music/another/song.mp3']
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_clean_empty(d):
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
def test_duplicate_recursive(d):
    filetypes = {
        '\.mp4$': 'mp4_files/'
    }

    to_sort = 's'

    to_make = ['s/300.mp4', 's/movie/300.mp4', ]

    helper.initialize_dir(d, filetypes, to_make)

    args = [to_sort, '-r', '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = [
        'movie/',
        'movie/300.mp4',
        'mp4_files/',
        'mp4_files/300.mp4'
    ]
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_process_dirs_no_rules(d):
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
    expected = [] + helper.build_path_tree(to_make)
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
    filetypes = {
        r'\.pdf$': 'docs/'
    }

    unknown = 'unknown.txt'
    to_sort = 'files/'

    u_files = ['movie.mp4', 'kerry.mp3', 'phantom.mp3', ('direct', ['a.pdf'])]
    to_make = ['thesis.pdf'] + u_files

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    # --- compare sorted
    args = [to_sort, '-u', unknown, '--filetypes', 'filetypes.py']
    pysorter.main(args)

    data = set(_ for _ in d.read(unknown, encoding="utf8").split('\n') if _)

    unhandled = {'movie.mp4', 'kerry.mp3', 'phantom.mp3', 'direct/a.pdf', 'direct/'}
    assert not data.difference(unhandled)


@helper.tempdir
def test_absolute_path(d):
    filetypes = {
        r'.*': d.path + '/files/docs/'
    }

    to_sort = 'files/'

    to_make = ['movie.mp4', 'kerry.mp3', 'phantom.mp3', ('direct', ['a.pdf'])]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py', '--process-dirs']
    pysorter.main(args)

    # --- compare sorted
    expected = helper.build_path_tree(to_make, 'docs/') + ['docs/']
    d.compare(expected=expected, path=to_sort)
