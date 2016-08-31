import os
import helper
from testfixtures import TempDirectory
from pysorter import pysorter


def initialize_dir(d, filetypes, paths_to_make, paths_prefix=None):
    """

    Parameters
    ----------
    filetypes: dict
        mapping of strings to strings for filetypes

    paths_prefix: str or None
        prefix that will be joined to each file-path in `paths_to_make`

    paths_to_make: list
        list of string tuples (path, type)
        where type is either 'f' or 'd'

    """
    # --- create a mapping file
    d.write('filetypes.txt', helper.mkfiletypesstr(filetypes))

    root = d.path

    if paths_prefix:
        if os.path.isabs(paths_prefix):
            raise ValueError("Paths must be relative: {}".format(paths_prefix))
        root = os.path.join(root, paths_prefix)

    d.makedir(root)

    # --- create temp files
    for path, ftype in paths_to_make:
        if os.path.isabs(path):
            raise ValueError("Paths must be relative: {}".format(path))

        path = os.path.join(root, path)
        if ftype == 'f':
            d.write(path, '')
        elif ftype == 'd':
            d.makedir(path)
        else:
            raise ValueError("Invalid Type: {}".format(ftype))


def test_noargs():
    with TempDirectory() as d:
        os.chdir(d.path)
        filetypes = {
            '.*\\.pdf$': 'docs/'
        }

        to_sort = 'source'
        to_sort_fp = os.path.join(d.path, to_sort)

        to_make = [('file.pdf', 'f')]

        initialize_dir(d, filetypes, to_make, paths_prefix=to_sort)

        args = [to_sort_fp, '--filetypes', 'filetypes.txt']
        pysorter.main(args)

        # --- compare sorted
        expected = ['docs/', 'docs/file.pdf', 'other/', 'directories/']
        expected.sort()
        d.compare(expected=expected, path=to_sort_fp)


def test_captures_1():
    with TempDirectory() as d:
        os.chdir(d.path)
        filetypes = {
            '.*\\.pdf$': 'docs/',
            '([^_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
        }

        to_sort = 'source'
        to_sort_fp = os.path.join(d.path, to_sort)

        to_make = [('file.pdf', 'f'),
                   ('awesome_song.mp3', 'f')]

        initialize_dir(d, filetypes, to_make, paths_prefix=to_sort)

        args = [to_sort_fp, '--filetypes', 'filetypes.txt']
        pysorter.main(args)

        # --- compare sorted
        expected = ['docs/', 'docs/file.pdf', 'music/', 'music/awesome/', 'music/awesome/song.mp3', 'other/',
                    'directories/']
        expected.sort()
        d.compare(expected=expected, path=to_sort_fp)


if __name__ == '__main__':
    # test_noargs()
    pass
