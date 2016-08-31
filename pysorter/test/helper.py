import cStringIO as sio


def mkfiletypesstr(mapping):
    """
    Takes a string to string mapping and
    writes them as a mapping, returns a string
    """

    f = sio.StringIO()
    for k, v in mapping.iteritems():
        l = [k, ' --> ', v, '\n']
        f.write(''.join(l))

    return f.getvalue()
