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

import weakref
from PyQt4 import QtCore, QtGui

from .. import qtgraphview
from .. import edgefactory


class FloatingEdge(QtGui.QGraphicsPathItem, qtgraphview.QtGraphViewFloatingEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    and deleted at the end of the user
    interaction
    """

    def __init__(self, srcPoint, graphadapter):
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.QtGraphViewFloatingEdge.__init__(self, srcPoint, graphadapter)
        
    def get_connections(self):
        #find the port items that were activated
        srcPortItem = self.scene().itemAt( self.sourcePoint )
        dstPortItem = self.scene().itemAt( self.destPoint   )

        #find the vertex items that were activated
        srcVertexItem = srcPortItem.parentItem()
        dstVertexItem = dstPortItem.parentItem()

        #if the input and the output are on the same vertex...
        if(srcPortItem.port().vertex() == dstPortItem.port().vertex()):
            raise Exception("Nonsense connection : plugging self to self.")            

        #actually, the source might not be an output, and the target
        #might not be an input, so we sort:
        if( self.graph.is_output(srcPortItem.port()) and 
            self.graph.is_input(dstPortItem.port())):
            return (srcVertexItem.vertex(), srcPortItem.port()), \
                (dstVertexItem.vertex(), dstPortItem.port())
        elif( self.graph.is_input(srcPortItem.port()) and 
              self.graph.is_output(dstPortItem.port())):
            return (dstVertexItem.vertex(), dstPortItem.port()), \
                (srcVertexItem.vertex(), srcPortItem.port())
        else:
            raise Exception("Nonsense connection : " + \
                                "plugging input to input or output to output")


class GraphicalEdge(QtGui.QGraphicsPathItem, qtgraphview.QtGraphViewEdge):
    """ An edge between two graphical vertices """
        
    def __init__(self, edgeModel, graphadapter, port1, port2, parent=None):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, parent)
        qtgraphview.QtGraphViewEdge.__init__(self, edgeModel, graphadapter, port1, port2)
        self.initialise_from_model()


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""
        menu = QtGui.QMenu(self.scene().views()[0])
        action = menu.addAction("Delete connection")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        menu.move(event.screenPos())
        menu.show()
        event.accept()
        
    def remove(self):
        self.graph.remove_edge( (self.src().vertex(), self.src()),
                                (self.dst().vertex(), self.dst()) )
