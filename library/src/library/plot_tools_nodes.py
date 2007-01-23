# -*- python -*-
#
#       OpenAlea Library: OpenAlea Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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
utils nodes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



#from core.core import Node
#from openalea.core.interface import IFloat
#from openalea.core.interface import IStr
from openalea.core import *
import plot_tools


class plot2D( Node ):
    """Generate a plot from 2D plotable object
    Input 0 : 2D plotable object list"""

    def __init__(self ):
        Node.__init__( self )

        #defines I/O
        self.add_input( name='plotObjList', interface=Node )
        self.add_input( name='title', interface=IStr, value='MyPlot' )
        self.add_input( name='xlabel', interface=IStr, value='x-axis' )
        self.add_input( name='ylabel', interface=IStr, value='y-axis' )

    def __call__( self, inputs=() ):
        plot_tools.plot2D( self.get_input_by_key( 'plotObjList' ), self.get_input_by_key( 'title' ), self.get_input_by_key( 'xlabel' ), self.get_input_by_key( 'ylabel' ) )
