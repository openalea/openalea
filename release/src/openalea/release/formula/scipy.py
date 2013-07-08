from openalea.release import Formula

class scipy(Formula):
    license = "Scipy License"
    authors = "(c) Enthought"
    description = "Scipy packaged as an egg"  
    py_dependent   = True
    arch_dependent = True        
    def setup(self):
        return dict( VERSION = self.package.version.full_version )
                    )             