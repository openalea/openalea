# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): CHAUBERT Florence <florence.chaubert@cirad.fr>
#                       Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *

def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'F. Chaubert and D. Da Silva',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'File manipulations.',
               'url' : 'http://rpy.sourceforge.net and http://www.scipy.org/'
               }
    
    
    package = Package("stat.file", metainfo)
    
    
###### begin nodes definitions #############


    nf = Factory( name="load file",
                  description="Read .txt file ",
                  category="file",
                  nodemodule="file",
                  nodeclass="Load",
                  inputs= ( dict( name = "file", interface=IFileStr("txt (*.txt)"), showwidget=True ),
                          ),
                  outputs=(dict(name="data", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="extract row",
                  description="Extract the lth row ",
                  category="file",
                  nodemodule="file",
                  nodeclass="ExtractLigne",
                  inputs= ( dict( name = "data", interface=None),
                            dict( name = "L", interface=IInt, showwidget=True),
                            dict( name = "Test", interface=IFloat, value = -1., showwidget=True),
                          ),
                  outputs=(dict(name="Row", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="extract column",
                  description="Extract the cth column ",
                  category="file",
                  nodemodule="file",
                  nodeclass="ExtractCol",
                  inputs= ( dict( name = "data", interface=None),
                            dict( name = "L", interface=IInt, showwidget=True),
                            dict( name = "Test", interface=IFloat, value = -1., showwidget=True),
                          ),
                  outputs=(dict(name="Column", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkg_manager.add_package(package)
