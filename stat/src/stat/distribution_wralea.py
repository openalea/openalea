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
               'description' : 'Probability distributions from Rpy and Scipy.',
               'url' : 'http://rpy.sourceforge.net and http://www.scipy.org/'
               }
    
    
    package = Package("stat.distribution", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="random continuous (rpy)",
                  description="Generate random values from continuous distribution",
                  category="distribution",
                  nodemodule="distribution",
                  nodeclass="random_continuous_law",
                  inputs= ( dict( name = "law", interface=IEnumStr(['exp','norm','unif']), showwidget=True ),
                            dict( name = "n", interface=IInt, showwidget=True ),
                            dict( name = "args", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="res", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="random discrete (rpy)",
                  description="Generate random values from discrete distribution",
                  category="distribution",
                  nodemodule="distribution",
                  nodeclass="random_discrete_law",
                  inputs= ( dict( name = "law", interface=IEnumStr(['binom','geom','pois']), showwidget=True ),
                            dict( name = "n", interface=IInt, showwidget=True ),
                            dict( name = "args", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="res", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )
    

###### end nodes definitions ###############

    pkg_manager.add_package(package)
