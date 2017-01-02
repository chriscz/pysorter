"""
    Contains the core logic of the sorting implementation
"""
from __future__ import print_function

import logging

import os

from .. import action
from .. import filesystem as fs
from .util import escape_singles

log = logging.getLogger(__name__)

class PySorter(object):
    def __init__(self,
                 source_dir,
                 sort_rule,
                 no_process=None,
                 dest_dir=None,

                 dry_run=False,

                 do_process_dirs=False,
                 do_recurse=False,
                 do_remove_empty_dirs=False):
        """
        Construct a new instance of PySorter for organizing some directory
        using certain parameters

        Parameters
        -----------
        source_dir: string
           path to the directory that must be organized

        sort_rule: RuleSet
            ruleset used to determine the sorting destinations of files

        no_process: set()
            names of toplevel directories that should not be traversed

        dest_dir: string
            the directory to organize your files into, instead of doing it in-place,
            if not set, it will be set to `source_dir`

        dry_run: boolean
            prints all file and directory that would occur changes without
            actually performing organization.

        do_recurse: boolean
            should directories in the `source_dir` be traversed recursively?

        do_remove_empty_dirs: boolean
            toggles recursive empty directory removal
        """
        dest_dir = dest_dir or source_dir

        if not os.path.isdir(source_dir):
            raise OSError("Directory to organize does not exist or is a file: {}".format(source_dir))

        if not os.path.isdir(dest_dir):
            log.warn("Destination directory does not exist, creating: %s", dest_dir)
            fs.make_path(dest_dir)

        self.path_source = os.path.abspath(source_dir)
        self.path_dest = os.path.abspath(dest_dir)

        self.sort_rule = sort_rule

        self.unhandled_paths = set()

        # directories or files that should not be processed paths are relative
        # to the directory to be sorted and should exclude any starting ./

        self.no_process = no_process or set()
        self.no_recurse = set()

        self.dry_run = dry_run

        self.do_remove_empty_dirs = do_remove_empty_dirs
        self.do_recurse = do_recurse
        self.do_process_dirs = do_process_dirs

        # --- variables used in a dry run

        # functions as an overlay of the destination directory,
        # so that changes in the source may be reflected through it.

        self.dry_src = set()
        self.dry_dst = set()
        self.dry_mv_tuples = []
        self.dry_rmdir = []

        self.files = {}

    @fs.save_cwd
    def sortrule_destination(self, path):
        """
        Invokes self.sortrule.destination, ensured that  Skip, SkipReturn or Unhandled
        are raised when the function returns them.
        """
        retval = self.sort_rule.destination(path)
        if retval in action.actionset:
            raise retval()
        return retval

    @fs.save_cwd
    def organize(self):
        """
        The `main` function for organization.
        """
        os.chdir(self.path_source)

        def filter_no_process(base, alist, skipset=self.no_process):
            """
            Removes items from a list returned by os.walk, in place.
            """
            L = len(alist)
            for idx, i in enumerate(list(reversed(alist))):
                i = fs.cjoin(base, i)
                if i in skipset:
                    del alist[L - idx - 1]

        for base, dirs, files in os.walk('.'):
            filter_no_process(base, files)
            filter_no_process(base, dirs)

            for file in files:
                self.process(fs.cjoin(base, file))

            if self.do_process_dirs:
                for dir in dirs:
                    self.process(fs.cjoin(base, dir, is_dir=True))
                filter_no_process(base, dirs, skipset=self.no_recurse)
                self.no_recurse = set()  # clear out

            if not self.do_recurse:
                del dirs[:]

        if self.do_remove_empty_dirs:
            if self.dry_run:
                self.dry_rmdir = fs.collect_terminal_empty_dirs(self.path_source, self.dry_mv_tuples)
                for path in self.dry_rmdir:
                    print("rmdir '{}'".format(escape_singles(path)))
            else:
                fs.remove_empty_dirs(self.path_source)


    def process(self, src):
        """
        Take a single path to a directory or a file and
        apply some action to it, as defined by the sorting rule
        """
        name = fs.name(src)

        try:
            raw_dst = self.sortrule_destination(src)

            # a relative destination
            if not os.path.isabs(raw_dst):
                raw_dst = os.path.join(self.path_dest, raw_dst)

            if raw_dst.endswith('/'):
                # the destination is a directory, so the
                # file / directory must go INSIDE
                dst = fs.cjoin(raw_dst, name)
            else:
                # the destination is absolute, file must go there
                dst = fs.cjoin(raw_dst)

        except action.Unhandled:
            self.unhandled_paths.add(src)
            return
        except action.Skip:
            return
        except action.SkipRecurse:
            if src.endswith('/'):
                # strip the trailing slash because the path will be compared
                # with `dirs` returned by os.walk (which do not contain
                # a trailing slash `/`)
                self.no_recurse.add(src.rstrip('/'))
            return

        if os.path.exists(dst) or (dst in self.dry_dst):
            log.info("destination exists: `%s` --> `%s`", src, dst)
            return

        if self.dry_run:
            abs_src = os.path.join(self.path_source, src)
            self.dry_src.add(abs_src)
            self.dry_dst.add(dst)

            self.dry_mv_tuples.append((abs_src, dst))

            if not fs.is_file(src):
                self.no_recurse.add(src.rstrip('/'))
            print("mv '{}' '{}'".format(escape_singles(abs_src), escape_singles(dst)))
            return

        fs.make_path(os.path.dirname(dst))
        log.info("move {} --> {}".format(src, dst))
        if fs.is_file(src):
            fs.move_file(src, dst)
        else:
            fs.move_dir(src, dst)
