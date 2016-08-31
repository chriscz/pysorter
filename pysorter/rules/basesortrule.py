from __future__ import print_function

import logging

log = logging.getLogger(__name__)


class UnhandledPathException(Exception):
    """
    Raised by a RuleSet if it does not know how to organize the given file
    or directory.
    """


class BaseSortRule(object):
    """
    Base implementation that all sorting rules must extend.
    """

    def process(self, file_entity):
        """
        processes the given entity (file or directory), returning the destination.
        The destination can be either relative or absolute
        where the entity must be moved to.
         If the entity cannot be handled and UnhandledPathException should be
        raised.
        """
        raise NotImplementedError()
