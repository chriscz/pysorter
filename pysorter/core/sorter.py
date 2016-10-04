"""
    Contains the core logic of the sorting implementation
"""
from __future__ import print_function

import logging

import os

from .. import action
from .. import filesystem as fs

log = logging.getLogger(__name__)

class PySorter(object):
    def __init__(self,
                 source_dir,
                 sort_rule,
                 no_process=None,
                 dest_dir=None,

                 do_process_dirs=False,
                 do_recurse=False,
                 do_remove_empty_dirs=False):
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

        no_process: set()
            names of toplevel directories that should not be traversed

        do_remove_empty_dirs : boolean
            toggles recursive empty directory removal

        dest_dir: string
            the directory to organize your files into, instead of doing it in-place,
            if not set, it will be set to `source_dir`

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

        self.do_remove_empty_dirs = do_remove_empty_dirs
        self.do_recurse = do_recurse
        self.do_process_dirs = do_process_dirs

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
                self.no_recurse = set() # clear out

            if not self.do_recurse:
                del dirs[:]


        if self.do_remove_empty_dirs:
            fs.remove_empty_dirs(self.path_source)

    def process(self, path):
        name = fs.name(path)

        try:
            raw_dst = self.sortrule_destination(path)

            # a relative destination
            if not os.path.isabs(raw_dst):
                raw_dst = os.path.join(self.path_dest, raw_dst)

            if raw_dst.endswith('/'):
                # the destination is a directory
                dst = fs.cjoin(raw_dst, name)
            else:
                # the destination is absolute, file must go there
                dst = fs.cjoin(raw_dst)

        except action.Unhandled:
            self.unhandled_paths.add(path)
            return
        except action.Skip:
            return
        except action.SkipRecurse:
            if path.endswith('/'):
                # we have to strip the trailing slash in this instance
                self.no_recurse.add(path[:-1])
            return

        if os.path.exists(dst):
            log.info("destination exists: `%s` --> `%s`", path, dst)
            return

        fs.make_path(os.path.dirname(dst))
        log.info("move `%s` --> `%s`", path, dst)

        if fs.is_file(path):
            fs.move_file(path, dst)
        else:
            fs.move_dir(path, dst)
