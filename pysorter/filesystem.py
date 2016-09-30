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


def _os_path_split_asunder(path, debug=False):
    """
    http://stackoverflow.com/a/4580931/171094
    """
    parts = []
    while True:
        newpath, tail = os.path.split(path)
        if debug: print(repr(path), (newpath, tail))
        if newpath == path:
            assert not tail
            if path: parts.append(path)
            break
        parts.append(tail)
        path = newpath
    parts.reverse()
    return parts


def _get_normalized_parts(path):
    """Returns the path parts in normalized form"""
    return _os_path_split_asunder(os.path.realpath(os.path.abspath(os.path.normpath(path))))


def is_subdir(potential_subdirectory, expected_parent_directory):
    """
    http://stackoverflow.com/a/17624617

    Is the first argument a sub-directory of the second argument?

    :param potential_subdirectory:
    :param expected_parent_directory:
    :return: True if the potential_subdirectory is a child of the expected parent directory

    >>> is_subdir('/var/test2', '/var/test')
    False
    >>> is_subdir('/var/test', '/var/test2')
    False
    >>> is_subdir('var/test2', 'var/test')
    False
    >>> is_subdir('var/test', 'var/test2')
    False
    >>> is_subdir('/var/test/sub', '/var/test')
    True
    >>> is_subdir('/var/test', '/var/test/sub')
    False
    >>> is_subdir('var/test/sub', 'var/test')
    True
    >>> is_subdir('var/test', 'var/test')
    True
    >>> is_subdir('var/test', 'var/test/fake_sub/..')
    True
    >>> is_subdir('var/test/sub/sub2/sub3/../..', 'var/test')
    True
    >>> is_subdir('var/test/sub', 'var/test/fake_sub/..')
    True
    >>> is_subdir('var/test', 'var/test/sub')
    False
    >>> is_subdir(r'C:\\foo\\baz', 'C:\\foo\\bar')
    False
    >>> is_subdir(r'C:\\foo\\bar', 'C:\\foo\\bar')
    False
    """
    # make absolute and handle symbolic links, split into components
    sub_parts = _get_normalized_parts(potential_subdirectory)
    parent_parts = _get_normalized_parts(expected_parent_directory)

    if len(parent_parts) > len(sub_parts):
        # a parent directory never has more path segments than its child
        return False

        # we expect the zip to end with the short path, which we know to be the parent
    return all(part1 == part2 for part1, part2 in zip(sub_parts, parent_parts))


def relative_to(subdir, parentdir):
    """Returns a string that's path relative to a parent directory parent

    >>> relative_to('/foo/bar/', '/foo/')
    'bar'
    >>> relative_to('/foo/bar', '/foo/')
    'bar'
    >>> relative_to('/foo/bar/baz/', '/foo/')
    'bar/baz'
    """
    assert is_subdir(subdir, parentdir)

    sub_parts = _get_normalized_parts(subdir)
    parent_parts = _get_normalized_parts(parentdir)

    split_at = len(parent_parts)
    for i in range(len(parent_parts)):
        if sub_parts[i] != parent_parts[i]:
            split_at = i
            break

    return os.path.sep.join(sub_parts[split_at:])
