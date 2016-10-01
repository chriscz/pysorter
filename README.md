[![Build Status](https://travis-ci.org/chriscz/pysorter.svg?branch=master)](https://travis-ci.org/chriscz/pysorter)
[![Coverage Status](https://coveralls.io/repos/github/chriscz/pysorter/badge.svg?branch=master)](https://coveralls.io/github/chriscz/pysorter?branch=master)

Pysorter
========
Commandline utility for organizing files into predefined directories according to their filetype.

To add your own sorting rules make a copy of  `pysorter/filetypes.py`.
The file is a normal python scripy with a dictionary definition `RULES`,
in the global scope. Rules are tuples of the form (regex_string, callable or string).
For more information, read the comment in the `filetypes.py` file.

As stated in the python documentation, the shutil library may not copy all file metadata.
This will not affect the content of your files, however

## Quick Start
  * `pip install pysorter`
  * `pysorter`

# Requirements
Python version:
 * 2.7
 * 3.3
 * 3.4
 * 3.5

## Releases / Revisions / Changes 

The following will be kept for historical reasons. The future numbering of releases will 
follow a form of semantic versioning.

### Alpha Release 0.0.5 (Repository) 
  * Change version numbering to something more sensible
  * Add setup.py script

### Alpha Release 4.0.2
  * Tested on Windows
  * Refactoring
  * Started rewriting filetypes.txt
  * Added option for empty directory removal

### Alpha Release 4.0.0 17 May 2013
  * Complete rewrite
  * Removed TUI (Text User Interface) <Linux users don't need this =P>
  * Removed configuration file, write a script if you need to store config
  * Standalone Script
  * Added recursive sorting
  * Python2.7 compatibility
  * *Issues*
    * Exceptions that are not handled
      * Write/Read permission denied on move_dir
    * Not yet tested on Windows
        
### Fifth Revision: 11 June 201
  * Now has a TUI (Text User Interface)
  * Exceptions moved to the ioExcept file
  * New menu and config parsers
  * TUI Documentation

### Fourth Revision: 28 May 2010(Released with v3)
  * Fixed a bug when parsing the filetypes file
  * Enabled comments in config files
  * Improved Readablility of source
  * Moved file parsing methods to a new file: ioReader
  * New pySorter.conf, that can be used instead of the comand line

### Third Revision: 18 May 2010
  * Now handles most important exceptions(File moving etc.)
  * Now uses pyParser for command-line parsing. pyParser is a fully featured command-line parsing tool for novices
  * All code has been rewritten and comments added
  * Runs only on Python 3.1 and up, (backports of python 3.1 available for Ubuntu, search Google)
  * If backported to older versions of python, shuttle library of python 2.6 >= is required
  * New default option for getting the job done faster


### Second Revision: 02 April 2010
  * Now uses infinite.eparser for command-line processing

First Revision: 2009 December

Created: 2009 November
