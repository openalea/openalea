# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__="""
Composite Node Widgets
"""

__license__= "CeCILL v2"
__revision__=" $Id$ "



import sys
import math
import weakref

from PyQt4 import QtCore, QtGui
from openalea.core.node import RecursionError
from openalea.core.pkgmanager import PackageManager
from openalea.core.observer import lock_notify
from openalea.core.settings import Settings
from openalea.core import cli

import annotation

from openalea.visualea.node_widget import NodeWidget, SignalSlotListener

from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser
from openalea.visualea.util import busy_cursor, exception_display, open_dialog
from openalea.visualea.node_widget import DefaultNodeWidget


class DisplayGraphWidget(QtGui.QWidget, NodeWidget):
    """ Display widgets contained in the graph """
    
    def __init__(self, node, parent=None, autonomous=False):

        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)

        vboxlayout = QtGui.QVBoxLayout(self)
        self.vboxlayout = vboxlayout
        
        self.node = node

        # Container
        self.container = QtGui.QTabWidget(self)
        vboxlayout.addWidget(self.container)


        if(autonomous):
            self.set_autonomous()
            return
        
        # empty_io is a flag to define if the composite widget add only io widgets 
        
        # Trey to create a standard node widget for inputs
        default_widget = DefaultNodeWidget(node, parent)

        if(default_widget.is_empty()):
            default_widget.close()
            default_widget.destroy()
            del default_widget
            empty_io = True

        else:
            empty_io = False 
            self.container.addTab(default_widget, "Inputs")


        # Add subwidgets (Need to sort widget)
        for id in node.vertices():

            subnode = node.node(id)

            # Do not display widget if hidden
            hide = subnode.internal_data.get('hide', False) 
            user_app = subnode.internal_data.get('user_application', False) 
            if(hide and not empty_io): continue

            if(not user_app):
                # ignore node with all input connected
                states = [ bool(subnode.get_input_state(p)=="connected")
                           for p in xrange(subnode.get_nb_input())]
                
                if(all(states)): continue

            # Add tab
            try:
                factory = subnode.get_factory()
                widget = factory.instantiate_widget(subnode, self)
                assert widget
            except:
                continue
            
            if(widget.is_empty()) :
                widget.close()
                del widget
            else : 
                # Add as tab
                caption = "%s"%(subnode.caption)
                self.container.addTab(widget, caption)

        
                
           
    def set_autonomous(self):
        """ Create autonomous widget with user applications buttons and dataflow """

        # User App panel
        userapp_widget = QtGui.QWidget(self)
        userapp_layout = QtGui.QVBoxLayout(userapp_widget)


        for id in self.node.vertices():

            subnode = self.node.node(id)
            user_app = subnode.internal_data.get('user_application', False) 

            # add to user app panel
            if(user_app):
                
                label = QtGui.QLabel(subnode.caption, userapp_widget)
                runbutton = QtGui.QPushButton("Run", userapp_widget)
                runbutton.id = id
                
                widgetbutton = QtGui.QPushButton("Widget", userapp_widget)
                widgetbutton.id = id

                self.connect(runbutton, QtCore.SIGNAL("clicked()"), self.run_node)
                self.connect(widgetbutton, QtCore.SIGNAL("clicked()"), self.open_widget)

                buttons = QtGui.QHBoxLayout()
                buttons.addWidget(label)
                buttons.addWidget(runbutton)
                buttons.addWidget(widgetbutton)
                userapp_layout.addLayout(buttons)

        
        
        dataflow_widget = EditGraphWidget(self.node, self.container)
        self.container.addTab(dataflow_widget, "Dataflow")
        self.dataflow_widget = dataflow_widget

        self.container.addTab(userapp_widget, "User Applications")

        exitbutton = QtGui.QPushButton("Exit", self)
        self.connect(exitbutton, QtCore.SIGNAL("clicked()"), self.exit)
           
        buttons = QtGui.QHBoxLayout()
        buttons.addWidget(exitbutton)
        self.vboxlayout.addLayout(buttons)


    @exception_display
    @busy_cursor    
    def run_node(self):
        self.node.eval_as_expression(self.sender().id)

    def open_widget(self):
        self.dataflow_widget.open_item(self.sender().id)
        

    def exit(self):
        self.parent().close()
        

        

class EditGraphWidget(QtGui.QGraphicsView, NodeWidget):
    """ Graph widget allowing to edit the network """
    
    def __init__(self, node, parent=None):
        """ Constructor """

        QtGui.QGraphicsView.__init__(self, parent)
        NodeWidget.__init__(self, node)

        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            
        self.scale(0.8, 0.8)

        self.newedge = None

        # dictionnary mapping elt_id and graphical items
        self.graph_item = {}
        
        # dictionnary mapping elt_id with tupel (dialog, widget)
        self.node_dialog = {}

        self.rebuild_scene()

        
    # Node property 
    def set_node(self, node):
        """ Define the associated node (overloaded) """
        NodeWidget.set_node(self, node)
        self.rebuild_scene()

    node = property(NodeWidget.get_node, set_node)


    def clear_scene(self):
        """ Remove all items from the scene """

        # close dialog
        #for (dialog, widget) in self.node_dialog.items():
            #dialog.close()
            #dialog.destroy()
            
        self.node_dialog = {}

        # Close items
        self.graph_item = {}
        # Scene
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.setScene(scene)
        

    @lock_notify      
    def rebuild_scene(self):
        """ Build the scene with graphic node and edge"""

        self.clear_scene()
        # create items
        ids = self.node.vertices()
        for eltid in ids:
            self.add_graphical_node(eltid)

        # create connections
        dataflow = self.node
        for eid in dataflow.edges():
            (src_id, dst_id) = dataflow.source(eid), dataflow.target(eid)
            
            src_item = self.graph_item[src_id]
            dst_item = self.graph_item[dst_id]

            src_port = dataflow.local_id(dataflow.source_port(eid))
            tgt_port = dataflow.local_id(dataflow.target_port(eid))
            
            src_connector = src_item.get_output_connector(src_port)
            dst_connector = dst_item.get_input_connector(tgt_port)

            self.add_graphical_connection(src_connector, dst_connector)


    # Mouse events

    def mouseMoveEvent(self, event):
        
        # update new edge position
        if(self.newedge) :
            self.newedge.setMousePoint(self.mapToScene(event.pos()))
            event.ignore()
        else:
            QtGui.QGraphicsView.mouseMoveEvent(self, event)



    @lock_notify
    def mouseReleaseEvent(self, event):
        
        if(self.newedge):
            try:
                item = self.itemAt(event.pos())
                if(item and isinstance(item, ConnectorIn)
                   and isinstance(self.newedge.connector(), ConnectorOut)):

                    self.connect_node(self.newedge.connector(), item)
                    self.add_graphical_connection( self.newedge.connector(), item)


                elif(item and isinstance(item, ConnectorOut) and
                     isinstance(self.newedge.connector(), ConnectorIn) ):

                    self.connect_node(item, self.newedge.connector())
                    self.add_graphical_connection( item, self.newedge.connector())
                    
            finally:
                self.scene().removeItem(self.newedge)
                self.newedge = None

        QtGui.QGraphicsView.mouseReleaseEvent(self, event)


#     def itemMoved(self, item, newvalue):
#         """ function called when a node item has moved """


    def wheelEvent(self, event):
        #self.centerOn(self.mapToScene(event.globalPos()))
        self.scaleView(-event.delta() / 1200.0)
        QtGui.QGraphicsView.wheelEvent(self, event)
        
    def scaleView(self, scaleFactor):

        scaleFactor += 1
        self.scale(scaleFactor, scaleFactor)

    
    def notify(self, sender, event):
        """ Function called by observed objects """

        if(not event): return

        if(event[0] == "connection_modified"):
            self.rebuild_scene()
            
        elif(event[0] == "graph_modified"):
            self.rebuild_scene()


    def start_edge(self, connector):
        """ Start to create an edge """

        self.newedge= SemiEdge(self, connector, None, self.scene())

  
    # graph edition

    def add_graphical_node(self, eltid):
        """
        Add the node graphical representation in the widget
        @param eltid : element id 
        """

        subnode = self.node.node(eltid)

        # Annotation
        if(subnode.__class__.__dict__.has_key("__graphitem__")):

            # Test if Annotation is available
            if("Annotation" in subnode.__graphitem__ and
               not annotation.is_available()):
                mess = QtGui.QMessageBox.warning(None, "Error",
                                                 "This function need PyQT >= 4.2")
                return None
            else:                
                classobj = eval(subnode.__graphitem__)
                gnode = classobj(self, eltid)

        # Standard Node
        else:
            nin = subnode.get_nb_input()
            nout = subnode.get_nb_output()
            gnode = GraphicalNode(self, eltid)

            # do not display in and out nodes if not necessary
            if(nin == 0 and nout == 0 and
               (eltid == self.node.id_in or eltid == self.node.id_out)):
                gnode.setVisible(False)
 
        self.graph_item[eltid] = gnode
        
        return gnode


    def add_graphical_connection(self, connector_src, connector_dst):
        """ 
        Create the graphical Edge between two connectorse 
        Do not create the REAL dataflow connection
        """
        
        edge = Edge(self, connector_src.parentItem(), connector_src.index(),
                    connector_dst.parentItem(), connector_dst.index(),
                    None, self.scene())

        return edge
        
    
    def connect_node(self, connector_src, connector_dst):
        """
        Connect the 2 nodes given its connectors (convenience function)
        """
        
        self.node.connect(connector_src.parentItem().get_id(), 
                          connector_src.index(),
                          connector_dst.parentItem().get_id(), 
                          connector_dst.index())


    def open_item(self, elt_id):
        """ Open the widget of the item elt_id """

        # Test if the node is already opened
        if(self.node_dialog.has_key(elt_id)):
            (d,w) = self.node_dialog[elt_id]

            if(d.isVisible()):
                d.raise_ ()
                d.activateWindow ()
            else:
                d.show()

            return

        node = self.node.node(elt_id)

        # Click on IO node
        # TO refactore 
        from openalea.core.compositenode import CompositeNodeInput, CompositeNodeOutput
        from dialogs import IOConfigDialog
        if(isinstance(node, CompositeNodeInput) or
           isinstance(node, CompositeNodeOutput)):
            
            dialog = IOConfigDialog(self.node.input_desc,
                                    self.node.output_desc,
                                    parent=self)
            ret = dialog.exec_()

            if(ret):
                self.node.set_io(dialog.inputs, dialog.outputs)
                self.rebuild_scene()
            return
        ########### End refactor
            
        factory = node.get_factory()
        if(not factory) : return
        # We Create a new Dialog
        widget = factory.instantiate_widget(node, self)
        
        if(not widget) : return 
        if (widget.is_empty()):
            widget.close()
            del widget
            return

        container = open_dialog(self, widget, factory.get_id(), False)
        self.node_dialog[elt_id] = (container, widget)


    def get_selected_item(self):
        """ Return the list id of the selected item """

        # get the selected id
        return [ id for id, item in self.graph_item.items() if item.isSelected()]


    def remove_selection(self):
        """ Remove selected nodes """

        # Ensure to not remove in and out node
        self.graph_item[self.node.id_in].setSelected(False)
        self.graph_item[self.node.id_out].setSelected(False)

        # remove the nodes
        nodes = self.get_selected_item()
        for i in nodes : self.remove_node(i)

        # Remove other item
        items = self.scene().selectedItems()
        for i in items : i.remove()


    def group_selection(self, factory):
        """
        Export selected node in a new factory
        """

        s = self.get_selected_item()
        if(not s): return None
        def cmp_x(i1, i2):
            return cmp(self.graph_item[i1].pos().x(), self.graph_item[i2].pos().x())

        s.sort(cmp=cmp_x)

        self.node.to_factory(factory, s, auto_io=True)

        pos = self.get_center_pos(s)

        # Instantiate the new node
        new_id = self.add_new_node(factory, pos)
        if new_id is not False:
            new_edges = self.node.compute_external_io(s, new_id)

            self.add_new_connections(new_edges)
            self.remove_selection()


    def copy(self, session):
        """ Copy Selection """
        
        s = self.get_selected_item()
        if(not s): return 

        session.clipboard.clear()
        self.node.to_factory(session.clipboard, s, auto_io=False)


    @lock_notify
    def paste(self, session):
        """ Paste from clipboard """

        l = lambda x :  x + 30
        modifiers = [('posx', l), ('posy', l)]
        new_ids = session.clipboard.paste(self.node, modifiers)

        self.rebuild_scene()

        # select new nodes
        for i in new_ids:
            item = self.graph_item[i]
            item.setSelected(True)



    def get_center_pos(self, items):
        """ Return the center of items (items is the list of id) """

        l = len(items)
        if(l == 0) : return QtCore.QPointF(30,30)
        
        sx = sum((self.graph_item[i].pos().x() for i in items))
        sy = sum((self.graph_item[i].pos().y() for i in items))
        return QtCore.QPointF( float(sx)/l, float(sy)/l )
    

    def close_node_dialog(self, elt_id):
        """ Close a node dialog """

        # close dialog
        try:
            (dialog, widget) = self.node_dialog[elt_id]
            dialog.close()
            dialog.destroy()
            
            del(self.node_dialog[elt_id])
        except KeyError:
            pass


    @lock_notify      
    def remove_node(self, elt_id):
        """ Remove node identified by elt_id """

        if(elt_id == self.node.id_in) : return
        if(elt_id == self.node.id_out) : return

        self.close_node_dialog(elt_id)
        
        item = self.graph_item[elt_id]
        try:
            item.remove_connections()
        except:
            pass
        
        self.scene().removeItem(item)
        del(self.graph_item[elt_id])

        self.node.remove_node(elt_id)



    @lock_notify
    def remove_connection(self, edge_item):
        """ Remove a connection """

        connector_src = edge_item.source
        connector_dst = edge_item.dest
        
        connector_src.edge_list.remove(edge_item)
        connector_dst.edge_list.remove(edge_item)

        edge_item.dest = None
        edge_item.source= None
        
        self.scene().removeItem(edge_item)

        self.node.disconnect(connector_src.parentItem().get_id(), connector_src.index(),
                               connector_dst.parentItem().get_id(), connector_dst.index()) 
    

    # Drag and Drop from TreeView support
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalea/nodefactory"):
            event.accept()
        else:
            QtGui.QGraphicsView.dragEnterEvent(self, event)


    def dragMoveEvent(self, event):
        if ( event.mimeData().hasFormat("openalea/nodefactory") ):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            QtGui.QGraphicsView.dragMoveEvent(self, event)


    @lock_notify
    def add_new_node(self, factory, position):
        """ Convenience function : Return new id if success"""
        
        try:
            newnode = factory.instantiate([self.node.factory.get_id()])
            newnode.set_data('posx', position.x(), False)
            newnode.set_data('posy', position.y(), False)
        
            newid = self.node.add_node(newnode)
            self.add_graphical_node(newid)
            return newid

        except RecursionError:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                                 "A graph cannot be contained in itself.")
            return False


    @lock_notify
    def add_new_connections(self, edges):
        """ Convenience function : 
            Add new edges in the current dataflow.
            Create graphical connections. """
        
        dataflow = self.node
        for src_vid, src_pid, tgt_vid, tgt_pid in edges:
            eid = dataflow.connect(src_vid, src_pid, tgt_vid, tgt_pid) 

            src_item = self.graph_item[src_vid]
            tgt_item = self.graph_item[tgt_vid]

            src_connector = src_item.get_output_connector(src_pid) 
            tgt_connector = tgt_item.get_input_connector(tgt_pid)
            self.add_graphical_connection(src_connector, tgt_connector)


    @lock_notify
    def add_graphical_annotation(self, position=None):
        """ Add text annotation """

        if(not annotation.is_available()):
            mess = QtGui.QMessageBox.warning(None, "Error",
                                             "This function need PyQT >= 4.2")
            return

        # Get Position from cursor
        if(not position) :
            position = self.mapToScene(
            self.mapFromGlobal(self.cursor().pos()))

        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager["System"]
        factory = pkg.get_factory("annotation")

        self.add_new_node(factory, position)

    
    def acceptEvent(self, event):
        """ Return True if event is accepted """
        return bool(
            event.mimeData().hasFormat("openalea/data_instance")
            or
            event.mimeData().hasFormat("openalea/nodefactory"))



    def dragEnterEvent(self, event):
        event.setAccepted(self.acceptEvent(event))
            

    def dragMoveEvent(self, event):
        if (self.acceptEvent(event)):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

        
    def dropEvent(self, event):

        # Drag and Drop from the PackageManager 
        if (event.mimeData().hasFormat("openalea/nodefactory")):
            pieceData = event.mimeData().data("openalea/nodefactory")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            
            package_id = QtCore.QString()
            factory_id = QtCore.QString()
            
            dataStream >> package_id >> factory_id

            # Add new node
            pkgmanager = PackageManager()
            pkg = pkgmanager[str(package_id)]
            factory = pkg.get_factory(str(factory_id))

            position = self.mapToScene(event.pos())
                    
            self.add_new_node(factory, position)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        # Drag and Drop from the DataPool
        elif(event.mimeData().hasFormat("openalea/data_instance")):

            pieceData = event.mimeData().data("openalea/data_instance")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            
            data_key = QtCore.QString()
            
            dataStream >> data_key
            data_key = str(data_key)

            # Add new node
            pkgmanager = PackageManager()
            pkg = pkgmanager["system"]
            factory = pkg.get_factory("pool reader")

            position = self.mapToScene(event.pos())
                    
            # Set key val
            eltid = self.add_new_node(factory, position)
            subnode = self.node.node(eltid)
            subnode.set_input(0, data_key)
            subnode.set_caption("pool ['%s']"%(data_key,))

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        # Propagate the Signal
        else:
            QtGui.QGraphicsView.dropEvent(self, event)


    # Keybord Event
    def keyPressEvent(self, e):
        QtGui.QGraphicsView.keyPressEvent(self, e)
        if(e.isAccepted ()): return
        
        key = e.key()
        if( key == QtCore.Qt.Key_Delete):
            self.remove_selection()
            e.setAccepted(True)

        elif(key == QtCore.Qt.Key_Space):
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            e.setAccepted(True)


    def keyReleaseEvent(self, e):
        QtGui.QGraphicsView.keyReleaseEvent(self, e)
        if(e.isAccepted ()): return

        key = e.key()
        if(key == QtCore.Qt.Key_Space):
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            e.setAccepted(True)
        

    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        if(self.itemAt(event.pos())):
           QtGui.QGraphicsView.contextMenuEvent(self, event)
           return

        menu = QtGui.QMenu(self)
        action = menu.addAction("Add Annotation")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.add_graphical_annotation)
        
        menu.move(event.globalPos())
        menu.show()
        event.accept()




      
    

class GraphicalNode(QtGui.QGraphicsItem, SignalSlotListener):
    """ Represents a node in the graphwidget """

    # Color Definition
    not_modified_color = QtGui.QColor(0, 0, 255, 200)
    modified_color = QtGui.QColor(255, 0, 0, 200)        

    selected_color = QtGui.QColor(180, 180, 180, 180)
    not_selected_color = QtGui.QColor(255, 255, 255, 100)

    error_color = QtGui.QColor(255, 0, 0, 255)    
    selected_error_color = QtGui.QColor(0, 0, 0, 255)
    not_selected_error_color = QtGui.QColor(100, 0, 0, 255)


    def __init__(self, graphview, elt_id):
        """
        @param graphview : EditGraphWidget container
        @param elt_id : id in the graph
        """

        scene = graphview.scene()
        QtGui.QGraphicsItem.__init__(self)
        SignalSlotListener.__init__(self)

        # members
        self.elt_id = elt_id
        self.graphview = graphview
        self.subnode = self.graphview.node.node(elt_id)
        
        self.nb_cin = 0
        self.connector_in = [None] * self.subnode.get_nb_input()
        self.connector_out = [None] * self.subnode.get_nb_output()

        
        # Record item as a listener for the subnode
        self.initialise(self.subnode)

        self.setFlag(QtGui.QGraphicsItem.GraphicsItemFlag(
            QtGui.QGraphicsItem.ItemIsMovable +
            QtGui.QGraphicsItem.ItemIsSelectable))
        self.setZValue(1)

        
        # Set ToolTip
        doc = self.subnode.__doc__
        try:
            node_name = self.subnode.factory.name
        except:
            node_name = self.subnode.__class__.__name__

        try:
            pkg_name = self.subnode.factory.package.get_id()
        except:
            pkg_name = ''

        if doc:
            doc = doc.split('\n')
            doc = [x.strip() for x in doc] 
            doc = '\n'.join(doc)
        else:
            if(self.subnode.factory):
                doc = self.subnode.factory.description

        self.setToolTip( "Name : %s\n"%(node_name) +
                         "Package : %s\n"%(pkg_name) +
                         "Documentation : \n%s"%(doc,))

        #self.fullname = node_name
                              
        # Font and box size
        self.sizex = 20
        self.sizey = 35

        self.font = self.graphview.font()
        self.font.setBold(True)
        self.font.setPointSize(10)
        self.fm = QtGui.QFontMetrics(self.font)


        # Add to scene
        scene.addItem(self)

        self.set_connectors()

        # Set Position
        try:
            x = self.subnode.internal_data['posx']
            y = self.subnode.internal_data['posy']
        except:
            (x,y) = (10,10)
        self.setPos(QtCore.QPointF(x,y))
        
        self.more_port = None
        self.adjust_size()

        # color
        if(hasattr(self.subnode, "__color__")):
            r,g,b = self.subnode.__color__
            self.not_modified_color = QtGui.QColor(r, g, b, 200)
            self.modified_color = self.not_modified_color

        # modified
        self.modified_item = QtGui.QGraphicsRectItem(5,5,7,7, self)
        self.modified_item.setBrush(self.modified_color)
        
        self.modified_item.setAcceptedMouseButtons(QtCore.Qt.NoButton)


    def set_connectors(self):
        """ Add connectors """

        scene = self.graphview.scene()
        
        self.nb_cin = 0
        for i,desc in enumerate(self.subnode.input_desc):

            hide = self.subnode.is_port_hidden(i)

            # hidden connector
            if(hide and self.subnode.input_states[i] is not "connected"):
                c = self.connector_in[i]
                if(c):
                    self.scene().removeItem(c)
                    del c
                    self.connector_in[i] = None
                continue

            # show connector (update if necessary)
            elif(not self.connector_in[i]):
                tip = desc.get_tip()
                self.connector_in[i] = ConnectorIn(self.graphview, self,
                                                   scene, i, tip)
            # nb connector
            self.nb_cin += 1 
                
            
        for i,desc in enumerate(self.subnode.output_desc):
            if(not self.connector_out[i]): # update if necessary
                tip = desc.get_tip()
                self.connector_out[i] = ConnectorOut(self.graphview, self,
                                                     scene, i, tip)


    def adjust_size(self, force=False):
        """ Compute the box size """

        newsizex = self.fm.width(self.get_caption()) + 30
        
        # when the text is small but there are lots of ports, 
        # add more space.
        nb_ports = max(self.nb_cin, len(self.connector_out))
        newsizex = max(nb_ports * Connector.WIDTH * 2, newsizex)
        
        if(newsizex != self.sizex or force):
            self.sizex = newsizex

            i = 0
            # i index can differ from real index since port can hidden
            for c in self.connector_in:
                if(not c) : continue
                c.adjust_position(self, i, self.nb_cin)
                c.adjust()
                i += 1

            nb_cout = len(self.connector_out)
            for i,c in enumerate(self.connector_out):
                c.adjust_position(self, i, nb_cout)
                c.adjust()

            self.set_symbols()



    def set_symbols(self):
        """ Set symbols around the box """

        phiden = bool( self.nb_cin != self.subnode.get_nb_input())
        
        if(phiden != self.more_port):
           
            if(self.more_port):
                self.scene().removeItem(self.more_port)
                self.more_port = None

            if(phiden):
                self.more_port = QtGui.QGraphicsTextItem(">>", self)
                self.more_port.setDefaultTextColor(QtGui.QColor(0, 100, 0))
                #self.more_port.mouseDoubleClickEvent = ConnectorIn.mouseDoubleClickEvent
                self.more_port.setPos(self.sizex - 20, -4)
           

    def get_caption(self):
        """ Return the node caption (convenience)"""
        
        return self.subnode.caption


    def notify(self, sender, event):
        """ Notification sended by the node associated to the item """

        if(event and
           event[0] == "caption_modified" or
           event[0] == "data_modified"):

            self.adjust_size()
            self.update()
            QtGui.QApplication.processEvents()

        elif(event and
             event[0] == "port_modified"):
            self.set_connectors()
            self.adjust_size(force=True)
            self.update()

            # del widget
            self.graphview.close_node_dialog(self.elt_id)
             
           
        elif(self.modified_item.isVisible() != sender.modified):
            self.modified_item.setVisible(bool(sender.modified or not sender.lazy))
            self.update()
            QtGui.QApplication.processEvents()


    def get_id(self):
        return self.elt_id
    

    def get_input_connector(self, index):
        return self.connector_in[index]
        

    def get_output_connector(self, index):
        return self.connector_out[index]


    def remove_connections(self):
        """ Remove edge connected to this item """ 

        for cin in self.connector_in:
            if(not cin) : continue # cin is none if hidden

            for e in list(cin.edge_list):
                e.remove()
            #cout.edge_list = []
                
        for cout in self.connector_out:
            if(not cout) : continue # cout is none if hidden

            for e in list(cout.edge_list):
                e.remove()
            #cout.edge_list = []
                

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
        painter.setBrush(QtGui.QColor(100, 100, 100, 50))
        painter.drawRoundRect(3, 3, self.sizex, self.sizey)

        # Select color
        if hasattr(self.subnode, 'raise_exception'):
            color = self.error_color
            if(self.isSelected()):
                secondcolor = self.selected_error_color
            else:
                secondcolor = self.not_selected_error_color

        else:
            if(self.isSelected()):
                color = self.selected_color
            else:
                color = self.not_selected_color

            if(self.subnode.user_application):
                secondcolor = QtGui.QColor(255, 144, 0, 200)
            else:
                secondcolor = self.not_modified_color

        # Draw Box

        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, color)
        gradient.setColorAt(1.0, secondcolor)
        painter.setBrush(QtGui.QBrush(gradient))
        
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.drawRoundRect(0, 0, self.sizex, self.sizey)
        
        # Draw Text
        textRect = QtCore.QRectF(0, 0, self.sizex, self.sizey)
        painter.setFont(self.font)
        painter.drawText(textRect, QtCore.Qt.AlignCenter,
                         self.get_caption())
        

        


    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """

        ret = QtGui.QGraphicsItem.itemChange(self, change, value)
        
        if (change == QtGui.QGraphicsItem.ItemPositionChange):
            
            for c in self.connector_in :
                if(c): c.adjust()
            for c in self.connector_out :
                if(c): c.adjust()

            point = value.toPointF()
        
            self.subnode.set_data('posx', point.x(), False)
            self.subnode.set_data('posy', point.y(), False)
         
        return ret


    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)


    def mouseDoubleClickEvent(self, event):

        QtGui.QGraphicsItem.mouseDoubleClickEvent(self, event)
  
        # Read settings
        try:
            localsettings = Settings()
            str = localsettings.get("UI", "DoubleClick")
        except:
            str = "['open']"

        if('open' in str):
            self.graphview.open_item(self.elt_id)
            
        if('run' in str):
            self.run_node()
            

    @lock_notify
    def mouseMoveEvent(self, event):
        QtGui.QGraphicsItem.mouseMoveEvent(self, event)
        
        if (event.buttons() & QtCore.Qt.MidButton):
            drag = QtGui.QDrag(self.graphview)

            pixmap = QtGui.QPixmap(":/icons/ccmime.png")
            linecode = cli.get_node_code(self.elt_id)
            
            mimeData = QtCore.QMimeData()
            mimeData.setText(linecode)
            drag.setMimeData(mimeData)

            drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
            drag.setPixmap(pixmap)
            drag.start(QtCore.Qt.MoveAction)


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.graphview)

        action = menu.addAction("Run")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.run_node)
        
        action = menu.addAction("Open Widget")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.open_widget)

        menu.addSeparator()

        action = menu.addAction("Delete")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.remove)

        action = menu.addAction("Reset")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.subnode.reset)
        
        action = menu.addAction("Replace By")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.replace_by)
        
        menu.addSeparator()

        action = menu.addAction("Caption")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.set_caption)

        action = menu.addAction("Show/Hide ports")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.show_ports)

        menu.addSeparator()
        
        action = menu.addAction("Mark as User Application")
        action.setCheckable(True)
        action.setChecked(bool(self.subnode.user_application))
        self.scene().connect(action, QtCore.SIGNAL("triggered(bool)"), self.set_user_application)

        
        action = menu.addAction("Lazy")
        action.setCheckable(True)
        action.setChecked(self.subnode.lazy)
        self.scene().connect(action, QtCore.SIGNAL("triggered(bool)"), self.set_lazy)


        action = menu.addAction("Internals")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.set_internals)
        
        
