from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class pyopengl(Formula):
    license = "BSD-style Open-Source license"
    authors = ""
    description = "The Python OpenGL Binding"  
    py_dependent   = True
    arch_dependent = True 
    version = "3.0.2"       
    download_url = "http://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-3.0.2.win32.exe"
    homepage = "http://pyopengl.sourceforge.net/"
    download_name  = "pyopengl.exe"
    
    def unpack(self):
        return True
        
    def configure(self):
        return True
        
    def make(self):
        return True
        
    @in_dir("dldir")
    def install(self):
        return util_install(self.download_name)        