
from openalea.core import *

def register_packages(pkgmanager):

    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }


    package1 = Package("Test", metainfo)

    # Test buitin
    nf = Factory( name= "sum", 
                  nodeclass = "sum",
		  inputs=(dict(name='in', interface=None),),
		  outputs=(dict(name='out', interface=None),),
                  )


    package1.add_factory( nf )

    # user function
    nf = Factory( name= "userfunc", 
                  nodeclass = "userfunc",
                  nodemodule = "moduletest",
                  )


    package1.add_factory( nf )

    # user class
    nf = Factory( name= "userclass", 
                  nodeclass = "userclass",
                  nodemodule = "moduletest",
                  )


    package1.add_factory( nf )

    
    pkgmanager.add_package(package1)

