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
from openalea.core import observer
from openalea.core.node import InputPort, OutputPort, AbstractPort, AbstractNode
from openalea.grapheditor import qtutils
from openalea.grapheditor.qtutils import mixin_method
from openalea.grapheditor import qtgraphview, baselisteners
import painting
import adapter
from collections import deque

"""

"""



class GraphicalVertex(QtGui.QGraphicsWidget, qtgraphview.Vertex):

    #color of the small box that indicates evaluation
    eval_color = QtGui.QColor(255, 0, 0, 200)

    def __init__(self, vertex, graph, parent=None):
        QtGui.QGraphicsWidget.__init__(self, parent)
        qtgraphview.Vertex.__init__(self, vertex, graph)
        self.set_painting_strategy(painting.default_dataflow_paint)
        self.setZValue(1)
        self.destroyed.connect(self.clear_observed)

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

        self.__configure_layout(self._inPortLayout())
        self.__configure_layout(self._outPortLayout())
        self.layout().setAlignment(self._caption(), QtCore.Qt.AlignHCenter)

        self.initialise_from_model()

    def remove_from_view(self, view):
        """An element removes itself from the given view"""
        self.__remove_outputs(view)
        self.__remove_inputs(view)
        qtgraphview.Vertex.remove_from_view(self, view)

    def terminate_from_model(self):
        """todo evaluate this for inclusion into the interfaces"""
        self.vertex().exclusive_command(self, self.vertex().simulate_destruction_notifications)


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
        graphicalConn = GraphicalPort(port)
        self.destroyed.connect(graphicalConn.close_and_delete)
        self._inPortLayout().addItem(graphicalConn)

    def __add_out_connection(self, port):
        graphicalConn = GraphicalPort(port)
        self.destroyed.connect(graphicalConn.close_and_delete)
        self._outPortLayout().addItem(graphicalConn)

    ####################
    # Observer methods #
    ####################
    def store_view_data(self, key, value, notify=True):
        self.vertex().get_ad_hoc_dict().set_metadata(key, value)

    def get_view_data(self, key):
        return self.vertex().get_ad_hoc_dict().get_metadata(key)

    def announce_view_data(self, exclusive=False):
        if not exclusive:
            self.vertex().get_ad_hoc_dict().simulate_full_data_change()
            self.vertex().simulate_construction_notifications()
        else:
            self.vertex().exclusive_command(exclusive,
                                            self.vertex().get_ad_hoc_dict().simulate_full_data_change)
            self.vertex().exclusive_command(exclusive,
                                            self.vertex().simulate_construction_notifications)

    def notify(self, sender, event):
        """ Notification sent by the vertex associated to the item """
        if event is None : return

        #this one simply catches events like becoming lazy
        #or blocked of user app...
        if(event[0] in ["internal_data_changed", "data_modified"]):
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
            self.set_caption(event[1])

        elif(event[0] == "metadata_changed" and event[1]=="userColor"):
            if event[2] is None:
                self.store_view_data("useUserColor", False, False)
            self.update()

        elif(event[0] == "input_port_added"):
            self.__add_in_connection(event[1])

        elif(event[0] == "output_port_added"):
            self.__add_out_connection(event[1])

        elif(event[0] == "cleared_input_ports"):
            self.__remove_inputs()

        elif(event[0] == "cleared_output_ports"):
            self.__remove_outputs()

        qtgraphview.Vertex.notify(self, sender, event)

    def set_caption(self, caption):
        """Sets the name displayed in the vertex widget, doesn't change
        the vertex data"""
        if caption == "":
            caption = " "
        self._caption().setText(caption)
        if(self.layout()): self.layout().updateGeometry()

    def __remove_inputs(self, view=None):
        self.clear_layout(self._inPortLayout())

    def __remove_outputs(self, view=None):
        self.clear_layout(self._outPortLayout())

    def clear_layout(self, layout):
        count = layout.count()
        for i in range(count):
            item = layout.itemAt(0)
            layout.removeAt(0)
            del item

    def __configure_layout(self, layout):
        layout.setSpacing(0.0)
        layout.setMinimumHeight(GraphicalPort.HEIGHT)
        self.layout().setAlignment(layout, QtCore.Qt.AlignHCenter)



    ###############################
    # ----Qt World overloads----  #
    ###############################
    def setGeometry(self, geom):
        #forcing a full recomputation of the geometry so that shrinking works
        pos = self.pos()
        QtGui.QGraphicsWidget.setGeometry(self, QtCore.QRectF(pos.x(),
                                                              pos.y(),-1.0,-1.0))
        pos = self.pos()
        self.store_view_data('position', [pos.x(), pos.y()])

        #this is a not so bad place to check for port visibility
        #because it gets called when ports are hidden.
        self.hiddenPorts_item.setVisible(not self._all_inputs_visible())
        self.hiddenPorts_item.setPos(self.rect().width() - self.hiddenPorts_item.boundingRect().width() - 2,
                                     self._inPortLayout().geometry().top()+4 )
        self.shapeChanged=True

    mousePressEvent = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsWidget,
                                   "mousePressEvent")
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsWidget,
                              "itemChange")



