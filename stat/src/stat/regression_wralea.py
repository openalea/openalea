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
               'description' : 'Regressions from Rpy and Scipy.',
               'url' : 'http://rpy.sourceforge.net and http://www.scipy.org/'
               }
    
    
    package = Package("stat.regression", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="glm (rpy)",
                  description="compute the generalized linear regression",
                  category="regression",
                  nodemodule="regression",
                  nodeclass="Glm",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Y", interface=ISequence, showwidget=True ),
                            dict( name = "Family", interface=IEnumStr(['binomial','Gamma','gaussian','poisson']), showwidget=True ),
                          ),
                  outputs=(dict(name="Glm", interface = IDict),
                          ),
                  )

    package.add_factory( nf )


############## Linear regression section ##########################

    nf = Factory( name="linear regression (rpy)",
                  description="compute the linear regression",
                  category="regression",
                  nodemodule="regression",
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

    nf = Factory( name="multiple linear regression (rpy)",
                  description="compute a multiple linear regression",
                  category="regression",
                  nodemodule="regression",
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


    nf = Factory( name="linear regression to plot (pylab)",
                  description="generate plotable object from linear regression",
                  category="regression",
                  nodemodule="regression",
                  nodeclass="LR2Plot",
                  inputs= ( dict( name='reg', interface=IDict ),
                          ),
                  outputs=( dict(name='plotObjList',),
                            dict(name='plotObjList',),
                          ),
                  )

    package.add_factory( nf )


############## End of section #####################################


    nf = Factory( name="linear regression (scipy)",
                  description="compute the linear regression with scipy",
                  category="regression",
                  nodemodule="regression",
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
