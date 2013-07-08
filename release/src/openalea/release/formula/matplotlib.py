from openalea.release import Formula

class matplotlib(Formula):
    license = "Python Software Foundation License Derivative - BSD Compatible."
    authors = "Matplotlib developers"
    description = "Matplotlib packaged as an egg"  
    py_dependent   = True
    arch_dependent = True   
    yet_installed = True
    
    def setup_2(self):        
        return dict( VERSION = self.package.__version__ )   