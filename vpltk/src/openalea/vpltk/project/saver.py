from openalea.core.path import path
from openalea.vpltk.plugin import iter_plugins
import warnings
import os


def get_saver(name="GenericSaver"):
    for saver in iter_plugins('vpltk.saver'):
        if saver.default_name == name:
            return saver


class ISaver(object):
    """
    Generic interface class for savers
    """
    def save(self, obj, filename):
        raise NotImplementedError


class GenericSaver(object):
    """
    Classical saver that write str(obj) into file
    """
    default_name = "GenericSaver"
    output_format = "*.py"
    def save(self, obj, filename):
        """
        Store str(obj) into filename
        """
        filename = path(filename)
        try:
            file_ = open(filename, "w")
        except IOError:
            os.makedirs(filename.splitpath()[0])
            file_ = open(filename, "w")
        code = str(obj).encode("utf8", "ignore")
        file_.write(code)
        file_.close()


class CPickleSaver(object):
    """
    Specific saver that use cPickle.dump
    """
    default_name = "CPickleSaver"
    output_format = "*"
    def save(self, obj, filename):
        """
        Store obj into filename
        """
        filename = path(filename)
        try:
            file_ = open(filename, "w")
        except IOError:
            os.makedirs(filename.splitpath()[0])
            file_ = open(filename, "w")
        try:
            import cPickle
            cPickle.dump(obj, file_)
        except ImportError:
            warnings.warn("You must install cPickle.")


class BGEOMSaver(object):
    """
    Specific loader that is used to manipulate PlantGL objects
    """
    default_name = "BGEOMSaver"
    output_format = "*.BGEOM"
    def save(self, obj, filename):
        """
        Store obj into filename
        """
        filename = path(filename)
        try:
            from openalea.plantgl.all import Scene
            sc = Scene()
            sc.add(obj)
            return sc.save(str(filename), "BGEOM")
        except ImportError:
            warnings.warn("You must install PlantGL if you want to load a BGEOM object.")
        except Exception, e:
            print e
            warnings.warn("Impossible to save the scene for object %s into %s" % (obj, filename))
