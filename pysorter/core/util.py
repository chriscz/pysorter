from os.path import *

def escape_singles(string):
    """escapes all single quotes in a string"""
    return string.replace("'", r"\'")

def script_directory():
    """Returns the full path to where this script located"""
    return abspath(join(dirname(abspath(__file__)), '../'))


def write_unknown(unknowns, path):
    """Appends all the unknown filetypes to the file at the given path.
    A filetype per line"""
    with open(path, 'a') as ufile:
        for i in unknowns:
            ufile.write(i)
            ufile.write('\n')


def is_string(obj):
    import sys

    PY3 = sys.version_info[0] == 3

    if PY3:
        string_types = str,
    else:
        string_types = basestring, str
    return isinstance(obj, string_types)
