
from openalea.core.path import path as Path
from openalea.vpltk.plugin import iter_plugins


__all__ = ["data", "dataclass"]


def datatype(path):
    if path.ext:
        return path.ext[1:]
    else:
        return None


def dataname(path):
    return path.namebase


def dataclass(dtype):
    """
    Return class wich match dtype.
    For example, for 'python' dtype it return PythonModel class.

    Matching can be extended with plugins.
    """
    from openalea.oalab.model.model import Data
    return Data


def arrange_data_args(name, path, dtype):
    if name is None:
        name = dataname(path)
    if dtype is None:
        dtype = datatype(path)
    return name, path, dtype


def data(path, name=None, dtype=None, **kwargs):
    default_content = kwargs['default_content'] if 'default_content' in kwargs else None

    path = Path(path)
    if path.isfile():
        if default_content is not None:
            raise ValueError("got multiple values for content (parameter and '%s')" % path.name)
        else:
            name, path, dtype = arrange_data_args(name, path, dtype)
            DataClass = dataclass(dtype)
            return DataClass(name, path, dtype)
    elif path.exists():
        raise ValueError("'%s' exists but is not a file" % path)
    elif not path.exists():
        if default_content is None:
            default_content = b''
        try:
            f = path.open('wb')
        except IOError:
            content = default_content
        else:
            f.write(default_content)
            f.close()
            content = None

        name, path, dtype = arrange_data_args(name, path, dtype)
        DataClass = dataclass(dtype)
        return DataClass(name, path, dtype, content=content)
