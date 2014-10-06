import warnings
from openalea.core.path import path
from openalea.core.plugin import iter_plugins

def get_loader(name="GenericLoader"):
    for loader in iter_plugins('vpltk.loader'):
        if loader.default_name == name:
            return loader

class ILoader(object):
    """
    Generic interface class for loaders
    """
    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object
        """
        raise NotImplementedError

class GenericLoader(object):
    """
    Classical loader that read file
    """
    default_name = "GenericLoader"
    input_format = "*.py"
    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from string "text"
        """
        filename = path(filename)
        if filename.exists():
            obj = open(filename, 'rU').read()
            return obj

class BinaryLoader(object):
    default_name = "BinaryLoader"
    input_format = "*"

    def load(self, filename):
        return path(filename)

class PythonLoader(object):
    """
    Classical loader that read file and try to eval object
    """
    default_name = "PythonLoader"
    input_format = "*.py"
    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from string "text"
        """
        filename = path(filename)
        if filename.exists():
            obj = open(filename, 'rU').read()
            try:
                return eval(obj)
            except SyntaxError:
                return obj
            except NameError:
                return obj

class CPickleLoader(ILoader):
    """
    Specific loader that use cPickle.loads
    """
    default_name = "CPickleLoader"
    input_format = "*"
    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from filename
        """
        filename = path(filename)
        if filename.exists():
            cpik = "False"
            try:
                import cPickle
                cpik = "True"
            except ImportError:
                warnings.warn("You must install cPickle.")
            if cpik:
                try:
                    file_ = open(filename, "r")
                    ret = cPickle.load(file_)
                    file_.close()
                    return ret
                except Exception, e:
                    print "Can't load file " + filename + " with loader CPickleLoader. "
                    print e

class BGEOMLoader(ILoader):
    """
    Specific loader that is used to manipulate PlantGL objects
    """
    default_name = "BGEOMLoader"
    input_format = "*.BGEOM"
    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from string "text"
        """
        filename = path(filename)
        if filename.exists():
            try:
                from openalea.plantgl.all import Scene
                sc = Scene()
                sc.clear()
                sc.read(str(filename), "BGEOM")
                return sc
            except ImportError:
                warnings.warn("You must install PlantGL if you want to load a BGEOM object.")
            except Exception, e:
                print e
                warnings.warn("Impossible to load the scene")
