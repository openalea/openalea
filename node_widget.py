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
        #scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(scene)
        #self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.scale(0.8, 0.8)
        #self.setMinimumSize(400, 400)

        self.newedge = None
        

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

    def mouseMoveEvent(self, event):
        # update new edge position
        if(self.newedge) :
            self.newedge.setMousePoint(self.mapToScene(event.pos()))
            event.ignore()
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):

        
        if(self.newedge):
            item = self.itemAt(event.pos())
            if(item and isinstance(item, ConnectorIn)):
                self.connect_node( self.newedge.connector(), item)
            elif(item and isinstance(item, ConnectorOut)):
                self.connect_node( item, self.newedge.connector())
        
            self.scene().removeItem(self.newedge)
            self.newedge = None

            
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)


#     def itemMoved(self):
#         pass

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor)\
                 .mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    def start_edge(self, connector):
        """ Start to create an edge """

        self.newedge= SemiEdge(connector, None, self.scene())

        
        

    # subgraph edition

    def add_graphicalnode(self, position, pkg_id, factory_id):
        """
        @param position : node position in the subgraph
        @param pkg_id : package id string the factory is from 
        @param factory_id : Factory id string 
        @return the new GraphicalNode
        """

        gnode = GraphicalNode(self)
        gnode.setPos(position)

        return gnode

    def connect_node(self, connector_src, connector_dst):
        """
        @return the new Edge
        """

        if(connector_dst.is_connected()):
            return None
        
        edge = Edge(connector_src.parentItem(), connector_src.index(),
                    connector_dst.parentItem(), connector_dst.index(),
                    None, self.scene())

        return edge


    # Drag and Drop from TreeView support
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalea/nodefactory"):
            event.accept()
        else:
            event.ignore()


    def dragLeaveEvent(self, event):
        event.accept()


    def dragMoveEvent(self, event):
        if ( event.mimeData().hasFormat("openalea/nodefactory") ):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):

        if (event.mimeData().hasFormat("openalea/nodefactory")):
            pieceData = event.mimeData().data("openalea/nodefactory")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            
            packageid = QtCore.QString()
            factoryid = QtCore.QString()
            
            dataStream >> packageid >> factoryid

            # Add new node
            self.add_graphicalnode(self.mapToScene(event.pos()), str(packageid), str(factoryid))


            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            event.ignore()

    



class GraphicalNode(QtGui.QGraphicsItem):
    """ Represent a node in the subgraphwidget """

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
            self.connector_in.append(ConnectorIn(self.graph, self, scene, i))
        for i in range(noutput):
            self.connector_out.append(ConnectorOut(self.graph, self, scene, i))

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


    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(0 - adjust, 0 - adjust,
                             self.sizex + adjust, self.sizey + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(0, 0, self.sizex, self.sizey)
        return path


    def paint(self, painter, option, widget):

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
                 
            #self.graph.itemMoved()

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

    def __init__(self, graphview, parent, scene, index):
        """
        @param graphview : The SubGraphWidget
        @param parent : QGraphicsItem parent
        @param scene : QGrpahicsScene container
        @param index : connector index
        """
        QtGui.QGraphicsItem.__init__(self, parent, scene)
        
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 200)))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        self.mindex = index
        self.graphview= graphview

    def index(self):
        return self.mindex

     

class ConnectorIn(Connector):
    """ Input node connector """

    def __init__(self, graphview, parent, scene, index):

        Connector.__init__(self, graphview, parent, scene, index)

        self.edge = None

        self.setPos(index * self.WIDTH * 2, 0)
        self.setRect(0, 0, self.WIDTH, self.HEIGHT)

    def set_edge(self, edge):
        self.edge = edge

    def is_connected(self):
        return bool(self.edge)

    def adjust(self):
        if(self.edge): self.edge.adjust()

    def mousePressEvent(self, event):
        QtGui.QGraphicsItem.mousePressEvent(self, event)

        if(not self.edge):
            self.graphview.start_edge(self)
    


class ConnectorOut(Connector):
    """ Output node connector """

    def __init__(self, graphview, parent, scene, index):
        Connector.__init__(self, graphview, parent, scene, index)
        
        self.setPos(index * self.WIDTH * 2, parent.sizey - self.HEIGHT)
        self.setRect(0, 0, self.WIDTH, self.HEIGHT)

        self.edge_list = []

    def add_edge(self, edge):
        self.edge_list.append(edge)

    def adjust(self):
        for e in self.edge_list:
            e.adjust()


    def mousePressEvent(self, event):
        QtGui.QGraphicsItem.mousePressEvent(self, event)

        self.graphview.start_edge(self)



################################################################################

class AbstractEdge(QtGui.QGraphicsItem):
    """
    Base classe for edges
    """

    def __init__(self, parent=None, scene=None):
        QtGui.QGraphicsItem.__init__(self, parent, scene)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()


    def boundingRect(self):

        penWidth = 1
        extra = (penWidth + 5) / 2.0

        rect = QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y()))
        
        return rect.normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        painter.drawLine(line)


class SemiEdge(AbstractEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    """

    def __init__(self, connector, parent=None, scene=None):
        AbstractEdge.__init__(self, parent, scene)

        self.connect = connector
        self.sourcePoint = self.mapFromItem(connector, connector.rect().center())

    def connector(self):
        return self.connect

    def setMousePoint(self, scene_point):
        self.destPoint = scene_point
        self.update()
    


class Edge(AbstractEdge):
    """ An edge between two graphical nodes """
    
    
    def __init__(self, sourceNode, out_index, destNode, in_index, parent=None, scene=None):
        """
        @param sourceNode : source GraphicalNode
        @param out_index : output connector index
        @param destNode : destination GraphicalNode
        @param in_index : input connector index
        """
        AbstractEdge.__init__(self, parent, scene)

        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)

        src = sourceNode.get_output_connector(out_index)
        if( src ) : src.add_edge(self)

        dst = destNode.get_input_connector(in_index)
        if( dst ) : dst.set_edge(self)

        self.source = src
        self.dest = dst
        self.adjust()


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



