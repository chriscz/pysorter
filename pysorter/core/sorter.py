"""
    Contains the core logic of the sorting implementation
"""
from __future__ import print_function

import logging
import os

from .. import filesystem as fs
from ..rules.basesortrule import UnhandledPathException

log = logging.getLogger(__name__)


class PySorter(object):
    def __init__(self,
                 source_dir,
                 sort_rule,
                 unknown_suffix=None,
                 directories_dest=None,
                 no_process=None,
                 other_files=None,
                 dest_dir=None,

                 do_recurse=False,
                 do_remove_empty_dirs=False,
                 do_process_dirs=False):
        """
        Construct a new instance of PySorter for organizing some directory
        using certain parameters

        Parameters
        -----------
        source_dir : string
           path to the directory that must be organized

        sort_rule: RuleSet
            ruleset used to determine the sorting destinations of files

        do_recurse : boolean
            should directories in the `source_dir` be traversed recursively?

        unknown_suffix : string
            suffix string that is joined with the file extension for
            use when there is no ruleset rule for it.

        no_process: set()
            names of toplevel directories that should not be traversed

        directories_dest : string
            `dest_dir` relative or absolute path  where all directories must be moved

        other_files : string
           `dest_dir` relative or absolute directory path where all files of unknown type are relocated to.

        do_remove_empty_dirs : boolean
            toggles recursive empty directory removal

        dest_dir: string
            the directory to organize your files into, instead of doing it in-place,
            if not set, it will be set to `source_dir`

        do_sort_directories: boolean
            should directories also be considered for sorting?
        """

        directories_dest = directories_dest or "directories"
        other_files = other_files or "other"
        self.unknown_file_suffix = unknown_suffix or "_files"

        dest_dir = dest_dir or source_dir

        if os.path.exists(source_dir) and not os.path.isdir(source_dir):
            raise OSError("Directory to organize does not exist or is a file: {}".format(source_dir))

        if not os.path.isdir(dest_dir):
            log.warn("Destination directory does not exist, creating: %s", dest_dir)
            fs.make_path(dest_dir)

        self.path_source = os.path.abspath(source_dir)
        self.path_dest = os.path.abspath(dest_dir)

        self.sort_rule = sort_rule

        self.unknown_types = set()

        # directories or files that should not be processed paths are relative
        # to the directory to be sorted and should exclude any starting ./

        self.no_process = no_process or set()

        self.do_remove_empty_dirs = do_remove_empty_dirs
        self.do_recurse = do_recurse
        self.do_process_dirs = do_process_dirs

        if not os.path.isabs(directories_dest):
            directories_dest = os.path.join(self.path_dest, directories_dest)

        if not os.path.isabs(other_files):
            other_files = os.path.join(self.path_dest, other_files)

        self.path_dirs_dest = fs.cjoin(directories_dest, is_dir=True)
        self.path_other_files = fs.cjoin(other_files, is_dir=True)

        # if these folders are within our organize destination don't try and organize them
        if fs.is_subdir(directories_dest, self.path_dest):
            relative = fs.relative_to(directories_dest, self.path_dest)
            self.no_process.add(fs.cjoin(relative))

        if fs.is_subdir(other_files, self.path_dest):
            relative = fs.relative_to(other_files, self.path_dest)
            self.no_process.add(fs.cjoin(relative))

        fs.make_path(self.path_dirs_dest)
        fs.make_path(self.path_other_files)

    def unknown_ext_dirname(self, extension):
        """Returns the destination directory name for a file with unknown extension"""
        return extension.lower() + self.unknown_file_suffix

    @fs.save_cwd
    def organize(self):
        os.chdir(self.path_source)

        def filter_no_process(base, alist):
            """
            Removes items from a list returned by os.walk, in place.
            """
            L = len(alist)
            for idx, i in enumerate(list(reversed(alist))):
                i = fs.cjoin(base, i)
                if i in self.no_process:
                    del alist[L - idx - 1]

        for base, dirs, files in os.walk('.'):
            filter_no_process(base, files)
            filter_no_process(base, dirs)

            for file in files:
                self.process(fs.cjoin(base, file))

            if self.do_process_dirs:
                for dir in dirs:
                    self.process(fs.cjoin(base, dir, is_dir=True))

            if not self.do_recurse:
                del dirs[:]

        if self.do_remove_empty_dirs:
            fs.remove_empty_dirs(self.path_source)

    def process(self, path):
        name = fs.name(path)

        try:
            raw_dst = self.sort_rule.destination(path)

            # a relative destination
            if not os.path.isabs(raw_dst):
                raw_dst = os.path.join(self.path_dest, raw_dst)

            if raw_dst.endswith('/'):
                # the destination is a directory
                dst = fs.cjoin(raw_dst, name)
            else:
                # the destination is absolute, file must go there
                dst = fs.cjoin(raw_dst)

        except UnhandledPathException:
            if fs.is_file(path):
                name = os.path.basename(path)
                ext = fs.extension(name)
                if not ext:
                    dst = fs.cjoin(self.path_other_files, name)
                else:
                    dst = fs.cjoin(self.path_other_files, self.unknown_ext_dirname(ext[1:]), name)
                    self.unknown_types.add(ext[1:])
            elif self.do_recurse:
                # don't relocate a directory while busy recurring
                return
            else:
                dst = fs.cjoin(self.path_dirs_dest, name)

        if os.path.exists(dst):
            log.info("destination exists: `%s` --> `%s`", path, dst)
            return

        fs.make_path(os.path.dirname(dst))
        log.info("move `%s` --> `%s`", path, dst)

        if fs.is_file(path):
            fs.move_file(path, dst)
        else:
            fs.move_dir(path, dst)
