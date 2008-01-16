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
               'description' : 'Test functions from Rpy and Scipy.',
               'url' : 'http://rpy.sourceforge.net and http://www.scipy.org/' 
               }
    
    
    package = Package("stat.test", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="chi square test (rpy)",
                  description="compute the Chisquare Test",
                  category="test",
                  nodemodule="stattest",
                  nodeclass="chisqtest",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "Proportion", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="chisqtest", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="student test (scipy)",
                  description="compute the Student Test",
                  category="test",
                  nodemodule="stattest",
                  nodeclass="ttest",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "mu", interface=IFloat, value=0. ),
                          ),
                  outputs=(dict(name="ttest", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="kolmogorov smirnov test (scipy)",
                  description="compute the Kolmogorov-Smirnov Test",
                  category="test",
                  nodemodule="stattest",
                  nodeclass="kstest",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "Cdf", interface=IStr, showwidget=True ),
                            dict( name = "Args", interface=ISequence, showwidget=True),
                          ),
                  outputs=(dict(name="kstest", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkg_manager.add_package(package)
