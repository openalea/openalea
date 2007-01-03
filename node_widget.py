# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the GPL License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.gnu.org/licenses/gpl.txt
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#       This code is inspired from the puzzle QT4 example

__doc__="""
SubGraph widget inspired.

"""

__license__= "GPL"
__revision__=" $Id$"


import sys
import math

from PyQt4 import QtCore, QtGui
from aleacore.core import NodeWidget


class DefaultNodeWidget(QtGui.QWidget, NodeWidget):
    """
    Default implementation of a NodeWidget
    It provide a input box for each parameter
    """

    def __init__(self, node, factory, parent=None):

        NodeWidget.__init__(self, node, factory)
        QtGui.QWidget.__init__(self, parent)

    # to complete


class SubGraphWidget(NodeWidget, QtGui.QGraphicsView):
    """ Subgraph widget allowing to edit the network """
    
    def __init__(self, node, factory, parent=None):

        NodeWidget.__init__(self, node, factory)
        QtGui.QGraphicsView.__init__(self, parent)

        self.timerId = 0

        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        #cene.setSceneRect(-200, -200, 400, 400)
        self.setScene(scene)
        #elf.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        node1 = GraphicalNode(self)
        node2 = GraphicalNode(self)
        node3 = GraphicalNode(self)
        node4 = GraphicalNode(self)

        node1.setPos(-200, -200)
        node2.setPos(0, -200)
        node3.setPos(200, -200)
        node4.setPos(-200, 0)

        e1 = Edge(node1, 0, node2, 0, None, scene)
        e2 = Edge(node2, 1, node3, 1, None, scene)


        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

    def drawBackground(self, painter, rect):
        pass

    def itemMoved(self):
        pass

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    
# class SubgraphWidget(NodeWidget, QtGui.QGraphicsView):
#     """ Subgraph widget allowing to edit the network """
    
#     def __init__(self, node, factory, parent=None):

#         NodeWidget.__init__(self, node, factory, parent)
    
#         self.piecePixmaps = []
#         self.pieceRects = []
#         self.highlightedRect = QtCore.QRect()
#         self.inPlace = 0

#         self.setAcceptDrops(True)

#     def clear(self):
#         self.piecePixmaps = []
#         self.pieceRects = []
#         self.highlightedRect = QtCore.QRect()
#         self.inPlace = 0
#         self.update()

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasFormat("openalea/nodefactory"):
#             event.accept()
#         else:
#             event.ignore()

#     def dragLeaveEvent(self, event):
#         updateRect = self.highlightedRect
#         self.highlightedRect = QtCore.QRect()
#         self.update(updateRect)
#         event.accept()

#     def dragMoveEvent(self, event):
#         updateRect = self.highlightedRect.unite(self.targetSquare(event.pos()))

#         if ( event.mimeData().hasFormat("openalea/nodefactory") ):
#             self.highlightedRect = self.targetSquare(event.pos())
#             event.setDropAction(QtCore.Qt.MoveAction)
#             event.accept()
#         else:
#             self.highlightedRect = QtCore.QRect()
#             event.ignore()

#         self.update(updateRect)

#     def dropEvent(self, event):

#         if (event.mimeData().hasFormat("openalea/nodefactory")):
#             pieceData = event.mimeData().data("openalea/nodefactory")
#             dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
#             square = self.targetSquare(event.pos())
#             pixmap = QtGui.QPixmap()
#             dataStream >> pixmap 

#             self.piecePixmaps.append(pixmap)
#             self.pieceRects.append(square)

#             self.hightlightedRect = QtCore.QRect()
#             self.update(square)

#             event.setDropAction(QtCore.Qt.MoveAction)
#             event.accept()

#         else:
#             self.highlightedRect = QtCore.QRect()
#             event.ignore()



#     def paintEvent(self, event):
#         painter = QtGui.QPainter()
#         painter.begin(self)
#         painter.fillRect(event.rect(), QtCore.Qt.white)

#         if self.highlightedRect.isValid():
#             painter.setBrush(QtGui.QColor(255, 0, 0, 127))
#             painter.setPen(QtCore.Qt.NoPen)
#             painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

#         for i in range(len(self.pieceRects)):
  
#             painter.setBrush(QtGui.QColor(0, 0, 255, 127))
#             painter.setPen(QtCore.Qt.NoPen)
#             painter.drawRect(self.pieceRects[i].adjusted(0, 0, -1, -1))
#             painter.drawPixmap(self.pieceRects[i], self.piecePixmaps[i])


#         painter.end()


#     def targetSquare(self, position):
#         """ Return the rectangle associated to position """
        
#         return QtCore.QRect(position.x()- 40/2, position.y()- 40/2, 40, 40)
    



