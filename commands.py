import os
import sys

from setuptools import Command
from setuptools.command.test import test as TestCommand

name = 'pysorter'
base_dir = os.path.dirname(__file__)

def version_path():
    return os.path.join(base_dir, name, 'version.txt')

def read_version():
    return open(version_path()).read().strip()

def write_version(string):
    f = open(version_path(), 'w')
    f.write(string)
    f.write('\n')

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

class BumpVersionCommand(Command):
    description = "bumps the versions minor "
    user_options = [
        ('field=', None, 'which field should be bumped: major, minor or patch?')
    ]

    def initialize_options(self):
        self.cwd = None
        self.field = 'patch'
        self.field_index = {'major':0, 'minor':1, 'patch':2}

    def finalize_options(self):
        self.cwd = os.getcwd()
        assert self.field in ('major', 'minor', 'patch'), 'Invalid field!'


    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        current = read_version()
        version = [int(_) for _ in current.split('.')]
        version[self.field_index[self.field]] += 1
        for i in range(self.field_index[self.field] + 1, len(self.field_index)):
            version[i] = 0


        version = '.'.join([str(_) for _ in version])
        write_version(version)
        print("version bumped {} --> {}".format(current, version))
    

class PyTestCommand(TestCommand):
    """Setup the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = []# ['--cov', name]
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))
