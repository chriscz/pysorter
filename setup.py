from setuptools import setup

setup(
        name='pysorter',
        version='0.0.6',
        description='A file-type based organizer',
        url='https://github.com/chriscz/pySorter',
        author='Chris Coetzee',
        author_email='chriscz93@gmail.com',
        license='GPL',
        packages=['pysorter'],
        zip_safe=False,
        entry_points = {
        "console_scripts": ['pysorter = pysorter.pysorter:main']
        },
        package_data={'pysorter': ['*.txt']}
    )
