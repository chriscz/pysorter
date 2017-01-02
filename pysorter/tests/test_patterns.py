from __future__ import print_function
import os

import pytest

from . import helper
from ..core import pysorter
from .. import action



def test_keyword_captures(tempdir):
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{keyword}/{name}.{ext}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'cruel/',
        'cruel/hello.pdf']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_numerical_captures(tempdir):
    filetypes = {
        '.*\\.pdf$': 'docs/',
        '([^_]*)_([^_]*)\\.(mp3)$': 'music/{1}/{2}.{3}'
    }

    to_sort = 'source/'

    to_make = ['file.pdf',
               'awesome_song.mp3']

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '--filetypes', 'filetypes.py']
    pysorter.main(args)

    # --- compare sorted
    expected = ['docs/',
                'docs/file.pdf',
                'music/',
                'music/awesome/',
                'music/awesome/song.mp3']
    tempdir.compare(expected=expected, path=to_sort)



def test_bad_keyword_captures(tempdir):
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{unknown}/{keyword}/{name}.{ext}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    with pytest.raises(ValueError):
        pysorter.main(args)



def test_bad_numerical_capture(tempdir):
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{keyword}/{name}.{ext}/{4}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    with pytest.raises(ValueError):
        pysorter.main(args)



def test_callable_as_action(tempdir):
    def comparison_function(match, entity):
        return 'foobar/'

    filetypes = {
        '\.pdf$': comparison_function
    }

    to_sort = 'files/'
    dest = 'sorted/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '-d', dest]

    pysorter.main(args)
    # --- compare sorted
    expected = [
        'foobar/',
        'foobar/hello_cruel.pdf']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=dest)



def test_rule_behaviour_into_directory_for_file(tempdir):
    filetypes = {
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/hello_cruel.pdf']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_rule_behaviour_to_for_file(tempdir):
    filetypes = {
        '.*\.pdf$': 'pdf'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'pdf']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_rule_behaviour_into_directory_for_dir(tempdir):
    filetypes = {
        'foo/$': 'pdf/'
    }

    to_sort = 'files/'

    to_make = ['foo/']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/foo/']
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_rule_behaviour_to_for_dir(tempdir):
    filetypes = {
        'foo/$': 'pdf'
    }

    to_sort = 'files/'

    to_make = ['foo/']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    expected = [
        'pdf/'
    ]
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_skip_pattern_file(tempdir):
    filetypes = {
        '\.xml$': action.Skip,
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'
    to_make = ['hello_cruel.pdf', 'config.xml']
    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']
    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/hello_cruel.pdf',
        'config.xml'
    ]
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)



def test_skip_recurse_directory(tempdir):
    filetypes = {
        'foo/$': action.SkipRecurse,
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'
    to_make = [('foo', ['docfoo.pdf']), ('bar', ['docbar.pdf'])]

    helper.initialize_dir(tempdir, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-r', '-p', '-t', 'filetypes.py']
    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/docbar.pdf',
        'bar/',
        'foo/',
        'foo/docfoo.pdf'
    ]
    pysorter.main(args)
    tempdir.compare(expected=expected, path=to_sort)
