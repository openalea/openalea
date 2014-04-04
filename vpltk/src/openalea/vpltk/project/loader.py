import warnings
from openalea.core.path import path

class ILoader(object):
    """
    Generic class for loaders
    """    
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
    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from filename
        """
        filename = path(filename)
        if filename.exists():
            try:
                import cPickle
                file_ = open(filename, "r")
                ret = cPickle.load(file_)
                file_.close()
                return ret
            except ImportError:
                warnings.warn("You must install cPickle.")
        
class BGEOMLoader(ILoader):
    """
    Specific loader that is used to manipulate PlantGL objects
    """
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
