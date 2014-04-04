from openalea.core.path import path    
import warnings    
    
class ISaver(object):
    """
    Generic class for savers
    """
    def save(self, obj, filename):
        """
        Store obj into filename
        """
        filename = path(filename)
        
        file_ = open(filename, "w")
        code = str(obj).encode("utf8","ignore") 
        file_.write(code)
        file_.close()
        
class CPickleSaver(ISaver):
    """
    Specific saver that use cPickle.dump
    """
    def save(self, obj, filename):
        """
        Store obj into filename
        """
        filename = path(filename)
        file_ = open(filename, "w")
        try:
            import cPickle
            cPickle.dump(obj, file_)
        except ImportError:
            warnings.warn("You must install cPickle.")
        
class BGEOMSaver(ISaver):
    """
    Specific loader that is used to manipulate PlantGL objects
    """
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
            warnings.warn("Impossible to save the scene for object %s into %s"%(obj,filename))        
