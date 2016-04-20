#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2013 Chris Coetzee (chriscz93@gmail.com)
# You may redistribute this file as long as the distribution complies with below license.
# Furthermore, you are required to mention the author and the source homepage in your application
#
# Version 0.0.6 (Alpha)
#
#    pySorter is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pySorter is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySorter.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
import os
import sys
import shutil
import argparse

DEBUG = False
def debug(fmat, *args):
    if DEBUG:
        print("[DEBUG] {}".format(fmat.format(*args)))

class PySorter(object):
    def __init__(self, path, file_types, recursive=False, unknown_suffix=" files",
                move_directories="Directories", other_files="Other", clean_empty_dirs=False, all_dirs=False, log_moves=False):
        '''Construct a new instance of PySorter for organizing some directory
           using certain parameters
           
           Parameters
           -----------
               path : string
                   Path to the directory that PySorter must oganize
               file_types : dict
                   Dictonary containing file type --> relative
                   path mappings
               recursive : boolean
                   Should sorting occur recursively, i.e. should 
                   top-level directories be traversed and contents
                   sorted recursively
               unknown_suffix : string
                   The suffix that will be appended to the direcory name
                   for file types that aren't defined in the 
                   `file_types`  file
               move_directories : string
                    Relative directory path into which directories should 
                    be moved
               other_files : string
                    Relative directory path which should be used to store
                    files that are not defined in `filet_types`
               clean_empty_dirs : boolean
                    Toggles the removal of empty directories. this
                    flag recursively looks through all directories
                    and removes any empty ones that it finds
               log_moves: boolean
                    Toggles whether the moving of files are logged to stdout or not
               all_dirs : boolean
                   Flag is only considered if the `recursive` flag is set.
                   When true, the sorter will enter "reserved" directories,
                   i.e. the relative root direcotries defined in 
                   the `file_types` file
        '''
        self.PATH = path_to_unix(os.path.abspath(path))
        if not os.path.isdir(path):
            self.error(1, "[Error] Invalid directory")
        self.CLEAN = clean_empty_dirs
        self.RECURSIVE = recursive
        self.ALL_DIRS = all_dirs
        self.UNKNOWN_SUFFIX = unknown_suffix
        self.DIRECTORIES_TO = path_join(self.PATH, move_directories)
        self.OTHER_FILES_TO = path_join(self.PATH, other_files)
        self.types = file_types
        self.unknown = set()
        self.log_moves = log_moves
        
        self.TOP_LEVEL_DIRS = set()
        self.TOP_LEVEL_DIRS.add(path_base_dir(move_directories))
        
        self.TOP_LEVEL_DIRS.add(path_base_dir(other_files))
        for i in self.types.keys():
            self.TOP_LEVEL_DIRS.add(path_base_dir(self.types[i]))
        
        self.make_path(path_to_unix(self.DIRECTORIES_TO))
        self.make_path(path_to_unix(self.OTHER_FILES_TO))
        
    def sort(self):
        top_dirs = []
        for path, top_dirs, files in os.walk(self.PATH):
            for file in files:
                fullpath = path_join(path, file)
                self.sort_file(fullpath)
            break
        
        for i in top_dirs:
            if not self.ALL_DIRS and i in self.TOP_LEVEL_DIRS:
                continue
            dir_path = path_join(self.PATH, i)
            if self.RECURSIVE:
                for path, dirs, files in os.walk(dir_path):
                    for file in files:
                        fullpath = path_join(path, file)
                        self.sort_file(fullpath)
            else:
                self.sort_dir(i)
        if self.CLEAN:
            self.clean_empty_dirs()
                
    def sort_dir(self, dir):
        frm = path_join(self.PATH, dir)
        to = path_join(self.DIRECTORIES_TO, dir)
        if os.path.exists(to):
            debug("Directory exists: {}, skipping", to)            
            return
        shutil.move(frm, self.DIRECTORIES_TO)
        if self.log_moves:
            print("[MoveDir] `{}` --> `{}`".format(frm, to))
        
    def sort_file(self, path):
        listing = split_extension(path)
        fullname = listing[1]
        has_extension = listing[2]!= ""
        #print("[sortFile]: " + path)
        if has_extension:
            fullname = listing[1]+'.'+listing[2]
        if listing[1]=='' and not has_extension:
            self.error(2, "[Error] File with no extension and no name, report this")
            return

        if self.types.has_key(listing[2].lower()):
            to = path_join(self.PATH, self.types[listing[2].lower()], fullname)
        elif not has_extension:
            to = path_join(self.OTHER_FILES_TO, fullname)
        else:
            to = path_join(self.OTHER_FILES_TO, listing[2].upper() + self.UNKNOWN_SUFFIX, fullname)
            self.unknown.add(listing[2].lower())
            
        if os.path.exists(to):
            print("[File already exists]: " + to + ", skipping...", file=sys.stderr)

        if has_extension:
            self.make_path(to, end_is_a_dir=False)

        if self.log_moves:
            print("[Move] `{}` --> `{}`".format(path, to))
        else:
            debug("[Move] `{}` --> `{}`", path, to)

        shutil.move(path, to)
    
    def clean_empty_dirs(self):
        for path, dirs, files in os.walk(self.PATH, topdown=False):
            debug("[Cleaning at] {}", path)
            if len(os.listdir(path))==0:
                os.rmdir(path)
                debug("[RemoveDir] {}", path)
    
    def error(self, code, msg=None):
        if msg:
            print(msg, file=sys.stderr)
        sys.exit(code)
        
    def make_path(self, in_path,end_is_a_dir=True):
        '''Takes a standard UNIX path and creates neccesary directories'''
        if os.path.isdir(in_path):
            return
        parts = in_path.split('/')
        if not end_is_a_dir:
            parts = parts[:-1]
        # Do this in case of windows starting with a drive letter not a /
        path = parts[0]
        if parts[0]=='' :
            path = '/'
            
        parts = parts[1:]
        for i in parts:
            #print("  >[ToMakeParts]: " + path)
            path = path_join(path, i)
            exists = os.path.exists(path)
            is_dir = os.path.isdir(path)
            if not exists:
                os.mkdir(path)
                debug('[MkDir] {}', path)
                continue
            if is_dir:
                continue
            if exists and not is_dir:
                raise OSError("File {} exists, but is not a directory".replace("{}", path))

