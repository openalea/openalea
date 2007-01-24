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

__doc__="""
Default Node Widget and Subgraph Widget
"""

__license__= "GPL"
__revision__=" $Id$ "



import sys
import math

from PyQt4 import QtCore, QtGui
from openalea.core.core import NodeWidget, RecursionError



class DisplaySubGraphWidget(NodeWidget, QtGui.QWidget):
    """ Display subwidget contained in the subgraph """
    
    def __init__(self, node, parent=None):

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        vboxlayout = QtGui.QVBoxLayout(self)
        
        for id in node.get_ids():

            subnode = node.get_node_by_id(id)
            factory = subnode.get_factory()

            if(not factory): continue
            
            widget = factory.instantiate_widget(subnode, self)

            caption = "%s ( %s )"%(node.get_factory().get_caption(id), id)
            groupbox = QtGui.QGroupBox(caption, self)
            layout = QtGui.QVBoxLayout(groupbox)
            layout.setMargin(3)
            layout.setSpacing(2)

            layout.addWidget(widget)
            
            vboxlayout.addWidget(groupbox)

        

class EditSubGraphWidget(NodeWidget, QtGui.QGraphicsView):
    """ Subgraph widget allowing to edit the network """
    
    def __init__(self, node, parent=None):

        NodeWidget.__init__(self, node)
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

        # notification is enabled if the queue is empty
        self.notification_enabled = []


        # dictionnary mapping elt_id and graphical items
        self.graph_item = {}
        
        # dictionnary mapping elt_id with tupel (dialog, widget)
        self.node_dialog = {}

        self.rebuild_scene()


    def clear_scene(self):
        """ Remove all items from the scene """

        for (d,w) in self.node_dialog.values():
            d.close()
            w.release_listeners()

        self.node_dialog = {}
        self.graph_item = {}
        scene = self.scene()
        del(scene)
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.setScene(scene)


    def rebuild_scene(self):
        """ Build the scene with graphic node and edge"""
        self.notification_enabled.append(False)

        self.clear_scene()
        # create items
        for eltid in self.factory.elt_factory.keys():
            self.add_graphical_node(eltid)

        if(self.factory.num_input>0):
            self.add_graphical_node('in')
            
        if(self.factory.num_output>0):
            self.add_graphical_node('out')

        # create connections
        for ((dst_id, in_port), (src_id, out_port)) in self.factory.connections.items():

            srcitem = self.graph_item[src_id]
            out_connector = srcitem.get_output_connector(out_port)

            dstitem = self.graph_item[dst_id]
            in_connector = dstitem.get_input_connector(in_port)

            self.add_graphical_connection(out_connector, in_connector)

        self.notification_enabled.pop()



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
            if(item and isinstance(item, ConnectorIn) and
               isinstance(self.newedge.connector(), ConnectorOut)):

                self.connect_node( self.newedge.connector(), item)

            elif(item and isinstance(item, ConnectorOut) and
                 isinstance(self.newedge.connector(), ConnectorIn) ):
                self.connect_node( item, self.newedge.connector())
        
            self.scene().removeItem(self.newedge)
            self.newedge = None
            
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)


    def itemMoved(self, item, newvalue):
        """ function called when a node item has moved """
        elt_id = item.elt_id
        point = newvalue.toPointF()
        
        self.notification_enabled.append(False)
        self.factory.move_element(elt_id, (point.x(), point.y()))
        self.notification_enabled.pop()


    def notify(self):
        """ Function called by observed objects """

        if(len(self.notification_enabled)==0):
            self.rebuild_scene()


    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor)\
                 .mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    def start_edge(self, connector):
        """ Start to create an edge """

        self.newedge= SemiEdge(self, connector, None, self.scene())

  
    # subgraph edition

    def add_graphical_node(self, eltid):
        """
        Add the node graphical representation in the widget
        @param eltid : element id in the factory
        """

        subnode = self.node.get_node_by_id(eltid)
        
        nin = subnode.get_nb_input()
        nout = subnode.get_nb_output()

        caption = self.factory.get_caption(eltid)

        try:
            factory_name = self.node.get_node_by_id(eltid).factory.get_id()
        except:
            # There is no factory associated to the node
            factory_name = eltid

        if(caption):
            caption = "%s ( %s )" %(factory_name, caption)
        else:
            caption = "%s" %(factory_name,)

        position = self.factory.get_position(eltid)

        if(position) : (x,y) = position
        else : (x,y) = (10,10)

        gnode = GraphicalNode(self, eltid, nin, nout, caption )

        gnode.setPos(QtCore.QPointF(x,y))
        self.graph_item[eltid] = gnode
        
        return gnode


    def add_graphical_connection(self, connector_src, connector_dst):
        """ Return the new edge """
        
        edge = Edge(self, connector_src.parentItem(), connector_src.index(),
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

        self.notification_enabled.append(False)

        eltid = self.factory.add_nodefactory(pkg_id, factory_id, (position.x(), position.y()))

        # Try to instantiate
        try:
            self.factory.instantiate_id(eltid, self.node, [self.factory.get_id()])

        except RecursionError:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "A Subgraph cannot be contained in itself.")
            
            self.factory.remove_element(eltid)
            self.notification_enabled.pop()
            return None

        self.notification_enabled.pop()
        return self.add_graphical_node(eltid)

    
    def connect_node(self, connector_src, connector_dst):
        """
        @return the new Edge
        """
        if(connector_dst.is_connected()):
            return None

        self.notification_enabled.append(False)

        self.factory.connect(connector_src.parentItem().get_id(), connector_src.index(),
                             connector_dst.parentItem().get_id(), connector_dst.index())
        self.node.connect_by_id(connector_src.parentItem().get_id(), connector_src.index(),
                                connector_dst.parentItem().get_id(), connector_dst.index())

        self.notification_enabled.pop()
        
        return self.add_graphical_connection(connector_src, connector_dst)


    def open_item(self, elt_id):
        """ Open the widget of the item elt_id """

        # Test if the node is already opened
        if( self.node_dialog.has_key(elt_id)):

            (d,w) = self.node_dialog[elt_id]
            d.show()
            d.raise_()
            d.activateWindow ()
            return

        # We Create a new Dialog
        node = self.node.get_node_by_id(elt_id)
        factory = node.get_factory()

        container = QtGui.QDialog(self)
        #container.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            
        widget = factory.instantiate_widget(node, container)
        
        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(5)

        vboxlayout.addWidget(widget)

        container.setWindowTitle(factory.get_id())

        self.node_dialog[elt_id] = ( container, widget )
        
        container.show()


    def remove_selection(self):
        """ Remove selected nodes """

        # get the selected id
        s = []
        for id in self.graph_item.keys():
            item = self.graph_item[id]
            if(item.isSelected()):
                s.append(id)

        # remove the nodes
        map(self.remove_node, s)


    def remove_graphical_node(self, elt_id):
        """ Remove the graphical node item identified by elt_id """

        # close dialog
        try:
            (dialog, widget) = self.node_dialog[elt_id]
            widget.release_listeners()
            dialog.close()
        except KeyError:
            pass
        
        item = self.graph_item[elt_id]
        item.remove_connections()
        self.scene().removeItem(item)
        del(self.graph_item[elt_id])
                

    def remove_node(self, elt_id):
        """ Remove node identified by elt_id """

        self.notification_enabled.append(False)

        self.remove_graphical_node(elt_id)
        self.factory.remove_element(elt_id)
        self.node.remove_node_by_id(elt_id)
        
        self.notification_enabled.pop()


    def remove_graphical_connection(self, src_connector, dst_connector):
        """ Remove a graphical edge """

        item = dst_connector.edge
        dst_connector.set_edge(None)
        src_connector.edge_list.remove(item)
        self.scene().removeItem(item)


    def remove_connection(self, connector_src, connector_dst):
        """ Remove a connection """

        self.notification_enabled.append(False)

        self.remove_graphical_connection(connector_src, connector_dst)
        self.factory.disconnect(connector_src.parentItem().get_id(), connector_src.index(),
                               connector_dst.parentItem().get_id(), connector_dst.index()) 

        self.node.disconnect_by_id(connector_src.parentItem().get_id(), connector_src.index(),
                               connector_dst.parentItem().get_id(), connector_dst.index()) 

        self.notification_enabled.pop()
    

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

    # Keybord Event
    def keyPressEvent(self, e):
        """
        Handle user input a key
        """
        key   = e.key()
        if( key == QtCore.Qt.Key_Delete):
            self.remove_selection()



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

        subnode = self.graph.node.get_node_by_id(elt_id)
        
        # Set ToolTip
        factory =  subnode.get_factory()
        graphfactory = self.graph.node.get_factory()
        doc = subnode.__doc__
        
        if(factory) : 
            self.setToolTip( "Instance : %s\n"%(elt_id,) +
                             "Caption : %s\n"%(graphfactory.get_caption(elt_id),)+
                             "Doc : \n %s"%(doc,))
                
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
            (name, interface) = subnode.input_desc[i]
            if(interface): interface = str(interface).split('.')[-1]
            tip = "%s (%s)"%(name, interface)
            self.connector_in.append(ConnectorIn(self.graph, self, scene, i, ninput, tip))
            
        for i in range(noutput):
            (name, interface) = subnode.output_desc[i]
            if(interface): interface = str(interface).split('.')[-1]
            tip = "%s (%s)"%(name, interface)
            self.connector_out.append(ConnectorOut(self.graph, self, scene, i, noutput, tip))


    def get_id(self):
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


    def remove_connections(self):
        """ Remove edge connected to this item """ 

        for cin in self.connector_in:
            if(cin.edge) :
                cin.edge.remove_edge()
                cin.edge = None
                
        for cout in self.connector_out:
            for e in cout.edge_list:
                e.remove_edge()
            cout.edge_list = []
                

    def boundingRect(self):
        adjust = 4.0
        return QtCore.QRectF(0 , 0,
                             self.sizex + adjust, self.sizey + adjust)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(0, 0, self.sizex, self.sizey)
        return path


    def paint(self, painter, option, widget):
        # Shadow
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0,0,0, 80))
        painter.drawRoundRect(3, 3, self.sizex, self.sizey)

        # Draw Box
        if(self.isSelected()):
            color = QtGui.QColor(120, 120, 120, 180)
        else:
            color = QtGui.QColor(200, 200, 200, 100)

        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, color)
        gradient.setColorAt(1.0, QtGui.QColor(0, 0, 255, 200))
        painter.setBrush(QtGui.QBrush(gradient))
        
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.drawRoundRect(0, 0, self.sizex, self.sizey)
        
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

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsItem.mouseMoveEvent(self, event)


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.graph)

        action = menu.addAction("Run")
        self.scene().connect(action, QtCore.SIGNAL("activated()"), self.run_node)
        
        action = menu.addAction("Open Widget")
        self.scene().connect(action, QtCore.SIGNAL("activated()"), self.open_widget)

       #  action = menu.addAction("Edit")