#         action = menu.addAction("Edit")
#         self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.edit_code)

        menu.move(event.screenPos())
        menu.show()

        event.accept()


    def set_lazy(self, val):
        self.subnode.lazy = val
        self.update()
        

    def set_user_application(self, val):
        
        #self.subnode.user_application = val
        self.graphview.node.set_continuous_eval(self.elt_id, bool(val))
        self.update()


    def show_ports(self):
        """ Open port show/hide dialog """

        editor = ShowPortDialog(self.subnode, self.graphview)
        editor.exec_()


    def set_internals(self):
        """ Edit node internal data """
        editor = DictEditor(self.subnode.internal_data, self.graphview)
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                self.subnode.set_data(k, editor.pdict[k])

            
    @exception_display
    @busy_cursor
    def run_node(self):
        """ Run the current node """
        self.graphview.node.eval_as_expression(self.elt_id)


    def open_widget(self):
        """ Open widget in dialog """
        self.graphview.open_item(self.elt_id)


    def remove(self):
        """ Remove current node """
        self.graphview.remove_node(self.elt_id)
        

    def set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.subnode 
        (result, ok) = QtGui.QInputDialog.getText(self.graphview, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result)


    def replace_by(self):
        """ Replace a node by an other """
        
        self.dialog = NodeChooser(self.graphview)
        self.dialog.search('', self.subnode.get_nb_input(), self.subnode.get_nb_output())
        ret = self.dialog.exec_()

        if(not ret): return
        
        factory = self.dialog.get_selection()
        newnode = factory.instantiate()
        self.graphview.node.replace_node(self.elt_id, newnode)
        
        self.graphview.rebuild_scene()


