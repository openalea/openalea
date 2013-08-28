from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class svn(Formula):
    license = "Apache License, Version 2.0"
    authors = "The Apache Software Foundation"
    description = "The R Project for Statistical Computing"  
    py_dependent   = True
    arch_dependent = True 
    version = "1.8.0-1"       
    download_url = "http://sourceforge.net/projects/win32svn/files/1.8.0/apache22/Setup-Subversion-1.8.0-1.msi"
    homepage = "http://subversion.apache.org/"
    download_name  = "svn.msi"
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