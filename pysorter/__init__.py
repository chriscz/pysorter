import os
BASE = os.path.dirname(__file__)
__version__ = open(os.path.join(BASE, 'version.txt')).read().strip()

del BASE
del os