################################################################################

class Connector(QtGui.QGraphicsEllipseItem):
    """ A node connector """
    WIDTH = 12
    HEIGHT = 8

    MAX_TIPLEN = 2000 # Tooltip max length

    def __init__(self, graphview, parent, scene, index, tooltip=""):
        """
        @param graphview : EditGraphWidget container
        @param parent : QGraphicsItem parent
        @param scene : QGraphicsScene container
        @param index : connector index
        """
        
        QtGui.QGraphicsItem.__init__(self, parent, scene)

        self.mindex = index
        self.graphview = weakref.ref(graphview)

        self.base_tooltip = tooltip
        self.setRect(0, 0, self.WIDTH, self.HEIGHT)

        gradient = QtGui.QRadialGradient(-3, -3, 10)
        gradient.setCenter(3, 3)
        gradient.setFocalPoint(3, 3)
        gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
        gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        
        self.setBrush(QtGui.QBrush(gradient))
        self.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        self.edge_list = []
        self.setAcceptsHoverEvents(True)
        

    def index(self):
        return self.mindex


    def add_edge(self, edge):
        self.edge_list.append(edge)
        

    def adjust(self):
        for e in self.edge_list:
            e.adjust()

    def update_tooltip(self):
        self.setToolTip(self.base_tooltip)


    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            self.graphview().start_edge(self)
        
        QtGui.QGraphicsItem.mousePressEvent(self, event)

    
    def hoverEnterEvent(self, event):
        self.update_tooltip()
        self.setPen(QtGui.QPen(QtCore.Qt.darkYellow, 0))


    def hoverLeaveEvent(self, event):
        self.setPen(QtGui.QPen(QtCore.Qt.black, 0))