#         self.scene().connect(action, QtCore.SIGNAL("activated()"), self.edit_widget)

        action = menu.addAction("Delete")
        self.scene().connect(action, QtCore.SIGNAL("activated()"), self.delete_node)
        
#         action = menu.addAction("Enable in Widget")
#         self.scene().connect(action, QtCore.SIGNAL("activated()"), self.enable_in_widget)
        
        action = menu.addAction("Edit Caption")
        self.scene().connect(action, QtCore.SIGNAL("activated()"), self.set_caption)

        menu.move(event.screenPos())
        menu.show()
        

    def run_node(self):
        """ Run the current node """
        cnode = self.graph.node.get_node_by_id(self.elt_id)
        self.graph.node.eval_as_expression(cnode)


    def open_widget(self):
        """ Open widget in dialog """
        self.graph.open_item(self.elt_id)


    def edit_widget(self):
        pass


    def delete_node(self):
        """ Remove current node """
        self.graph.remove_node(self.elt_id)
        

    def enable_in_widget(self):
        pass


    def set_caption(self):
        """ Open a input dialog to set node caption """
        
        factory =  self.graph.node.get_factory()
        if(not factory): return

        text = factory.get_caption(self.elt_id)
        if(not text) : text = ""
        
        (result, ok) = QtGui.QInputDialog.getText(self.graph, "Node caption", "",
                                   QtGui.QLineEdit.Normal, text)
        if(ok):
            factory.set_caption(self.elt_id, str(result))



