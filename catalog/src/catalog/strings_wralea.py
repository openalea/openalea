# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ Catalog.String """

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from openalea.core import *



def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """
    
        # Base Library

    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'String library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }


    package = Package("Catalog.String", metainfo)

    nf = Factory( name="split", 
                  description="split a string", 
                  category="String", 
                  nodemodule="strings",
                  nodeclass="str_split",

                  inputs=(dict(name="String", interface=IStr, value=''),
                          dict(name="Split Char", interface=IStr, value='\n'),
                          ),
                  outputs=(dict(name="List", interface=ISequence),),
                  )

    package.add_factory( nf )
    
    
    nf = Factory( name="join", 
                  description="Join a list of string", 
                  category="String", 
                  nodemodule="strings",
                  nodeclass="str_join",

                  inputs=(dict(name="String List", interface=ISequence, value=[]),
                          dict(name="Join Char", interface=IStr, value='\n'),
                          ),
                  outputs=(dict(name="List", interface=IStr),),
                  )

    package.add_factory( nf )


    pkgmanager.add_package(package)

