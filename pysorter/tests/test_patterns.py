from __future__ import print_function
import os

import pytest

from . import helper
from ..core import pysorter
from .. import action


@helper.tempdir
def test_keyword_captures(d):
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{keyword}/{name}.{ext}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'cruel/',
        'cruel/hello.pdf']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_numerical_captures(d):
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
                'music/awesome/song.mp3']
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_bad_keyword_captures(d):
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{unknown}/{keyword}/{name}.{ext}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    with pytest.raises(ValueError):
        pysorter.main(args)


@helper.tempdir
def test_bad_numerical_capture(d):
    filetypes = {
        '(?P<name>\w+)_(?P<keyword>\w+)\.(?P<ext>pdf)$': '{keyword}/{name}.{ext}/{4}'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    with pytest.raises(ValueError):
        pysorter.main(args)


@helper.tempdir
def test_callable_as_action(d):
    def comparison_function(match, entity):
        return 'foobar/'

    filetypes = {
        '\.pdf$': comparison_function
    }

    to_sort = 'files/'
    dest = 'sorted/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '-d', dest]

    pysorter.main(args)
    # --- compare sorted
    expected = [
        'foobar/',
        'foobar/hello_cruel.pdf']
    pysorter.main(args)
    d.compare(expected=expected, path=dest)


@helper.tempdir
def test_rule_behaviour_into_directory_for_file(d):
    filetypes = {
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/hello_cruel.pdf']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_rule_behaviour_to_for_file(d):
    filetypes = {
        '.*\.pdf$': 'pdf'
    }

    to_sort = 'files/'

    to_make = ['hello_cruel.pdf']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']

    # --- compare sorted
    expected = [
        'pdf']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_rule_behaviour_into_directory_for_dir(d):
    filetypes = {
        'foo/$': 'pdf/'
    }

    to_sort = 'files/'

    to_make = ['foo/']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/foo/']
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_rule_behaviour_to_for_dir(d):
    filetypes = {
        'foo/$': 'pdf'
    }

    to_sort = 'files/'

    to_make = ['foo/']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py', '--process-dirs']

    # --- compare sorted
    expected = [
        'pdf/'
    ]
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_skip_pattern_file(d):
    filetypes = {
        '\.xml$': action.Skip,
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'
    to_make = ['hello_cruel.pdf', 'config.xml']
    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

    args = [to_sort, '-t', 'filetypes.py']
    # --- compare sorted
    expected = [
        'pdf/',
        'pdf/hello_cruel.pdf',
        'config.xml'
    ]
    pysorter.main(args)
    d.compare(expected=expected, path=to_sort)


@helper.tempdir
def test_skip_recurse_directory(d):
    filetypes = {
        'foo/$': action.SkipRecurse,
        '\.pdf$': 'pdf/'
    }

    to_sort = 'files/'
    to_make = [('foo', ['docfoo.pdf']), ('bar', ['docbar.pdf'])]

    helper.initialize_dir(d, filetypes, helper.build_path_tree(to_make, to_sort))

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
    d.compare(expected=expected, path=to_sort)
