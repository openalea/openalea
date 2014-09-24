from openalea.core.project.saver import GenericSaver
from openalea.core.project.loader import GenericLoader, PythonLoader
from openalea.core.path import path
import os


def test_python_str():
    obj1 = "this is a beautifull test text"
    filename = path("temp.py")
    saver = GenericSaver()
    saver.save(obj1, filename)
    loader = GenericLoader()
    obj2 = loader.load(filename)
    assert obj1 == obj2

    if filename.exists():
        os.remove(filename)


def test_python_dict():
    obj1 = {'test1': True, 'test2': 42, 'test3': 'ok'}
    filename = path("temp.py")
    saver = GenericSaver()
    saver.save(obj1, filename)
    loader = PythonLoader()
    obj2 = loader.load(filename)
    assert obj1 == obj2

    if filename.exists():
        os.remove(filename)
        

def test_python_int():
    obj1 = 42
    filename = path("temp.py")
    saver = GenericSaver()
    saver.save(obj1, filename)
    loader = PythonLoader()
    obj2 = loader.load(filename)
    assert obj1 == obj2

    if filename.exists():
        os.remove(filename)
