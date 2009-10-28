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

import sys, numpy, weakref
from PyQt4 import QtCore, QtGui

from .. import gengraphview
from .. import qtgraphview

import openalea.core.node


class AbstractEdge(QtGui.QGraphicsPathItem, qtgraphview.QtGraphViewEdge):
    """
    Base class for edges 
    """

    def __init__(self, edge, src=None, dst=None, parent=None):
        QtGui.QGraphicsPathItem.__init__(self, parent)
        qtgraphview.QtGraphViewEdge.__init__(self, edge, src, dst)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()

        self.edge_path = qtgraphview.edge_factory()
        path = self.edge_path.get_path(self.sourcePoint, self.destPoint)
        self.setPath(path)

        self.setPen(QtGui.QPen(QtCore.Qt.black, 3,
                               QtCore.Qt.SolidLine,
                               QtCore.Qt.RoundCap,
                               QtCore.Qt.RoundJoin))

    def shape(self):
        path = self.edge_path.shape()
        if not path:
            return QtGui.QGraphicsPathItem.shape(self)
        else:
            return path
        
    def update_line(self):
        path = self.edge_path.get_path(self.sourcePoint, self.destPoint)
        self.setPath(path)

    def paint(self, painter, options, widget):
        QtGui.QGraphicsPathItem.paint(self, painter, options, widget)


class AleaQtFloatingEdge(AbstractEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    and deleted at the end of the user
    interaction
    """

    def __init__(self, srcPoint):
        AbstractEdge.__init__(self, None)
        self.sourcePoint = QtCore.QPointF(*srcPoint)

    def set_destination_point(self, *args):
        self.destPoint = QtCore.QPointF(*args)

    def notify(self, sender, event):
        return 

    def consolidate(self, model):
        try:
            srcNode, idSrc, dstNode, idDst = self.get_connections()
            model.connect(srcNode.get_id(), idSrc, dstNode.get_id(), idDst)
        except Exception, e:
            print "consolidation failed :", e
        return
        
    def get_connections(self):
        #find the port items that were activated
        srcPortItem = self.scene().itemAt( self.sourcePoint )
        dstPortItem = self.scene().itemAt( self.destPoint   )

        #find the node items that were activated
        srcNodeItem = srcPortItem.parentItem()
        dstNodeItem = dstPortItem.parentItem()

        #if the input and the output are on the same node...
        if(srcPortItem.observed().node() == dstPortItem.observed().node()):
            raise Exception("Nonsense connection : plugging self to self.")            

        #actually, the source might not be an output, and the target
        #might not be an input, so we sort:
        if( isinstance(srcPortItem.observed(), openalea.core.node.OutputPort) and
            isinstance(dstPortItem.observed(), openalea.core.node.InputPort)):
            print "right side"
            return srcNodeItem.observed(), srcPortItem.get_index(), \
                dstNodeItem.observed(), dstPortItem.get_index()
        elif( isinstance(srcPortItem.observed(), openalea.core.node.InputPort) and
              isinstance(dstPortItem.observed(), openalea.core.node.OutputPort)):
            print "opposite side"
            return dstNodeItem.observed(), dstPortItem.get_index(), \
                srcNodeItem.observed(), srcPortItem.get_index()
        else:
            raise Exception("Nonsense connection : " + \
                                "plugging input to input or output to output")


class AleaQtGraphicalEdge(AbstractEdge):
    """ An edge between two graphical nodes """
        
    def __init__(self, edgeModel, port1, port2, parent=None):
        """ """
        AbstractEdge.__init__(self, edgeModel, port1, port2, parent)
        self.initialise_from_model()

    def update_line_source(self, *pos):
        self.sourcePoint = QtCore.QPointF(*pos)
        self.update_line()

    def update_line_destination(self, *pos):
        self.destPoint = QtCore.QPointF(*pos)
        self.update_line()

    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.scene().views()[0])

        action = menu.addAction("Delete connection")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        
        menu.move(event.screenPos())
        menu.show()

        event.accept()

    def remove(self):
        view = self.scene().views()[0]
        view.observed().disconnect(self.src().node().get_id(), self.src().get_id(),
                                   self.dst().node().get_id(), self.dst().get_id())
        
