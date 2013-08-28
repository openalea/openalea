from openalea.release import Formula
from openalea.release.utils import in_dir, install as util_install

class pillow(Formula):
    license = "Pillow License."
    authors = "Copyright (c) 1997-2011 by Secret Labs AB, Copyright (c) 1995-2011 by Fredrik Lundh."
    description = "Pillow packaged as an egg. Pillow is the 'friendly' PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors."  
    __modulename__  = "Image"
    __packagename__  = "PIL"
    py_dependent   = True
    arch_dependent = True  
    version = "2.1.0"       
    download_url = "https://pypi.python.org/packages/2.7/P/Pillow/Pillow-2.1.0.win32-py2.7.exe"
    homepage = "https://pypi.python.org/pypi/Pillow"
    download_name  = "pillow.exe"
    
    def unpack(self):
        return True
        
    def configure(self):
        return True
        
    def make(self):
        return True
        
    @in_dir("dldir")
    def install(self):
        return util_install(self.download_name)   