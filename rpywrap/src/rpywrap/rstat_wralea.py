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
               'description' : 'Statistical functions from R and RPy.',
               'url' : 'http://rpy.sourceforge.net'
               }
    
    
    package = Package("r", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="ChisquareTest",
                  description="compute the Chisquare Test",
                  category="Stat",
                  nodemodule="rstat",
                  nodeclass="chisqtest",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "Proportion", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="chisqtest", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="RandomContinuous",
                  description="Generate random values from continuous distribution",
                  category="Stat",
                  nodemodule="rstat",
                  nodeclass="random_continuous_law",
                  inputs= ( dict( name = "law", interface=IStr, showwidget=True ),
                            dict( name = "n", interface=IInt, showwidget=True ),
                            dict( name = "args", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="res", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

############## Linear regression section ##########################

    nf = Factory( name="LinearRegression",
                  description="compute the linear regression",
                  category="Stat",
                  nodemodule="rstat",
                  nodeclass="LinearRegression",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "alpha", interface=IFloat, value=5. ),
                            dict( name = "origin", interface=IBool, value=False ),
                          ),
                  outputs=(dict(name="reg", interface = IDict),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="MultipleLinearRegression",
                  description="compute a multiple linear regression",
                  category="Stat",
                  nodemodule="rstat",
                  nodeclass="multiReg",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "colList", interface=ISequence, showwidget=True ),
                            dict( name = "alpha", interface=IFloat, value=5. ),
                          ),
                  outputs=(dict(name="reg", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="LRtoPlot",
                  description="generate plotable object from linear regression",
                  category="Stat",
                  nodemodule="rstat",
                  nodeclass="LR2Plot",
                  inputs= ( dict( name='reg', interface=IDict ),
                          ),
                  outputs=( dict(name='plotObjList',),
                            dict(name='plotObjList',),
                          ),
                  )

    package.add_factory( nf )


############## End of section #####################################

###### end nodes definitions ###############

    pkg_manager.add_package(package)
