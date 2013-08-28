from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class scipy(Formula):
    license = "Scipy License"
    authors = "(c) Enthought"
    description = "Scipy packaged as an egg"  
    py_dependent   = True
    arch_dependent = True 
    version = "0.12.0"       
    download_url = "http://freefr.dl.sourceforge.net/project/scipy/scipy/0.12.0/scipy-0.12.0-win32-superpack-python2.7.exe"
    download_name  = "scipy.exe"
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
        return dict( VERSION = self.package.version.full_version )
      