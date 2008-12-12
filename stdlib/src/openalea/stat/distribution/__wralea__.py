# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
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

__name__ = "openalea.stat.distribution"
__alias__ = ["stat.distribution"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea consortium'
__institutes__ = 'INRIA/CIRAD/UM2'
__description__ = 'Probability distributions from Rpy and Scipy.'
__url__ = 'http://rpy.sourceforge.net and http://www.scipy.org/'
 
__editable__ = 'False' 
 
__all__ = ['randomcontinuous', 'densitynormal', 'cumulativenormal', 'randomnormal', 'densitypoisson', 'cumulatepoisson', 'randompoisson', 'randomdiscrete']
    
    
###### begin nodes definitions #############

randomcontinuous = Factory( name="random continuous (rpy)",
                            description="Generate random values from continuous distribution",
                            category="statistics",
                            nodemodule="distribution",
                            nodeclass="random_continuous_law",
                            inputs= ( dict( name = "law", interface=IEnumStr(['exp','norm','unif']), showwidget=True ),
                                      dict( name = "n", interface=IInt, showwidget=True ),
                                      dict( name = "args", interface=ISequence, showwidget=True ),
                                    ),
                            outputs=(dict(name="res", interface = ISequence),
                                    ),
                            )



####### normal distribution ################
    
densitynormal = Factory( name="density normal",
                         description="Compute the density of normal distribution",
                         category="statistics.normal distribution",
                         nodemodule="distribution",
                         nodeclass="dnorm",
                         inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                                   dict( name = "Mean", interface=IFloat, value=0. ),
                                   dict( name = "Sd", interface=IFloat, value=1. ),
                                 ),
                         outputs=(dict(name="density", interface = ISequence),
                                 ),
                         )

cumulativenormal = Factory( name="cumulative normal",
                  description="Compute the cumulative probability of normal distribution",
                  category="statistics.normal distribution",
                  nodemodule="distribution",
                  nodeclass="pnorm",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            dict( name = "Mean", interface=IFloat, value=0. ),
                            dict( name = "Sd", interface=IFloat, value=1. ),
                          ),
                  outputs=(dict(name="cumulate", interface = ISequence),
                          ),
                  )

randomnormal = Factory(   name="random normal",
                          description="Generate random values from normal distribution",
                          category="statistics.normal distribution",
                          nodemodule="distribution",
                          nodeclass="rnorm",
                          inputs= ( dict( name = "n", interface=IInt, value = 1, showwidget=True ),
                                    dict( name = "Mean", interface=IFloat, value=0. ),
                                    dict( name = "Sd", interface=IFloat, value=1. ),
                                  ),
                          outputs=(dict(name="random", interface = ISequence),
                                  ),
                          )

    
###### end normal distribution ##############

####### poisson distribution ################
    
densitypoisson = Factory( name="density poisson",
                          description="Compute the density of poisson distribution",
                          category="statistics.poisson distribution",
                          nodemodule="distribution",
                          nodeclass="dpois",
                          inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                                    dict( name = "Lambda", interface=IFloat, value=1. ),
                                  ),
                          outputs=(dict(name="density", interface = ISequence),
                                  ),
                          )

cumulatepoisson = Factory(    name="cumulate poisson",
                              description="Compute the cumulative probability of poisson distribution",
                              category="statistics.poisson distribution",
                              nodemodule="distribution",
                              nodeclass="ppois",
                              inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                                        dict( name = "Lambda", interface=IFloat, value=1. ),
                                      ),
                              outputs=(dict(name="cumulate", interface = ISequence),
                                      ),
                              )


randompoisson = Factory(  name="random poisson",
                          description="Generate random values from poisson distribution",
                          category="statistics.poisson distribution",
                          nodemodule="distribution",
                          nodeclass="rpois",
                          inputs= ( dict( name = "n", interface=IInt, value=1, showwidget=True ),
                                    dict( name = "Lambda", interface=IFloat, value=1. ),
                                  ),
                          outputs=(dict(name="random", interface = ISequence),
                                  ),
                          )

    
###### end poisson distribution ##############
    
randomdiscrete = Factory( name="random discrete (rpy)",
                          description="Generate random values from discrete distribution",
                          category="statistics",
                          nodemodule="distribution",
                          nodeclass="random_discrete_law",
                          inputs= ( dict( name = "law", interface=IEnumStr(['binom','geom','pois']), showwidget=True ),
                                    dict( name = "n", interface=IInt, showwidget=True ),
                                    dict( name = "args", interface=ISequence, showwidget=True ),
                                  ),
                          outputs=(dict(name="res", interface = ISequence),
                                  ),
                          )

    

###### end nodes definitions ###############