class ConnectorIn(Connector):
    """ Input node connector """

    def __init__(self, graphview, parent, scene, index, tooltip):

        Connector.__init__(self, graphview, parent, scene, index, tooltip)
        self.setAcceptDrops(True)


    def update_tooltip(self):
        node = self.parentItem().subnode
        data = node.get_input(self.mindex)
        s = str(data)
        if(len(s) > Connector.MAX_TIPLEN): s = "String too long..."

        self.setToolTip("%s \nValue: %s"%(self.base_tooltip, s))

    
    def adjust_position(self, parentitem, index, ntotal):
        width = parentitem.sizex / float(ntotal+1)
        self.setPos((index+1) * width - self.WIDTH/2., - self.HEIGHT/2)


    # Drag and Drop from TreeView support
    def dragEnterEvent(self, event):
        event.setAccepted(event.mimeData().hasFormat("openalea/data_instance"))


    def dragMoveEvent(self, event):
        if (event.mimeData().hasFormat("openalea/data_instance") ):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

            
    def dropEvent(self, event):
        if (event.mimeData().hasFormat("openalea/data_instance")):
            pieceData = event.mimeData().data("openalea/data_instance")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            
            data_key = QtCore.QString()
            
            dataStream >> data_key
            data_key = str(data_key)

            from openalea.core.session import DataPool
            datapool = DataPool()  # Singleton

            node = self.parentItem().subnode
            data = node.set_input(self.mindex, datapool[data_key])

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            event.ignore()

            
    def mouseDoubleClickEvent(self, event):
        self.parentItem().show_ports()


