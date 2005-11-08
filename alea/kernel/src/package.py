"""
Package.

The package manager register, install and load packages.
"""

$License: $

import cPickle
from zope.interface import Interface, implements

class Package:
    def __init__(self, name, **kwds):
        self.name=name
    	for k, v in kwds.iteritems():
    	    setattr(self,k,v)
    	    
    def components(self):
    	""" for now a composent is a name """
        return []
        
    def interfaces(self):
    	""" for now a composent is a name """
    	return []
	
    def has_gui(self):
    	""" Return true if the package has a GUI """
    	return False
    
    def load(self):
    	""" Load the current package """
    	pass
    
    def get_loaded(self):
    	""" Return true if the package is loaded"""
    	return False
    
    loaded = property(get_loaded)

def pid(package):
    """ Package id. """
    return package.name

class PkgConfig:
    def __init__(self,package):
        self.package= package
        self.status="register"
    def is_loaded(self):
        return self.status=="load"
    def is_installed(self):
        return self.status=="install"

	
class PkgManager:
    """
    The PackageManager register, install and load packages.
    """
    def __init__(self):
        self.pkgs= {}

    def register( self, package ):
        p= PkgConfig(package)
        self.pkgs[pid(package)]= p
        return True

    def unregister( self, package ):
        if pid(package) in self.pkgs:
            del self.pkgs[pid(package)]
            return True
        else:
            return False
                
    def install( self, package ):
        if not pid(package) in self.pkgs:
            self.register
        return False

    def uninstall( self, package ):
        return False

    def packages(self):
        return self.pkgs.keys()

    def loaded_packages(self):
        return self.pkgs.keys()

    def installed_packages(self):
        return self.pkgs.keys()
    


# Factory
def load():
    pass

def register(package):
    bus= load()
    ok= pkgs.register(package)
    bus.save()
    


