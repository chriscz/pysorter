import re
import logging
from rule import UnhandledPathException

log = logging.getLogger(__name__)

# Comments
DELIM = '-->'
P_COMMENT = re.compile(r'(?<!\\)#[^\n]*\n?')
P_ITEM = re.compile(r'^(.*)\s*' + re.escape(DELIM) + r'\s*(.*?)\s*$')
P_IMPORT = re.compile(r'^from \s*([\d\w_]*)\s* import ([\d\w_]*)\s*;\s*$')


def process_item(match, line_count):
    if not match:
        return None

    # take out the bits and pieces
    regex = match.group(1).strip()
    destination = match.group(2).strip()

    try:
        regex = re.compile(regex)
    except:
        raise ValueError("L{}: Bad Regex".format(line_count))

    return regex, destination


def parse(text):
    items = []

    # strip all the comments
    text = P_COMMENT.sub("\n", text)

    # replace all escaped hashes with single hash

    text = text.replace('\\#', '#')

    lines = text.split('\n')

    line_count = 0
    for line in lines:
        # strip all blanks
        line = line.strip()

        line_count += 1
        if not line: continue

        processed = process_item(P_ITEM.match(line), line_count)
        if processed:

        else:
            processed = process_item(P_IMPORT.match(line), line_count)

        if not processed:
            raise ValueError("[L{}]: Incorrect syntax for rule/import".format(line_count))

        items.append(processed)
    return items


if __name__ == "__main__":
    import sys

    f = open(sys.argv[1], 'r')
    from pprint import pprint

    pprint(parse(f.read()))
