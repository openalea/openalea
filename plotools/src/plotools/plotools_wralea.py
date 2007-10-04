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
    # Base Library

    metainfo = { 'version' : '0.0.1',
                 'license' : 'CECILL-C',
                 'authors' : 'OpenAlea Consortium',
                 'institutes' : 'INRIA/CIRAD',
                 'description' : 'Plotools library.',
                 'url' : 'http://openalea.gforge.inria.fr'
                 }


    package = Package("PlotTools", metainfo)

    nf = Factory( name= "VS Plot", 
                  description="Plot a list of 2D points plotable objects", 
                  category="Vizualisation", 
                  nodemodule="plotable2",
                  nodeclass="display_VisualSequence",
                  inputs=(dict(name='vis_seq_list', interface=ISequence, showwidget=False),
                          dict(name='visualisation', interface=IEnumStr(["PointLine", "Hist"])),
                          dict(name='title', interface=IStr, value='MyPlot'),
                          dict(name='xlabel', interface=IStr, value='x-axis-label'),
                          dict(name='ylabel', interface=IStr, value='y-axis-label'),
                          dict(name='figure', interface=IInt(0,10), value=0), ), 
                  outputs=(dict(name='result', interface=None ),)

                )

    package.add_factory(nf)

    nf = Factory( name= "PointLine Style", 
                  description="Allows us to edit VisualSequence plot", 
                  category="Vizualisation", 
                  nodemodule="plotable2",
                  nodeclass="change_VisualSequence_PointLineView",
                  inputs=(dict(name='vis_seq', interface=None, showwidget=False),
                            dict(name='new_legend', interface=IStr, value='Default'),
                            dict(name='new_linestyle', interface=IEnumStr( ['Default','-','--',':','-.'] )),
                            dict(name='new_marker', interface=IEnumStr( ['Default','.',',','o','^','v','<','>','s','+','x','D','d','1','2','3','4','h','H','p','p','|','_'] ) ),
                            dict(name='new_color', interface=IStr, value='Default'),
                          ),
                  outputs=( dict(name='vis_seq', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Hist Style", 
                  description="Allows us to edit VisualSequence Hist style properties", 
                  category="Vizualisation", 
                  nodemodule="plotable2",
                  nodeclass="change_VisualSequence_HistView",
                  inputs=(dict(name='vis_seq', interface=None, showwidget=False),
                            dict(name='new_bins', interface=IInt, value=10),
                            dict(name='new_color', interface=IStr, value='Default'),
                          ),
                  outputs=( dict(name='vis_seq', interface=None), )
                )
    package.add_factory(nf)


    nf = Factory( name= "Iterables to Sequence", 
                  description="Generates VisualSequence from 2 iterables", 
                  category="Vizualisation", 
                  nodemodule="plotable2",
                  nodeclass="seqs2VisualSequence",
                  inputs=(dict(name='seq1', interface=ISequence),
                            dict(name='seq2', interface=ISequence),
                          ),
                  outputs=( dict(name='vis_seq', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Dict to Sequence", 
                  description="Generates VisualSequence from a dictionary", 
                  category="Vizualisation", 
                  nodemodule="plotable2",
                  nodeclass="dict2VisualSequence",
                  inputs=(dict(name='dict', interface=IDict),
                          ),
                  outputs=( dict(name='vis_seq', interface=None), )
                )
    package.add_factory(nf)



    pkgmanager.add_package(package)



