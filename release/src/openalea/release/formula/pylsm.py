from openalea.release import Formula
from openalea.release.utils import with_original_sys_path

class pylsm(Formula):
    license = "PYLSM License."
    authors = "Freesbi.ch"
    description = "Patched version of PyLSM"  
    py_dependent   = True
    arch_dependent = False
    version = "0.1-r34"
    
    @property 
    @with_original_sys_path
    def package(self):
        return __import__(self.packagename)
        
    def configure(self):
        return True
        
    def make(self):
        return True
        
    def install(self):
        return True
    
    def setup_2(self):
        pth = self.package.__path__[0]
        for p in pth.split("\\"):
            if ".egg" in p:
                self.version = p.split("-")[1]+"_1" # we have a patched version
        return dict( VERSION = self.version )      