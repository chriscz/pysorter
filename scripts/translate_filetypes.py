"""
A utility script to translate from the new filetypes.txt format
to the new .py alternative
"""

import re
import sys
import os
import argparse
# Comments

DELIM = '-->'
P_COMMENT = re.compile(r'(?<!\\)#[^\n]*\n?')
P_ITEM = re.compile(r'^([^\s]*)\s*' + re.escape(DELIM) + r'\s*([^\s]*?)\s*$', re.MULTILINE)


def process_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help='the input file to traslate')

    return parser.parse_args()

def main(infile):
    with open(infile, 'r') as f:
        data = f.read()

    data = P_COMMENT.sub('', data)
    print '['
    for m in P_ITEM.finditer(data):
        regex, dest = m.groups()
        print "    ({}, {}),".format(repr(regex), repr(dest))
    print ']'

if __name__ == '__main__':
    args = process_arguments()
    main(args.infile)
