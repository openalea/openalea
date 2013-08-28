from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class setuptools_formula(Formula):
    license = ""
    authors = "Python Software Foundation"
    description = "Download, build, install, upgrade, and uninstall Python packages -- easily!"  
    py_dependent   = True
    arch_dependent = True 
    version = "0.6c11"       
    download_url = "http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe"
    download_name  = "setuptools.exe"
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