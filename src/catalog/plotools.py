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
plotting tools
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core import *
#import plotable
import pylab
from matplotlib import rc
rc( 'text', usetex=True )

class plot2D( Node ):
    """Generate a plot from 2D plotable object
    Input 0 : 2D plotable object list"""

    def __init__(self, inputs, outputs ):

        Node.__init__( self, inputs, outputs )


    def __call__( self, inputs ):
        objList = self.get_input( 'plotObjList' )
        title=self.get_input( 'title' )
        xlabel=self.get_input( 'xlabel' )
        ylabel=self.get_input( 'ylabel' )
        
        
        if objList == None :
          pass
        else :
            legend =[]
            for obj in objList :
        
                pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color )
                legend.append(r''+obj.legend )

            pylab.show()

            pylab.legend( tuple( legend ), loc='best', shadow=True )
            pylab.title( title )
            pylab.xlabel( xlabel )
            pylab.ylabel( ylabel )

