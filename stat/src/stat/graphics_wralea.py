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
               'description' : 'Graphical statistics from Rpy and Scipy.',
               'url' : 'http://rpy.sourceforge.net and http://www.scipy.org/'
               }
    
    
    package = Package("stat.graphics", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="plot (x,y)",
                  description="Plot (x,y)",
                  category="graphics",
                  nodemodule="graphics",
                  nodeclass="Plot",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True),
                            dict( name = "Y", interface=ISequence, showwidget=True),
                            dict( name = "xlab", interface=IStr,value = None, showwidget=True),
                            dict( name = "ylab", interface=IStr, value = None, showwidget=True),
                            dict( name = "main", interface=IStr, value = None, showwidget=True),
                          ),
                  outputs=(dict(name="Plot", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="hist (x)",
                  description="Histogram (x)",
                  category="graphics",
                  nodemodule="graphics",
                  nodeclass="Hist",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True),
                            dict( name = "K", interface=IInt, value = 0, showwidget=True),
                            dict( name = "xlab", interface=IStr,value = None, showwidget=True),
                            dict( name = "main", interface=IStr, value = None, showwidget=True),
                            dict( name = "counts", interface=IBool, showwidget=True),
                          ),
                  outputs=(dict(name="Histogram", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )
    
    nf = Factory( name="plot density(x)",
                  description="Plot the kernel density estimation",
                  category="graphics",
                  nodemodule="graphics",
                  nodeclass="PlotDens",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True),
                          ),
                  outputs=(dict(name="PlotDens", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )
    
###### end nodes definitions ###############

    pkg_manager.add_package(package)
