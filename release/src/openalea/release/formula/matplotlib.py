from openalea.release import Formula

# InstalledPackageEggBuilder !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
  C:\OpenAlea\openalea_trunk\deploy\src\openalea\deploy\system_dependencies\dependency_builder.py (1 hit)
	Line 1516: class InstalledPackageEggBuilder(BaseEggBuilder, object):
  C:\OpenAlea\openalea_trunk\deploy\src\openalea\deploy\system_dependencies\egg_rules.py (6 hits)
	Line 284: class egg_numpy(InstalledPackageEggBuilder):
	Line 293: class egg_scipy(InstalledPackageEggBuilder):
	Line 302: class egg_matplotlib(InstalledPackageEggBuilder):
	Line 311: class egg_PIL(InstalledPackageEggBuilder):
	Line 321: class egg_pylsm(InstalledPackageEggBuilder):
"""
class matplotlib(Formula):
    license = "Python Software Foundation License Derivative - BSD Compatible."
    authors = "Matplotlib developers"
    description = "Matplotlib packaged as an egg"  
    py_dependent   = True
    arch_dependent = True        
    def setup(self):        
        return dict( VERSION = self.package.__version__ )   