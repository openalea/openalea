
from openalea.core.path import path as Path
from openalea.vpltk.plugin import iter_plugins


__all__ = ["data", "dataclass"]


def datatype(path):
    if path.ext:
        return path.ext[1:]
    else:
        return None


def dataclass(dtype):
    """
    Return class wich match dtype.
    For example, for 'python' dtype it return PythonModel class.

    Matching can be extended with plugins.
    """
    from openalea.vpltk.datamodel.data import Data
    return Data


def arrange_data_args(path, dtype):
    if dtype is None:
        dtype = datatype(path)
    return path, dtype


def data(path, dtype=None, **kwargs):
    path = Path(path)
    default_content = kwargs['default_content'] if 'default_content' in kwargs else None

    if path.isfile():
        if default_content is not None:
            raise ValueError("got multiple values for content (parameter and '%s')" % path.name)
        else:
            path, dtype = arrange_data_args(path, dtype)
            DataClass = dataclass(dtype)
            return DataClass(path=path, dtype=dtype)
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

        path, dtype = arrange_data_args(path, dtype)
        DataClass = dataclass(dtype)
        return DataClass(path=path, dtype=dtype, content=content)
