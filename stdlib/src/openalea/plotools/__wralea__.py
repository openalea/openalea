# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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

__revision__=" $Id$ "


from openalea.core import *
 
__name__ = "openalea.plottools"
__alias__ = ["plottools"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Plottools library'
__url__ = 'http://openalea.gforge.inria.fr'
                 

__all__ = []



vsplot = Factory( name= "VS Plot", 
              description="Plot a list of 2D points plotable objects", 
              category="Visualization,plot", 
              nodemodule="plotable",
              nodeclass="display_VisualSequence",
              inputs=(dict(name='vis_seq_list', interface=None, showwidget=False),
                      dict(name='visualisation', interface=IEnumStr(['PointLine', 'Hist']), 
                           value = 'PointLine'),
                      dict(name='title', interface=IStr, value='MyPlot'),
                      dict(name='xlabel', interface=IStr, value='x-axis-label'),
                      dict(name='ylabel', interface=IStr, value='y-axis-label'),
                      dict(name='figure', interface=IInt(0,10), value=0), ), 
              outputs=(dict(name='result', interface=None ),)

              )


__all__.append('vsplot')

ptline_style = Factory( name= "PointLine Style", 
              description="Allows us to edit VisualSequence plot", 
              category="Visualization,plot", 
              nodemodule="plotable",
              nodeclass="change_VisualSequence_PointLineView",
              inputs=(dict(name='vis_seq', interface=None, showwidget=False),
                      dict(name='new_legend', interface=IStr, value='Default'),
                      dict(name='new_linestyle', 
                           interface=IEnumStr( ['Default','-','--',':','-.'] )),
                      dict(name='new_marker', 
                           interface=IEnumStr( ['Default','.',',','o','^','v','<',
                                                '>','s','+','x','D','d','1','2','3',
                                                '4','h','H','p','p','|','_'] ) ),
                      dict(name='new_color', interface=IStr, value='Default'),
                          ),
              outputs=( dict(name='vis_seq', interface=None), )
              )


__all__.append('ptline_style')


hist_style = Factory( name= "Hist Style", 
                      description="Allows us to edit VisualSequence Hist style properties", 
                      category="Visualization,plot", 
                      nodemodule="plotable",
                      nodeclass="change_VisualSequence_HistView",
                      inputs=(dict(name='vis_seq', interface=None, showwidget=False),
                              dict(name='new_bins', interface=IInt, value=10),
                              dict(name='new_color', interface=IStr, value='Default'),
                              ),
                      outputs=( dict(name='vis_seq', interface=None), )
                      )


__all__.append('hist_style')

it2seq = Factory( name= "Iterables to Sequence", 
                  description="Generates VisualSequence from 2 iterables", 
                  category="codec", 
                  nodemodule="plotable",
                  nodeclass="seqs2VisualSequence",
                  inputs=(dict(name='seq1', interface=ISequence),
                          dict(name='seq2', interface=ISequence),
                          ),
                  outputs=( dict(name='vis_seq', interface=None), )
                  )

__all__.append('it2seq')
    
tuples2seq = Factory( name= "tuples2seq", 
                      description="Generates VisualSequence from 2-uples", 
                      category="codec", 
                      nodemodule="plotable",
                      nodeclass="tuples2VisualSequence",
                      inputs=(dict(name='seq1', interface=ISequence, desc='list of 2 uples'),                          ),
                      outputs=( dict(name='vis_seq', interface=None), )
                      )
    

__all__.append('tuples2seq')

dict2seq = Factory( name= "Dict to Sequence", 
                    description="Generates VisualSequence from a dictionary", 
                    category="codec", 
                    nodemodule="plotable",
                    nodeclass="dict2VisualSequence",
                    inputs=(dict(name='dict', interface=IDict),
                            ),
                    outputs=( dict(name='vis_seq', interface=None), )
                    )


__all__.append('dict2seq')


    


