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

__name__ = "openalea.stat.graphics"
__alias__ = ["stat.graphics"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea consortium'
__institutes__ = 'INRIA/CIRAD/UM2'
__description__ = 'Graphical statistics from Rpy and Scipy.'
__url__ = 'http://rpy.sourceforge.net and http://www.scipy.org/'
 
__editable__ = 'False' 
 
__all__ = ['plot', 'hist', 'plotdensity',]
    
    
###### begin nodes definitions #############

plot = Factory( name="plot (x,y)",
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

hist = Factory( name="hist (x)",
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

plotdensity = Factory( name="plot density(x)",
                       description="Plot the kernel density estimation",
                       category="graphics",
                       nodemodule="graphics",
                       nodeclass="PlotDens",
                       inputs= ( dict( name = "X", interface=ISequence, showwidget=True),
                               ),
                       outputs=(dict(name="PlotDens", interface = ISequence),
                               ),
                       )

    
###### end nodes definitions ###############