class ConnectorOut(Connector):
    """ Output node connector """

    def __init__(self, graphview, parent, scene, index, tooltip):
        Connector.__init__(self, graphview, parent, scene, index, tooltip)
        
        #self.adjust_position(parent, index, ntotal)

        
    def update_tooltip(self):
        node = self.parentItem().subnode
        data = node.get_output(self.mindex)
        
        s = str(data)
        if(len(s) > Connector.MAX_TIPLEN): s = "String too long..."

        self.setToolTip("%s\nValue: %s"%(self.base_tooltip, s))


    def adjust_position(self, parentitem, index, ntotal):
            
        width= parentitem.sizex / float(ntotal+1)
        self.setPos((index+1) * width - self.WIDTH/2., parentitem.sizey - self.HEIGHT/2)


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.graphview())

        action = menu.addAction("Send to Pool")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.send_to_pool)

        action = menu.addAction("Print")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.print_value )

        menu.move(event.screenPos())
        menu.show()

        event.accept()


    def print_value(self):
        """ Print the value of the connector """

        node = self.parentItem().subnode
        data = node.get_output(self.mindex)
        print data
        

    def send_to_pool(self):

        (result, ok) = QtGui.QInputDialog.getText(self.graphview(), "Data Pool", "Instance name",
                                                      QtGui.QLineEdit.Normal, )
        if(ok):
            from openalea.core.session import DataPool
            datapool = DataPool()  # Singleton

            #self.parentItem().run_node()
            node = self.parentItem().subnode
            data = node.get_output(self.mindex)
            datapool[str(result)] = data




