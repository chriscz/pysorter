import os
import pytest
from testfixtures.tempdirectory import TempDirectory

@pytest.fixture()
def tempdir():
    with TempDirectory() as d:
        os.chdir(d.path)
        yield d
