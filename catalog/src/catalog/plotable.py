#!/usr/bin/env python
"""Definition of plotable object


Mainly based on mathplotlib.

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""
# Module documentation variables:
__authors__="""David Da Silva,
Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"


from matplotlib import rc, rcParams,use
rc('text', usetex=True )
use('Qt4Agg')
import pylab


class PlotableObject(object):
    """Object containing basic plot information.
    
    <Long description of the function functionality.>    
    """

    def __init__( self, x=[], y=[], legend="", linestyle="", marker="", color="" ):
        """Object used to store plot information. 
        
        It use the syntax of mathplot lib so go there for details.
        
        :parameters:
            x : `[float]`
                X coordinates
            y : `[float]`
                values f(X)
            legend : `string`
                legend of a line
            linestyle : `string`
                One of - : -. -
            marker : `string`
                One of + , o . s v x > <,
            color : `string`
                A matplotlib color arg

        
        """  
        self.x = x
        self.y = y
        self.legend = str(legend)
        self.linestyle = str(linestyle)
        self.marker = str(marker)
        self.color = str(color)



def plot_plotable(  plotable_list=[], title="", xlabel="", ylabel="", **keys ):
    """Plots plotable Object.
    
    :parameters:
        plotable_list : `[PlotableObject]`
            Contains primordium id to creation time mapping.
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    objList=plotable_list
    pylab.cla()
    legend_printed = False
    try:
        iter( objList )
        legend =[]
        for obj in objList :
            pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color, **keys )
            if obj.legend:
                legend.append(r''+obj.legend )
                legend_printed = True
        if legend_printed: pylab.legend( tuple( legend ), loc='best', shadow=True )
    except  TypeError:
        # do sth with exceptions
        obj=plotable_list
        pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color, **keys )
        #if obj.legend:
        #    pylab.legend( (obj.legend), loc='best', shadow=True )
    pylab.title( title )
    pylab.xlabel( xlabel )
    pylab.ylabel( ylabel )
    pylab.show()
        
            
def plot_single_plotable(  plotable=PlotableObject(), title="", xlabel="", ylabel="", **keys ):
    """Plots plotable Object.
    
    :parameters:
        plotable : `PlotableObject`
            Contains primordium id to creation time mapping.
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    plot_plotable( [ plotable ], title=title, xlabel=xlabel, ylabel=ylabel, **keys )


def generate_plotable_from_dict(  dict2plotable={}, legend="", linestyle="-",marker=".", color="r", **keys ):
    """Plots plotable Object.
    
    :parameters:
        plotable : `PlotableObject`
            Contains primordium id to creation time mapping.
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    r=list(dict2plotable.items())
    r.sort()
    #print [r[i][0] for i in range(len(r))]
    return PlotableObject(x=[r[i][0] for i in range(len(r))], y=[r[i][1] for i in range(len(r))], legend=legend, linestyle=linestyle, marker=marker, color=color )

