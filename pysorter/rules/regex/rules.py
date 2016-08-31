from __future__ import print_function

import logging

log = logging.getLogger(__name__)

from ..basesortrule import BaseSortRule, UnhandledPathException
from . import parsefile


class RegexSortRule(BaseSortRule):
    """pysorter default implementation, uses the regex definitions as given in the
    filetypes.txt specification file
    """

    def __init__(self, rules):
        super(RegexSortRule, self).__init__()
        self.rules = rules

    def first_match(self, finditer):
        for match in finditer:
            return match
        return None

    def process(self, entity):
        for R, function in self.rules:
            match = self.first_match(R.finditer(entity.name))
            if match:
                return function(match, entity)
        raise UnhandledPathException()

    @classmethod
    def load_from(cls, filepath):
        with open(filepath, 'r') as f:
            text = f.read()
        regexes = parsefile.parse(text)
        return cls(regexes)


def make_path_rule(pattern, path):
    """Creates a new path processing function"""
    def process(match, entity):
        # dont't handle directories
        if entity.is_dir:
            log.debug("process: is_dir --> skip(%s)", entity.full_path)
            raise UnhandledPathException()
        # FIXME only match against the filename
        name = entity.name
        # NOTE TODO Only uses the first match!
        groups = (match.group(0),) + match.groups()
        destination = path.format(*groups)
        log.debug("process: RE[%s](%s) --> %s", pattern.pattern, name, destination)
        return destination

    # attach special attributes for identification of functions
    # TODO

    return process

# Alternative name
path_rule = make_path_rule
