
from openalea.core.path import path as Path
from openalea.vpltk.plugin import iter_plugins
import mimetypes

__all__ = ["data", "dataclass"]

REGISTERY_MIME_CLASS = {}
for ModelClass in iter_plugins('oalab.model'):
    REGISTERY_MIME_CLASS[ModelClass.mimetype] = ModelClass

for DataClass in iter_plugins('oalab.dataclass'):
    REGISTERY_MIME_CLASS[DataClass.mimetype] = DataClass

REGISTERY_NAME_MIME = {}
for ModelClass in iter_plugins('oalab.model'):
    REGISTERY_NAME_MIME[ModelClass.default_name] = ModelClass.mimetype
    REGISTERY_NAME_MIME[ModelClass.extension] = ModelClass.mimetype


for DataClass in iter_plugins('oalab.dataclass'):
    REGISTERY_NAME_MIME[ModelClass.default_name] = DataClass.mimetype
    REGISTERY_NAME_MIME[ModelClass.extension] = DataClass.mimetype

def datatype(path):
    """
    Return mimetype for path.
    First, try to find extension in registery filled by models.
    If datatype is not found, use builtin module "mimetypes".
    If it cannot guess, returns False.

    Search in module allows to specify
    """
    if path:
        ext = Path(path).ext[1:]
        if ext in REGISTERY_NAME_MIME:
            return REGISTERY_NAME_MIME[ext]
        else:
            mtype, encoding = mimetypes.guess_type(path)
            return mtype
    else:
        return False


def dataclass(dtype):
    """
    Return class wich match dtype.
    For example, for 'python' dtype it return PythonModel class.

    Matching can be extended with plugins.
    """
    from openalea.vpltk.datamodel.data import Data
    if dtype in REGISTERY_MIME_CLASS:
        return REGISTERY_MIME_CLASS[dtype]
    else:
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
