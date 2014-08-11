
from openalea.core.path import path as Path

class Data(object):
    def __init__(self, name, path, datatype):
        self.name = name
        self.path = Path(path)
        self.datatype = datatype

def data(category, path, **kwargs):
    content = kwargs['content'] if 'content' in kwargs else None

    path = Path(path)
    if path.isfile():
        if content:
            raise ValueError, 'err'
        else:
            return Data(path.namebase, path, path.ext)
    elif path.exists() :
        raise ValueError, '%s exists but is not a file'
    elif not path.exists():
        if content is None:
            content = b''
        f = path.open('wb')
        f.write(content)
        f.close()
        return Data(path.namebase, path, path.ext)
