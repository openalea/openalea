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
from openalea.grapheditor.grapheditor_baselisteners import GraphListenerBase
from openalea.grapheditor.qtgraphview import QtGraphViewVertex, QtGraphViewEdge, QtGraphViewFloatingEdge
from openalea.grapheditor.edgefactory import LinearEdgePath
from PyQt4 import QtGui, QtCore
from custom_graph_model import Graph as GraphType
from custom_graph_model import Vertex as VertexModel


class SimpleVertex(QtGui.QGraphicsWidget, QtGraphViewVertex):
    __vertex_size__= QtCore.QSizeF(30.0, 30.0)
    __border_size__=2

    def __init__(self, vertex, graph, parent=None):
        QtGui.QGraphicsWidget.__init__(self, parent)
        QtGraphViewVertex.__init__(self, vertex, graph)
        self.setZValue(1.0)
        self.initialise_from_model()

    ##################
    # QtWorld-Layout #
    ##################
    def size(self):
        size = self.__vertex_size__
        return size

    def sizeHint(self, blop, blip):
        return self.size()

    ##################
    # QtWorld-Events #
    ##################
    def mousePressEvent(self, event):
        QtGraphViewVertex.mousePressEvent(self, event)        
        QtGui.QGraphicsWidget.mousePressEvent(self, event)

    def polishEvent(self):
        QtGraphViewVertex.polishEvent(self)
        QtGui.QGraphicsWidget.polishEvent(self)

    def moveEvent(self, event):
        QtGraphViewVertex.moveEvent(self, event)
        QtGui.QGraphicsWidget.moveEvent(self, event)
    
    def contextMenuEvent(self, event): #called on right click on the vertex.
        menu = QtGui.QMenu(event.widget())
        action= menu.addAction("Delete vertex")
        action.connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        menu.popup(event.screenPos())
        event.accept()

    def remove(self):
        self.graph().remove_vertex(self.vertex())

    def paint(self, painter, option, widget):
        rect = self.rect()
        rect.adjust(self.__border_size__, self.__border_size__,
                    self.__border_size__, self.__border_size__)
        
        #we choose the avocado colors
        painter.setBrush( QtGui.QBrush(QtCore.Qt.yellow) )
        pen=QtGui.QPen(QtCore.Qt.darkGreen)
        pen.setWidth(self.__border_size__-1)
        painter.setPen(pen)
        painter.drawEllipse(rect)
        


class SimpleEdge(QtGui.QGraphicsPathItem, QtGraphViewEdge):
    def __init__(self, edgeModel, graphadapter, vert1, vert2, parent=None):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, parent)
        QtGraphViewEdge.__init__(self, edgeModel, graphadapter, vert1, vert2)
        self.set_edge_path(LinearEdgePath())
        self.initialise_from_model()

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self.scene().views()[0])
        action = menu.addAction("Delete edge")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), remove)
        menu.popup(event.screenPos())
        event.accept()
        
    def remove(self):
        self.graph().remove_edge( self.src(), self.dst() )



class SimpleFloatingEdge(QtGui.QGraphicsPathItem, QtGraphViewFloatingEdge):
    def __init__(self, srcPoint, graph):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, None)
        QtGraphViewFloatingEdge.__init__(self, srcPoint, graph)
        self.set_edge_path(LinearEdgePath())
        self.setZValue(0.0)







def GraphicalVertexFactory(vtype, *args, **kwargs):
    VT = SimpleStrategy.get_vertex_widget_types().get(vtype)
    if VT: return VT(*args, **kwargs)

def GraphicalEdgeFactory(etype, *args, **kwargs):
    ET = SimpleStrategy.get_edge_widget_types().get(etype)
    if ET: return ET(*args, **kwargs)






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


GraphListenerBase.register_strategy(SimpleStrategy)
VertexModel.extend_ad_hoc_slots({"position":list, "connectorPosition":list})
