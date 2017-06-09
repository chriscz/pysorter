"""
Module for the base regex rule implementation
"""
from __future__ import print_function

import logging
import re

log = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------
class Unhandled(Exception):
    """
    Raised or returned when a path cannot be handled by the
    function.
    """

class Skip(Exception):
    """
    Riased or returned when a path should be skipped from moving.
    """

class SkipRecurse(Exception):
    """
    Raised or returned when a directory path should not
    be recursed into. 
    
    The directory itself may still be relocated though.
    """

actions = frozenset([Unhandled, Skip, SkipRecurse])


class RulesFileClassifier(object):
    """
    Default rule implementation that 
    uses the regex definitions as given in a `filetypes.py` specification file.
    
    """

    def __init__(self, rules):
        super(RulesFileClassifier, self).__init__()
        self.rules = rules

    def first_match(self, finditer):
        for match in finditer:
            return match
        return None

    def destination(self, path):
        for R, function in self.rules:
            match = self.first_match(R.finditer(path))
            if match:
                return function(match, path)
        raise Unhandled

    @classmethod
    def load_file(cls, path):
        """
        Loads sorting rules from a text file and return 
        a RulesFileClassifier containing all the sorting entries.
        """
        namespace = {'__builtins__': __builtins__}
        with open(path, 'r') as f:
            exec(f.read(), namespace)

        if 'RULES' not in namespace:
            msg = "Configuration file missing RULES: {}".format(path)
            raise RuntimeError(msg)

        rules = []
        for regex, destination in namespace['RULES']:
            pattern = re.compile(regex)
            matcher = None

            if is_string(destination):
                # destination --> format string
                matcher = make_regex_rule_function(pattern, destination)
            elif destination in actions:
                # constant action ex. Skip
                matcher = make_constant_function(destination)
            elif callable(destination):
                # custom processing_function(re_match, filepath)
                matcher = destination
            else:
                msg = "Unhandled type in rule list. " \
                      "Second item in pair must be " \
                      "callable, string or action: " + repr(destination)
                raise ValueError(msg)

            rules.append((pattern, matcher))

        return cls(rules)

    def __call__(self, path):
        return self.destination(path)


def is_string(obj):
    import sys

    PY3 = sys.version_info[0] == 3

    if PY3:
        string_types = str,  # pragma: no cover
    else:
        string_types = basestring, str  # pragma: no cover
    return isinstance(obj, string_types)


def make_constant_function(action):
    """Return a function that always returns `action`, regardless of its arguments"""

    def function(*args):
        return action

    return function


def make_regex_rule_function(pattern, dstfmt):
    """
    Return a path processing function. 
    """

    def process(re_match, path):
        """
        
        Parameters
        ----------
        re_match: regex match
        path: str
            original path that was used to create `match`

        Returns
        -------

        """
        # FIXME only re_match against the filename
        try:
            pargs = [re_match.group(0)] + list(re_match.groups())
            destination = dstfmt.format(*pargs,
                                        **re_match.groupdict())
        except IndexError:
            raise ValueError("Destination string placeholders out of range: {}".format(dstfmt))
        except KeyError as e:
            msg = "Destination string placeholder " \
                  "unknown key {}: {}".format(repr(e.args[0]), dstfmt)
            raise ValueError(msg)
        log.debug("process: RE[%s](%s) --> %s", pattern.pattern, path, destination)
        return destination

    return process
