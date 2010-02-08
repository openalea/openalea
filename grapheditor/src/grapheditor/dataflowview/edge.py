# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import weakref
from PyQt4 import QtCore, QtGui

from openalea.grapheditor import qtgraphview
from openalea.grapheditor import edgefactory
import vertex
from openalea.grapheditor import baselisteners

from math import sqrt

class FloatingEdge(QtGui.QGraphicsPathItem, qtgraphview.FloatingEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    and deleted at the end of the user
    interaction
    """

    def __init__(self, srcPoint, graph):
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.FloatingEdge.__init__(self, srcPoint, graph)
        self.setZValue(0.0)
        
    def get_connections(self):
        boxsize = 10.0
        #find the port items that were activated
        srcPortItem = self.scene().itemAt( self.sourcePoint )

        #creation of a square which is a selected zone for ports 
        rect = QtCore.QRectF((self.destPoint.x() - boxsize/2), 
                             (self.destPoint.y() - boxsize/2), 
                             boxsize, boxsize);
        dstPortItems = self.scene().items(rect)        
        #the following could be more generic maybe?
        dstPortItems = [item for item in dstPortItems if isinstance(item, vertex.GraphicalPort)]

        distance = float('inf')
        dstPortItem = None
                 
        for item in dstPortItems:
            d = sqrt((item.boundingRect().center().x() - self.destPoint.x())**2 + 
                        (item.boundingRect().center().y() - self.destPoint.y())**2)
            if d < distance:
                distance = d
                dstPortItem = item

        if not dstPortItem: return None, None 

        #find the vertex items that were activated
        srcVertexItem = srcPortItem.parentItem()
        dstVertexItem = dstPortItem.parentItem()

        if(not hasattr(dstPortItem, "port")): return None, None

        #if the input and the output are on the same vertex...
        if(srcPortItem.port().vertex() == dstPortItem.port().vertex()):
            raise Exception("Nonsense connection : plugging self to self.")         

        #actually, the source might not be an output, and the target
        #might not be an input, so we sort:
        if( self.graph().is_output(srcPortItem.port()) and 
            self.graph().is_input(dstPortItem.port())):
            return (srcVertexItem.vertex(), srcPortItem.port()), \
                (dstVertexItem.vertex(), dstPortItem.port())
        elif( self.graph().is_input(srcPortItem.port()) and 
              self.graph().is_output(dstPortItem.port())):
            return (dstVertexItem.vertex(), dstPortItem.port()), \
                (srcVertexItem.vertex(), srcPortItem.port())
        else:
            raise Exception("Nonsense connection : " + \
                                "plugging input to input or output to output")


class GraphicalEdge(QtGui.QGraphicsPathItem, qtgraphview.Edge):
    """ An edge between two graphical vertices """
        
    def __init__(self, edgeModel, graphadapter, port1, port2, parent=None):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, parent)
        qtgraphview.Edge.__init__(self, edgeModel, graphadapter, port1, port2)
        self.setZValue(0.5)
        self.initialise_from_model()

    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""
        menu = QtGui.QMenu(event.widget())
        action = menu.addAction("Delete connection")
        action.triggered.connect(self.remove)
        menu.move(event.screenPos())
        menu.show()
        event.accept()
        
    def remove(self):
        self.graph().remove_edge( (self.srcBBox().vertex(), self.srcBBox()),
                                  (self.dstBBox().vertex(), self.dstBBox()) )

    store_view_data = None
    get_view_data   = None
    announce_view_data = None

    def announce_view_data_src(self, exclusive=False):
        if not exclusive:
            self.srcBBox().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.srcBBox().exclusive_command(exclusive, 
                                             self.srcBBox().get_ad_hoc_dict().simulate_full_data_change)

    def announce_view_data_dst(self, exclusive=False):
        if not exclusive:
            self.dstBBox().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.dstBBox().exclusive_command(exclusive, 
                                             self.dstBBox().get_ad_hoc_dict().simulate_full_data_change)
