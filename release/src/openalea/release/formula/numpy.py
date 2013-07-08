from openalea.release import Formula

class numpy(Formula):
    license = "Numpy License"
    authors = "(c) Numpy Developers"
    description = "Numpy packaged as an egg"      
    py_dependent   = True
    arch_dependent = True    
    def setup(self):
        return dict( VERSION = self.package.version.full_version )