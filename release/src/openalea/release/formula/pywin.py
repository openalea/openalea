from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class pywin(Formula):
    license = "Python Software Foundation License"
    authors = "Mark Hammond"
    description = "Python for Windows Extensions"  
    py_dependent   = True
    arch_dependent = True 
    version = "218"       
    download_url = "http://freefr.dl.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe"
    homepage = "http://pywin32.sourceforge.net/"
    download_name  = "pywin.exe"
    
    def unpack(self):
        return True
        
    def configure(self):
        return True
        
    def make(self):
        return True
        
    @in_dir("dldir")
    def install(self):
        return util_install(self.download_name)         