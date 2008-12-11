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

__name__ = "openalea.stat.descriptive"
__alias__ = ["stat.descriptive"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea consortium'
__institutes__ = 'INRIA/CIRAD/UM2'
__description__ = 'Descriptive statistics from Rpy and Scipy.'
__url__ = 'http://rpy.sourceforge.net and http://www.scipy.org/'
 
__editable__ = 'False' 
 
__all__ = [ 'log','statsummary','correlation', 'mean', 'median', 'mode', \
            'variance', 'standarddeviation', 'frequencies', 'density', ]
 

###### begin nodes definitions #############

log = Factory( name="log",
               description="Compute the log of each item of the input list",
               category="Math,stat",
               nodemodule="descriptive",
               nodeclass="list_log",
               inputs= ( dict( name = "x", interface=ISequence, showwidget=True ),
                       ),
               outputs=(dict(name="log", interface = ISequence),
                       ),
                )

statsummay = Factory( name="stat summary",
                      description="Compute the statistical summary (min, max, median, mean, sd) ",
                      category="descriptive",
                      nodemodule="descriptive",
                      nodeclass="StatSummary",
                      inputs= ( dict( name = "x", interface=ISequence, showwidget=True ),
                              ),
                      outputs=(dict(name="statsummary", interface = ISequence),
                              ),
                      )

correlation = Factory( name="correlation",
                       description="Compute the correlations",
                       category="descriptive",
                       nodemodule="descriptive",
                       nodeclass="Corr",
                       inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                                    dict( name = "Y", interface=ISequence, showwidget=True ),
                                ),
                       outputs=(dict(name="Corr", interface = IDict),
                                ),
                       )

mean = Factory( name="mean",
                description="Compute the mean",
                category="descriptive",
                nodemodule="descriptive",
                nodeclass="Mean",
                inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                        ),
                outputs=(dict(name="Mean", interface = IFloat),
                        ),
                )

median = Factory( name="median",
                  description="Compute the median",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Median",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Median", interface = IFloat),
                          ),
                  )

mode = Factory( name="mode",
                description="Compute the mode",
                category="descriptive",
                nodemodule="descriptive",
                nodeclass="Mode",
                inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                outputs=(dict(name="Mode", interface = IDict),
                          ),
                  )

variance = Factory( name="variance",
                    description="Compute the variance",
                    category="descriptive",
                    nodemodule="descriptive",
                    nodeclass="Var",
                    inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                            ),
                    outputs=(dict(name="Variance", interface = IFloat),
                            ),
                   )

standarddeviation = Factory( name="standard deviation",
                             description="Compute the standard deviation",
                             category="descriptive",
                             nodemodule="descriptive",
                             nodeclass="Std",
                             inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                                     ),
                             outputs=(dict(name="Std", interface = IFloat),
                                     ),
                             )

frequencies = Factory( name="frequencies",
                       description="Compute the frequencies",
                       category="descriptive",
                       nodemodule="descriptive",
                       nodeclass="Freq",
                       inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                               ),
                       outputs=(dict(name="Freq", interface = IDict),
                               ),
                       )

density = Factory( name="density",
                   description="Compute the Kernel density estimation",
                   category="descriptive",
                   nodemodule="descriptive",
                   nodeclass="Density",
                   inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                           ),
                   outputs=(dict(name="density", interface = IDict),
                           ),
                   )

    
###### end nodes definitions ###############