################################################################################

class Connector(QtGui.QGraphicsEllipseItem):
    """ A node connector """
    WIDTH = 12
    HEIGHT = 8

    def __init__(self, graphview, parent, scene, index, tooltip=""):
        """
        @param graphview : The SubGraphWidget
        @param parent : QGraphicsItem parent
        @param scene : QGrpahicsScene container
        @param index : connector index
        """
        QtGui.QGraphicsItem.__init__(self, parent, scene)
        

        self.mindex = index
        self.graphview= graphview

        self.setToolTip(tooltip)
        self.setRect(0, 0, self.WIDTH, self.HEIGHT)

        gradient = QtGui.QRadialGradient(-3, -3, 10)
        gradient.setCenter(3, 3)
        gradient.setFocalPoint(3, 3)
        gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
        gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        

        self.setBrush(QtGui.QBrush(gradient))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 0))


    def index(self):
        return self.mindex

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsItem.mouseMoveEvent(self, event)



class ConnectorIn(Connector):
    """ Input node connector """

    def __init__(self, graphview, parent, scene, index, ntotal, tooltip):

        Connector.__init__(self, graphview, parent, scene, index, tooltip)

        self.edge = None

        width= parent.sizex / float(ntotal+1)
        self.setPos((index+1) * width - self.WIDTH/2., - self.HEIGHT/2)

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

    def __init__(self, graphview, parent, scene, index, ntotal, tooltip):
        Connector.__init__(self, graphview, parent, scene, index, tooltip)
        
        width= parent.sizex / float(ntotal+1)
        self.setPos((index+1) * width - self.WIDTH/2., parent.sizey - self.HEIGHT/2)
        

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

