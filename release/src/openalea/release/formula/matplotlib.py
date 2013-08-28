from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class matplotlib(Formula):
    license = "Python Software Foundation License Derivative - BSD Compatible."
    authors = "Matplotlib developers"
    version = "1.2.1"
    download_url = "http://freefr.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.2.1/matplotlib-1.2.1.win32-py2.7.exe"
    download_name  = "matplotlib.exe"
    description = "Matplotlib packaged as an egg"  
    py_dependent   = True
    arch_dependent = True   

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
        return dict( VERSION = self.package.__version__ )   