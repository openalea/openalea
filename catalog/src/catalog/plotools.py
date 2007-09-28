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

__doc__="""
plotting tools
"""


from openalea.core import *
from openalea.catalog.plotable import *

class Plot2D(object):
    """Generate a plot from 2D plotable object
    Input 0 : 2D plotable object list"""
    def __call__( self, plotObjList, title, xlabel, ylabel, **keys ):
        plot_plotable(  plotable_list=plotObjList, title=title, xlabel=xlabel, ylabel=ylabel, **keys )        