def set_composite_in_out_position(graph, isInNode):
    """Recomputes the position of In and Out ports to place them above or below
    every other port"""
    verticalNodeSize = 60
    midX, top, bottom, left, right = 0.0, 0.0, 0.0, 0.0, 0.0
    first = True
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
    if isInNode :
        y = top - verticalNodeSize
        graph.node(graph.id_in).get_ad_hoc_dict().set_metadata("position", [midX, y])
    else :
        y = bottom + verticalNodeSize
        graph.node(graph.id_out).get_ad_hoc_dict().set_metadata("position", [midX, y])


class GraphicalInVertex(GraphicalVertex):
    def __init__(self, vertex, graph, parent=None):
        GraphicalVertex.__init__(self, vertex, graph, parent=None)

    def polishEvent(self):
        set_composite_in_out_position(self.graph(), True)
        GraphicalVertex.polishEvent(self)

class GraphicalOutVertex(GraphicalVertex):
    def __init__(self, vertex, graph, parent=None):
        GraphicalVertex.__init__(self, vertex, graph, parent=None)

    def polishEvent(self):
        set_composite_in_out_position(self.graph(), False)
        GraphicalVertex.polishEvent(self)



class GraphicalPort(QtGui.QGraphicsWidget, qtgraphview.Element):
    """ A vertex port """
    MAX_TIPLEN = 2000
    __spacing  = 5.0
    WIDTH      = 10.0
    HEIGHT     = 10.0

    __size = QtCore.QSizeF(WIDTH+__spacing,
                           HEIGHT)

    __nosize = QtCore.QSizeF(0.0, 0.0)

    def __init__(self, port):
        """
        """
        QtGui.QGraphicsWidget.__init__(self)
        qtgraphview.Element.__init__(self, observed=port)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        self.__vertBBox = baselisteners.ObservedBlackBox(self,port.vertex())
        self.setZValue(1.5)
        self.highlighted = False
        port.simulate_construction_notifications()

    port = baselisteners.GraphElementObserverBase.get_observed

    def change_observed(self, old, new):
        if isinstance(new, AbstractPort):
            qtgraphview.Element.clear_observed(self)
            self.set_observed(new)
        elif isinstance(new, AbstractNode):
            self.__vertBBox.clear_observed()
            self.__vertBBox(new)

    def close_and_delete(self, obj):
        self.clear_observed()
        del self


    def notify(self, sender, event):
        try : self.port(); self.__vertBBox()
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
            elif(sender == self.__vertBBox() and event[1]=="position"):
                self.__update_scene_center()

    def clear_observed(self, *args):
        self.__vertBBox.clear_observed()
        qtgraphview.Element.clear_observed(self)
        return

    def get_scene_center(self):
        pos = self.rect().center() + self.scenePos()
        return [pos.x(), pos.y()]

    def __update_scene_center(self):
        self.port().get_ad_hoc_dict().set_metadata("connectorPosition",
                                                   self.get_scene_center())
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

    def set_highlighted(self, val):
        self.highlighted = val
        self.update()

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
    ##################
    def mousePressEvent(self, event):
        scene = self.scene()
        if (scene and event.buttons() & QtCore.Qt.LeftButton):
            scene.new_edge_start(self.get_scene_center())
            return

    def paint(self, painter, option, widget):
        if(not self.isVisible()):
            return

        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        gradient = QtGui.QLinearGradient(0, 0, 10, 0)
        if self.highlighted:
            gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.red).light(120))
            gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkRed).light(120))
        else:
            gradient.setColorAt(0.8, QtGui.QColor(QtCore.Qt.yellow).light(120))
            gradient.setColorAt(0.2, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        painter.drawEllipse(self.__spacing/2+1,1,self.WIDTH-2, self.HEIGHT-2)

