# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): David Da SILVA <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Catalog.PlotTools 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


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
                 'description' : 'Catalog library.',
                 'url' : 'http://openalea.gforge.inria.fr'
                 }


    package = Package("Catalog.PlotTools", metainfo)

    nf = Factory( name= "SequencePlot2D", 
                  description="Plot a list of 2D points plotable objects", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="display_visual_sequence2D",
                  inputs=(dict(name='vis_seq2D_list', interface=ISequence, showwidget=False),
                          dict(name='title', interface=IStr, value='MyPlot'),
                          dict(name='xlabel', interface=IStr, value='x-axis-label'),
                          dict(name='ylabel', interface=IStr, value='y-axis-label'),  ),
                  outputs=()

                )

    package.add_factory(nf)


    nf = Factory( name= "SeqStyle", 
                  description="Allows us to edit plotable object", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="change_vis_seq2D",
                  inputs=(dict(name='vis_seq2D', interface=None, showwidget=False),
                            dict(name='new_legend', interface=IStr, value='Default'),
                            dict(name='new_linestyle', interface=IStr, value='Default'),
                            dict(name='new_marker', interface=IStr, value='Default'),
                            dict(name='new_color', interface=IStr, value='Default'), 
                          ),
                  outputs=( dict(name='vis_seq2D', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Iterable to Vis_Seq2D", 
                  description="Generates Vis_Seq2D from 2 iterables", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="seqs2visual_sequence2D",
                  inputs=(dict(name='seq1', interface=ISequence),
                            dict(name='seq2', interface=ISequence),
                          ),
                  outputs=( dict(name='vis_seq2D', interface=None), )
                )
    package.add_factory(nf)

    nf = Factory( name= "Dict to Vis_Seq2D", 
                  description="Generates Vis_Seq2D from a dictionary", 
                  category="Vizualisation", 
                  nodemodule="plotable",
                  nodeclass="dict2visual_sequence2D",
                  inputs=(dict(name='dict', interface=IDict),
                          ),
                  outputs=( dict(name='vis_seq2D', interface=None), )
                )
    package.add_factory(nf)


    pkgmanager.add_package(package)



