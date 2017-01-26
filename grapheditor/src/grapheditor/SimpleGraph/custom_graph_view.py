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


"""In this file we implement the basic graph views"""

from Qt import QtWidgets, QtGui, QtCore

from openalea.grapheditor.baselisteners import GraphListenerBase
from openalea.grapheditor.qtutils  import mixin_method, extend_qt_scene_event
from openalea.grapheditor.qtgraphview import Vertex, Edge, FloatingEdge
from openalea.grapheditor.edgefactory import LinearEdgePath

from custom_graph_model import Graph as GraphType
from custom_graph_model import Vertex as VertexModel

##############################################################
# Designing the widgets that will represent our vertices and #
# edges                                                      #
##############################################################

class SimpleVertex(QtWidgets.QGraphicsEllipseItem, Vertex):
    __vertex_size__= QtCore.QSizeF(30.0, 30.0)
    __border_size__=5

    def __init__(self, vertex, graph, parent=None):
        QtWidgets.QGraphicsEllipseItem.__init__(self, 0.0, 0.0,
                                            self.__vertex_size__.width(),
                                            self.__vertex_size__.height(),
                                            parent)
        Vertex.__init__(self, vertex, graph)
        self.setZValue(1.0)

        #we choose the avocado colors
        self.setBrush( QtGui.QBrush(QtCore.Qt.yellow) )
        pen=QtGui.QPen(QtCore.Qt.darkGreen)
        pen.setWidth(self.__border_size__-2)
        self.setPen(pen)

        self.initialise_from_model()

    ##################
    # QtWorld-Layout #
    ##################
    def size(self):
        return self.__vertex_size__

    def sizeHint(self, blop, blip):
        return self.__vertex_size__

    ##################
    # QtWorld-Events #
    ##################
    mousePressEvent = mixin_method(Vertex, QtWidgets.QGraphicsEllipseItem, "mousePressEvent")
    itemChange = mixin_method(Vertex, QtWidgets.QGraphicsEllipseItem, "itemChange")

    def contextMenuEvent(self, event): #called on right click on the vertex.
        menu = QtWidgets.QMenu(event.widget())
        action= menu.addAction("Delete vertex")
        action.connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        menu.popup(event.screenPos())
        event.accept()

    def remove(self):
        self.graph().remove_vertex(self.vertex())

    def paint(self, painter, painterOptions, widget):
        QtWidgets.QGraphicsEllipseItem.paint(self, painter, painterOptions, widget)

    def store_view_data(self, key, value, notify=True):
        self.vertex().get_ad_hoc_dict().set_metadata(key, value, notify)

    def get_view_data(self, key):
        return self.vertex().get_ad_hoc_dict().get_metadata(key)

    def announce_view_data(self, exclusive=False):
        if not exclusive:
            self.vertex().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.vertex().exclusive_command(exclusive,
                                            self.vertex().get_ad_hoc_dict().simulate_full_data_change)


class SimpleEdge(QtWidgets.QGraphicsPathItem, Edge):
    def __init__(self, edgeModel, graphadapter, vert1, vert2, parent=None):
        """ """
        QtWidgets.QGraphicsPathItem.__init__(self, parent)
        Edge.__init__(self, edgeModel, graphadapter, vert1, vert2)
        self.set_edge_path(LinearEdgePath())
        self.initialise_from_model()

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self.scene().views()[0])
        action = menu.addAction("Delete edge")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        menu.popup(event.screenPos())
        event.accept()

    def remove(self):
        self.graph().remove_edge( self.srcBBox(), self.dstBBox() )

    store_view_data = None
    get_view_data   = None
    announce_view_data = None

    def announce_view_data_src(self, exclusive=False):
        if not exclusive:
            self.srcBBox().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.srcBBox().exclusive_command(exclusive,
                                             self.srcBBox().get_ad_hoc_dict().simulate_full_data_change)

    def announce_view_data_dst(self, exclusive=False):
        if not exclusive:
            self.dstBBox().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.dstBBox().exclusive_command(exclusive,
                                             self.dstBBox().get_ad_hoc_dict().simulate_full_data_change)


class SimpleFloatingEdge(QtWidgets.QGraphicsPathItem, FloatingEdge):
    def __init__(self, srcPoint, graph):
        """ """
        QtWidgets.QGraphicsPathItem.__init__(self, None)
        FloatingEdge.__init__(self, srcPoint, graph)
        self.set_edge_path(LinearEdgePath())
        self.setZValue(0.0)




#########################################################
# Creating the strategy class that the view will use to #
# create the right widget at the right time.            #
#########################################################

class SimpleStrategy(object):
    @classmethod
    def get_graph_model_type(cls):
        """Returns the classobj defining the graph type"""
        return GraphType

    @classmethod
    def get_vertex_widget_factory(cls):
        """Returns a factory that instantiates vertices according
        to their types."""
        return GraphicalVertexFactory

    @classmethod
    def get_vertex_widget_types(cls):
        return {"vertex":SimpleVertex}

    @classmethod
    def get_edge_widget_factory(cls):
        """Returns a factory that instantiates edges according
        to their types."""
        return GraphicalEdgeFactory

    @classmethod
    def get_edge_widget_types(cls):
        return {"default":SimpleEdge,
                "floating-default":SimpleFloatingEdge}

    @classmethod
    def get_graph_adapter_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return None

    @classmethod
    def get_connector_types(cls):
        return [SimpleVertex]


def GraphicalVertexFactory(vtype, *args, **kwargs):
    VT = SimpleStrategy.get_vertex_widget_types().get(vtype)
    if VT: return VT(*args, **kwargs)

def GraphicalEdgeFactory(etype, *args, **kwargs):
    ET = SimpleStrategy.get_edge_widget_types().get(etype)
    if ET: return ET(*args, **kwargs)


GraphListenerBase.register_strategy(SimpleStrategy)
VertexModel.extend_ad_hoc_slots({"position"         :(list,[0,0]),
                                 "connectorPosition":(list,[0,0])})
