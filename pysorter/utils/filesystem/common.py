import os


class File(object):
    """
    A light file wrapper that supports some basic operations and
    checks.
    """

    def __init__(self, parent, name, relative_to=None):
        self._relative_to = relative_to

        if relative_to:
            assert not os.path.isabs(parent)
        else:
            assert os.path.isabs(parent)

        self.parent = parent
        self.name = name

    @property
    def full_path(self):
        if self._relative_to:
            return os.path.join(self._relative_to, self.parent, self.name)
        return os.path.join(self.parent, self.name)

    @property
    def relative_path(self):
        return os.path.join(self.parent, self.name)

    @property
    def is_dir(self):
        return os.path.isdir(self.full_path)

    @property
    def is_link(self):
        return os.path.islink(self.full_path)

    @property
    def is_file(self):
        return os.path.isfile(self.full_path)

    @property
    def extension(self):
        _, extension = os.path.splitext(self.name)

        if extension:
            # strip the dot
            extension = extension[1:]
        return extension
