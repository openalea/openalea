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

import weakref
from PyQt4 import QtCore, QtGui,QtSvg
from openalea.visualea.graph_operator import GraphOperator
from openalea.core import observer, compositenode
from openalea.core.node import InputPort, OutputPort, AbstractPort, AbstractNode
from openalea.core.settings import Settings
from openalea.grapheditor import qtgraphview, baselisteners, qtutils
from openalea.grapheditor.qtutils import mixin_method, safeEffects
from openalea.visualea import images_rc
import adapter

"""
"""


class EvalObserver( observer.AbstractListener ):
    def __init__(self, callback):
        observer.AbstractListener.__init__(self)
        self.callback = callback
    def notify(self, sender, event):
        if event[0] == "start_eval":
            self.callback(sender, event)


class OpenAleaPortLayoutEngine(object):

    portSpacing      = 5.0
    outMargins       = 5.0
    delayMargins     = 7.0
    evalColor        = QtGui.QColor(255, 0, 0, 200)

    def __init__(self, graphicalParent):
        self._parent = weakref.proxy(graphicalParent)

        self.vLayout = qtutils.VerticalLayout(margins=(self.outMargins, self.outMargins, 0., 0.),
                                              center=True)
        # --- in ports ---
        self.inPortLayout = qtutils.HorizontalLayout(parent=self.vLayout,
                                                     innerMargins=(self.portSpacing,0.),
                                                     center=True,
                                                     mins=(5, 5))
        # --- Caption ---
        self._caption = QtGui.QGraphicsSimpleTextItem(graphicalParent)
        self.vLayout.addItem(self._caption)
        # --- out ports ---
        self.outPortLayout = qtutils.HorizontalLayout(parent=self.vLayout,
                                                      innerMargins=(self.portSpacing,0.),
                                                      center=True,
                                                      mins=(5, 5))

        # ---Small dots when the vertex has hidden ports---
        hiddenPortItem = HiddenPort(graphicalParent)
        hiddenPortItem.setVisible(False)
        self.hiddenPortItem = hiddenPortItem
        self.inPortLayout.addFinalItem(hiddenPortItem)

        # ---Small box when the vertex is busy, beping evaluated---
        self._busyItem = QtGui.QGraphicsRectItem(0,0,7,7, graphicalParent)
        self._busyItem.setBrush(self.evalColor)
        self._busyItem.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self._busyItem.setVisible(False)

        # ---Clock image when the vertex has a delay---
        self._delayItem = QtSvg.QGraphicsSvgItem(":icons/clock.svg",graphicalParent)
        self._delayItem.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self._delayItem.setVisible(False)

        self._delayText = QtGui.QGraphicsSimpleTextItem("0",self._delayItem)
        self._delayText.setFont(QtGui.QFont("ariana",6) )
        self._delayText.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0,200) ) )
        self._delayText.setZValue(self._delayItem.zValue() + 1)
        self._delayText.setVisible(False)

    def initialise_from_model(self):
        for it in self.inPortLayout+self.outPortLayout:
            it.initialise_from_model()

    def notify(self, graphicalVertex, event, attach=None):
        if event=="delayItemChange":
            self.update_delay_item(graphicalVertex)
        elif event=="evaluationStart":
            self._busyItem.setVisible(graphicalVertex.isVisible())
        elif event=="evaluationStop":
            self._busyItem.setVisible(False)
        elif event=="hiddenPortChange":
            self.update_hidden_port_item(graphicalVertex)
        elif event=="caption":
            self.__set_caption(attach)
        graphicalVertex.refresh_geometry()

    def add_port(self, port, graphicalParent):
        if isinstance(port, InputPort)    : l=self.inPortLayout
        elif isinstance(port, OutputPort) : l=self.outPortLayout
        if port not in l:
            gp = GraphicalPort(graphicalParent, port)
            l.addItem(gp)
            return gp

    def remove_port(self, port):
        if isinstance(port, InputPort)    : l=self.inPortLayout
        elif isinstance(port, OutputPort) : l=self.outPortLayout
        for gp in l:
            if gp.port() == port:
                l.removeItem(gp)

    def remove_ports(self, which="input"):
        if which == "input"    :
            l = self.inPortLayout
        elif which == "output" :
            l = self.outPortLayout
        for it in l:
            it.scene().removeItem(it) #???
        l.clear()

    def layout_items(self, graphicalParent):
        geom = self.vLayout.boundingRect(force=True)
        self.vLayout.setPos(QtCore.QPointF(0.,0.))
        self._busyItem.setPos(0, 0)
        self._delayItem.setPos( - self._delayItem.boundingRect().width()/2 - self.delayMargins,
                                (geom.height() - self._delayItem.boundingRect().height())/2 )
        self._delayText.setPos( (self._delayItem.boundingRect().width()-self._delayText.boundingRect().width())/2,
                                (self._delayItem.boundingRect().height()-self._delayText.boundingRect().height())/2 )
        return geom

    def __set_caption(self, caption):
        """Sets the name displayed in the vertex widget, doesn't change
        the vertex data"""
        if caption == "":
            caption = " "
        self._caption.setText(caption)

    def _all_inputs_visible(self):
        for i in self.inPortLayout:
            if not i.isVisible():
                return False
        return True

    def update_hidden_port_item (self, graphicalParent) :
        visible = not self._all_inputs_visible() and graphicalParent.isVisible()
        self.hiddenPortItem.setVisible(visible)

    def update_delay_item (self, graphicalParent) :
        visible = graphicalParent.vertex().delay > 0
        self._delayItem.setVisible(visible and graphicalParent.isVisible())
        self._delayText.setVisible(visible and graphicalParent.isVisible())
        if visible :
            self._delayText.setText("%d" % graphicalParent.vertex().delay)