class GraphicalNode(QtGui.QGraphicsItem):
    """ Represent a node in the subgraphwidget """

    Type = QtGui.QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, elt_id=0, ninput=2, noutput=2,  caption="Node"):
        """
        @param graphwidget : scene container
        @param elt_id : id in the subgraph
        @param ninput : number of input
        @param noutput : number of output
        @param caption : box text
        """

        scene = graphWidget.scene()

        QtGui.QGraphicsItem.__init__(self)

        self.elt_id = elt_id

        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)

        self.caption = caption

        # Font and box size
        self.font = self.graph.font()
        self.font.setBold(True)
        self.font.setPointSize(10)
        fm = QtGui.QFontMetrics(self.font);
        
        self.sizex = fm.width(self.caption)+ 20;
        self.sizey = 30


        # Add to sene
        scene.addItem(self)

        # Connectors
        self.connector_in = []
        self.connector_out = []
        for i in range(ninput):
            self.connector_in.append(ConnectorIn(self, scene, i))
        for i in range(noutput):
            self.connector_out.append(ConnectorOut(self, scene, i))

    def get_input_connector(self, index):
        try:
            return self.connector_in[index]
        except:
            return None


    def get_output_connector(self, index):
        try:
            return self.connector_out[index]
        except:
            return None

    def type(self):
        return self.Type


    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(0 - adjust, 0 - adjust,
                             self.sizex + adjust, self.sizey + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(0, 0, self.sizex, self.sizey)
        return path


    def paint(self, painter, option, widget):

        # Shadow
#         painter.setPen(QtCore.Qt.NoPen)
#         painter.setBrush(QtCore.Qt.darkGray)
#         painter.drawRect(-7, -7, 20, 20)

        # Draw Box
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 255, 100)))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawRect(0, 0, self.sizex, self.sizey)

        # Draw Text
        textRect = QtCore.QRectF(0, 0, self.sizex, self.sizey)
        painter.setFont(self.font)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(textRect, QtCore.Qt.AlignCenter, self.caption)


    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for c in self.connector_in :
                c.adjust()
            for c in self.connector_out :
                c.adjust()
                 
            self.graph.itemMoved()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

################################################################################

class Connector(QtGui.QGraphicsRectItem):
    """ A node connector """
    WIDTH = 6
    HEIGHT = 4

    def __init__(self, parent, scene, index):
        """
        @param parent : QGraphicsItem parent
        @param scene : QGrpahicsScene container
        @param index : connector index
        """
        QtGui.QGraphicsItem.__init__(self, parent, scene)
        
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 200)))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        self.edge = None

    def setEdge(self, edge):
        self.edge = edge

    def adjust(self):
        if(self.edge): self.edge.adjust()

class ConnectorIn(Connector):
    """ Input node connector """

    def __init__(self, parent, scene, index):

        Connector.__init__(self, parent, scene, index)
        self.setPos(index * self.WIDTH * 2, 0)
        self.setRect(0, 0, self.WIDTH, self.HEIGHT)


class ConnectorOut(Connector):
    """ Output node connector """

    def __init__(self, parent, scene, index):
        Connector.__init__(self, parent, scene, index)
        self.setPos(index * self.WIDTH * 2, parent.sizey - self.HEIGHT)
        self.setRect(0, 0, self.WIDTH, self.HEIGHT)



################################################################################


class Edge(QtGui.QGraphicsItem):
    """ An edget between two node """
    
    Type = QtGui.QGraphicsItem.UserType + 2
    
    def __init__(self, sourceNode, out_index, destNode, in_index, parent=None, scene=None):
        """
        @param sourceNode : source GraphicalNode
        @param out_index : output connector index
        @param destNode : destination GraphicalNode
        @param in_index : input connector index
        """
        QtGui.QGraphicsItem.__init__(self, parent, scene)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)

        src = sourceNode.get_output_connector(out_index)
        if( src ) : src.setEdge(self)

        dst = destNode.get_input_connector(in_index)
        if( dst ) : dst.setEdge(self)

        self.source = src
        self.dest = dst
        self.adjust()

    def type(self):
        return Edge.Type

    def adjust(self):
        if not self.source or not self.dest:
            return

        line = QtCore.QLineF(self.mapFromItem(self.source, self.source.rect().center() ),
                              self.mapFromItem(self.dest, self.dest.rect().center() ))
       
        length = line.length()
        if length == 0.0:
            return
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() 
        self.destPoint = line.p2() 

    def boundingRect(self):
        if not self.source or not self.dest:
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + 5) / 2.0

        rect = QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y()))
        
        return rect.normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawLine(line)


