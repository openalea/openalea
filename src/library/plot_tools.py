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
plot_tools nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: utils_nodes.py $ "



import pylab
from matplotlib import rc
rc( 'text', usetex=True )

"""
:Abstract: Contain plot tools
"""

##########################Plotting utils#######################################

def plot2D( objList = None, title='MyPlot', xlabel='x-axis', ylabel='yaxis' ):
    if objList == None :
        pass
    else :
        legend =[]
        for obj in objList :
            pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color )
            legend.append(r''+obj.legend )
        pylab.legend( tuple( legend ), loc='best', shadow=True )
        pylab.title( title )
        pylab.xlabel( xlabel )
        pylab.ylabel( ylabel )
        pylab.show()


class plotObject:

    def __init__( self, x, y, legend, linestyle, marker, color, ):
        self.x = x
        self.y = y
        self.legend = legend
        self.linestyle = linestyle
        self.marker = marker
        self.color = color
