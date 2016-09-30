#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The main implementation for calling pysorter from the commandline"""

from __future__ import print_function

import argparse
import logging
import os
import sys

from . import util
from .sorter import PySorter

from ..rules import DefaultSortRule

log = logging.getLogger(__name__)


def validate_arguments(args):
    """
        Checks whether the paths and options
        provided as commandline arguments are valid.
        The application exits if they are not.
    """
    if args.filetypes:
        args.filetypes = os.path.abspath(args.filetypes)
    else:
        args.filetypes = os.path.join(util.script_directory(), 'filetypes.py')

    if not os.path.isfile(args.filetypes):
        raise OSError("Filetypes is not a file or does not exist: {}".format(args.filetypes))

    if args.unknown_filetypes:
        args.unknown_filetypes = os.path.abspath(args.unknown_filetypes)

    return args


def parse_args(args=None):
    """Create an argument parser"""
    parser = argparse.ArgumentParser(description='Sort Files in a directory according to their file type')

    parser.add_argument('directory',
                        help='The directory to be organized')

    parser.add_argument('-d', '--destination',
                        help='The (root) destination directory to move_dir the organized files to',
                        dest='dest_dir',
                        default=None)

    parser.add_argument('-p', '--process-dirs',
                        help='Should directories be included in the files that are to be sorted',
                        action='store_true',
                        dest="do_process_dirs")

    parser.add_argument('-t', '--filetypes',
                        help='File containing file types [Default: filetypes.py]',
                        default=None)

    parser.add_argument('-m', '--move-dirs-to',
                        help='Move unprocessed directories here [Default: directories/]',
                        dest="directories_dest")

    parser.add_argument('-o', '--other-files',
                        help='Move unprocessed files here [Default: other/]')

    parser.add_argument('-u', '--unknown-filetypes',
                        help='Write unknown filetypes to this file', )

    parser.add_argument('-r', '--recursive',
                        help='Recursively organize directories',
                        action='store_true',
                        dest="do_recurse")

    parser.add_argument('-c', '--remove-empty-dirs',
                        help='Recursively removes all empty directories',
                        action='store_true',
                        dest='do_remove_empty_dirs')

    return validate_arguments(parser.parse_args(args))


def main(args=None):
    logging.basicConfig()
    args = parse_args(args)

    rules = DefaultSortRule.load_from(args.filetypes)

    topass = dict(vars(args))

    # --- remove processed arguments
    del topass['directory']
    del topass['filetypes']
    del topass['unknown_filetypes']

    sorter = PySorter(args.directory, rules, **topass)
    sorter.organize()

    # write out all the unknown file types
    if args.unknown_filetypes:
        util.write_unknown(sorter.unknown_types, args.unknown_filetypes)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # sys.argv = ['pySorter.py', '/tmp/test/','-t', '/home/chris/Development/soft_dev/pySorter/pysorter/filetypes.txt', '-r', '-c']
    main()
