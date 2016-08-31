import shutil
import os


def move_file(src, dst):
    if not os.path.isfile(src):
        raise OSError("Source path is not a file: {}".format(src))
    shutil.move(src, dst)
