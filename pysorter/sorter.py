"""
    Contains the core logic of the sorting implementation
"""
from __future__ import print_function

import logging
import os
import sys
from collections import namedtuple

from rules.basesortrule import UnhandledPathException
from utils import filesystem
from utils.filesystem import File

log = logging.getLogger(__name__)


class FatalPySorterException(Exception):
    def __init__(self, msg, errcode):
        super(FatalPySorterException, self).__init__()
        self.message = msg
        self.error_code = errcode


class Actions:
    FILE_FILE = 1
    FILE_DIR = 2

    move = namedtuple("move_dir", ["src", "dst", "type"])
    skip = namedtuple("skip", ["path", "type"])


class PySorter(object):
    def __init__(self,
                 source_dir,
                 sort_ruleset,
                 recursive=False,
                 unknown_suffix=None,
                 directories_dest=None,
                 other_files=None,
                 clean_empty_dirs=False,
                 all_dirs=False,
                 log_moves=False, dest_dir=None):
        """
        Construct a new instance of PySorter for organizing some directory
        using certain parameters

        Parameters
        -----------
        source_dir : string
           path to the directory that must be organized

        sort_ruleset: RuleSet
            ruleset used to determine the sorting destinations of files

        recursive : boolean
            should directories in the `source_dir` be traversed recursively?

        unknown_suffix : string
            suffix string that is joined with the file extension for
            use when there is no ruleset rule for it.

        directories_dest : string
            `dest_dir` relative or absolute path  where all directories must be moved

        other_files : string
           `dest_dir` relative or absolute directory path where all files of unknown type are relocated to.

        clean_empty_dirs : boolean
            toggles recursive empty directory removal

        all_dirs : boolean
            toglles whether all directories should be sorted recursively.
            Only works if used in conjunction with `recursive`

        log_moves: boolean
            Toggles whether the moving of files are logged to stdout or not

        dest_dir: string
            the directory to organize your files into, instead of doing it in-place,
            if not set, it will be set to `source_dir`
        """

        directories_dest = directories_dest or "directories"
        other_files = other_files or "other"
        self.unknown_file_suffix = unknown_suffix or " files"

        dest_dir = dest_dir or source_dir

        if not os.path.isdir(source_dir):
            raise OSError("Directory to organize does not exist or is a file: {}".format(source_dir))

        if not os.path.isdir(dest_dir):
            log.warn("Destination directory does not exist, creating: %s", dest_dir)
            filesystem.directory.make_path(dest_dir)

        self.path_source = os.path.abspath(source_dir)
        self.path_dest = os.path.abspath(dest_dir)

        self.sort_rule = sort_ruleset

        self.unknown_types = set()
        # directories that should NOT be traversed
        self.not_traverse = set()
        self.action_log = []

        self.do_clean_empty_dirs = clean_empty_dirs
        self.do_recurse = recursive
        self.do_traverse_all = all_dirs
        self.do_log_move = log_moves

        if not os.path.isabs(directories_dest):
            directories_dest = os.path.join(self.path_dest, directories_dest)

        if not os.path.isabs(other_files):
            other_files = os.path.join(self.path_dest, other_files)

        self.path_dirs_dest = directories_dest
        self.path_other_files = other_files

        # if these folders are within our organize destination don't try and organize them
        if filesystem.directory.is_subdir(directories_dest, self.path_dest):
            relative = filesystem.directory.relative_to(directories_dest, self.path_dest)
            self.not_traverse.add(relative)

        if filesystem.directory.is_subdir(other_files, self.path_dest):
            relative = filesystem.directory.relative_to(other_files, self.path_dest)
            self.not_traverse.add(relative)

        filesystem.directory.make_path(self.path_dirs_dest)
        filesystem.directory.make_path(self.path_other_files)

    def organize(self):
        top_dirs, files = filesystem.directory.ls(self.path_source)

        # organize toplevel files
        for file in files:
            fp = File(os.path.curdir, file, relative_to=self.path_source)
            self.process_file(fp)

        # organize toplevel directories
        should_not_traverse = lambda d: d in self.not_traverse

        for d in top_dirs:
            fullpath = os.path.join(self.path_source, d)
            if self.do_traverse_all:
                self.process_dir(fullpath)
            elif should_not_traverse(d):
                continue

            self.process_dir(fullpath)

        if self.do_clean_empty_dirs:
            filesystem.directory.clean_empty(self.path_source)

    def process_dir(self, path):
        if self.do_recurse:
            for path, dirs, files in os.walk(path):
                subdir = filesystem.directory.relative_to(path, self.path_source)
                for f in files:
                    file = File(subdir, f, relative_to=self.path_source)
                    self.process_file(file)
        else:
            subdir, dirname = os.path.split(filesystem.directory.relative_to(path, self.path_source))
            dir = File(subdir, dirname, self.path_source)
            self.process_dir_single(dir)

    def process_dir_single(self, dir):
        src = dir.full_path
        try:
            dst = self.sort_rule.process(dir)

            # ensure path is absoulte
            if not os.path.isabs(dst):
                dst = os.path.join(self.path_dest, dst)

        except UnhandledPathException:
            dst = os.path.join(self.path_dirs_dest, dir.name)

        if os.path.exists(dst):
            log.info("Directory exists: %s, skipping", dst)
            return

        if self.do_log_move:
            self.action_log.append(Actions.move(src, dst, Actions.FILE_DIR))
            log.debug("[MoveDir] `%s` --> `%s`", src, dst)

        # move_dir src INTO destination
        filesystem.directory.move_dir(src, self.path_dirs_dest)

    def unknown_ext_dirname(self, extension):
        """Returns the destination directory name for a file with unknown extension"""
        return extension.upper() + self.unknown_file_suffix

    def process_file(self, file):
        if not file.name and not file.extension:
            # This should never happen
            self.raise_error("[Error] File with no extension and no name, report this", 2)

        # --- Try handling by the ruleset
        try:
            dest = self.sort_rule.process(file)
            # case where destination is relative
            if not os.path.isabs(dest):
                dest = os.path.join(self.path_dest, dest)
        except UnhandledPathException:
            if not file.extension:
                dest = os.path.join(self.path_other_files, file.name)
            else:
                to_dir = os.path.join(self.path_other_files, self.unknown_ext_dirname(file.extension))
                filesystem.directory.make_path(to_dir)
                dest = os.path.join(to_dir, file.name)

                self.unknown_types.add(file.extension.lower())

        if os.path.exists(dest):
            print("[File already exists]: " + dest + ", skipping...", file=sys.stderr)
            return

        # --- ensure destination directory exists, if not create it
        dest_dir, _ = os.path.split(dest)
        filesystem.directory.make_path(dest_dir)

        if self.do_log_move:
            print("[Move] `{}` --> `{}`".format(file.full_path, dest))
        else:
            log.debug("Move `%s` --> `%s`", file.full_path, dest)

        filesystem.file.move_file(file.full_path, dest)

    def raise_error(self, msg, code=1):
        raise FatalPySorterException(msg, code)
