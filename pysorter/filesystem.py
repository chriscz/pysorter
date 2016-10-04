from __future__ import print_function

import logging
import os
import shutil

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
#  Canonical path functions
# --------------------------------------------------------------------------
def cjoin(path, *paths, **kwargs):
    """
    Canonical join.
    Ensures the following invariants hold:
        - all paths relative to ./ are given without the ./ specifier,
          unless they refer to `.`, in which case ./ would be returned
        - all direcory paths end in '/'

    Examples
    >>> cjoin("foo", "bar", "baz")
    foo/bar/baz
    >>> cjoin("foo", "bar", "baz", is_dir=True)
    foo/bar/baz/
    >>> cjoin('./foo')
    foo
    >>> cjoin('./foo', is_dir=True)
    foo/
    >>> cjoin('.', is_dir=True)
    ./
    >>> cjoin('./')
    ./


    Parameters
    ----------
    path
    paths
    kwargs:
        is_dir: boolean
            is this path a directory?
    Returns
    -------

    """
    joined = os.path.join(path, *paths)
    if kwargs.get('is_dir', False) and not path.endswith('/'):
        joined += '/'

    if joined != './' and joined.startswith('./'):
        joined = joined[2:]

    return joined


def is_file(path):
    """
    tests whether a canonical path refers to a file or a directory
    """
    return not path.endswith('/')


def extension(path):
    return os.path.splitext(path)[1]


def name(path):
    """
    Return the name of the last element in the path. if the path ends in a slash,
    then the name of the directory before the slash is returned
    """
    if path.endswith('/'):
        path = path[:-1]
    return os.path.basename(path)


# --------------------------------------------------------------------------
#  Common
# --------------------------------------------------------------------------
def save_cwd(function):
    def func(*args, **kwargs):
        _pwd = os.getcwd()
        try:
            return function(*args, **kwargs)
        finally:
            os.chdir(_pwd)

    return func


# --------------------------------------------------------------------------
#  File related
# --------------------------------------------------------------------------

def move_file(src, dst):
    if not os.path.isfile(src):
        raise OSError("Source path is not a file: {}".format(src))
    #print "mv  {} --> {}".format(src, dst)
    shutil.move(src, dst)


# --------------------------------------------------------------------------
#  Directory related
# --------------------------------------------------------------------------

def move_dir(src, dst):
    """Moves the source directory INTO the destination"""
    if not os.path.isdir(src):
        raise OSError("Source path is not a directory: {}".format(src))
    #print "mvd {} --> {}".format(src, dst)
    shutil.move(src, dst)

def remove_empty_dirs(path):
    """Recursively removes empty direcotries contained within path"""
    for path, dirs, files in os.walk(path, topdown=False):
        log.debug("[clean_empty.at] %s", path)
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
            log.debug("rmdir %s", path)


def make_path(path):
    """Creates intermediary directories so that the path exists"""
    path = os.path.abspath(path)
    if os.path.exists(path) and not os.path.isdir(path):
        raise OSError("File {} exists, but is not a directory".format(path))
    log.debug("make_path: %s", path)
    if not os.path.exists(path):
        os.makedirs(path)