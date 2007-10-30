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
from openalea.plotools import plotable

import rpy
import pylab

def chisqtest(x,y = [], p = []):
    """
    Compute the Student's t-test

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values
     - 'y': an optional (non-empty) numeric vector of data values
     - 'p': an optional (non_empty) numeric vector of probabilities

    :Types:
     - 'x': float list
     - 'y': float list
     - 'p': float list

     :Returns the p-value of the Chi-square test
     :Returntype: float list

     :attention: the 2 vectors must have the same size and the sum of probabilities must be equal to 1   
     """
    
    if p == []:
        p = rpy.r.rep(1./len(x), len(x))
        
    if y == []:
        res = rpy.r.chisq_test(x,p=p)
        TestType = 'Chi-square goodness-of-fit test'
    else:
        res = rpy.r.chisq_test(x,y)
        TestType = 'Chi-square test for contingency table, chi-square test for independence'

    pvalue = res['p.value']
    statistic = res['statistic']['X-squared']
    
    data = {'Test Type':TestType, 'p.value':pvalue, 'X-squared':statistic} 
    return data



def random_continuous_law(law ,n , args):
    """
    Generate random values from continuous distribution

    :Parameters:
     - 'law': distribution to simulate
     - 'n' : number of random values
     - 'args': parameters of continuous distribution to simulate

     :Types:
     - 'law': string
     - 'n': int
     - 'args': float list

     :Returns the vector of the random values from continuous distributions
     :Returntype: float list

     :attention:  n must be greater than 0
     """

    if law == 'norm':
        res = rpy.r.rnorm(n, mean = args[0], sd = args[1])
    else:
        if law == 'unif':
            res = rpy.r.runif(n, args[0], args[1])
        else:
           if law == 'exp':
               res = rpy.r.rexp(n, rate = args[0])

    return (res,)

def random_discrete_law(law ,n , args):
    """
    Generate random values from discrete distribution

    :Parameters:
     - 'law': distribution to simulate
     - 'n' : number of random values
     - 'args': parameters of discrete distribution to simulate

     :Types:
     - 'law': string
     - 'n': int
     - 'args': float list

     :Returns the vector of the random values from discrete distributions
     :Returntype: float list

     :attention:  n must be greater than 0
     """

    if law == 'binom':
        res = rpy.r.rbinom(n, size = args[0], prob = args[1])
    else:
        if law == 'pois':
            res = rpy.r.rpois(n, args[0])
        else:
           if law == 'geom':
               res = rpy.r.rgeom(n, prob = args[0])

    return (res,)


def StatSummary( x ):
    """
    Compute the statistical summary (min, max, median, mean, sd) 

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values

     :Types:
     - 'x': float list

     :Returns the vector of the statistical summary
     :Returntype: float list

     :attention:  x cannot be empty
     """

    result = rpy.r.summary(x)
    minimum = result['Min.']
    maximum = result['Max.']
    median = result['Median']
    mean = result['Mean']
    sd = rpy.r.sd(x)

    data = {'minimum':minimum, 'maximum':maximum, 'median':median, 'mean':mean, 'standard deviation':sd}
    return data


def Corr( x , y ):#= []):
    """
    Compute the statistical correlation

    :Parameters:
     - 'x': a (non-empty) numeric vector of data values 
     - 'y': an optionnal (non-empty) numeric vector of data values

     :Types:
     - 'x': float list
     - 'y': float list

     :Returns the vector of the correlation
     :Returntype: float list

     :attention:  x cannot be empty, x and y must have the same size
     """

    res = rpy.r.cor(x,y)
        
    data = {'Cor': res, 'x':x, 'y':y}

    return data


def Glm(x, y, famil = 'gaussian'): 
    """
    Compute the slope and intercept of the 2 given vector generalized linear regression.
    
    :Parameters:
     - `x`: X-axis values
     - `y`: Y-axis values
     - 'famil': family objects for models and link function
    
    :Types:
     - `x`: float list
     - `y`: float list
     - 'famil': string
    
    :Returns: the slope and the intercept of the generalized linear regression
    :Returntype: float cople

    :attention: the 2 vector/list must have the same size
    """
    
    model = rpy.r("Y~X")

    d = rpy.r.data_frame(X=x, Y=y)

    reg = rpy.r.glm(model, data = d, family = famil)


    #print reg
    
    intercept = reg['coefficients']['(Intercept)']
    slope = reg['coefficients']['X']
    family = reg['family']['family']
    #link = reg['link']

    data = {'Intercept':intercept, 'Slope':slope, 'Family': famil}#, 'Link':lin}
    return data
    


############## Linear regression section ##########################

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
    """
    Generate 2 plotable object from a linear regression
    Input 0 : linear regression object
    Output 0 : plotable object from points
    Output 1 : plotable object from regression line
    """

    def __init__( self, inputs, outputs):

        Node.__init__( self, inputs, outputs )

    def __call__( self, inputs ):

        reg=self.get_input( 'reg' )
        reg_x=rpy.array( [ min(reg[ 'x' ]), max(reg[ 'x' ]) ] )
        reg_y = reg_x*reg[ 'pente' ]+reg[ 'intercept' ]
        if reg.has_key('ic'):
          reg_legend = "y = "+str( round( reg[ 'pente' ],3 ) )+ \
                       "x + "+str( round(reg[ 'intercept' ],3 ))+ \
                       " $\pm$ "+str( round( reg[ 'ic' ],3 ) )+ \
                       r"    $r^2$ = "+str( round( reg[ 'r2' ],3 ) )
        else :
          reg_legend = "y = "+str( round( reg[ 'pente' ],3 ) )+ \
                       "x + "+str( round(reg[ 'intercept' ],3 ))+ \
                       r"    $r^2$ = "+str( round( reg[ 'r2' ],3 ) )
        reg_color='red'
        points = plotable.VisualSequence2D( x=reg[ 'x' ], y=reg[ 'y' ], legend= 'Data', linestyle='None', marker = '^', color='dodgerblue' )
        line = plotable.VisualSequence2D( x=reg_x, y=reg_y, legend=reg_legend, linestyle='-', marker='None', color=reg_color )
        return ( points, line )


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
 
############## End of section #####################################

