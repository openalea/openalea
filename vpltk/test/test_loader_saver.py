from openalea.vpltk.project.saver import ISaver
from openalea.vpltk.project.loader import ILoader
from openalea.core.path import path
import os

def test_python_dict():
    obj1 = {'test1': True, 'test2': 42, 'test3': 'ok'}
    filename = path("temp.py")
    saver = ISaver()
    saver.save(obj1, filename)
    loader = ILoader()
    obj2 = loader.load(filename)
    assert obj1 == obj2

    if filename.exists():
        os.remove(filename)
        
def test_python_str():
    obj1 = "this is a beautifull test text"
    filename = path("temp.py")
    saver = ISaver()
    saver.save(obj1, filename)
    loader = ILoader()
    obj2 = loader.load(filename)
    assert obj1 == obj2

    if filename.exists():
        os.remove(filename)

def test_python_int():
    obj1 = 42
    filename = path("temp.py")
    saver = ISaver()
    saver.save(obj1, filename)
    loader = ILoader()
    obj2 = loader.load(filename)
    assert obj1 == obj2

    if filename.exists():
        os.remove(filename)
