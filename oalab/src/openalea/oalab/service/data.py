
from openalea.core.path import path as Path

class Data(object):
    def __init__(self, name, path, datatype):
        self.name = name
        self.path = Path(path)
        self.datatype = datatype

def datatype(path):
    return path.ext

def dataname(path):
    return path.namebase

def dataclass(dtype):
    """
    Return class wich match dtype.
    For example, for 'python' dtype it return PythonModel class.

    Matching can be extended with plugins.
    """
    return Data

def arrange_data_args(name, path, dtype):
    if name is None:
        name = dataname(path)
    if dtype is None:
        dtype = datatype(path)
    return name, path, dtype

def data(path, name=None, dtype=None, **kwargs):
    content = kwargs['content'] if 'content' in kwargs else None

    path = Path(path)
    if path.isfile():
        if content is not None:
            raise ValueError, "got multiple values for content (parameter and '%s')" % path.name
        else:
            name, path, dtype = arrange_data_args(name, path, dtype)
            DataClass = dataclass(dtype)
            return DataClass(name, path, dtype)
    elif path.exists() :
        raise ValueError, '%s exists but is not a file'
    elif not path.exists():
        if content is None:
            content = b''
        f = path.open('wb')
        f.write(content)
        f.close()
        name, path, dtype = arrange_data_args(name, path, dtype)
        DataClass = dataclass(dtype)
        return DataClass(name, path, dtype)
