from openalea.release import Formula

class pil(Formula):
    license = "PIL License."
    authors = "Copyright (c) 1997-2011 by Secret Labs AB, Copyright (c) 1995-2011 by Fredrik Lundh."
    description = "PIL packaged as an egg"  
    __modulename__  = "Image"
    py_dependent   = True
    arch_dependent = True  
    yet_installed = True
    
    def setup_2(self):
        return dict( VERSION = self.module.VERSION )