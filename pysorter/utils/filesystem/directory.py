import logging
import os
import shutil

log = logging.getLogger(__name__)


def clean_empty(path):
    """Recursively removes empty direcotries contained within path"""
    for path, dirs, files in os.walk(path, topdown=False):
        log.debug("[clean_empty.at] %s", path)
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
            log.debug("[clean_empty.rm] %s", path)


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
        if debug: print repr(path), (newpath, tail)
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


def ls(path):
    """Returns a tuple (dirnames, filenames) for dirs and files in the path"""
    for dirpath, dirnames, filenames in os.walk(path):
        return (dirnames, filenames)


def move_dir(src, dst):
    """Moves the source directory INTO the destination"""
    if not os.path.isdir(src):
        raise OSError("Source path is not a directory: {}".format(src))

    shutil.move(src, dst)
