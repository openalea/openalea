
from openalea.core.path import path as Path
from openalea.core.service.plugin import plugins
from openalea.core.model import Model

import mimetypes

__all__ = ["ModelFactory", "ModelClass"]

REGISTERY_MIME_CLASS = {}
for pl in plugins('openalea.core', criteria=dict(implement='IModel')):
    REGISTERY_MIME_CLASS[pl.mimetype] = pl

REGISTERY_DTYPE_MIME = {}
for ModelClass in plugins('openalea.core', criteria=dict(implement='IModel')):
    REGISTERY_DTYPE_MIME[pl.dtype.lower()] = pl.mimetype


def ModelClass(dtype=None, mimetype=None):
    """
    Return class wich match dtype.
    For example, for 'python' dtype it return PythonModel class.

    Matching can be extended with plugins.
    if both dtype and mimetype is None, returns all available ModelClasses
    """
    if dtype is None and mimetype is None:
        return set([pl.implementation for pl in REGISTERY_MIME_CLASS.values()] + [Model])

    if mimetype in REGISTERY_MIME_CLASS:
        return REGISTERY_MIME_CLASS[mimetype].implementation
    elif dtype and dtype.lower() in REGISTERY_DTYPE_MIME:
        return ModelClass(mimetype=REGISTERY_DTYPE_MIME[dtype.lower()])
    else:
        return Model


def ModelFactory(*args, **kwds):
    dtype = kwds.pop('dtype', None)
    mimetype = kwds.pop('mimetype', None)
    klass = ModelClass(dtype, mimetype)
    return klass(*args, **kwds)


def to_model(data, mimetype=None):
    # TODO: must be extend with plugins instead of being hard coded
    if isinstance(data, Model):
        return data
    if mimetype is None:
        mimetype = data.mimetype
    kwds = {}
    kwds['code'] = data.read()
    kwds['name'] = data.filename
    dtype = data.dtype
    if mimetype is None and dtype is None:
        return None
    else:
        klass = ModelClass(mimetype=mimetype, dtype=dtype)
        return klass(**kwds)
