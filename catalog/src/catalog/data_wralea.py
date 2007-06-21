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

    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }


    package = Package("Catalog.Data", metainfo)

    nf = Factory( name="inputfile", 
                  description="File name", 
                  category="Data Types", 
                  nodemodule="data",
                  nodeclass="InputFile",

                  inputs=(dict(name='FileStr', interface=IFileStr, value=''),),
                  outputs=(dict(name='FileStr', interface=IFileStr),)
                  )

    package.add_factory( nf )


    nf = Factory( name="string", 
                  description="String", 
                  category="Data Types", 
                  nodemodule="data",
                  nodeclass="String",

                  inputs=(dict(name="String", interface=IStr, value=''),),
                  outputs=(dict(name="String", interface=IStr),),
                  )

    package.add_factory( nf )


    nf = Factory( name="bool", 
                  description="boolean", 
                  category="Data Types", 
                  nodemodule="data",
                  nodeclass="Bool",

                  inputs=(dict(name="Bool", interface=IBool, value=False),),
                  outputs=(dict(name="Bool", interface=IBool),),
                  )


    package.add_factory( nf )


    nf = Factory( name="float",
                  description="Float Value",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="Float",

                  inputs=(dict(name="Float", interface=IFloat, value=0.0),),
                  outputs=(dict(name="Float", interface=IFloat),),
                  )

    package.add_factory( nf )


    nf = Factory( name="int",
                  description="Int Value",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="Int",

                  inputs=(dict(name="Int", interface=IInt, value=0),),
                  outputs=(dict(name="Int", interface=IInt),),
                  )

    package.add_factory( nf )


    nf = Factory( name="enumTest",
                  description="String Enumeration",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="EnumTest",

                  inputs=(dict(name="Str", interface=IEnumStr(["enum1", "enum2", "enum3"]),
                               value="enum1"),),
                  outputs=(dict(name="Str", interface = IStr),),
                  )
                      
    package.add_factory( nf )


    nf = Factory( name="rgb",
                  description="RGB tuple",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="RGB",

                  inputs=(dict(name="RGB", interface=IRGBColor, value=(0,0,0)),),
                  outputs=(dict(name="RGB", interface = ISequence),),
                  )
    
    package.add_factory( nf )


    
    nf = Factory( name="list",
                  description="Python list",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="List",

                  inputs=(dict(name="List", interface=ISequence),),
                  outputs=(dict(name="List", interface=ISequence),),
                  )
    
    package.add_factory( nf )


    nf = Factory( name="dict",
                  description="Python dictionary",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="Dict",

                  inputs=(dict(name="Dict", interface=IDict),),
                  outputs=(dict(name="Dict", interface=IDict),),
                  )

    package.add_factory( nf )


    nf = Factory( name="pair",
                  description="Python 2-uple",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="Pair",
                  inputs=(dict(name="IN0", interface=None,),
                          dict(name="IN1", interface=None,),),
                  outputs=(dict(name="OUT", interface = ISequence),),
                  )

    package.add_factory( nf )


    nf = Factory( name="list9",
                  description="Create a list with lots of elements.",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="List9",
                  )



    nf = Factory( name="Pool Reader",
                  description="Read data from data pool.",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="PoolReader",
                  inputs = (dict(name='Key', interface=IStr),),
                  outputs = (dict(name='Obj', interface=None),)
                  )
    
    package.add_factory( nf )
    

    nf = Factory(name="Pool Writer",
                 description="Read data from data pool.",
                 category="Data Types",
                 nodemodule="data",
                 nodeclass="PoolWriter",
                 inputs = (dict(name='Key', interface=IStr),
                           dict(name='Obj', interface=None),),
                 )

    
    package.add_factory( nf )


    pkgmanager.add_package(package)

