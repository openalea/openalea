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

__doc__ = """ Catalog.File """

__license__ = "Cecill-C"
__revision__ = " $Id$ "


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
                    description='File manimulation library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.File", metainfo)


    # Factories

    # File name
    nf = Factory( name="filename", 
                  description="File name", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="FileName",

                  inputs=(dict(name='FileStr', interface=IFileStr, value=''),),
                  outputs=(dict(name='FileStr', interface=IFileStr),)
                  )

    package.add_factory( nf )


    nf = Factory( name="dirname", 
                  description="Directory name", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="DirName",

                  inputs=(dict(name='DirStr', interface=IDirStr, value=''),),
                  outputs=(dict(name='DirStr', interface=IDirStr),)
                  )

    package.add_factory( nf )


    nf = Factory( name="packagedir", 
                  description="Package Directory", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="PackageDir",

                  inputs=(dict(name='PackageStr', interface=IStr, value=''),),
                  outputs=(dict(name='DirStr', interface=IDirStr),)
                  )

    package.add_factory( nf )

    # Path
    nf = Factory( name="joinpath", 
                  description="Join several strings to form a path", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="joinpath",

                  inputs=(dict(name='a', interface=ISequence, value=[]),
                          ),
                  outputs=(dict(name='path', interface=IStr),)
                  )

    package.add_factory( nf )

    nf = Factory( name="glob", 
                  description="Return a list of path that math the pattern", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="glob",

                  inputs=(dict(name='pattern', interface=IStr, value="*"),
                          ),
                  outputs=(dict(name='path_list', interface=ISequence),)
                  )

    package.add_factory( nf )


    # IO
    nf = Factory(name="read", 
                 description="read a file", 
                 category="File", 
                 inputs=(dict(name="filename", interface=IFileStr),
                         ),
                 outputs=(dict(name="string", interface=IStr),),

                 nodemodule="files",
                 nodeclass="FileRead",
                 )

    package.add_factory(nf)

    
    nf = Factory(name="readlines", 
                 description="read a file as a sequence of lines", 
                 category="File", 
                 inputs=(dict(name="filename", interface=IFileStr),
                         ),
                 outputs=(dict(name="string", interface=ISequence),),
                 nodemodule="files",
                 nodeclass="FileReadlines",
                 )

    package.add_factory(nf)


    nf = Factory( name="write",
                  description="write to a file",
                  category="File",
                  inputs=(dict(name="x", interface=IStr),
                          dict(name="filename", interface=IFileStr),
                          dict(name="mode", interface=IStr, value="w"),
                          ),
                  outputs=(),
                  nodemodule="files",
                  nodeclass="py_write",

                  )

    package.add_factory(nf)
    
    pkgmanager.add_package(package)

