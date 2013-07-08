from openalea.release import Formula

class scipy(Formula):
    license = "Scipy License"
    authors = "(c) Enthought"
    description = "Scipy packaged as an egg"  
    py_dependent   = True
    arch_dependent = True 
    yet_installed = True
    
    def setup_2(self):
        return dict( VERSION = self.package.version.full_version )
                    )             