class ObserverOnlyGraphicalVertex(qtgraphview.VertexWithPorts, QtGui.QGraphicsRectItem):
    LayoutEngine = OpenAleaPortLayoutEngine

    # --- PAINTING STUFF ---
    path_cache   = weakref.WeakKeyDictionary()
    # Color Definition
    default_not_modified_color       = QtGui.QColor(0, 0, 255, 255)
    default_selected_color           = QtGui.QColor(180, 180, 180, 255)
    default_not_selected_color       = QtGui.QColor(255, 255, 255, 255)
    default_error_color              = QtGui.QColor(255, 0, 0, 255)
    default_selected_error_color     = QtGui.QColor(0, 0, 0, 255)
    default_not_selected_error_color = QtGui.QColor(100, 0, 0, 255)

    #Shape definition
    default_corner_radius = 2.0
    default_margin        = 3.0

    def __init__(self, vertex, graph, parent=None):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, 1, 1, parent)
        qtgraphview.VertexWithPorts.__init__(self, vertex, graph)
        if safeEffects:
            fx = QtGui.QGraphicsDropShadowEffect()
            fx.setOffset(2,2)
            fx.setBlurRadius(5)
            self.setGraphicsEffect(fx)

    def _initialise_from_model(self):
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
        self.notify(vertex, ("hiddenPortChange",))
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

    def _refresh_geometry(self, geom):
        geom = geom.adjusted(0, 5, 0, -5)
        self.setRect(geom)

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
        elif event[0] == "hiddenPortChange":
            self.layoutEngine.notify(self, event[0])
        elif(event[0] == "internal_data_changed"):
            self.layoutEngine.notify(self, "delayItemChange")
        elif(event[0] == "data_modified"):
            if event[1] == "caption":
                caption = event[2] if len(event[2])<20 else event[2][:20]+"...'"
                self.layoutEngine.notify(self, "caption", caption)
            else:
                self.layoutEngine.notify(self, "delayItemChange")
        elif(event[0]=="tooltip_modified"):
            tt = event[1]
            if tt is None:
                tt=""
            self.setToolTip(tt)
        elif(event[0] == "start_eval"):
            self.layoutEngine.notify(self, "evaluationStart")
            QtGui.QApplication.processEvents()

        elif(event[0] == "stop_eval"):
            self.layoutEngine.notify(self, "evaluationStop")
            QtGui.QApplication.processEvents()

        elif(event[0] == "caption_modified"):
            caption = event[1] if len(event[1])<20 else event[1][:20]+"...'"
            self.layoutEngine.notify(self, "caption", caption)

        elif(event[0] == "metadata_changed" and event[1]=="userColor"):
            if event[2] is None:
                self.store_view_data(useUserColor = False)
        elif(event[0] == "input_port_added"):
            self.add_port(event[1])
        elif(event[0] == "output_port_added"):
            self.add_port(event[1])
        elif(event[0] == "cleared_input_ports"):
            self.remove_ports("input")
        elif(event[0] == "cleared_output_ports"):
            self.remove_ports("output")
        self.update()
        qtgraphview.VertexWithPorts.notify(self, sender, event)

    def paint(self, painter, options, widget):
        path = self.path_cache.get(self, None)
        if(path is None or self.shapeChanged):
            rect = self.rect()
            #prevent the painter from drawing outside the bounding rect
            rect.adjust(1,1,-1,-1)
            path = QtGui.QPainterPath()
            path.addRoundedRect(rect, self.default_corner_radius,
                                self.default_corner_radius)
            self.shapeChanged = False
            self.path_cache[self] = path

        pen = QtGui.QPen(QtCore.Qt.black, 1)
        userColor = self.get_view_data("userColor")

        if hasattr(self.vertex(), 'raise_exception'):
            color = self.default_error_color
            if(self.isSelected()):
                pen.setColor(QtGui.QColor(QtCore.Qt.red))
                secondcolor = self.default_selected_error_color
            else:
                secondcolor = self.default_not_selected_error_color
        else:
            if(self.isSelected()):
                pen.setColor(QtGui.QColor(180, 180, 255, 255))
                color = self.default_selected_color
            elif(self.get_view_data("useUserColor")):
                color=QtGui.QColor(*userColor)
            else:
                color = self.default_not_selected_color

        if(self.get_view_data("useUserColor")):
            secondcolor=QtGui.QColor(*userColor)
        elif(self.vertex().user_application):
            secondcolor = QtGui.QColor(255, 144, 0, 200)
        else:
            secondcolor = self.default_not_modified_color

        # Draw Box
        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, color)
        gradient.setColorAt(0.8, secondcolor)
        painter.setBrush(QtGui.QBrush(gradient))

        painter.setPen(pen)
        painter.drawPath(path)

        if(self.vertex().block):
            painter.setBrush(QtGui.QBrush(QtCore.Qt.BDiagPattern))
            painter.drawPath(path)

    mousePressEvent = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsRectItem,
                                   "mousePressEvent")
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsRectItem,
                              "itemChange")


