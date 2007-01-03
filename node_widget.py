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
        scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        node1 = GraphicalNode(self)
        node2 = GraphicalNode(self)
        node3 = GraphicalNode(self)
        node4 = GraphicalNode(self)
        self.centerNode = GraphicalNode(self)
        node6 = GraphicalNode(self)
        node7 = GraphicalNode(self)
        node8 = GraphicalNode(self)
        node9 = GraphicalNode(self)
        scene.addItem(node1)
        scene.addItem(node2)
        scene.addItem(node3)
        scene.addItem(node4)
        scene.addItem(self.centerNode)
        scene.addItem(node6)
        scene.addItem(node7)
        scene.addItem(node8)
        scene.addItem(node9)
        scene.addItem(Edge(node1, node2))
        scene.addItem(Edge(node2, node3))
        scene.addItem(Edge(node2, self.centerNode))
        scene.addItem(Edge(node3, node6))
        scene.addItem(Edge(node4, node1))
        scene.addItem(Edge(node4, self.centerNode))
        scene.addItem(Edge(self.centerNode, node6))
        scene.addItem(Edge(self.centerNode, node8))
        scene.addItem(Edge(node6, node9))
        scene.addItem(Edge(node7, node4))
        scene.addItem(Edge(node8, node7))
        scene.addItem(Edge(node9, node8))

        node1.setPos(-50, -50)
        node2.setPos(0, -50)
        node3.setPos(50, -50)
        node4.setPos(-50, 0)
        self.centerNode.setPos(0, 0)
        node6.setPos(50, 0)
        node7.setPos(-50, 50)
        node8.setPos(0, 50)
        node9.setPos(50, 50)

        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(self.tr("Elastic Nodes"))

    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Up:
            self.centerNode.moveBy(0, -20)
        elif key == QtCore.Qt.Key_Down:
            self.centerNode.moveBy(0, 20)
        elif key == QtCore.Qt.Key_Left:
            self.centerNode.moveBy(-20, 0)
        elif key == QtCore.Qt.Key_Right:
            self.centerNode.moveBy(20, 0)
        elif key == QtCore.Qt.Key_Plus:
            self.scaleView(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scaleView(1 / 1.2)
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
            for item in self.scene().items():
                if isinstance(item, Node):
                    item.setPos(-150 + QtCore.qrand() % 300, -150 + QtCore.qrand() % 300)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)

    def timerEvent(self, event):
        nodes = [item for item in self.scene().items() if isinstance(item, Node)]

        for node in nodes:
            node.calculateForces()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        rightShadow = QtCore.QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        bottomShadow = QtCore.QRectF(sceneRect.left() + 5, sceneRect.bottom(), sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
	        painter.fillRect(rightShadow, QtCore.Qt.darkGray)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
	        painter.fillRect(bottomShadow, QtCore.Qt.darkGray)

        # Fill.
        gradient = QtGui.QLinearGradient(sceneRect.topLeft(), sceneRect.bottomRight())
        gradient.setColorAt(0, QtCore.Qt.white)
        gradient.setColorAt(1, QtCore.Qt.lightGray)
        painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(sceneRect)

        # Text.
        textRect = QtCore.QRectF(sceneRect.left() + 4, sceneRect.top() + 4,
                                 sceneRect.width() - 4, sceneRect.height() - 4)
        message = self.tr("Click and drag the nodes around, and zoom with the "
                          "mouse wheel or the '+' and '-' keys")

        font = painter.font()
        font.setBold(True)
        font.setPointSize(14)
        painter.setFont(font)
        painter.setPen(QtCore.Qt.lightGray)
        painter.drawText(textRect.translated(2, 2), message)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(textRect, message)

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

    def __init__(self, graphWidget, elt_id=0):
        """
        @param graphwidget : scene container
        @param elt_id : id in the subgraph
        """

        QtGui.QGraphicsItem.__init__(self)

        self.elt_id = elt_id

        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)
        
    def type(self):
        return Node.Type

    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):
        return self.edgeList


    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10 - adjust,
                             23 + adjust, 23 + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)

        gradient = QtGui.QRadialGradient(-3, -3, 10)
        if option.state & QtGui.QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
            gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        else:
            gradient.setColorAt(0, QtCore.Qt.yellow)
            gradient.setColorAt(1, QtCore.Qt.darkYellow)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge.adjust()
            self.graph.itemMoved()

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)



class Edge(QtGui.QGraphicsItem):
    """ An edget between two node """
    
    Type = QtGui.QGraphicsItem.UserType + 2
    Pi = math.pi
    TwoPi = 2.0 * Pi
    
    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)

        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()

    def adjust(self):
        if not self.source or not self.dest:
            return

        line = QtCore.QLineF(self.mapFromItem(self.source, 0, 0),
                             self.mapFromItem(self.dest, 0, 0))
        length = line.length()
        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)

        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def boundingRect(self):
        if not self.source or not self.dest:
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0

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

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        sourceArrowP1 = self.sourcePoint +\
                        QtCore.QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
                                       math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        
        sourceArrowP2 = self.sourcePoint + \
                        QtCore.QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
                                       math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize)
        
        destArrowP1 = self.destPoint + \
                      QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                     math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        
        destArrowP2 = self.destPoint + \
                      QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                     math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))

