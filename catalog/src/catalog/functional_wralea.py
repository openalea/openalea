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

__doc__ = """ Catalog.Functional """
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
                    description='Functional Node library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.Functional", metainfo)

    nf = Factory( name="map",
                  description="Apply a function on a sequence",
                  category="Functional",
                  nodemodule="functional",
                  nodeclass="pymap",
                  )
    
    package.add_factory(nf)
    

    nf = Factory( name="filter",
                  description="Apply a function on a sequence and return only true values",
                  category="Functional",
                  nodemodule="functional",
                  nodeclass="pyfilter",
                  )
    
    package.add_factory(nf)


    nf = Factory( name="reduce",
                  description="Apply a function of two arguments cumulatively to the items of a sequence",
                  category="Functional",
                  nodemodule="functional",
                  nodeclass="pyreduce",
                  )
    
    package.add_factory(nf)


    nf = Factory( name="ax+b", 
                  description="Linear function", 
                  category="Functional", 
                  nodemodule="functional",
                  nodeclass="Linear",
                  )


    package.add_factory( nf )
    

    nf = Factory( name="f op g",
                  description="Create a function h: x-> f(x) op g(x)",
                  category="Functional",
                  nodemodule="functional",
                  nodeclass="Generator",
                  )
    
    package.add_factory(nf)

    nf = Factory( name="function",
                  description="Creates a function from a python string",
                  category="Functional",
                  nodemodule="functional",
                  nodeclass="pyfunction",
		  inputs = (dict(name="func_str",interface=ITextStr),),
                  )
    
    package.add_factory(nf)


    
    pkgmanager.add_package(package)