################################################################################

def edge_factory():
    try:
        settings = Settings()
        style = settings.get('UI', 'EdgeStyle')
    except:
        style = 'Line'

    if style == 'Line':
        return LinearEdgePath()
    elif style == 'Polyline':
        return PolylineEdgePath()
    else:
        return SplineEdgePath()


class LinearEdgePath(object):
    """ Draw edges as line. """
    def __init__(self): 
        self.p1 = QtCore.QPointF()
        self.p2 = QtCore.QPointF()

    def shape(self):
        path = QtGui.QPainterPath()

        # Enlarge selection zone
        diff = self.p2 - self.p1

        if( abs(diff.x()) > abs(diff.y())):
            dp = QtCore.QPointF(0, 10)
        else:
            dp = QtCore.QPointF(10, 0)
        
        p1 = self.p1 - dp
        p2 = self.p1 + dp
        p3 = self.p2 + dp
        p4 = self.p2 - dp
        poly = QtGui.QPolygonF([p1, p2, p3, p4])
        path.addPolygon(poly)
        
        return path

    def getPath( self, p1, p2 ):
        self.p1 = p1
        self.p2 = p2
        path = QtGui.QPainterPath(self.p1)
        path.lineTo(self.p2)
        return path

        
class PolylineEdgePath(LinearEdgePath):
    """ Edge as Polyline """
    
    WIDTH = 30
    def __init__(self): 
        LinearEdgePath.__init__(self)

    def shape(self):
        return None

    def getPath( self, p1, p2 ):
        self.p1 = p1
        self.p2 = p2
        path = QtGui.QPainterPath(self.p1)

        points = []

        sd= self.p2 - self.p1
        if abs(sd.x()) <= self.WIDTH: # draw a line
            pass
        elif sd.y() < 2 * self.WIDTH:
            s1 = self.p1 + QtCore.QPointF(0,self.WIDTH)
            d1 = self.p2 - QtCore.QPointF(0,self.WIDTH)

            s1d1= d1 -s1
            s2 = s1 + QtCore.QPointF(s1d1.x() / 2., 0)
            d2 = s2 + QtCore.QPointF(0, s1d1.y())
            points.extend([s1, s2, d2, d1])
        else:
            s1 = self.p1 + QtCore.QPointF(0, sd.y() / 2.)
            d1= self.p2 - QtCore.QPointF(0, sd.y() / 2.)
            points.extend([s1, d1])
        
        points.append(self.p2)
        for pt in points:
            path.lineTo(pt)

        return path


