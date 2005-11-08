"""
Package Manager.

The package manager register, install and load packages.
"""

$License: $

import cPickle
from zope.interface import Interface, implements


class ISoftwareBus(Interface):
    """
    A software bus manages packages.
    """
    def register( self, package ):
        ""
    def unregister(self, package):
        ""
    def install( self, package ):
        ""
    def uninstall( self, package ):
        ""
    def load(self,package):
        ""

    def packages(self):
        ""
    def loaded_packages(self):
        ""
    def installed_packages(self):
        ""

class BusPackage:
    def __init__(self,package):
        self.package= package
        self.status="register"
    def is_loaded(self):
        return self.status=="load"
    def is_installed(self):
        return self.status=="install"
    
def pid(package):
    """ Package id. """
    return package.name

class Bus:
    """
    The software bus  register, install and load packages.
    """

    implements(IBus)
   
    def __init__(self):
        self.bus= {}

    def register( self, package ):
        pckg= BusPackage(package)
        self.bus[pid(package)]= pckg
        return True

    def unregister( self, package ):
        if pid(package) in self.bus:
            del self.bus[pid(package)]
            return True
        else:
            return False
                
    def install( self, package ):
        if not pid(package) in self.bus:
            slef.register
        return False

    def uninstall( self, package ):
        return False

    def packages(self):
        return self.bus.keys()

    def loaded_packages(self):
        return self.bus.keys()

    def installed_packages(self):
        return self.bus.keys()
    


# Factory
def load():
    pass

def register(package):
    bus= load()
    ok= bus.register(package)
    bus.save()
    
