

import pickle

def serialize(data):
    txt = pickle.dumps(data)
    return txt

def unserialize(txt):
    data = pickle.loads(txt)
    return data