class GraphicalVertex(ObserverOnlyGraphicalVertex):
    def __init__(self, vertex, graph, parent=None):
        ObserverOnlyGraphicalVertex.__init__(self, vertex, graph, parent)

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



class GraphicalInVertex(GraphicalVertex):
    def initialise_from_model(self):
        GraphicalVertex.initialise_from_model(self)
        self.polishEvent()

    def polishEvent(self):
        #fix input or output node position
        midX, top, bottom, left, right = 0.0, 0.0, 0.0, 0.0, 0.0
        first = True
        itemGeoms = self.scene().get_items(filterType=GraphicalVertex, subcall= lambda x: x.boundingRect().translated(x.pos()))
        bounds = reduce(lambda x,y: x|y, itemGeoms)
        midX = bounds.center().x()
        y = bounds.top() - self.boundingRect().height()*2
        self.store_view_data(position=[midX, y])

class GraphicalOutVertex(GraphicalVertex):
    def initialise_from_model(self):
        GraphicalVertex.initialise_from_model(self)
        self.polishEvent()

    def polishEvent(self):
        #fix input or output node position
        midX, top, bottom, left, right = 0.0, 0.0, 0.0, 0.0, 0.0
        first = True
        itemGeoms = self.scene().get_items(filterType=GraphicalVertex, subcall= lambda x: x.boundingRect().translated(x.pos()))
        bounds = reduce(lambda x,y: x|y, itemGeoms)
        midX = bounds.center().x()
        y = bounds.bottom()
        self.store_view_data(position=[midX, y])






class HiddenPort (QtGui.QGraphicsItem):
    """Graphical representation of hidden ports"""
    __size = QtCore.QSizeF(15.,4.)
    __nosize = QtCore.QSizeF(0.0, 0.0)
    def __init__ (self, parent) :
        """"""
        QtGui.QGraphicsItem.__init__(self, parent)
        self.setToolTip("hidden ports")

    def add_to_view(self, view):
        return

    def initialise_from_model(self):
        return

    def get_id(self):
        return float("inf")

    def size(self):
        return self.__size

    def sizeHint(self, blop, blip):
        return self.size()

    def boundingRect(self):
        pos  = QtCore.QPointF(0,0)
        size = self.size()
        return QtCore.QRectF(pos, size)

    def paint(self, painter, option, widget):
        if not self.isVisible() :
            return
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50,50,50,200) ) )
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0) )
        for i in (0,1,2) :
            painter.drawEllipse(QtCore.QRectF(i * 5.,0.,4.,4.) )


# --------------------------- ConnectorType ---------------------------------
class GraphicalPort(QtGui.QGraphicsEllipseItem, qtgraphview.Connector):
    """ A vertex port """
    MAX_TIPLEN = 2000
    WIDTH      = 10.0
    HEIGHT     = 10.0

    def __init__(self, parent, port):
        """
        """
        QtGui.QGraphicsEllipseItem.__init__(self, 0, 0, self.WIDTH, self.HEIGHT, parent)
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

    def get_id(self):
        return self.port().get_id()

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
        pos = self.pos()
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
        painter.drawEllipse(QtCore.QRectF(0, 0, self.WIDTH, self.HEIGHT) )


    itemChange = mixin_method(qtgraphview.Connector, QtGui.QGraphicsItem,
                              "itemChange")

