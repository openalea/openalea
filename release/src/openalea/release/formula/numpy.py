from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class numpy(Formula):
    license = "Numpy License"
    authors = "(c) Numpy Developers"
    description = "Numpy packaged as an egg"    
    version = "1.7.1"    
    py_dependent   = True
    arch_dependent = True      
    download_url = "http://freefr.dl.sourceforge.net/project/numpy/NumPy/1.7.1/numpy-1.7.1-win32-superpack-python2.7.exe"
    download_name  = "numpy.exe"
    yet_installed = False
    
    def unpack(self):
        return True
        
    def configure(self):
        return True
        
    def make(self):
        return True
        
    @in_dir("dldir")
    def install(self):
        return util_install(self.download_name)   
    
    def setup(self):
        return dict( VERSION = self.package.version.full_version, )