from __future__ import print_function

import logging

log = logging.getLogger(__name__)


class UnhandledPathException(Exception): pass


class BaseSortRule(object):
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
