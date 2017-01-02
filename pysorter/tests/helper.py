from __future__ import unicode_literals
import os
from .. import action

import pytest


def is_string(obj):
    import sys

    PY3 = sys.version_info[0] == 3

    if PY3:
        string_types = str,
    else:
        string_types = basestring,
    return isinstance(obj, string_types)


def initialize_dir(d, filetypes, paths_to_make):
    """

    Parameters
    ----------
    filetypes: dict
        mapping of strings to strings for filetypes

    paths_to_make: list
        list of string tuples (path, type)
        directories end in / and files do not end in /

    """
    # --- create a mapping file
    d.write('filetypes.py', bytearray(mkfiletypesstr(filetypes), encoding="utf-8"))

    # --- create temp files
    for path in paths_to_make:
        if os.path.isabs(path):
            raise ValueError("Paths must be relative: {}".format(path))

        dirpath, filename = os.path.split(path)

        if dirpath and not os.path.isdir(dirpath):
            d.makedir(dirpath)

        if filename:
            d.write(path, b'')


def mkfiletypesstr(mapping):
    """
    Takes a string to string mapping and
    writes them as a mapping, returns a string
    """
    import inspect
    import textwrap
    from io import StringIO
    s = StringIO()
    s.write('from pysorter import action\n')
    # --- first dump any functions definitions
    for v in mapping.values():
        if v in action.actionset:
            continue
        elif callable(v):
            source = textwrap.dedent(inspect.getsource(v))
            # accomodate for python3
            try:
                source = unicode(source, encoding="utf-8")
            except NameError:
                pass
            s.write(source)
            s.write('\n')

    # write out the rules array
    s.write('RULES = [')
    for k in mapping:
        value = mapping[k]

        if value in action.actionset:
            value = 'action.' + value.__name__
        elif callable(value):
            value = v.__name__
        else:
            value = repr(value)

        s.write('({}, {}),\n'.format(repr(k), value))
    s.write(']\n')
    s = s.getvalue()
    #print s
    return s


def _build_path_tree(paths, path_set, prefix=None):
    # print paths, prefix
    for path in paths:
        if is_string(path):
            if prefix is not None:
                path = os.path.join(prefix, path)
            dirpath = os.path.dirname(path)

            parts = dirpath.split('/')

            if len(parts) > 1:
                total = parts[0] + '/'
                if not prefix:
                    path_set.add(total)
                for part in parts[1:]:
                    total = total + part + '/'
                    path_set.add(total)
            path_set.add(path)
        else:
            new_prefix = path[0]
            if not path[0].endswith('/'):
                new_prefix += '/'

            if prefix:
                new_prefix = os.path.join(prefix, new_prefix)

            path_set.add(new_prefix)

            _build_path_tree(path[1], path_set, prefix=new_prefix)


def build_path_tree(paths, prefix=None):
    """
    Creates and returns a sorted list of all possible paths that
    can be generateed from paths.

    Examples
    --------
    >>> build_path_tree(['1/2/file'])
    ['1/', '1/2/', '1/2/file']
    >>> build_path_tree(['file', ('d1', ['f1', 'f2']), ('d2', [('d3', ['f1']), 'f1'])])
    ['d1/', 'd1/f1', 'd1/f2', 'd2/', 'd2/d3/', 'd2/d3/f1', 'd2/f1', 'file']
    >>> build_path_tree(['file', ('d1', ['f1', 'f2']), ('d2', [('d3', ['f1']), 'f1'])], 'sorted')
    ['sorted/d1/', 'sorted/d1/f1', 'sorted/d1/f2', 'sorted/d2/', 'sorted/d2/d3/', 'sorted/d2/d3/f1', 'sorted/d2/f1', 'sorted/file']


    Parameters
    ----------
    paths: list
        A list of strings or tuples representing the paths to be created.

    prefix: str
        string to prefix to all created paths

    Returns
    -------

    """
    pathset = set()
    _build_path_tree(paths, pathset, prefix=prefix)
    return sorted(pathset)
