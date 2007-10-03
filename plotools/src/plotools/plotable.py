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
__revision__="$Id: plotable.py 805 2007-10-01 17:01:00Z stymek $"

from matplotlib import rc, rcParams,use
rc('text', usetex=True )
use('Qt4Agg')
import pylab

#the following allows a smooth use of pylab windows with Qt4.2#
try:
  from matplotlib.backends.backend_qt4 import qApp
except ImportError:
  import matplotlib as mymat
  from matplotlib.backends import backend_qt4, backend_qt4agg
  from PyQt4 import QtGui
  backend_qt4.qApp = QtGui.qApp
  backend_qt4agg.matplotlib = mymat
#=============================================================#

class Hist2D(object):
    """Object containing basic plot information.
    
    <Long description of the function functionality.>    
    """

    def __init__( self, y=[], bins=10 ):
        """Object used to store histogram plot information. 
        
        It use the syntax of mathplot lib so go there for details.
        
        :parameters:
            y : `[float]`
                values f(X)
            bins : `int`
                Number of bins

        
        """  
        self.y = y
        self.bins = bins
        
class VisualSequence2D(object):
    """Object containing basic plot information.
    
    <Long description of the function functionality.>    
    """

    def __init__( self, x=[], y=[], legend="", linestyle="", marker="", color="", bins=10 ):
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
        self.bins = bins

def change_VisualSequence2D( vis_seq2D, new_legend, new_linestyle, new_marker, new_color ): 

        """Returns vis_seq2D object with values changed from default
        
        :parameters:
            vis_seq2D : `VisualSequence2D`
                object to be modified
            legend : `string`
                legend of a line
            linestyle : `string`
                One of - : -. -
            marker : `string`
                One of + , o . s v x > <,
            color : `string`
                A matplotlib color arg
        :rtype: `VisualSequence2D`
        :return: Updated object.
        """

        #plotable = self.get_input( "plotable" )
        #legend = self.get_input( "legend" )
        #linestyle = self.get_input( "linestyle" )
        #marker = self.get_input( "marker" )
        #color = self.get_input( "color" )
        plotable = vis_seq2D
        if not new_linestyle=="Default":
            plotable.linestyle = new_linestyle
        if not new_marker=="Default":
            plotable.marker = new_marker
        if not new_color=="Default":
            plotable.color = new_color
        if not new_legend=="Default":
            plotable.legend = new_legend
        return  plotable

def display_VisualSequence2D(  vis_seq_list=[], title="", xlabel="", ylabel="", **keys ):
    """Plots 2D visual sequences.
    
    :parameters:
        vis_seq_list : `[VisualSequence2D]`
            Contains a list of object to display
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    objList=vis_seq_list
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
        obj=vis_seq_list
        pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color, **keys )

    xmin, xmax = pylab.xlim()
    xr = (xmax-xmin)/20.
    pylab.xlim(xmin-xr, xmax+xr)
    ymin, ymax = pylab.ylim()
    yr = (ymax-ymin)/20.
    pylab.ylim(ymin-yr, ymax+yr)
    pylab.title( title )
    pylab.xlabel( xlabel )
    pylab.ylabel( ylabel )
    pylab.show()

def display_VisualSequence2D_as_hist(  hist_list=[], title="", xlabel="", ylabel="", **keys ):
    """Plots 2D visual sequences.
    
    :parameters:
        vis_seq_list : `[VisualSequence2D]`
            Contains a list of object to display
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    objList=vis_seq_list
    pylab.cla()
    try:
        iter( objList )
        for obj in objList :
            pylab.hist( obj.y, bins=obj.bins, **keys )
    except  TypeError:
        # do sth with exceptions
        obj=hist_list
        pylab.plot( obj.y, obj.bins **keys )

    pylab.title( title )
    pylab.xlabel( xlabel )
    pylab.ylabel( ylabel )
    pylab.show()


def seqs2VisualSequence2D( seq1=[], seq2=[], legend="", linestyle="",marker="o", color="b", **keys ):
    """generates visual sequence2D with list1 as x  and list2 as y
    
    :parameters:
        seq1 : `iterable`
            Contains the x sequence
        seq2 : `iterable`
            Contains the x sequence
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    return VisualSequence2D(x=seq1, y=seq2, legend=legend, linestyle=linestyle, marker=marker, color=color )
       

def dict2VisualSequence2D(  dict2vis_seq={}, legend="", linestyle="",marker="o", color="g", **keys ):
    """generates visual sequence2D with keys as x  and values as y
    
    :parameters:
        dict2vis_seq : `dict{float:float}`
            Contains a list of object to display
        title : `string`
            Title of the plot.
        xlabel : `string`
            X axis description
        ylabel : `string`
            Y label description
    """
    r=list(dict2vis_seq.items())
    r.sort()
    return VisualSequence2D(x=[r[i][0] for i in range(len(r))], y=[r[i][1] for i in range(len(r))], legend=legend, linestyle=linestyle, marker=marker, color=color )