def path_to_unix(path):
    path = path.replace('\\','/').strip()
    return path

def path_base_dir(path):
    #print("[pathBaseDir] "+ path)
    index = path.find("/",1)
    if index < 0:
        return path
    else:
        return path[:index]

def path_join(*path):
    final = ''
    for i in path:
        i = i.replace("\\",'/')
        final += i + '/'
    final = final.replace("//","/")
    return final[:-1]
    
def split_extension(filename):
    period = filename.rfind('.')
    slash = filename.rfind('/')
    path = ''
    name = ''
    extension = ''
    
    if slash > 0 and period < 0:
        path = filename[:slash+1]
        name = filename[slash+1:]

    elif slash < 0 and period >0:
        name = filename[:period]
        extension = filename[period+1:]

    elif slash < 0 and period < 0:
        name = filename

    elif slash > 0 and period > 0:
        path = filename[:slash+1]
        name = filename[slash+1:period]
        extension = filename[period+1:]
    return path, name, extension


def read_filetype_file(afile):
    import re
    pattern = re.compile(r'(?!#)\s*(.*?)\s*\$(.*)(?<!\s)')
    infile = open(afile)
    data = infile.read(-1)
    filetypes_dict = {}
    for i in pattern.findall(data):
        if(not i[0]=="" and not i[1]==""):
            filetypes_dict[i[0]]=i[1]
    return filetypes_dict

def add_args(parser):
    '''Constructs command line options and reurns a parser'''
    parser.add_argument('directory', help='The directory to be sorted')
    parser.add_argument('-t','--filetypes', help='File containing file types [Default: filetypes.txt]')
    parser.add_argument('-m','--move-directories-to', help='Move directories here[Default: Directories/]')
    parser.add_argument('-o','--other-files', help='Move files of unknown type here [Default: Other/]')
    parser.add_argument('-u','--unknown-filetypes',help='Write unknown filetypes to this file')
    parser.add_argument('-r','--recursive',help='Recursively sort directories', action='store_true')
    parser.add_argument('-c','--clean',help='Recursively removes all empty directories', action='store_true')
    parser.add_argument('-a','--all-dirs',help='Will enter special directories during recursive sort [Default: Disabled]', action='store_true')
    parser.add_argument('-l', '--log-moves', help='Write all file moves to a file', action='store_true')

def get_script_directory():
    path = path_to_unix(os.path.dirname(os.path.abspath(__file__))).split("/")
    script_dir = ''
    for part in path:
        script_dir += part + '/'
    return script_dir
    
def validate_arguments(args):
    """
        Checks whether the paths and options
        provided as commandline arguments are valid.
        The application exits if they are not.    
    """
    script_dir = get_script_directory()
    #start validation
    filetypes = script_dir + "filetypes.txt"
    if args.filetypes:
            filetypes = os.path.join(os.getcwd(), args.filetypes)
    if not os.path.exists(filetypes):
        print("Invalid Filetypes file, please specify an existing file")
        sys.exit(2)
    if not os.path.exists(args.directory):
        print("Invalid Directory, please specify an existing directory")
        sys.exit(3)

def parse(args):
    """ 
        Checks the validity of the given arguments 
        Adjusts the given argumentparser and returns a dictionarry of 
        arguments that should be passed to pySorter
    """
    if args.filetypes:
        args.filetypes = os.path.join(os.getcwd(), args.filetypes)
    else:
        script_dir     = get_script_directory()
        args.filetypes = script_dir + "filetypes.txt"

    if args.unknown_filetypes:
        args.unknown_filetypes = os.path.abspath(args.unknown_filetypes)

    if args.all_dirs:
        args.recursive = True
    
    to_pass = {}
    # The following code remaps the arguments to pysorter arguments
    if args.recursive:
        to_pass['recursive'] = True
    if args.move_directories_to:
        to_pass['move_directories'] = args.move_directories_to
    if args.other_files:
        to_pass['other_files'] = args.other_files
    if args.clean:
        to_pass['clean_empty_dirs'] = True
    if args.all_dirs:
        to_pass['all_dirs'] = True
    if args.log_moves:
        to_pass['log_moves'] = True

    return to_pass

def write_unknown(iterable, path):
    afile = None
    with open(path,'a') as afile:
        for i in iterable:
            afile.write(i)
            afile.write('\n')

def main():
    parser = argparse.ArgumentParser(description='Sort Files in a directory according to their file type')
    
    add_args(parser)
    args = parser.parse_args()

    validate_arguments(args)
    to_pass = parse(args)
    
    sorter = PySorter(args.directory, read_filetype_file(args.filetypes),**to_pass)
    sorter.sort()

    if(args.unknown_filetypes):
        write_unknown(sorter.unknown, args.unknown_filetypes)

if __name__=="__main__":
    #sys.argv = ['pySorter.py', '/tmp/test/','-t', '/home/chris/Development/soft_dev/pySorter/pysorter/filetypes.txt', '-r', '-c']
    main()
