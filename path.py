import os
import sys
import re

UNIX = (os.name == "posix")

def to_unix(self, path):
    path = path.replace('\\','/').strip()
    return path

def base_dir(self, path):
    index = path.find("/",1)
    if(index < 0):
        return path
    else:
        return path[:index]

def formatter(self, string, *data):
    None

def join(self, *path):
    final = self.path_to_unix(path[0])
    ends_in_slash = self.path_to_unix(path[-1]).endswith("/")
    if(not final.endswith('/')): 
        final += '/'
    for i in range(1,len(path)):
        j = self.path_to_unix(path[i])
        if(j.startswith('/')):
            j = j[1:]
        if (not j.endswith('/')): 
            j += '/'
        final+=j
    if(ends_in_slash):
        return final
    return final[:-1]
    
def split_extension(self, filename):
    period = filename.rfind('.')
    slash = filename.rfind('/')
    
    path, name, extension = '','',''
    
    if slash > 0 and period < 0:
        path = filename[:slash+1]
        name = filename[slash+1:]
    elif slash < 0 and period >0:
        name = filename[:period]
        extension = filename[period+1:]
    elif slash < 0 and period < 0:
        name = filename
    elif slash > 0 and period > 0:
        path = filename[:slash+1]
        name = filename[slash+1:period]
        extension = filename[period+1:]
    return path, name, extension
