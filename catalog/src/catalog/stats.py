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
stats tools
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core import *
import rpy
import plotable
from matplotlib import rc, use
rc( 'text', usetex=True )
use('Qt4Agg')
import pylab

############## Node definition ##########################
class LinearRegression( Node ):
    """Linear regression 
    Input 0 : X values
    Input 1 : Y values
    Input 2 : alpha
    Output 0 : linear regression output"""

    def __init__( self, inputs, outputs ):

        Node.__init__( self, inputs, outputs )

    def __call__( self, inputs ):
        """ inputs is the list of input values """
        if self.get_input( "origin" ):
            print "Origin will not work if x values are < 0"
            reg = regLinOri(self.get_input( "X" ),self.get_input( "Y" ),self.get_input( "alpha" ) )
        else:
            reg = regLin(self.get_input( "X" ),self.get_input( "Y" ),self.get_input( "alpha" ) )
        return ( reg, )

class LR2Plot( Node ):
    """Generate a plotable object from a linear regression
    Input 0 : linear regression object
    Output 0 : plotable object"""

    def __init__( self, inputs, outputs):

        Node.__init__( self, inputs, outputs )

    def __call__( self, inputs ):

        reg=self.get_input( 'reg' )
        reg_x=pylab.array( [ min(reg[ 'x' ]), max(reg[ 'x' ]) ] )
        reg_y = reg_x*reg[ 'pente' ]+reg[ 'intercept' ]
        reg_legend = "y = "+str( round( reg[ 'pente' ],3 ) )+ \
                     "x + "+str( round(reg[ 'intercept' ],3 ))+ \
                     " $\pm$ "+str( round( reg[ 'ic' ],3 ) )+ \
                     "    r2 = "+str( round( reg[ 'r2' ],3 ) )
        reg_color='red'
        points = plotable.PlotableObject( x=reg[ 'x' ], y=reg[ 'y' ], legend= 'Data', linestyle='None', marker = '^', color='dodgerblue' )
        line = plotable.PlotableObject( x=reg_x, y=reg_y, legend=reg_legend, linestyle='-', marker='None', color=reg_color )
        #resseq = []
        #resseq.append(points)
        #resseq.append(line)
        return ( points, line )

############## End of Node definition ###################

def regression(x, y, regmodel, alpha ): 
    d = rpy.r.data_frame(X=x, Y=y)
    model = regmodel
    #reg = rpy.r.lm(model, data = d)
    n=rpy.sqrt( len( x ) )
    norm=rpy.r.qnorm( 1. - ( alpha/200. ) )
    Rlm = rpy.with_mode(rpy.NO_CONVERSION, rpy.r.lm)
    reg2 = Rlm(model, data = d)
    result = rpy.r.summary(reg2)
    coef=result['coefficients']
    r2 = result['r.squared']
    r2adj = result['adj.r.squared']
    ic = result[ 'sigma' ]*norm/n
    try:
      pente = coef[1][0]
      intercept = coef[0][0]
    except IndexError :
      pente = coef[0][0]
      intercept = 0

    data = {'pente':pente, 'intercept':intercept, 'r2':r2, 'adj_r2':r2adj, 'ic':ic, 'x':x, 'y':y}
    return data

def multiReg(x, y, colList, alpha):
    #d = rpy.r.data_frame(y)
    newX=[]
    d = {'Y':y}
    model_string = "Y~"
    #names = ["Y"]
    for i in colList:
      name = "X"+str(i) 
      #names.append( name )
      d[name] = x[i]
      newX.append(x[i])
      model_string = model_string + name + "+"
    print d
    #rpy.r.colnames(d) = names
    model_string = model_string + "1"
    model = rpy.r(model_string)

    n=rpy.sqrt( len( y ) )
    norm=rpy.r.qnorm( 1. - ( alpha/200. ) )
    Rlm = rpy.with_mode(rpy.NO_CONVERSION, rpy.r.lm)
    reg = Rlm(model, data = d)
    result = rpy.r.summary(reg)
    print result
    coef =result['coefficients']
    r2 = result['r.squared']
    r2adj = result['adj.r.squared']
    ic = result[ 'sigma' ]*norm/n
    regressor = coef[:,0]

    data = {'regressor':regressor[1:], 'intercept':regressor[0], 'r2':r2, 'adj_r2':r2adj, 'ic':ic, 'x':newX, 'y':y}
    return data
   
def regLin(x, y, alpha=5):
    """
    Compute the slope and intercept of the 2 given vector linear regression.
    
    :Parameters:
     - `x`: X-axis values
     - `y`: Y-axis values
    
    :Types:
     - `x`: float list
     - `y`: float list
    
    :Returns: the slope and the intercept of the linear regression
    :Returntype: float cople

    :attention: the 2 vector/list must have the same size
    """
    model = rpy.r("Y~X")
    data = regression(x, y, model, alpha )
    return data
    
    #return (reg['coefficients']['X'], reg['coefficients']['(Intercept)']) 

    
def regLinOri(x, y, alpha=5):
    """
    Compute the slope of the 2 given vector pass-through-origin linear regression.
    
    :Parameters:
     - `x`: X-axis values
     - `y`: Y-axis values

    :Types:
     - `x`: float list
     - `y`: float list

    :Returns: the slope of the linear regression
    :Returntype: float
    
    :attention: the 2 vector/list must have the same size
    """
    model = rpy.r("Y~-1+X")
    data = regression(x, y, model, alpha )
    return data
    

