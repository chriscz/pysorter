from __future__ import print_function
import os

from . import helper
from ..core import pysorter


def test_sort_only_filetypes_arg(tempdir):
    filetypes = {
        '.*\\.pdf$': 'docs/'
    }

    to_sort = 'source/'

    to_make = ['file.pdf']

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = ['docs/',
                'docs/file.pdf']

    tempdir.compare(expected=expected, path=to_sort)


def test_recursive_sort(tempdir):
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^/_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['nested/even/deeper/file.pdf',
               'awesome_song.mp3',
               'foo/another_song.mp3', ]

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

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
    tempdir.compare(expected=expected, path=to_sort)


def test_recursive_sort_with_directory_processing(tempdir):
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^/_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['nested/even/deeper/file.pdf',
               'awesome_song.mp3',
               'foo/another_song.mp3', ]

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

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
    tempdir.compare(expected=expected, path=to_sort)


def test_clean_empty(tempdir):
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^/_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['nested/even/deeper/file.pdf',
               'awesome_song.mp3',
               'foo/another_song.mp3', ]

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

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
    tempdir.compare(expected=expected, path=to_sort)


def test_duplicate_recursive(tempdir):
    filetypes = {
        '\.mp4$': 'mp4_files/'
    }

    to_sort = 's'

    to_make = ['s/300.mp4', 's/movie/300.mp4', ]

    helper.initialize_dir(tempdir, filetypes, to_make)

    args = [to_sort, '-r', '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = [
        'movie/',
        'movie/300.mp4',
        'mp4_files/',
        'mp4_files/300.mp4'
    ]
    tempdir.compare(expected=expected, path=to_sort)


def test_process_dirs_no_rules(tempdir):
    filetypes = {}

    to_sort = 'files/'

    to_make = [('movies',
                ['1.mp4', 'deep/2.mp4', '3.mp4']),
               'emptydir/'
               ]

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py', '--process-dirs']
    pysorter.main(args)

    # --- compare sorted
    expected = [] + helper.build_path_tree(to_make)
    tempdir.compare(expected=expected, path=to_sort)


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


def test_write_unknown_types_correct(tempdir):
    filetypes = {
        r'\.pdf$': 'docs/'
    }

    unknown = 'unknown.txt'
    to_sort = 'files/'

    u_files = ['movie.mp4', 'kerry.mp3', 'phantom.mp3', ('direct', ['a.pdf'])]
    to_make = ['thesis.pdf'] + u_files

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    # --- compare sorted
    args = [to_sort, '-u', unknown, '--filetypes', 'filetypes.py']
    pysorter.main(args)

    data = set(_ for _ in tempdir.read(unknown, encoding="utf8").split('\n') if _)

    unhandled = {'movie.mp4', 'kerry.mp3', 'phantom.mp3', 'direct/a.pdf', 'direct/'}
    assert not data.difference(unhandled)


def test_absolute_path(tempdir):
    filetypes = {
        r'.*': tempdir.path + '/files/docs/'
    }

    to_sort = 'files/'

    to_make = ['movie.mp4', 'kerry.mp3', 'phantom.mp3', ('direct', ['a.pdf'])]

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py', '--process-dirs']
    pysorter.main(args)

    # --- compare sorted
    expected = helper.build_path_tree(to_make, 'docs/') + ['docs/']
    tempdir.compare(expected=expected, path=to_sort)


def test_dry_run_has_no_effect(tempdir):
    filetypes = {
        r'\.pdf$': 'docs/',
        r'\.doc$': 'word/',
    }

    src_dir = 'src/'
    dst_dir = 'dst/'

    to_make = ['story.pdf',
               'subdirectory/news.pdf',
               'an/empty/dir/',
               'another/',
               'dir/story.pdf']

    src_tree = helper.build_path_tree(to_make, src_dir)
    root_tree = src_tree + [dst_dir, 'filetypes.py', src_dir]

    helper.initialize_dir(tempdir, filetypes, src_tree)
    tempdir.makedir(dst_dir)

    args = [os.path.join(tempdir.path, src_dir), '-nrc', '-d', dst_dir, '-t', 'filetypes.py']

    pysorter.main(args)
    tempdir.compare(expected=root_tree, path='.')

    # --- strip the common prefix from all the move (src, dst) pairs
    move_pairs = set()
    common = len(tempdir.path) + 1  # for the seperator
    for (src, dst) in pysorter._last_sorter.dry_mv_tuples:
        move_pairs.add((src[common:], dst[common:]))

    rmdir_paths = set()
    for path in pysorter._last_sorter.dry_rmdir:
        rmdir_paths.add(path[common:])

    assert len(move_pairs) == 2
    assert ('src/story.pdf', 'dst/docs/story.pdf') in move_pairs
    assert ('src/subdirectory/news.pdf', 'dst/docs/news.pdf') in move_pairs

    assert 'src/subdirectory' in rmdir_paths
    assert 'src/an/empty/dir' in rmdir_paths
    assert 'src/an/empty' in rmdir_paths
    assert 'src/an' in rmdir_paths
    assert 'src/another'in rmdir_paths
    assert len(rmdir_paths) == 5



def test_dry_run_with_directory_move(tempdir):
    filetypes = {
        r'\.pdf$': 'docs/',
        r'\.doc$': 'word/',
        r'r/$': 'directories/'
    }

    src_dir = 'src/'
    dst_dir = 'dst/'

    to_make = ['story.pdf',
               'subdirectory/news.pdf',
               'an/empty/dir/',
               'another/',
               'stories/deep/books/book.pdf']

    src_tree = helper.build_path_tree(to_make, src_dir)
    root_tree = src_tree + [dst_dir, 'filetypes.py', src_dir]

    helper.initialize_dir(tempdir, filetypes, src_tree)
    tempdir.makedir(dst_dir)

    args = [os.path.join(tempdir.path, src_dir), '-nrcp', '-d', dst_dir, '-t', 'filetypes.py']

    pysorter.main(args)
    tempdir.compare(expected=root_tree, path='.')

    # --- strip the common prefix from all the move (src, dst) pairs
    move_pairs = set()
    common = len(tempdir.path) + 1  # for the seperator
    for (src, dst) in pysorter._last_sorter.dry_mv_tuples:
        move_pairs.add((src[common:], dst[common:]))

    rmdir_paths = set()
    for path in pysorter._last_sorter.dry_rmdir:
        rmdir_paths.add(path[common:])

    assert len(move_pairs) == 5
    assert ('src/stories/deep/books/book.pdf', 'dst/docs/book.pdf') in move_pairs
    assert ('src/story.pdf', 'dst/docs/story.pdf') in move_pairs
    assert ('src/subdirectory/news.pdf', 'dst/docs/news.pdf') in move_pairs
    assert ('src/an/empty/dir/', 'dst/directories/dir') in move_pairs
    assert ('src/another/', 'dst/directories/another') in move_pairs

    should_be_removed = [
        'src/subdirectory',
        'src/an',
        'src/an/empty',
        'src/stories',
        'src/stories/deep',
        'src/stories/deep/books',
    ]

    assert set(should_be_removed) == rmdir_paths

