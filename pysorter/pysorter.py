#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The main implementation for calling pysorter from the commandline"""

from __future__ import print_function
import os
import sys
import util
import argparse
import logging

from sorter import PySorter
from rules import RegexSortRule

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
        args.filetypes = os.path.join(util.script_directory(), 'filetypes.txt')

    if not os.path.exists(args.filetypes):
        print("Invalid Filetypes file, please specify an existing file")
        sys.exit(2)
    if not os.path.exists(args.directory):
        print("Invalid Directory, please specify an existing directory")
        sys.exit(3)


def parse(args):
    """
        Checks the validity of the given arguments
        Adjusts the given argumentparser and returns a dictionarry of
        arguments that should be passed to pySorter
    """
    # replace filetypes path with full path
    if args.filetypes:
        args.filetypes = os.path.abspath(args.filetypes)
    else:
        args.filetypes = os.path.join(util.script_directory(), "filetypes.txt")

    if args.unknown_filetypes:
        args.unknown_filetypes = os.path.abspath(args.unknown_filetypes)

    if args.all_dirs and not args.recursive:
        log.warn("--all-dirs has no effect without --recursive")

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

    parser.add_argument('-t', '--filetypes',
                        help='File containing file types [Default: filetypes.txt]',
                        default=None)

    parser.add_argument('-m', '--move_dir-directories-to',
                        help='Move directories here [Default: Directories/]',
                        dest="directories_dest")

    parser.add_argument('-o', '--other-files',
                        help='Move files of unknown type here [Default: Other/]')

    parser.add_argument('-u', '--unknown-filetypes',
                        help='Write unknown filetypes to this file', )

    parser.add_argument('-r', '--recursive',
                        help='Recursively organize directories',
                        action='store_true')

    parser.add_argument('-c', '--clean-empty',
                        help='Recursively removes all empty directories',
                        action='store_true',
                        dest='clean_empty_dirs')

    parser.add_argument('-a', '--all-dirs',
                        help='Will enter special directories during recursive organize, must be specified'
                             'in conjunction with --recursive to work [Default: Disabled]',
                        action='store_true')

    parser.add_argument('-l', '--log-moves', help='Write all file moves to a file',
                        action='store_true')

    return parser.parse_args(args)


def main(args=None):
    logging.basicConfig()
    args = parse_args(args or sys.argv)
    validate_arguments(args)

    rules = RegexSortRule.load_from(args.filetypes)

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
