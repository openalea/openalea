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

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import weakref, sys
from PyQt4 import QtCore, QtGui
from openalea.visualea.graph_operator import GraphOperator
from openalea.core import observer, compositenode
from openalea.core.node import InputPort, OutputPort, AbstractPort, AbstractNode
from openalea.core.settings import Settings
from openalea.grapheditor import qtgraphview, baselisteners, qtutils
from openalea.grapheditor.qtutils import mixin_method
import painting
import adapter
from collections import deque

from .. import images_rc
"""

"""



class GraphicalVertex(qtgraphview.Vertex, QtGui.QGraphicsWidget):

    #color of the small box that indicates evaluation
    eval_color = QtGui.QColor(255, 0, 0, 200)

    def __init__(self, vertex, graph, parent=None, isInOrOut=None):
        QtGui.QGraphicsWidget.__init__(self, parent)
        qtgraphview.Vertex.__init__(self, vertex, graph)
        self.set_painting_strategy(painting.default_dataflow_paint)
        self.destroyed.connect(self.clear_observed)
        self.__isInOrOut = isInOrOut
        # used by the node shape cache in painting.py
        # to speed up rendering.
        self.shapeChanged=True

        # ---Small box when the vertex is being evaluated---
        self.hiddenPorts_item = QtGui.QGraphicsSimpleTextItem("+", self)
        self.hiddenPorts_item.setVisible(False)

        # ---Small cross when the vertex has hidden ports---
        self.modified_item = QtGui.QGraphicsRectItem(2.5,12.5,7,7, self)
        self.modified_item.setBrush(self.eval_color)
        self.modified_item.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.modified_item.setVisible(False)

        # ---Clock image when the vertex has a delay---
        self.delay_item= QtGui.QGraphicsPixmapItem(QtGui.QPixmap(':icons/clock.png'), self)
        self.delay_item.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.delay_item.setVisible(False)
        #self.delay_item= QtGui.QGraphicsSimpleTextItem("@", self)
        #self.delay_item.setVisible(False)

        # ---Sub items layout---
        layout = QtGui.QGraphicsLinearLayout()
        layout.setOrientation(QtCore.Qt.Vertical)
        layout.setSpacing(2)
        self.setLayout(layout)

        layout = QtGui.QGraphicsLinearLayout()
        self.layout().addItem(layout)
        self._inPortLayout = weakref.ref(layout)
        cap = qtutils.AleaQGraphicsLabelWidget("")
        self._caption = weakref.ref(cap)
        self.layout().addItem(self._caption())
        layout = QtGui.QGraphicsLinearLayout()
        self.layout().addItem(layout)
        self._outPortLayout = weakref.ref(layout)

        def __configure_layout(layout):
            layout.setSpacing(0.0)
            layout.setMinimumHeight(GraphicalPort.HEIGHT)
            self.layout().setAlignment(layout, QtCore.Qt.AlignHCenter)
        __configure_layout(self._inPortLayout())
        __configure_layout(self._outPortLayout())
        self.layout().setAlignment(self._caption(), QtCore.Qt.AlignHCenter)
        self.initialise_from_model()

    def remove_from_view(self, view):
        """An element removes itself from the given view"""
        # self.__remove_ports_from_view(view)
        # self.__remove_ports_from_view(view, outputs=True)
        self.__remove_ports()
        self.__remove_ports(outputs=True)
        qtgraphview.Vertex.remove_from_view(self, view)

    def initialise_from_model(self):
        vertex = self.vertex()
        mdict  = vertex.get_ad_hoc_dict()
        #graphical data init.
        mdict.simulate_full_data_change(self, vertex)
        #other attributes init
        for i in vertex.input_desc:
            self.notify(vertex, ("input_port_added", i))
        for i in vertex.output_desc:
            self.notify(vertex, ("output_port_added", i))
        for i in vertex.map_index_in:
            self.notify(vertex, ("input_modified", i))
        self.notify(vertex, ("caption_modified", vertex.internal_data["caption"]))
        self.notify(vertex, ("tooltip_modified", vertex.get_tip()))
        self.notify(vertex, ("internal_data_changed",))
        userColor = self.get_view_data("userColor")
        if( userColor is None ):
            self.store_view_data(useUserColor=False)
        
    def terminate_from_model(self):
        vertex = self.vertex()
        for i in vertex.input_desc:
            self.notify(vertex, ("input_port_removed", i))
        self.notify(vertex, ("cleared_input_ports",))
        for i in vertex.output_desc:
            self.notify(vertex, ("output_port_removed", i))
        self.notify(vertex("cleared_output_ports",))


    #####################################
    # pseudo-protected or private stuff #
    #####################################
    def _all_inputs_visible(self):
        count = self._inPortLayout().count()
        for i in range(count):
            if not self._inPortLayout().itemAt(i).graphicsItem().isVisible():
                return False
        return True

    def __add_in_connection(self, port):
        graphicalConn = GraphicalPort(self, port)
        self.destroyed.connect(graphicalConn.close_and_delete)
        self._inPortLayout().addItem(graphicalConn)
        self.add_connector(graphicalConn)

    def __add_out_connection(self, port):
        graphicalConn = GraphicalPort(self, port)
        self.destroyed.connect(graphicalConn.close_and_delete)
        self._outPortLayout().addItem(graphicalConn)
        self.add_connector(graphicalConn)

    ####################
    # Observer methods #
    ####################
    def store_view_data(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.vertex().get_ad_hoc_dict().set_metadata(k, v)

    def get_view_data(self, key):
        return self.vertex().get_ad_hoc_dict().get_metadata(key)

    def notify(self, sender, event):
        """ Notification sent by the vertex associated to the item """
        if event is None : return

        #this one simply catches events like becoming lazy
        #or blocked of user app, and that do not set any
        #internal value (handled by the paintEvent method)
        elif(event[0] == "internal_data_changed"):
            self.delay_item.setVisible(self.vertex().delay>0)
            self.delay_item.update()
            self.update()
        elif(event[0] == "data_modified"):
            if event[1] == "caption":
                caption = event[2]
                self.__set_caption(caption if len(caption)<20 else caption[:20]+"...'")
            else:
                self.delay_item.setVisible(self.vertex().delay>0)
                self.delay_item.update()
                self.update()
        elif(event[0]=="tooltip_modified"):
            tt = event[1]
            if tt is None:
                tt=""
            self.setToolTip(tt)

        elif(event[0] == "start_eval"):
            self.modified_item.setVisible(self.isVisible())
            self.modified_item.update()
            self.update()
            QtGui.QApplication.processEvents()

        elif(event[0] == "stop_eval"):
            self.modified_item.setVisible(False)
            self.modified_item.update()
            self.update()
            QtGui.QApplication.processEvents()

        elif(event[0] == "caption_modified"):
            caption = event[1]
            self.__set_caption(caption if len(caption)<20 else caption[:20]+"...'")

        elif(event[0] == "metadata_changed" and event[1]=="userColor"):
            if event[2] is None:
                self.store_view_data(useUserColor = False)
            self.update()

        elif(event[0] == "input_port_added"):
            self.__add_in_connection(event[1])

        elif(event[0] == "output_port_added"):
            self.__add_out_connection(event[1])

        elif(event[0] == "cleared_input_ports"):
            self.__remove_ports()

        elif(event[0] == "cleared_output_ports"):
            self.__remove_ports(outputs=True)

        qtgraphview.Vertex.notify(self, sender, event)

    def __set_caption(self, caption):
        """Sets the name displayed in the vertex widget, doesn't change
        the vertex data"""
        if caption == "":
            caption = " "
        self._caption().setText(caption)
        if(self.layout()): self.layout().updateGeometry()

    def __remove_ports(self, outputs=False):
        lay = self._outPortLayout() if outputs else self._inPortLayout()
        self.clear_layout(lay)

    def clear_layout(self, layout):
        count = layout.count()
        for i in range(count):
            item = layout.itemAt(0)
            self.remove_connector(item.graphicsItem())
            layout.removeAt(0) #we remove from the start, or else we quickly segfault.
            del item

    ###############################
    # ----Qt World overloads----  #
    ###############################
    def setGeometry(self, geom):
        #forcing a full recomputation of the geometry so that shrinking works
        pos = self.pos()
        QtGui.QGraphicsWidget.setGeometry(self, QtCore.QRectF(pos.x(),
                                                              pos.y(),-1.0,-1.0))

        #this is not such a bad place to check for port visibility
        #because it gets called when ports are hidden.
        self.hiddenPorts_item.setVisible(not self._all_inputs_visible())
        self.hiddenPorts_item.setPos(self.rect().width() - self.hiddenPorts_item.boundingRect().width() - 2,
                                     self._inPortLayout().geometry().top()+4 )

        self.delay_item.setVisible(self.vertex().delay>0)
        self.delay_item.setPos(2, self._inPortLayout().geometry().top()+4 )

        self.shapeChanged=True

    def mouseDoubleClickEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            # Read settings
            try:
                localsettings = Settings()
                str = localsettings.get("UI", "DoubleClick")
            except:
                str = "['open']"

            view = self.scene().views()[0]
            operator=GraphOperator(view, self.graph())
            operator.set_vertex_item(self)

            if('open' in str):
                operator(fName="vertex_open")()
            elif('run' in str):
                operator(fName="vertex_run")()

    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""
        self.setSelected(True)

        operator = GraphOperator()
        operator.vertexType = GraphicalVertex
        operator.identify_focused_graph_view()
        operator.set_vertex_item(self)
        widget = operator.get_graph_view()
        menu = qtutils.AleaQMenu(widget)
        items = widget.scene().get_selected_items(GraphicalVertex)

        menu.addAction(operator("Run",             menu, "vertex_run"))
        menu.addAction(operator("Open Widget",     menu, "vertex_open"))
        if isinstance(self.vertex(), compositenode.CompositeNode):
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
        action.setChecked( bool(self.vertex().user_application))
        menu.addAction(action)

        action = operator("Lazy", menu, "vertex_set_lazy")
        action.setCheckable(True)
        action.setChecked(self.vertex().lazy)
        menu.addAction(action)

        action = operator("Block", menu, "vertex_block")
        action.setCheckable(True)
        action.setChecked(self.vertex().block)
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
        action = operator("Use user color", colorMenu, "graph_use_user_color")
        action.setCheckable(True)
        action.setChecked(False)
        for i in items:
            if i.vertex().get_ad_hoc_dict().get_metadata("useUserColor"):
                action.setChecked(True)
                break
        colorMenu.addAction(action)

        #display the menu...
        menu.move(event.screenPos())
        menu.show()
        event.accept()


    def polishEvent(self):
        if self.__isInOrOut is not None:
            #fix input or output node position
            verticalNodeSize = 60
            midX, top, bottom, left, right = 0.0, 0.0, 0.0, 0.0, 0.0
            first = True
            graph = self.graph()
            for node in graph.vertex_property("_actor").itervalues():
                if node == graph.node(graph.id_in) or node == graph.node(graph.id_out):
                    continue
                posX, posY = node.get_ad_hoc_dict().get_metadata("position")
                if first:
                    top, bottom, left, right = posY, posY, posX, posX
                    first = False
                    continue
                top     = min( top, posY )
                bottom  = max( bottom, posY )
                left    = min( left, posX )
                right   = max( right, posX )

            midX = (left+right)/2
            if self.__isInOrOut :
                y = top - verticalNodeSize
                graph.node(graph.id_in).get_ad_hoc_dict().set_metadata("position", [midX, y])
            else :
                y = bottom + verticalNodeSize
                graph.node(graph.id_out).get_ad_hoc_dict().set_metadata("position", [midX, y])

    mousePressEvent = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsWidget,
                                   "mousePressEvent")
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsWidget,
                              "itemChange")


