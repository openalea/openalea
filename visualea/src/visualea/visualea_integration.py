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
"""This file customizes the grapheditor to work well with visualea"""


__license__ = "Cecill-C"
__revision__ = " $Id$ "


import weakref
from PyQt4 import QtCore, QtGui
from graph_operator import GraphOperator
from openalea.core.pkgmanager import PackageManager
from openalea.core.node import RecursionError, InputPort, OutputPort
from openalea.core.compositenode import CompositeNode
from openalea.grapheditor import qtgraphview
from openalea.grapheditor import interactionstates as OAGIS
from openalea.visualea import dataflowview



####################################################
# Handling the drag and drop events over the graph #
####################################################
def OpenAleaNodeFactoryHandler(view, event):
    """ Drag and Drop from the PackageManager """
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

        position = view.mapToScene(event.pos())
        try:
            view.scene().clearSelection()
            view.scene().select_added_items(True)
            node = factory.instantiate([view.scene().graph().factory.get_id()])
            view.scene().graph().add_vertex(node, position=[position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


def OpenAleaNodeDataPoolHandler(view, event):
    # Drag and Drop from the DataPool
    if(event.mimeData().hasFormat("openalea/data_instance")):
        pieceData = event.mimeData().data("openalea/data_instance")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)

        data_key = QtCore.QString()

        dataStream >> data_key
        data_key = str(data_key)

        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager["system"]
        factory = pkg.get_factory("pool reader")

        position = view.mapToScene(event.pos())

        # Set key val
        try:
            view.scene().clearSelection()
            view.scene().select_added_items(True)
            node = factory.instantiate([view.scene().graph().factory.get_id()])
            view.scene().graph().add_vertex(node, [position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return

        node.set_input(0, data_key)
        node.set_caption("pool ['%s']"%(data_key,))

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


mimeFormatsMap = {"openalea/nodefactory":OpenAleaNodeFactoryHandler,
                  "openalea/data_instance":OpenAleaNodeDataPoolHandler}
qtgraphview.View.set_mime_handler_map(mimeFormatsMap)


##############################################
# Handling keyboard events on the graph view #
##############################################
def keyPressDelete(view, e):
    operator=GraphOperator(view, view.scene().graph())
    operator(fName="graph_remove_selection")()
    e.setAccepted(True)

def keyPressSpace(view, e):
    QtGui.QGraphicsView.keyPressEvent(view,e)
    if not e.isAccepted():
        view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        e.setAccepted(True)

def keyReleaseSpace(view, e):
    view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
    e.setAccepted(True)

keyPressMapping={ (QtCore.Qt.NoModifier, QtCore.Qt.Key_Delete ):keyPressDelete,
                  (QtCore.Qt.NoModifier, QtCore.Qt.Key_Space ):keyPressSpace
                  }

keyReleaseMapping={ (QtCore.Qt.NoModifier, QtCore.Qt.Key_Space ):keyReleaseSpace
                    }

def viewContextMenuEvent(view, event):
    if(view.itemAt(event.pos())):
        QtGui.QGraphicsView.contextMenuEvent(view, event)
        return

    operator=GraphOperator(view)
    menu = QtGui.QMenu(view)
    action = menu.addAction(operator("Add Annotation", menu, "graph_add_annotation"))
    menu.move(event.globalPos())
    menu.show()
    event.accept()
 
qtgraphview.View.set_keypress_handler_map(keyPressMapping)
qtgraphview.View.set_keyrelease_handler_map(keyReleaseMapping)
qtgraphview.View.set_event_handler("contextMenuEvent", viewContextMenuEvent,
                                      dataflowview.adapter.GraphAdapter)


#################################
# QtEvent handlers for vertices #
#################################
def vertexMouseDoubleClickEvent(graphItem, event):
    graphItem = weakref.ref(graphItem)
    if event.button()==QtCore.Qt.LeftButton:
        # Read settings
        try:
            localsettings = Settings()
            str = localsettings.get("UI", "DoubleClick")
        except:
            str = "['open']"

        view = graphItem().scene().views()[0]
        operator=GraphOperator(view, graphItem().graph())
        operator.set_vertex_item(graphItem())

        if('open' in str):
            operator(fName="vertex_open")()
        elif('run' in str):
            operator(fName="vertex_run")()

def vertexContextMenuEvent(graphItem, event):
    """ Context menu event : Display the menu"""
    graphItem = weakref.ref(graphItem)
    graphItem().setSelected(True)
    
    operator = GraphOperator()
    operator.identify_focused_graph_view()
    operator.set_vertex_item(graphItem())
    w = operator.get_graph_view()
    menu = QtGui.QMenu(w)
    items = w.scene().get_selected_items(qtgraphview.Vertex)
    #enabled = not w.scene().edition_locked()
    

    menu.addAction(operator("Run",             menu, "vertex_run"))
    menu.addAction(operator("Open Widget",     menu, "vertex_open"))
    if isinstance(graphItem().vertex(), CompositeNode):
        menu.addAction(operator("Inspect composite node", menu, "vertex_composite_inspect"))    
    menu.addSeparator()
    menu.addAction(operator("Delete",          menu, "vertex_remove"))
    menu.addAction(operator("Reset",           menu, "vertex_reset"))
    menu.addAction(operator("Replace By",      menu, "vertex_replace"))
    menu.addAction(operator("Reload",          menu, "vertex_reload"))
    menu.addSeparator()
    menu.addAction(operator("Caption",         menu, "vertex_set_caption"))
    menu.addAction(operator("Show/Hide ports", menu, "vertex_show_hide_ports"))
    menu.addSeparator()
    
    action = operator("Mark as User Application", menu, "vertex_mark_user_app")
    action.setCheckable(True)
    action.setChecked( bool(graphItem().vertex().user_application))
    menu.addAction(action)

    action = operator("Lazy", menu, "vertex_set_lazy")
    action.setCheckable(True)
    action.setChecked(graphItem().vertex().lazy)
    menu.addAction(action)

    action = operator("Block", menu, "vertex_block")
    action.setCheckable(True)
    action.setChecked(graphItem().vertex().block)
    menu.addAction(action)
    
    menu.addAction(operator("Internals", menu, "vertex_edit_internals"))
    menu.addSeparator()
    
    alignMenu = menu.addMenu("Align...")
    alignMenu.setDisabled(True)
    if len(items)>1:
        alignMenu.setDisabled(False)
        alignMenu.addAction(operator("Align horizontally", menu,  "graph_align_selection_horizontal"))
        alignMenu.addAction(operator("Align left", menu,  "graph_align_selection_left"))
        alignMenu.addAction(operator("Align right", menu,  "graph_align_selection_right"))
        alignMenu.addAction(operator("Align centered", menu,  "graph_align_selection_mean"))
        alignMenu.addAction(operator("Distribute horizontally", menu,  "graph_distribute_selection_horizontally"))
        alignMenu.addAction(operator("Distribute vertically", menu,  "graph_distribute_selection_vertically"))

    #The colouring
    colorMenu = menu.addMenu("Color...")
    colorMenu.addAction(operator("Set user color...", colorMenu, "graph_set_selection_color"))
    #check if the current selection is coloured and tick the 
    #menu item if an item of the selection uses the user color.
    action = operator("Use user color",  colorMenu, "graph_use_user_color")
    action.setCheckable(True)
    action.setChecked(False)
    for i in items:
        if i.vertex().get_ad_hoc_dict().get_metadata("useUserColor"):
            action.setChecked(True)
            break    
    colorMenu.addAction(action)
    
    #display the menu...
    pos = event.screenPos()
    menu.move(pos)
    menu.show()
    rect = menu.rect() ; rect.moveTo(pos)
    #fix the position of the menu if it tries to popup too close to the lower & right edges.
    #bad fixing strategy probably: what if we were create arabian menus?
    #We should maube sublcass QMenu to handle screen real estate and reuse it.
    if not QtGui.QApplication.desktop().availableGeometry(w).contains(rect, True):
        pos2 = menu.rect().bottomLeft()
        menu.move(pos-pos2)
    event.accept()



dataflowview.vertex.GraphicalVertex.set_event_handler("mouseDoubleClickEvent", vertexMouseDoubleClickEvent,
                                      dataflowview.adapter.GraphAdapter)
dataflowview.vertex.GraphicalVertex.set_event_handler("contextMenuEvent", vertexContextMenuEvent,
                                      dataflowview.adapter.GraphAdapter)



##############################
# QtEvent handlers for ports #
##############################
def portContextMenuEvent(graphItem, event):
    if isinstance(graphItem.port(), OutputPort):
        graphItem = weakref.ref(graphItem)
        view = graphItem().scene().views()[0]
        operator=GraphOperator(view, view.scene().graph())
        operator.set_port_item(graphItem())
        menu = QtGui.QMenu(view)

        menu.addAction(operator("Send to pool", menu, "port_send_to_pool"))
        menu.addAction(operator("Print",        menu, "port_print_value"))

        menu.move(event.screenPos())
        menu.show()

        event.accept()

dataflowview.vertex.GraphicalPort.set_event_handler("contextMenuEvent", portContextMenuEvent,
                                                    dataflowview.adapter.GraphAdapter)



##############################
# QtEvent handlers for edges #
##############################


def edgeContextMenuEvent(graphEdge, event):
    """ Context menu event : Display the menu"""
    operator = GraphOperator()
    operator.identify_focused_graph_view()
    w = operator.get_graph_view()
    if w.scene().get_interaction_flag() & OAGIS.TOPOLOGICALLOCK : return
    menu = QtGui.QMenu(event.widget())
    action = menu.addAction("Delete connection")
    action.triggered.connect(graphEdge.remove)
    menu.move(event.screenPos())
    menu.show()
    event.accept()

dataflowview.edge.GraphicalEdge.set_event_handler("contextMenuEvent", edgeContextMenuEvent,
                                                  dataflowview.adapter.GraphAdapter)

####################################
# QtEvent handlers for annotations #
####################################

#nothing special here the default
#actions of the dataflow strategy
#are fine



dataflowview.vertex.GraphicalVertex.static_init_handlers(dataflowview.adapter.GraphAdapter)
dataflowview.vertex.GraphicalPort.static_init_handlers(dataflowview.adapter.GraphAdapter)
dataflowview.edge.GraphicalEdge.static_init_handlers(dataflowview.adapter.GraphAdapter)
qtgraphview.View.static_init_handlers(dataflowview.adapter.GraphAdapter)
