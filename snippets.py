def path_to_unix(path):
    path = path.replace('\\','/').strip()
    return path

def pathj(*path):
    final = ''
    for i in path:
        i = i.replace("\\",'/')
        final += i + '/'
    final = final.replace("//","/")
    return final
    
