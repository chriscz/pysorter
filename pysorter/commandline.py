#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The main implementation for calling pysorter from the commandline"""

from __future__ import print_function

import argparse
import logging
import os
import sys

from .oranize import Organizer

from .rules import RulesFileClassifier

log = logging.getLogger(__name__)

_last_sorter = None  # variable used during testing, set by main


def package_directory():
    """Return the absolute path to where pysorter is located"""
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))

def validate_arguments(args):
    """
        Checks whether the paths and options
        provided as commandline arguments are valid.
        The application exits if they are not.
    """
    if args.filetypes:
        args.filetypes = os.path.abspath(args.filetypes)
    else:
        args.filetypes = os.path.join(package_directory(), 'filetypes.py')

    if not os.path.isfile(args.filetypes):
        raise OSError("Filetypes is not a file or does not exist: {}".format(args.filetypes))

    if args.unhandled_file:
        args.unhandled_file = os.path.abspath(args.unhandled_file)

    return args


def parse_args(args=None):
    """Create an argument parser"""
    from . import __version__
    parser = argparse.ArgumentParser(description='Reorganizes files and directories according to certain rules')

    parser.add_argument('directory',
                        help='The directory to be organized')

    parser.add_argument('-d', '--destination',
                        help='The destination directory to move organized files to.',
                        dest='dest_dir',
                        default=None)

    parser.add_argument('-p', '--process-dirs',
                        help='Should directories also be matched against the rules?',
                        action='store_true',
                        dest='do_process_dirs')

    parser.add_argument('-t', '--filetypes',
                        help='File containing regex rules [Default: filetypes.py]',
                        default=None)

    parser.add_argument('-u', '--unhandled-file',
                        help='Write the paths of all unhandled items to this file',
                        dest='unhandled_file')

    parser.add_argument('-r', '--recursive',
                        help='Recursively organize directories',
                        action='store_true',
                        dest='do_recurse')

    parser.add_argument('-c', '--remove-empty-dirs',
                        help='Recursively removes all empty directories in the directory being organized.',
                        action='store_true',
                        dest='do_remove_empty_dirs')

    parser.add_argument('-n', '--dry-run',
                        help='Prints out the changes that would occur, without actually executing them.',
                        action='store_true',
                        dest='dry_run')

    parser.add_argument('-V', '--version',
                        action='version',
                        version=__version__,
                        help='Prints out the current version of pysorter')

    return validate_arguments(parser.parse_args(args))

def main(args=None):
    global _last_sorter

    logging.basicConfig()
    args = parse_args(args)

    rules = RulesFileClassifier.load_file(args.filetypes)

    topass = dict(vars(args))

    # --- remove processed arguments
    del topass['directory']
    del topass['filetypes']
    del topass['unhandled_file']

    sorter = Organizer(args.directory, rules, **topass)
    sorter.organize()

    _last_sorter = sorter

    # write out all the unknown file types
    if args.unhandled_file:
        with open(args.unhandled_file, 'a') as ufile:
            for i in sorter.unhandled_paths:
                ufile.write(i)
                ufile.write('\n')
    return 0

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    sys.exit(main())
