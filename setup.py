from setuptools import setup
import os

name = 'pysorter'
base_dir = os.path.dirname(__file__)

setup(
        name='pysorter',
        version=open(os.path.join(base_dir, name, 'version.txt')).read().strip(),
        description='A file-extension based organizer',
        license='GPL',
        url='https://github.com/chriscz/pySorter',

        author='Chris Coetzee',
        author_email='chriscz93@gmail.com',
        
        packages=['pysorter'],

        include_package_data = True,
        zip_safe=False,

        entry_points = {
            "console_scripts": ['pysorter = pysorter.core.pysorter:main']
        },
        extras_require=dict(
            test=['pytest', 'testfixtures', 'pytest-cov'],
            build=[]
        ),
    )
