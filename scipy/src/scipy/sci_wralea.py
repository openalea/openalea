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
import scipy

def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'F. Chaubert and D. Da Silva',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Statistical functions from SciPy.',
               'url' : 'http://www.scipy.org'
               }
    
    
    package = Package("scipy", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="log",
                  description="compute the log of each item of the input list",
                  category="Math",
                  nodemodule="sci_base",
                  nodeclass="array_log",
                  inputs= ( dict( name = "List", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="log", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="StudentTest",
                  description="compute the Student Test",
                  category="Stat",
                  nodemodule="scistat",
                  nodeclass="ttest",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "mu", interface=IFloat, value=0. ),
                          ),
                  outputs=(dict(name="ttest", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="KolmogorovSmirnovTest",
                  description="compute the Kolmogorov-Smirnov Test",
                  category="Stat",
                  nodemodule="scistat",
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

    nf = Factory( name="ScipyLinearRegression",
                  description="compute the linear regression with scipy",
                  category="Stat",
                  nodemodule="scistat",
                  nodeclass="linearregress",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="linearregress", interface = IDict),
                          ),
                  )

    package.add_factory( nf )

###### end nodes definitions ###############

    pkg_manager.add_package(package)
