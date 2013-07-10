from openalea.release import Formula
import warnings

class pillow(Formula):
    license = "Pillow License."
    authors = "Copyright (c) 1997-2011 by Secret Labs AB, Copyright (c) 1995-2011 by Fredrik Lundh."
    description = "Pillow packaged as an egg. Pillow is the 'friendly' PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors."  
    __modulename__  = "Image"
    __packagename__  = "PIL"
    py_dependent   = True
    arch_dependent = True  
    yet_installed = True
    
    def configure(self):
        return True
        
    def make(self):
        return True
        
    def install(self):
        return True    
        
    def setup_2(self):
        return dict( VERSION = self.module.VERSION )