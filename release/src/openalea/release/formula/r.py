from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class r(Formula):
    license = "GNU General Public License"
    authors = "(c) 1998-2013 by Kurt Hornik"
    description = "The R Project for Statistical Computing"  
    py_dependent   = True
    arch_dependent = True 
    version = "2.15.3"       
    download_url = "http://mirror.ibcp.fr/pub/CRAN/bin/windows/base/old/2.15.3/R-2.15.3-win.exe"
    homepage = "http://www.r-project.org/"
    download_name  = "r.exe"
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