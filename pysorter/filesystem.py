from __future__ import print_function

import logging
import os
import shutil
from itertools import chain

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
    'foo/bar/baz'
    >>> cjoin("foo", "bar", "baz", is_dir=True)
    'foo/bar/baz/'
    >>> cjoin('./foo')
    'foo'
    >>> cjoin('./foo', is_dir=True)
    'foo/'
    >>> cjoin('.', is_dir=True)
    './'
    >>> cjoin('./')
    './'


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

def collect_terminal_empty_dirs(root, move_tuples):
    """Returns a list of all empty directories.

       With a recursive argument it can be shown that a list of (full)
       paths to all empty directories is sufficient to reconstruct
       all recursively empty directories as well.


       Arguments
       ---------
       path: the path to collect from

       move_tuples: list of 2-tuple
        pairs of absolute (src, dst) paths

    """

    # --- build root directory state as it currently is
    disk_state = []
    norm_root = os.path.normpath(os.path.abspath(root))
    for base, dirs, files in os.walk(root):
        norm_base = os.path.normpath(os.path.abspath(base))

        for d in dirs:
            disk_state.append(os.path.join(norm_base, d) + os.path.sep)
        for f in files:
            disk_state.append(os.path.join(norm_base, f))

    disk_tree = _paths_to_tree(disk_state)

    def traverse(tree, parts, mkdir=False):
        """traverses parts and returns a (parent, name) tuple
           where name is a key into the parent, identifying the
           last item in parts.

           if mkdir is true, intermediary directories are created,
           the final path component is not created.
        """
        item = tree

        parent = None
        name = None

        if mkdir:
            for s in parts:
                item[s] = item.get(s, {})
                item, parent = item[s], item
                name = s
            del parent[name]
        else:
            for s in parts:
                item, parent = item[s], item
                name = s

        return (parent, name)

    def move(source, dest, tree):
        src_parts = _path_parts(source)
        dst_parts = _path_parts(dest)

        src_parent, src_name = traverse(tree, src_parts)
        src_item = src_parent[src_name]
        del src_parent[src_name]

        dst_parent, dst_name = traverse(tree, dst_parts, mkdir=True)

        assert dst_name not in dst_parent
        # perform the actual move
        dst_parent[dst_name] = src_item


    for (src, dst) in move_tuples:
        print("*** MOVE", src, '-->', dst)
        move(src, dst, disk_tree)


    empties = set()

    def collect_empty(tree, parts):
        if tree is None:
            return False
        elif tree == {}:
            return True

        all_empty = True
        for name in tree:
            value = tree[name]
            parts.append(name)

            if collect_empty(value, parts):
                empties.add(os.path.join(*parts))
            else:
                all_empty = False

            parts.pop()

        return all_empty

    src_parent, src_name = traverse(disk_tree, _path_parts(norm_root))
    collect_empty(src_parent[src_name], [root])

    return empties


def remove_empty_dirs(path):
    """Recursively removes empty direcotries contained within path"""
    for root, dirs, files in os.walk(path, topdown=False):
        log.debug("[clean_empty.at] %s", path)

        # don't remove the source directory!
        if os.path.normpath(root) == os.path.normpath(path):
            break

        if len(os.listdir(root)) == 0:
            os.rmdir(root)
            log.debug("rmdir %s", root)



def make_path(path):
    """Creates intermediary directories so that the path exists"""
    path = os.path.abspath(path)
    if os.path.exists(path) and not os.path.isdir(path):
        raise OSError("File {} exists, but is not a directory".format(path))
    log.debug("make_path: %s", path)
    if not os.path.exists(path):
        os.makedirs(path)

def _path_parts(path):
    path = os.path.normpath(path)
    parts = path.split(os.path.sep)
    # the only empty parts should be the start
    # or the end
    return (_ for _ in parts if _)

def _paths_to_tree(paths):
    """
        Makes a directory tree from an iterable of file
        or directory paths. If a path corresponds to a directory
        it *MUST* end in the seperator of the filesystem

        Examples
        ---------
        >>> _paths_to_tree(['/hello/there/'])
        {'hello': {'there': {}}}
        >>> _paths_to_tree(['/hello/there'])
        {'hello': {'there': None}}
        >>> _paths_to_tree(['/'])
        {}
        >>> _paths_to_tree([])
        {}
        >>> _paths_to_tree(set())
        {}
        >>> _paths_to_tree(['hello/cruel/world', 'hello/cruel/earth/africa'])
        {'hello': {'cruel': {'world': None, 'earth': {'africa': None}}}}
    """
    print("PATHS", paths)

    tree = {}

    for path in paths:
        parent = None
        subtree = tree
        p = None
        try:
            for p in _path_parts(path):
                subtree[p] = subtree.get(p, {})
                subtree, parent = subtree[p], subtree
        except AttributeError:
            msg = 'Path previously classified as file, was\
                   accessed as directory. Ensure that all directory\
                   paths end in a `%s`' % (os.path.sep,)
            raise ValueError(msg)

        # case where the path references a file
        if p and not path[-1] in {os.path.sep, '/'}:
            parent[p] = None

    return tree



