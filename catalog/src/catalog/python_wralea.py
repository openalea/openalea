# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Core.Library 
"""

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
                    description='Python Node library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.Python", metainfo)


    # Factories
    nf = Factory(name="ifelse", 
                 description="Condition", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_ifelse",
                 )

    package.add_factory(nf)


    nf = Factory( name="getitem",
                  description="Python __getitem__",
                  category="Python",
                  nodemodule="python",
                  nodeclass="getitem",

                  widgetclass="ListSelectorWidget",
             
                  )

    package.add_factory(nf)


    nf = Factory(name="setitem",
                 description="Python __setitem__",
                 category="Python",
                 nodemodule="python",
                 nodeclass="setitem",
                 )

    package.add_factory(nf)


    nf = Factory(name="delitem",
                 description="Python __delitem__",
                 category="Python",
                 nodemodule="python",
                 nodeclass="delitem",
                 )

    package.add_factory(nf)


    nf = Factory( name="keys",
                  description="Python keys()",
                  category="Python",
                  nodemodule="python",
                  nodeclass="keys",
                  )

    package.add_factory(nf)

    
    nf = Factory(name="values",
                 description="Python values()",
                 category="Python",
                 nodemodule="python",
                 nodeclass="values",
                 )

    package.add_factory(nf)

    
    nf = Factory(name="items",
                 description="Python items()",
                 category="Python",
                 nodemodule="python",
                 nodeclass="items",
                 )

    package.add_factory(nf)

    nf = Factory(name="range",
                 description="Returns an arithmetic progression of integers",
                 category="Python",
                 nodemodule="python",
                 nodeclass="pyrange",
                 )
    
    package.add_factory(nf)


    nf = Factory(name="enumerate",
                 description="Returns a python enumerate object.",
                 category="Python",
                 nodemodule="python",
                 nodeclass="pyenumerate",
                 )
    
    package.add_factory(nf)


    nf = Factory(name="len",
                 description="Returns the number of items of a sequence or mapping.",
                 category="Python",
                 nodemodule="python",
                 nodeclass="pylen",
                 )
    
    package.add_factory(nf)


    nf = Factory(name="print", 
                 description="Console output", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_print",
                 outputs=(),
                 lazy=False,
                 )

    package.add_factory(nf)


    nf = Factory(name="fwrite", 
                 description="File output", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_fwrite",
                 inputs=(dict(name="x", interface=IStr),
                         dict(name="filename", interface=IFileStr),
                         dict(name="mode", interface=IStr, value="w"),
                         ),
                 outputs=(),
                 lazy=False,
                 )

    package.add_factory(nf)


    nf = Factory(name="fread", 
                 description="File input", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="FileRead",
                 inputs=(dict(name="filename", interface=IFileStr),
                         ),
                 outputs=(dict(name="String", interface=IStr),),
                 lazy = False,
                 )

    package.add_factory(nf)


    nf = Factory(name="method", 
                 description="Calls object method", 
                 category="Python", 
                 nodemodule="python",
                 nodeclass="py_method",
                 )


    package.add_factory(nf)
    
    
    nf = Factory( name="getattr",
                  description="Gets class attribute",
                  category="Python",
                  nodemodule="python",
                  nodeclass="py_getattr",

                  inputs=(dict(name="IN0", interface=None),
		    dict(name="Class_attribute_name", interface=IStr)),
                  outputs=(dict(name="Class_attribute", interface=None),),
                  )

    package.add_factory( nf )

    
    pkgmanager.add_package(package)

