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
__name__ = "openalea.stat.test"
__alias__ = ["stat.test"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea consortium'
__institutes__ = 'INRIA/CIRAD/UM2'
__description__ = 'Test functions  from Rpy and Scipy.'
__url__ = 'http://rpy.sourceforge.net and http://www.scipy.org/'
 
__editable__ = 'False' 
 
__all__ = ['chisquare','studenttest','kstest',]
    
    
###### begin nodes definitions #############

chisquare = Factory( name="chi square test (rpy)",
                     description="Compute the Chisquare Test",
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

studenttest = Factory( name="student test (scipy)",
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

kstest = Factory( name="kolmogorov smirnov test (scipy)",
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

###### end nodes definitions ###############
