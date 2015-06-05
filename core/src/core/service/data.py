
from openalea.core.path import path as Path
from openalea.core.plugin import iter_plugins
from openalea.core.data import Data

import mimetypes

__all__ = ["DataFactory", "DataClass", "MimeType", "DataType"]

REGISTERY_MIME_CLASS = {}
for DataClass in iter_plugins('oalab.dataclass'):
    REGISTERY_MIME_CLASS[DataClass.mimetype] = DataClass
# for ModelClass in iter_plugins('oalab.model'):
#     REGISTERY_MIME_CLASS[ModelClass.mimetype] = ModelClass

REGISTERY_NAME_MIME = {}
for DataClass in iter_plugins('oalab.dataclass'):
    REGISTERY_NAME_MIME[DataClass.default_name.lower()] = DataClass.mimetype
    REGISTERY_NAME_MIME[DataClass.extension.lower()] = DataClass.mimetype

# for ModelClass in iter_plugins('oalab.model'):
#     REGISTERY_NAME_MIME[ModelClass.default_name.lower()] = ModelClass.mimetype
#     REGISTERY_NAME_MIME[ModelClass.extension.lower()] = ModelClass.mimetype


def MimeType(path=None, name=None):
    """
    Return mimetype for path.
    First, try to find extension in registery filled by models.
    If datatype is not found, use builtin module "mimetypes".
    If it cannot guess, returns False.

    Search in module allows to specify
    """
    if path:
        name = Path(path).ext[1:].lower()
        if name in REGISTERY_NAME_MIME:
            return REGISTERY_NAME_MIME[name]
        else:
            mtype, encoding = mimetypes.guess_type(path)
            return mtype
    else:
        name = name.lower()
        if name in REGISTERY_NAME_MIME:
            return REGISTERY_NAME_MIME[name]
        else:
            return False


def DataType(path=None, name=None, mimetype=None):
    if path:
        name = Path(path).ext[1:].lower()
        return name
    elif name:
        return Path(name).ext[1:].lower()
    elif mimetype:
        #         for ModelClass in iter_plugins('oalab.model'):
        #             if ModelClass.mimetype == mimetype:
        #                 return ModelClass.default_name
        for DataClass in iter_plugins('oalab.dataclass'):
            if DataClass.mimetype == mimetype:
                return DataClass.default_name
    else:
        return None


def DataClass(dtype=None):
    """
    Return class wich match dtype.
    For example, for 'python' dtype it return PythonModel class.

    Matching can be extended with plugins.
    if dtype is None, returns all available DataClasses
    """
    if dtype in REGISTERY_MIME_CLASS:
        return REGISTERY_MIME_CLASS[dtype]
    else:
        return Data

DataClass.all = set(REGISTERY_MIME_CLASS.values() + [Data])


def arrange_data_args(path, mimetype, dtype):
    if mimetype is None:
        if dtype:
            return path, MimeType(name=dtype)
        elif path:
            return path, MimeType(path=path)
        else:
            return path, None
    else:
        if dtype:
            new_mimetype = MimeType(name=dtype)
            if mimetype != new_mimetype:
                raise ValueError('dtype %r (%s) and mimetype %r are not compatible' % (
                    dtype, new_mimetype, mimetype))
        return path, mimetype


def DataFactory(path, mimetype=None, **kwargs):
    path = Path(path)
    default_content = kwargs['default_content'] if 'default_content' in kwargs else None
    dtype = kwargs.pop('dtype', None)

    if path.isfile():
        if default_content is not None:
            raise ValueError(
                "got multiple values for content (parameter and '%s')" % path.name)
        else:
            path, mimetype = arrange_data_args(path, mimetype, dtype)
            klass = DataClass(mimetype)
            return klass(path=path, mimetype=mimetype)
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

        path, mimetype = arrange_data_args(path, mimetype, dtype)
        klass = DataClass(mimetype)
        return klass(path=path, mimetype=mimetype, content=content)


def to_data(model, mimetype):
    # TODO: check filename/filepath/path argument
    # TODO: must be extended using plugins
    klass = DataClass(DataType(mimetype=mimetype))
    kwds = {}
    if 'filename' not in kwds:
        kwds['filename'] = model.name + '.' + klass.extension
    kwds['dtype'] = model.dtype
    kwds['mimetype'] = klass.mimetype
    data = klass(**kwds)
    data.content = model.repr_code()


def get_data(name):
    from openalea.core.project.manager import ProjectManager
    pm = ProjectManager()
    data = pm.cproject.get_item('data', name)
    return data
