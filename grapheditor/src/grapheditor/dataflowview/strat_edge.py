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
            print e
        return
        
    def get_connections(self):
        srcItem = self.scene().itemAt( self.sourcePoint )
        dstItem = self.scene().itemAt( self.destPoint   )

        if(not srcItem or not dstItem):
            return

        if(not isinstance(srcItem, QtGui.QGraphicsProxyWidget) or 
            not isinstance(dstItem, QtGui.QGraphicsProxyWidget)):
            return

        #transform the points to item coordinate
        srcItemCoordPoint = srcItem.mapFromScene(self.sourcePoint)
        dstItemCoordPoint = dstItem.mapFromScene(self.destPoint)

        #find the widgets that were activated
        srcPortWidget=srcItem.widget().childAt(srcItemCoordPoint.toPoint())
        dstPortWidget=dstItem.widget().childAt(dstItemCoordPoint.toPoint())

        #actually, the source might not be an output, and the target
        #might not be an input, so we sort:
        if( isinstance(srcPortWidget.observed(), openalea.core.node.OutputPort) and
            isinstance(dstPortWidget.observed(), openalea.core.node.InputPort)):
            print "right side"
            return srcItem.observed(), srcPortWidget.get_index(), \
                dstItem.observed(), dstPortWidget.get_index()
        elif( isinstance(srcPortWidget.observed(), openalea.core.node.InputPort) and
              isinstance(dstPortWidget.observed(), openalea.core.node.OutputPort)):
            print "opposite side"
            return dstItem.observed(), dstPortWidget.get_index(), \
                srcItem.observed(), srcPortWidget.get_index()
        else:
            raise Exception("Nonsense connection")


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
        
