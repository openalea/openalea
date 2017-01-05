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

from Qt import QtCore, QtGui, QtWidgets

from openalea.visualea.graph_operator import GraphOperator

from openalea.grapheditor import baselisteners, qtgraphview, edgefactory, qtutils

class FloatingEdge(QtWidgets.QGraphicsPathItem, qtgraphview.FloatingEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    and deleted at the end of the user
    interaction
    """

    def __init__(self, srcPoint, graph):
        QtWidgets.QGraphicsPathItem.__init__(self, None)
        qtgraphview.FloatingEdge.__init__(self, srcPoint, graph)

    def get_connections(self):
        boxsize = 10.0
        #find the port items that were activated
        srcPortItem = self.scene().itemAt( self.srcPoint )
        dstPortItem = self.scene().find_closest_connectable(self.dstPoint, boxsize)
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
        if( self.scene().is_output(srcPortItem.port()) and
            self.scene().is_input(dstPortItem.port())):
            return (srcVertexItem.vertex(), srcPortItem.port()), \
                (dstVertexItem.vertex(), dstPortItem.port()), \
                srcPortItem, dstPortItem
        elif( self.scene().is_input(srcPortItem.port()) and
              self.scene().is_output(dstPortItem.port())):
            return (dstVertexItem.vertex(), dstPortItem.port()), \
                (srcVertexItem.vertex(), srcPortItem.port()), \
                srcPortItem, dstPortItem
        else:
            raise Exception("Nonsense connection : " + \
                                "plugging input to input or output to output")

class GraphicalEdge(QtWidgets.QGraphicsPathItem, qtgraphview.Edge):
    """ An edge between two graphical vertices """

    def __init__(self, edgeModel, graphadapter, port1, port2, parent=None):
        """ """
        QtWidgets.QGraphicsPathItem.__init__(self, parent)
        qtgraphview.Edge.__init__(self, edgeModel, graphadapter, port1, port2)
        self.__edge_creator = self.set_edge_creator(edgefactory.SplineEdgePath())

    def remove(self):
        self.scene().get_adapter().remove_edge( (self.srcBBox().vertex(), self.srcBBox()),
                                                (self.dstBBox().vertex(), self.dstBBox()) )

    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""
        menu = qtutils.AleaQMenu(event.widget())
        action = menu.addAction("Delete connection")
        action.triggered.connect(self.remove)
        menu.show()
        menu.move(event.screenPos())
        event.accept()
