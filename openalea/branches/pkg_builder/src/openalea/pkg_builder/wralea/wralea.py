
from openalea.core import *

def register_packages(pkgmanager):
    ''' Initialisation function
    
    Return the list of packages to be included in the package manager.
    This function is called by the package manager.
    '''

    metainfo={ 'version' : '0.0.0',
               'license' : 'XXX',
               'authors' : 'XXX',
               'institutes' : 'XXX',
               'description' : 'XXX',
               'url' : 'htp://XXX.org'
               }

    package = Package('pkg_builder', metainfo)

    # begin adding Factory after this line.

    # end adding factories

    pkgmanager.add_package(package)

