

import pickle

def serialize(data):
    txt = pickle.dumps(data)
    return txt

def unserialize(txt):
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