class SplineEdgePath(PolylineEdgePath):
    """ Edge as Spline """
    
    def __init__(self): 
        PolylineEdgePath.__init__(self)

    def getPath( self, p1, p2 ):
        self.p1 = p1
        self.p2 = p2
        path = QtGui.QPainterPath(self.p1)

        sd= self.p2- self.p1
        if abs(sd.x()) <= self.WIDTH: # draw a line
            path.lineTo(self.p2)
        elif sd.y() < self.WIDTH: 
            py = QtCore.QPointF(0, max(self.WIDTH, - sd.y()))
            path.cubicTo(self.p1 + py, self.p2 - py, self.p2)

        else:
            py = QtCore.QPointF(0, sd.y() / 2.)
            pm = (self.p1 + self.p2) / 2.
            path.quadTo(self.p1 + py, pm)
            path.quadTo(self.p2 - py, self.p2)

        return path
    

class AbstractEdge(QtGui.QGraphicsPathItem):
    """
    Base classe for edges 
    """

    def __init__(self, graphview, parent=None, scene=None):
        QtGui.QGraphicsPathItem.__init__(self, parent, scene)

        self.graph = graphview
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()

        self.edge_path = edge_factory()
        path = self.edge_path.getPath(self.sourcePoint, self.destPoint)
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
        path = self.edge_path.getPath(self.sourcePoint, self.destPoint)
        self.setPath(path)


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

        #self.setAcceptedMouseButtons(QtCore.Qt.NoButton)

        self.setFlag(QtGui.QGraphicsItem.GraphicsItemFlag(
            QtGui.QGraphicsItem.ItemIsSelectable))

        src = sourceNode.get_output_connector(out_index)
        if(src) : src.add_edge(self)

        dst = destNode.get_input_connector(in_index)
        if(dst) : dst.add_edge(self)

        self.source = src
        self.dest = dst
        self.adjust()


    def adjust(self):
        if not self.source or not self.dest:
            return

        source = self.source
        dest = self.dest
        line = QtCore.QLineF(self.mapFromItem(source, source.rect().center() ),
                              self.mapFromItem(dest, dest.rect().center() ))
       
        length = line.length()
        if length == 0.0:
            return
        self.prepareGeometryChange()
        self.sourcePoint = line.p1() 
        self.destPoint = line.p2()
        self.update_line()


    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """

        if (change == QtGui.QGraphicsItem.ItemSelectedChange):
            if(value.toBool()):
                color = QtCore.Qt.blue
            else:
                color = QtCore.Qt.black

            self.setPen(QtGui.QPen(color, 3,
                                   QtCore.Qt.SolidLine,
                                   QtCore.Qt.RoundCap,
                                   QtCore.Qt.RoundJoin))
        
                
        return QtGui.QGraphicsItem.itemChange(self, change, value)


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.graph)

        action = menu.addAction("Delete connection")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        
        menu.move(event.screenPos())
        menu.show()

        event.accept()


    def remove(self):
        """ Remove the Edge """
        self.graph.remove_connection(self)


    
