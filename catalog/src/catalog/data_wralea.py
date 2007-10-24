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


__doc__=""" Catalog.Data """
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


    nf = Factory( name="variable", 
                  description="Variable", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="Variable",

                  inputs=(dict(name='Caption', interface=IStr, value='Variable'),
                          dict(name='Object', interface=None, value=None),
                          ),
                  outputs=(dict(name='Object', interface=None),)
                  )

    package.add_factory( nf )



    nf = Factory( name="filename", 
                  description="File name", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="FileName",

                  inputs=(dict(name='FileStr', interface=IFileStr, value=''),),
                  outputs=(dict(name='FileStr', interface=IFileStr),)
                  )

    package.add_factory( nf )


    nf = Factory( name="dirname", 
                  description="Directory name", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="DirName",

                  inputs=(dict(name='DirStr', interface=IDirStr, value=''),dict(name='cwd', interface=IDirStr, value='', hide=True)),
                  outputs=(dict(name='DirStr', interface=IDirStr),)
                  )

    package.add_factory( nf )


    nf = Factory( name="string", 
                  description="String", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="String",

                  inputs=(dict(name="String", interface=IStr, value=''),),
                  outputs=(dict(name="String", interface=IStr),),
                  )

    package.add_factory( nf )


    nf = Factory( name="text", 
                  description="Text", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="Text",

                  inputs=(dict(name="Text", interface=ITextStr, value=''),),
                  outputs=(dict(name="Text", interface=ITextStr),),
                  )

    package.add_factory( nf )


    nf = Factory( name="datetime", 
                  description="DateTime", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="DateTime",

                  inputs=(dict(name="DateTime", interface=IDateTime, value=''),),
                  outputs=(dict(name="DateTime", interface=IDateTime),),
                  )

    package.add_factory( nf )


    nf = Factory( name="bool", 
                  description="boolean", 
                  category="Type", 
                  nodemodule="data",
                  nodeclass="Bool",

                  inputs=(dict(name="Bool", interface=IBool, value=False),),
                  outputs=(dict(name="Bool", interface=IBool),),
                  )


    package.add_factory( nf )


    nf = Factory( name="float",
                  description="Float Value",
                  category="Type",
                  nodemodule="data",
                  nodeclass="Float",

                  inputs=(dict(name="Float", interface=IFloat, value=0.0),),
                  outputs=(dict(name="Float", interface=IFloat),),
                  )

    package.add_factory( nf )

    nf = Factory( name="float scy",
                  description="Float Value",
                  category="Data Types",
                  nodemodule="data",
                  nodeclass="FloatScy",

                  inputs=(dict(name="str", interface=IStr, value="0.0"),),
                  outputs=(dict(name="Float", interface=IFloat),),
                  )

    package.add_factory( nf )


    nf = Factory( name="int",
                  description="Int Value",
                  category="Type",
                  nodemodule="data",
                  nodeclass="Int",

                  inputs=(dict(name="Int", interface=IInt, value=0),),
                  outputs=(dict(name="Int", interface=IInt),),
                  )

    package.add_factory( nf )


    nf = Factory( name="rgb",
                  description="RGB tuple",
                  category="Type,Color",
                  nodemodule="data",
                  nodeclass="RGB",

                  inputs=(dict(name="RGB", interface=IRGBColor, value=(0,0,0)),),
                  outputs=(dict(name="RGB", interface = ISequence),),
                  )
    
    package.add_factory( nf )


    
    nf = Factory( name="list",
                  description="Python list",
                  category="Type",
                  nodemodule="data",
                  nodeclass="List",

                  inputs=(dict(name="List", interface=ISequence),),
                  outputs=(dict(name="List", interface=ISequence),),
                  )
    
    package.add_factory( nf )


    nf = Factory( name="dict",
                  description="Python dictionary",
                  category="Type",
                  nodemodule="data",
                  nodeclass="Dict",

                  inputs=(dict(name="Dict", interface=IDict),),
                  outputs=(dict(name="Dict", interface=IDict),),
                  )

    package.add_factory( nf )


    nf = Factory( name="pair",
                  description="Python 2-uple",
                  category="Type",
                  nodemodule="data",
                  nodeclass="Pair",
                  inputs=(dict(name="IN0", interface=None,),
                          dict(name="IN1", interface=None,),),
                  outputs=(dict(name="OUT", interface = ISequence),),
                  )

    package.add_factory( nf )




    pkgmanager.add_package(package)

