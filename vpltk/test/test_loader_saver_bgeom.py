from openalea.vpltk.project.saver import BGEOMSaver
from openalea.vpltk.project.loader import BGEOMLoader
from openalea.plantgl.all import Sphere, Scene
from openalea.core.path import path
import os


def test_sphere():
    obj1 = Sphere()
    filename = path("temp.bgeom")
    saver = BGEOMSaver()
    saver.save(obj1, filename)
    loader = BGEOMLoader()
    obj2 = loader.load(filename)

    # TODO
    # How to know if obj1 == obj2 ?
    assert obj2 is not None
    assert isinstance(obj2, Scene)
    assert obj2 != obj2.clear()

    if filename.exists():
        os.remove(filename)


def test_scene():
    obj1 = Scene()
    filename = path("temp.bgeom")
    saver = BGEOMSaver()
    saver.save(obj1, filename)
    loader = BGEOMLoader()
    obj2 = loader.load(filename)

    # TODO
    # How to know if obj1 == obj2 ?
    assert obj2 is not None
    assert isinstance(obj2, Scene)

    if filename.exists():
        os.remove(filename)
