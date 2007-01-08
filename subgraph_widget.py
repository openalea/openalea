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
Default Node Widget and Subgraph Widget
"""

__license__= "GPL"
__revision__=" $Id $"



import sys
import math

from PyQt4 import QtCore, QtGui
from core.core import NodeWidget, RecursionError


class SubGraphWidget(NodeWidget, QtGui.QGraphicsView):
    """ Subgraph widget allowing to edit the network """
    
    def __init__(self, node, mainwindow, parent=None):

        NodeWidget.__init__(self, node, mainwindow)
        QtGui.QGraphicsView.__init__(self, parent)

        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.setScene(scene)
        #self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.scale(0.8, 0.8)

        self.newedge = None

        # dictionnary mapping elt_id and graphical items
        self.graphitem = {}
        
        # dictionnary mapping elt_id with sub dialog
        self.node_dialog = {}

        self.rebuild_scene()
        

    def closeEvent(self, event):
        """ Close all sub dialog and accept event """
        
        for d in self.node_dialog.values():
            d.close()

        event.accept()
    

    def clear_scene(self):
        """ Remove all items from the scene """

        for d in self.node_dialog.values():
            d.close()

        self.node_dialog = {}
        
        self.graphitem = {}
        for i in self.scene().items():
            del(i)
        

    def rebuild_scene(self):
        """ Build the scene with graphic node and edget"""
    
        self.clear_scene()
        # create items
        for eltid in self.factory.elt_factory.keys():
            self.add_graphical_node(eltid)

        # create connections
        for ((dst_id, in_port), (src_id, out_port)) in self.factory.connections.items():

            srcitem = self.graphitem[src_id]
            out_connector = srcitem.get_output_connector(out_port)

            dstitem = self.graphitem[dst_id]
            in_connector = dstitem.get_input_connector(in_port)

            self.add_graphical_connection(out_connector, in_connector)


    # Mouse events

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


    def itemMoved(self, item, newvalue):
        """ function called when a node item has moved """
        elt_id = item.elt_id
        point = newvalue.toPointF()
        self.factory.move_element(elt_id, (point.x(), point.y()))


    def notify(self):
        """ Function called by observed objects """
        
        #self.rebuild_scene()


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

    def reinstantiate_node(self):
        """ Return True if succeed """
        try:
            self.node = self.factory.instantiate()
            return True
        except RecursionError :
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "A Subgraph cannot be contained in itself.")
            return False


    def add_graphical_node(self, eltid):
        """
        Add the node graphical representation in the widget
        @param eltid : element id in the factory
        """

        subnode = self.node.get_node_by_id(eltid)
        
        nin = subnode.get_nb_input()
        nout = subnode.get_nb_output()
        caption = eltid
        position = self.factory.elt_position[eltid]

        if(position) : (x,y) = position
        else : (x,y) = (10,10)

        gnode = GraphicalNode(self, eltid, nin, nout, caption )
        gnode.setPos(QtCore.QPointF(x,y))

        self.graphitem[eltid] = gnode
        
        return gnode


    def add_graphical_connection(self, connector_src, connector_dst):
        """ Return the new edge """
        
        edge = Edge(connector_src.parentItem(), connector_src.index(),
                    connector_dst.parentItem(), connector_dst.index(),
                    None, self.scene())

        return edge
        

    def add_node_to_factory(self, pkg_id, factory_id, position):
        """
        @param pkg_id : package id string the factory is from 
        @param factory_id : Factory id string
        @param position : node position in the subgraph
        @return the new GraphicalNode
        """

        eltid = self.factory.add_nodefactory(pkg_id, factory_id, (position.x(), position.y()))

        # Try to instantiate
        if(not self.reinstantiate_node()):
            self.factory.del_element(eltid)
            return None
            
        return self.add_graphical_node(eltid)

    
    def connect_node(self, connector_src, connector_dst):
        """
        @return the new Edge
        """
        if(connector_dst.is_connected()):
            return None

        self.factory.connect(connector_src.parentItem().id(), connector_src.index(),
                             connector_dst.parentItem().id(), connector_dst.index())

        self.reinstantiate_node()
        
        return self.add_graphical_connection(connector_src, connector_dst)


    def open_item(self, elt_id):
        """ Open the widget of the item elt_id """

        
        # Test if the node is already opened
        if( self.node_dialog.has_key(elt_id)):
            self.node_dialog[elt_id].show()
            self.node_dialog[elt_id].raise_()
            self.node_dialog[elt_id].activateWindow ()
            return

        # We Create a new Dialog
        node = self.node.get_node_by_id(elt_id)
        factory = node.factory

        caption = "%s/%s"%(self.wcaption, elt_id)

        container = QtGui.QDialog(self)
            
        widget = factory.instantiate_widget(node, self, container)
        widget.wcaption = caption
        
        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        if(caption) : caption = " - %s "%(caption,)

        container.setWindowTitle(factory.get_id() + caption)

        self.node_dialog[elt_id] = container
        
        container.show()
        

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
            self.add_node_to_factory(str(packageid), str(factoryid), self.mapToScene(event.pos()))

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            event.ignore()



class GraphicalNode(QtGui.QGraphicsItem):
    """ Represent a node in the subgraphwidget """

    def __init__(self, graphWidget, elt_id, ninput, noutput,  caption="Node"):
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
        self.setFlag(QtGui.QGraphicsItem.GraphicsItemFlag(
            QtGui.QGraphicsItem.ItemIsMovable +
            QtGui.QGraphicsItem.ItemIsSelectable))
        self.setZValue(1)

        self.caption = caption

        # Set ToolTip
        f =  self.graph.node.get_node_by_id(elt_id).factory
        self.setToolTip( "Instance : %s\n"%(elt_id,) + f.get_tip())
                


        # Font and box size
        self.font = self.graph.font()
        self.font.setBold(True)
        self.font.setPointSize(10)
        fm = QtGui.QFontMetrics(self.font);
        
        self.sizex = fm.width(self.caption)+ 20;
        self.sizey = 30

        # Add to scene
        scene.addItem(self)

        # Connectors
        self.connector_in = []
        self.connector_out = []
        for i in range(ninput):
            self.connector_in.append(ConnectorIn(self.graph, self, scene, i))
        for i in range(noutput):
            self.connector_out.append(ConnectorOut(self.graph, self, scene, i))

        
    def id(self):
        return self.elt_id

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
        if(self.isSelected()):
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 255, 180)))
        else:
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
                 
            self.graph.itemMoved(self, value)

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):

        self.graph.open_item(self.elt_id)


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



