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

__authors__ = """David Da Silva, Szymon Stoma"""
__contact__ = ""
__license__ = "Cecill-C"
__date__ = "<Timestamp>"
__version__ = "0.1"
__docformat__ =  "restructuredtext en"
__revision__ = "$Id$"


from openalea.core import *
#from openalea.catalog.plotable import *

#class PointsPlot2D(object):
#    """Generate a plot from 2D plotable object
#    Input 0 : 2D plotable object list"""
#    def __call__( self, plotObjList, title, xlabel, ylabel, **keys ):
#        plot_plotable(  plotable_list=plotObjList, title=title,
#           xlabel=xlabel, ylabel=ylabel, **keys )        
#
#
#
#
#class IPointsPlot2DStyle(Node):
#    """Interface for points plotable object.
#    
#    <Long description of the class functionality.>
#    """
#
#    def __call__( self, inputs ):
#        """Returns plotable object with changed the values which were
#           changed from default.
#        
#        <Long description of the function functionality.>
#        
#        :parameters:
#            arg1 : `T`
#                <Description of `arg1` meaning>
#        :rtype: `PlotableObject`
#        :return: Updated PlotableObject.
#        :raise Exception: <Description of situation raising `Exception`>
#        """
#        #plotable, legend, linestyle, marker, color 
#        plotable = self.get_input( "plotable" )
#        legend = self.get_input( "legend" )
#        linestyle = self.get_input( "linestyle" )
#        marker = self.get_input( "marker" )
#        color = self.get_input( "color" )
#        if not linestyle=="Default":
#            plotable.linestyle = linestyle
#        if not marker=="Default":
#            plotable.marker = marker
#        if not color=="Default":
#            plotable.color = color
#        if not legend=="Default":
#            plotable.legend = legend
#        return  plotable
