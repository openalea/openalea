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
                  category="probability distribution",
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


####### normal distribution ################
    
    nf = Factory( name="density normal",
                  description="compute the density of normal distribution",
                  category="normal distribution",
                  nodemodule="distribution",
                  nodeclass="dnorm",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Mean", interface=IFloat, value=0. ),
                            dict( name = "Sd", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="density", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="cumulative normal",
                  description="compute the cumulative probability of normal distribution",
                  category="normal distribution",
                  nodemodule="distribution",
                  nodeclass="pnorm",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Mean", interface=IFloat, value=0. ),
                            dict( name = "Sd", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="cumulate", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="random normal",
                  description="generate random values from normal distribution",
                  category="normal distribution",
                  nodemodule="distribution",
                  nodeclass="rnorm",
                  inputs= ( dict( name = "n", interface=IInt, value = 1, showwidget=True ),
                            dict( name = "Mean", interface=IFloat, value=0. ),
                            dict( name = "Sd", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="random", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )
    
###### end normal distribution ##############

####### poisson distribution ################
    
    nf = Factory( name="density poisson",
                  description="compute the density of poisson distribution",
                  category="poisson distribution",
                  nodemodule="distribution",
                  nodeclass="dpois",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Lambda", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="density", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="cumulate poisson",
                  description="compute the cumulative probability of poisson distribution",
                  category="poisson distribution",
                  nodemodule="distribution",
                  nodeclass="ppois",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Lambda", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="cumulate", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="random poisson",
                  description="generate random values from poisson distribution",
                  category="poisson distribution",
                  nodemodule="distribution",
                  nodeclass="rpois",
                  inputs= ( dict( name = "n", interface=IInt, value=1, showwidget=True ),
                            dict( name = "Lambda", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="random", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )
    
###### end poisson distribution ##############
    
    nf = Factory( name="random discrete (rpy)",
                  description="Generate random values from discrete distribution",
                  category="probability distribution",
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
