
from __future__ import print_function

import pytest

from .. import rules

def test_no_rules_in_file(tempdir):
    tempdir.write('filetypes.py', 'import os', 'utf-8')
    with pytest.raises(RuntimeError) as excinfo:
        rules.RulesFileClassifier.load_file('filetypes.py')
    assert 'missing RULES' in str(excinfo.value)

def test_bad_rule(tempdir):
    tempdir.write('filetypes.py', "RULES = [('a', 1)]", 'utf-8')
    with pytest.raises(ValueError) as excinfo:
        rules.RulesFileClassifier.load_file('filetypes.py')
    assert 'unhandled type in rule list' in str(excinfo.value).lower()
