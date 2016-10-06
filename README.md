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

## Requirements
Python version:
 * 2.7
 * 3.3
 * 3.4
 * 3.5

## Contributing
See the [guide](CONTRIBUTING.md).
