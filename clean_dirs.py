import os
import sys
import shutil

def clean_empty_dirs(p):
    for path, dirs, files in os.walk(p, topdown=False):
        #print("[Cleaning at]: "+ path)
        if(len(os.listdir(path))==0):
            #os.rmdir(path)
            print("[RmDir]: " + path)
if __name__ == "__main__":
    clean_empty_dirs(sys.argv[1])