class GraphicalInVertex(GraphicalVertex):
    def __init__(self, vertex, graph, parent=None):
        GraphicalVertex.__init__(self, vertex, graph, parent=None, isInOrOut=True)

class GraphicalOutVertex(GraphicalVertex):
    def __init__(self, vertex, graph, parent=None):
        GraphicalVertex.__init__(self, vertex, graph, parent=None, isInOrOut=False)






# --------------------------- ConnectorType ---------------------------------
class GraphicalPort(QtGui.QGraphicsWidget, qtgraphview.Connector):
    """ A vertex port """
    MAX_TIPLEN = 2000
    __spacing  = 5.0
    WIDTH      = 10.0
    HEIGHT     = 10.0

    __size = QtCore.QSizeF(WIDTH+__spacing,
                           HEIGHT)

    __nosize = QtCore.QSizeF(0.0, 0.0)

    def __init__(self, parent, port):
        """
        """
        QtGui.QGraphicsWidget.__init__(self, parent)
        qtgraphview.Connector.__init__(self, observed=port)
        self.__interfaceColor = None
        self.set_connection_modifiers(QtCore.Qt.NoModifier)
        self.initialise_from_model()

    port = baselisteners.GraphElementListenerBase.get_observed

    def initialise_from_model(self):
        port = self.port()
        mdict  = port.get_ad_hoc_dict()
        #graphical data init.
        mdict.simulate_full_data_change(self, port)
        interface = port.get_interface()
        if interface and interface.__color__ is not None:
            self.__interfaceColor = QtGui.QColor(*interface.__color__)
        #update tooltip
        self.notify(port, ("tooltip_modified", port.get_tip()))

    def change_observed(self, old, new):
        if isinstance(new, AbstractPort):
            qtgraphview.Element.clear_observed(self)
            self.set_observed(new)

    def close_and_delete(self, obj):
        self.clear_observed()
        del self

    def notify(self, sender, event):
        try :
            self.port()
        except :
            self.clear_observed()
            del self
            return

        if(event[0] in ["tooltip_modified", "stop_eval"]):
            self.__update_tooltip()
        elif(event[0]=="metadata_changed"):
            if(sender == self.port()):
                if(event[1]=="hide"):
                    if event[2]: #if hide
                        self.hide()
                    else:
                        self.show()
                    self.updateGeometry()
        qtgraphview.Connector.notify(self, sender, event)

    def clear_observed(self, *args):
        qtgraphview.Element.clear_observed(self)
        return

    def __update_tooltip(self):
        node = self.port().vertex()
        if isinstance(self.port(), OutputPort):
            data = node.get_output(self.port().get_id())
        elif isinstance(self.port(), InputPort):
            data = node.get_input(self.port().get_id())
        s = str(data)
        if(len(s) > self.MAX_TIPLEN):
            s = "String too long..."
            self.setToolTip(s)
        else:
            #self.setToolTip("Value: " + s)
            self.setToolTip(self.port().get_tip(data) )

    ##################
    # QtWorld-Layout #
    ##################
    def size(self):
        size = self.__size
        if(not self.isVisible()):
            size = self.__nosize
        return size

    def sizeHint(self, blop, blip):
        return self.size()

    ##################
    # QtWorld-Events #
    #################
    def contextMenuEvent(self, event):
        if isinstance(self.port(), OutputPort):
            operator=GraphOperator()
            operator.identify_focused_graph_view()
            operator.set_port_item(self)
            menu = qtutils.AleaQMenu(operator.get_graph_view())
            menu.addAction(operator("Send to pool", menu, "port_send_to_pool"))
            menu.addAction(operator("Print",        menu, "port_print_value"))
            menu.show()
            menu.move(event.screenPos())
            event.accept()

    def paint(self, painter, option, widget):
        if(not self.isVisible()):
            return

        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        gradient = QtGui.QLinearGradient(0, 0, 10, 0)
        if self.highlighted:
            gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.red).light(120))
            gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkRed).light(120))
        else:
            if self.__interfaceColor is None:
                gradient.setColorAt(0.8, QtGui.QColor(QtCore.Qt.yellow).light(120))
                gradient.setColorAt(0.2, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
            else:
                gradient.setColorAt(0.8, self.__interfaceColor.light(120))
                gradient.setColorAt(0.2, self.__interfaceColor.light(120))

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        painter.drawEllipse(self.__spacing/2+1,1,self.WIDTH-2, self.HEIGHT-2)


    itemChange = mixin_method(qtgraphview.Connector, QtGui.QGraphicsWidget,
                              "itemChange")

