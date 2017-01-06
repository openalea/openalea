# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

from openalea.core.plugin import iter_plugins

def get_saver(name="GenericSaver"):
    for saver in iter_plugins('vpltk.saver'):
        if saver.default_name == name:
            return saver
    raise TypeError('saver plugin not found: ' + str(name))

def get_loader(name="GenericLoader"):
    for loader in iter_plugins('vpltk.loader'):
        if loader.default_name == name:
            return loader

def save(data, path, fmt=None, **kwds):
    pass

def load(path, fmt=None, **kwds):
    pass

def serialize(data, fmt=None, **kwds):
    import pickle
    txt = pickle.dumps(data)
    return txt

def deserialize(txt, fmt=None, **kwds):
    import pickle
    data = pickle.loads(txt)
    return data

def picklable_object(obj):
    """
    Returns a picklable wrapper of obj.
    This service is used to pickle objects that are not natively pickable
    and that cannot be modified to be compatible with pickle.

    entry_point:
    openalea.pickler
    """
    pass

#
# serialization.py ends here
