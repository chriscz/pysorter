# Raised / returned when path cannot be handled
class Unhandled(Exception): pass


# Raised / returned when a path should be skipped
class Skip(Exception): pass


# Raised / returned when a directory path should be skipped and
# not recursed into
class SkipRecurse(Exception): pass


actionset = frozenset([Unhandled, Skip, SkipRecurse])