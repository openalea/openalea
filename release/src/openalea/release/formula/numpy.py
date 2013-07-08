from openalea.release import Formula

class numpy(Formula):
    license = "Numpy License"
    authors = "(c) Numpy Developers"
    description = "Numpy packaged as an egg"      
    py_dependent   = True
    arch_dependent = True   
    yet_installed = True
    
    def setup_2(self):
        return dict( VERSION = self.package.version.full_version )