class AbstractEdge(QtGui.QGraphicsLineItem):
    """
    Base classe for edges
    """

    def __init__(self, graphview, parent=None, scene=None):
        QtGui.QGraphicsLineItem.__init__(self, parent, scene)

        self.graph = graphview
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()

        line = QtCore.QLineF(self.sourcePoint, self.destPoint)
        self.setLine(line)

        self.setPen(QtGui.QPen(QtCore.Qt.black, 3,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))

    def update_line(self):
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)
        self.setLine(line)

    
class SemiEdge(AbstractEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    """

    def __init__(self, graphview, connector, parent=None, scene=None):
        AbstractEdge.__init__(self, graphview, parent, scene)

        self.connect = connector
        self.sourcePoint = self.mapFromItem(connector, connector.rect().center())


    def connector(self):
        return self.connect


    def setMousePoint(self, scene_point):
        self.destPoint = scene_point
        self.update_line()
        self.update()
    


class Edge(AbstractEdge):
    """ An edge between two graphical nodes """
        
    def __init__(self, graphview, sourceNode, out_index, destNode, in_index,
                 parent=None, scene=None):
        """
        @param sourceNode : source GraphicalNode
        @param out_index : output connector index
        @param destNode : destination GraphicalNode
        @param in_index : input connector index
        """
        AbstractEdge.__init__(self, graphview, parent, scene)

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
        self.update_line()


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.graph)

        action = menu.addAction("Delete connection")
        self.scene().connect(action, QtCore.SIGNAL("activated()"), self.remove_edge)

        
        menu.move(event.screenPos())
        menu.show()


    def remove_edge(self):
        self.graph.remove_connection(self.source, self.dest)
    
