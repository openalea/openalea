# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): David Da SILVA <david.da_silva@cirad.fr>
#                       Szymon STOMA <szymon.stoma@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for PlotTools 
"""

__license__= "Cecill-C"
__revision__=" $Id: plotools_wralea.py 805 2007-10-01 17:01:00Z stymek $ "


from openalea.core import *
 

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """
    print "pt"
    # Base Library

    metainfo = { 'version' : '0.0.1',
                 'license' : 'CECILL-C',
                 'authors' : 'OpenAlea Consortium',
                 'institutes' : 'INRIA/CIRAD',
                 'description' : 'Plotools library.',
                 'url' : 'http://openalea.gforge.inria.fr'
                 }


    package = Package("PlotTools", metainfo)

    nf = Factory( name= "Sequence2D Plot", 
                  description="Plot a list of 2D points plotable objects", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="display_VisualSequence2D",
                  inputs=(dict(name='vis_seq2D_list', interface=ISequence, showwidget=False),
                          dict(name='title', interface=IStr, value='MyPlot'),
                          dict(name='xlabel', interface=IStr, value='x-axis-label'),
                          dict(name='ylabel', interface=IStr, value='y-axis-label'),  ),
                  outputs=()

                )

    package.add_factory(nf)

    nf = Factory( name= "Sequence2D Hist", 
                  description="Plot sequence values as a histogram", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="display_Hist2D",
                  inputs=(dict(name='seq', interface=ISequence, showwidget=False),
                          dict(name='title', interface=IStr, value='MyPlot'),
                          dict(name='xlabel', interface=IStr, value='x-axis-label'),
                          dict(name='ylabel', interface=IStr, value='y-axis-label'),  ),
                  outputs=()

                )

    package.add_factory(nf)


    nf = Factory( name= "VSequence2D Style", 
                  description="Allows us to edit VisualSequence2D plot", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="change_VisualSequence2D",
                  inputs=(dict(name='vis_seq2D', interface=None, showwidget=False),
                            dict(name='new_legend', interface=IStr, value='Default'),
                            dict(name='new_linestyle', interface=IEnumStr( ['Default','-','--',':','-.'] )),
                            dict(name='new_marker', interface=IEnumStr( ['Default','.',',','o','^','v','<','>','s','+','x','D','d','1','2','3','4','h','H','p','p','|','_'] ) ),
                            dict(name='new_color', interface=IStr, value='Default'), 
                          ),
                  outputs=( dict(name='vis_seq2D', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Iterables to Sequence2D", 
                  description="Generates VisualSequence2D from 2 iterables", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="seqs2VisualSequence2D",
                  inputs=(dict(name='seq1', interface=ISequence),
                            dict(name='seq2', interface=ISequence),
                          ),
                  outputs=( dict(name='vis_seq2D', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Dict to Sequence2D", 
                  description="Generates VisualSequence2D from a dictionary", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="dict2VisualSequence2D",
                  inputs=(dict(name='dict', interface=IDict),
                          ),
                  outputs=( dict(name='vis_seq2D', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Iterable to Hist", 
                  description="Generates Hist2D from iterable and bins number", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="seq2Hist2D",
                  inputs=(dict(name='seq1', interface=ISequence),
                            dict(name='bins', interface=IInt, value = 10),
                          ),
                  outputs=( dict(name='hist2D', interface=None), )
                )
    package.add_factory(nf)



    pkgmanager.add_package(package)



