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
               'description' : 'Descriptive statistics from Rpy and Scipy.',
               'url' : 'http://rpy.sourceforge.net and http://www.scipy.org/'
               }
    
    
    package = Package("stat.descriptive", metainfo)
    
    
###### begin nodes definitions #############


    nf = Factory( name="stat summary",
                  description="Compute the statistical summary (min, max, median, mean, sd) ",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="StatSummary",
                  inputs= ( dict( name = "x", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="statsummary", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="correlation",
                  description="compute the correlations",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Corr",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Corr", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkg_manager.add_package(package)
