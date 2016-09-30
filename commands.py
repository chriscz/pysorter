import os

from setuptools import Command


# --------------------------------------------------------------------------
#  Custom setup commands
# --------------------------------------------------------------------------
class CoverageCommand(Command):
    description = "generates a coverage report"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system("py.test --cov-report 'html:{}/coverage_report' --cov=pysorter".format(os.getcwd()))
