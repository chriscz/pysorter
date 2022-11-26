[![GitHub version](https://badge.fury.io/gh/chriscz%2Fpysorter.svg)](https://badge.fury.io/gh/chriscz%2Fpysorter)
[![PyPI version](https://badge.fury.io/py/pysorter.svg)](https://badge.fury.io/py/pysorter)
[![Build Status](https://travis-ci.org/chriscz/pysorter.svg?branch=master)](https://travis-ci.org/chriscz/pysorter)
[![Coverage Status](https://coveralls.io/repos/github/chriscz/pysorter/badge.svg?branch=master)](https://coveralls.io/github/chriscz/pysorter?branch=master)

# Pysorter

A Commandline utility for organizing files and directories according to regex patterns.

## Quick Start
  * `pip install pysorter`
  * `pysorter`

## Commandline Synopsys
```
usage: pysorter [-h] [-d DEST_DIR] [-p] [-t FILETYPES] [-u UNHANDLED_FILE]
                [-r] [-c] [-n] [-V]
                directory

Reorganizes files and directories according to certain rules

positional arguments:
  directory             The directory to be organized

optional arguments:
  -h, --help            show this help message and exit
  -d DEST_DIR, --destination DEST_DIR
                        The destination directory to move organized files to.
  -p, --process-dirs    Should directories also be matched against the rules?
  -t FILETYPES, --filetypes FILETYPES
                        File containing regex rules [Default: filetypes.py]
  -u UNHANDLED_FILE, --unhandled-file UNHANDLED_FILE
                        Write the paths of all unhandled items to this file
  -r, --recursive       Recursively organize directories
  -c, --remove-empty-dirs
                        Recursively removes all empty directories in the
                        directory being organized.
  -n, --dry-run         Prints out the changes that would occur, without
                        actually executing them.
  -V, --version         Prints out the current version of pysorter
```

## Configuration
Pysorter ships with a default rules file that has entries for many common 
file types. As a user of pysorter, you are encouraged to add your own rules
using `pysorter/filetypes.py` file for inspiration.

### Example 1
Suppose we would like all our pdfs to be placed under a pdf directory, 
located under `/home/chris/sorted/documents/`. As a first step we must write
a *rules* file. This file is a normal Python module that defines where
certain files will be moved to.

```python
    RULES = [
        # regex pattern, destination
        (r'.*\.pdf$', 'documents/pdf/' ),
    ]
```

#### Notes
 * Rules are attempted in the order they are defined. As soon as a match is found,
   we use its destination.
 * The slash in the destination (`documents/pdf/`) is important, as all pdfs will be placed 
   in the `documents/pdf/` directory. If the slash was removed as in `document/pdf`, then all pdfs would be
   moved to a file named `pdf` in the directory `document`. Which is definitely not what you wanted!
 * The destination could also be a Python that will be called during processing.

### Example 2
We would like all images downloaded from facebook to be located under `images/facebook/` instead of 
putting them directly inside `images/`. You'll notice that facebook images end in `_n.jpg`.
We would like to strip away that prefix as well. So we write the following rule,

```python
    RULES = [
        # ... some other rules ...
        (r'(?P<filename>[^/]+)_n.jpe?g$', 'images/facebook/{filename}.jpg')
        # ... yet some more rules ...
    ]
```
#### Notes
This example might look complicated, but it is really just using standard Python
functionality. To break it down.
 * `(?P<filename>[^/]+)` is a named capturing group, it matches any character that is not a 
   `/`, therefore the filename without extension. Here are some example matches

   * `tosort/myphoto_n.jpg`. *filename=myphoto*
   * `tosort/foo/y123_n.jpg`. *filename=y123*
 * In the destination of the rule we can make use of both named and unnamed capturing 
   groups.

You can look at the `pysorter.filetypes` module for some more inspiration.

## Caveats
The [Python shutil library](https://docs.python.org/3/library/shutil.html) used by pysorter carries the following warning:

```
Warning 
Even the higher-level file copying functions (shutil.copy(), shutil.copy2()) cannot copy all file metadata.

- On POSIX platforms, this means that file owner and group are lost as well as ACLs. 
- On Mac OS, the resource fork and other metadata are not used. 
  This means that resources will be lost and file type and 
  creator codes will not be correct. 
- On Windows, file owners, ACLs and alternate data streams are not copied.
```

If the files are on the same filesystem, then neither `copy` nor `copy2` are actually used,
so there shouldn't be *any* risks involved. 

If you still feel unsure, feel free to [create an issue](https://github.com/chriscz/pysorter/issues/new),
and we'll try our best to help. 

## Requirements
Python version:
 * 3.3
 * 3.4
 * 3.5

## Contributing
See the [guide](CONTRIBUTING.md).

