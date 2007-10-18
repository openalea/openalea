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


__doc__=""" Catalog.Model """

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *



def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Base Library
    metainfo = dict(version='0.0.1',
                    license='CECILL-C',
                    authors='OpenAlea Consortium',
                    institutes='INRIA/CIRAD',
                    description='Models.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.Model", metainfo)

    
    nf = Factory( name="linearmodel", 
                  description="Linear Model", 
                  category="Model", 
                  nodemodule="models",
                  nodeclass="linearmodel",
                  )


    package.add_factory(nf)


    
    pkgmanager.add_package(package)


