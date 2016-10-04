from __future__ import print_function

import logging

import re

from . import action
from .core.util import is_string

log = logging.getLogger(__name__)


class BaseRule(object):
    """
    Base implementation that all sorting rules must extend.
    """

    def destination(self, path):
        """
        Process the given path. If path ends in a `/` it's a directory else it's a file.
        This method can return an absolute or relative destination.

        When a destination ends in `/` the item at the path will me moved *inside*
        that destination, else the item will be moved to the location *at* destination.

        Raises
        ------
        UnhandledPathException:
            if the method cannot handle the given path

        """
        raise NotImplementedError()



class RulesFileRule(BaseRule):
    """
    Default sorint implementation, uses the regex definitions as given in the filetypes.py specification file
    """

    def __init__(self, rules):
        super(RulesFileRule, self).__init__()
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
        raise action.Unhandled

    @classmethod
    def load_from(cls, filepath):
        """
        Loads sorting rules from a text file

        Parameters
        ----------
        filepath

        Returns
        -------
        a RulesFileRule with all the sorting entries

        """
        namespace = {'__builtins__': __builtins__}
        with open(filepath, 'r') as f:
            exec(f.read(), namespace)

        if 'RULES' not in namespace:
            msg = "Configuration file missing RULES: {}".format(filepath)
            raise RuntimeError(msg)

        rules = []
        for item in namespace['RULES']:
            item = list(item)
            item[0] = re.compile(item[0])
            if is_string(item[1]):
                # XXX remove after debugging
                item[1] = make_regex_rule_function(item[0], item[1])
            elif item[1] in action.actionset:
                item[1] = make_return_function(item[1])
            elif callable(item[1]):
                pass
            else:
                msg = "Unhandled type in rule list. " \
                      "Second item in pair must be " \
                      "callable, string or action: " + repr(item[1])
                raise RuntimeError(msg)

            rules.append(item)

        return cls(rules)

def make_return_function(action):
    def function(match, path):
        return action
    return function

def make_regex_rule_function(pattern, dstfmt):
    """
    Creates a new path processing function.
    Does not support moving directories
    """

    def process(match, path):
        # FIXME only match against the filename
        try:
            pargs = [match.group(0)] + list(match.groups())
            destination = dstfmt.format(*pargs,
                                        **match.groupdict())
        except IndexError:
            raise ValueError("Destination string placeholders out of range: {}".format(dstfmt))
        except KeyError as e:
            msg = "Destination string placeholder " \
                  "unknown key {}: {}".format(repr(e.args[0]), dstfmt)
            raise ValueError(msg)
        log.debug("process: RE[%s](%s) --> %s", pattern.pattern, path, destination)
        return destination

    return process
