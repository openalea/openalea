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

    
    nf = Factory( name="log",
                  description="compute the log of each item of the input list",
                  category="Math",
                  nodemodule="descriptive",
                  nodeclass="list_log",
                  inputs= ( dict( name = "List", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="log", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="load file",
                  description="Read .txt file ",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Load",
                  inputs= ( dict( name = "file", interface=IFileStr("txt (*.txt)"), showwidget=True ),
                          ),
                  outputs=(dict(name="data", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="extract row",
                  description="Extract the lth row ",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="ExtractLigne",
                  inputs= ( dict( name = "data", interface=None),
                            dict( name = "L", interface=IInt, showwidget=True),
                            dict( name = "Test", interface=IFloat, value = -1., showwidget=True),
                          ),
                  outputs=(dict(name="Row", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="extract column",
                  description="Extract the cth column ",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="ExtractCol",
                  inputs= ( dict( name = "data", interface=None),
                            dict( name = "L", interface=IInt, showwidget=True),
                            dict( name = "Test", interface=IFloat, value = -1., showwidget=True),
                          ),
                  outputs=(dict(name="Column", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="plot (x,y)",
                  description="Plot (x,y)",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Plot",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True),
                            dict( name = "Y", interface=ISequence, showwidget=True),
                            dict( name = "xlab", interface=IStr,value = None, showwidget=True),
                            dict( name = "ylab", interface=IStr, value = None, showwidget=True),
                            dict( name = "main", interface=IStr, value = None, showwidget=True),
                          ),
                  outputs=(dict(name="Plot", interface = None),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="hist (x)",
                  description="Histogram (x)",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Hist",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True),
                            dict( name = "K", interface=IInt, value = 0, showwidget=True),
                            dict( name = "xlab", interface=IStr,value = None, showwidget=True),
                            dict( name = "main", interface=IStr, value = None, showwidget=True),
                            dict( name = "counts", interface=IBool, showwidget=True),
                          ),
                  outputs=(dict(name="Histogram", interface = None),
                          ),
                  )

    package.add_factory( nf )
    
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


    nf = Factory( name="mean",
                  description="compute the mean",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Mean",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Mean", interface = IFloat),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="median",
                  description="compute the median",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Median",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Median", interface = IFloat),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="mode",
                  description="compute the mode",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Mode",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Mode", interface = IDict),
                          ),
                  )

    package.add_factory( nf )

    
    nf = Factory( name="variance",
                  description="compute the variance",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Var",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Variance", interface = IFloat),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="standard deviation",
                  description="compute the standard deviation",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Std",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Std", interface = IFloat),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="frequencies",
                  description="compute the frequencies",
                  category="descriptive",
                  nodemodule="descriptive",
                  nodeclass="Freq",
                  inputs= ( dict( name = "X", interface=ISequence, showwidget=True ),
                          ),
                  outputs=(dict(name="Freq", interface = IDict),
                          ),
                  )

    package.add_factory( nf )
    
###### end nodes definitions ###############

    pkg_manager.add_package(package)
