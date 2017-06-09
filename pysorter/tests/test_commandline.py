import os
import subprocess
from .. import commandline


def test_help_option():
    basedir = os.path.dirname(commandline.package_directory())
    os.chdir(basedir)

    try:
        env = {'PYTHONPATH': basedir}
        output = subprocess.check_output(
                    ['python', '-m', 'pysorter', '--help'],
                    stderr=subprocess.STDOUT,
                    env=env
        )
    except subprocess.CalledProcessError as e:
        output = e.output

    assert '-d DEST_DIR' in output.decode('utf-8')
