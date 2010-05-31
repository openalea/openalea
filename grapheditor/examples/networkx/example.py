

"""
:mod:`networkx.example` -- An example of networkx GraphEditor strategy.
=======================================================================

.. module:: networkx.example
   :platform: All
   :synopsis: View and edit networkx.Graph.
.. moduleauthor:: Daniel Barbeau <daniel.barbeau@sophia.inria.fr>


This file demonstrates how to create views for graphs from the
`networkx <http://networkx.lanl.gov/_>` toolkit. This toolkit
provides efficient graph structures. We want to provide an Qt
widget that allows one to view/create networkx graphs and edit
them.
"""

import networkx as nx
import weakref
from openalea.core import observer

circleSize = 10.0
halfCircleSize = circleSize/2

# -- the graph model --
class NXObservedNode( observer.Observed ):
    """ Proxy on networkx nodes """
    def __init__(self, vertex, graph):
        observer.Observed.__init__(self)
        self.v = vertex
        self.g = weakref.ref(graph)

    def notify_update(self):
        self.notify_position()

    def notify_position(self):
        pos = self.g().node[self.v]["position"]
        self.notify_listeners(("metadata_changed", "position", pos))
        center = pos[0] + halfCircleSize, pos[1] + halfCircleSize
        self.notify_listeners(("metadata_changed", "connectorPosition", center))

class NXObservedEdge( observer.Observed ):
    """ Proxy on networkx edges. """
    def __init__(self, edge, graph):
        observer.Observed.__init__(self)
        self.e = edge
        self.g = weakref.ref(graph)

    def notify_update(self):
        pass #self.notify_listeners(self.e, ("update",))

class NXGraph( observer.Observed ):
    """An adapter to networkx.Graph"""
    def __init__(self):
        observer.Observed.__init__(self)
        self.set_graph(nx.Graph())
        self.__curVtx = 0

    def set_graph(self, graph):
        self.graph = graph

    def new_vertex(self, position=None):
        self.add_vertex(self.__curVtx, position=position)
        self.__curVtx += 1

    def add_vertex(self, vertex, **kwargs):
        if vertex in self.graph:
            proxy = self.graph.node[vertex]["proxy"]
            self.graph.add_node(vertex, **kwargs)
            proxy.notify_update()
        else:
            if "position" not in kwargs : kwargs["position"] = [0,0,0]
            proxy = NXObservedNode(vertex, self.graph)
            kwargs["proxy"] = proxy
            self.graph.add_node(vertex, **kwargs)
            self.notify_listeners(("vertex_added", ("vertex", proxy)))

    def get_vertex(self, vid):
        return vid # ?

    def remove_vertex(self, vertex_proxy):
        n = vertex_proxy.v
        edges = self.graph.edges([n])
        print 'edges : ', edges
        for src, tgt in edges:
            self.remove_edge(src, tgt)
        self.graph.remove_node(n)
        self.notify_listeners(("vertex_removed", ("vertex",vertex_proxy)))

    def remove_vertices(self, vertex_proxies):
        for vp in vertex_proxies:
            self.remove_vertex(vp)

    def add_edge(self, src_proxy, tgt_proxy, **kwargs):
        g = self.graph
        src, tgt = src_proxy.v, tgt_proxy.v
        edge = (src, tgt)
        if g.has_edge(*edge):
            data = g.get_edge_data(*edge)
            proxy = data["proxy"]
            data.update(kwargs)
            proxy.notify_update()
        else:
            proxy = NXObservedEdge(edge, g)
            g.add_edge(*edge, proxy=proxy, **kwargs)
            self.notify_listeners(("edge_added", ("default", proxy, src_proxy, tgt_proxy)))

        print 'edges ', self.graph.edges()

    def remove_edge(self, source, target):
        proxy = self.graph.edge[source][target]["proxy"]
        self.graph.remove_edge(source, target)
        self.notify_listeners(("edge_removed", ("default",proxy)))


    def remove_edges(self, edge_proxies):
        for ep in edge_proxies:
            self.remove_edge(*ep.e)

    # -- Utility methods, not always useful.
    def replace_vertex(self, oldVertex, newVertex):
        raise NotImplementedError

    def get_vertex_inputs(self, graphicalV):
        return self.graph.edges(graphicalV.v, data=True)

    def get_vertex_outputs(self, graphicalV):
        return self.graph.edges(graphicalV.v, data=True)

    def get_vertex_input(self, graphicalV, pid):
        return self.graph.edges(graphicalV.v, data=True)[pid]

    def get_vertex_output(self, graphicalV, pid):
        return self.graph.edges(graphicalV.v, data=True)[pid]

    #type checking
    def is_input(self, input):
        return True

    def is_output(self, output):
        return True

    #other checks
    def is_vertex_protected(self, vertex):
        return False

    def is_legal_connection(self, src, dst):
        return True

    @classmethod
    def get_vertex_types(cls):
        return ["vertex"]

    @classmethod
    def get_edge_types(cls):
        return ["default"]


# -- the graph qt view --
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from openalea.grapheditor import baselisteners
from openalea.grapheditor import qtgraphview
from openalea.grapheditor.qtgraphview import View
from openalea.grapheditor.qtutils import mixin_method
from openalea.grapheditor.edgefactory import LinearEdgePath

class GraphicalNode( qtgraphview.Vertex, QtGui.QGraphicsEllipseItem  ):
    def __init__(self, vertex, graph):
        QtGui.QGraphicsEllipseItem .__init__(self, 0, 0, circleSize, circleSize, None)
        qtgraphview.Vertex.__init__(self, vertex, graph)
        # ---Qt Stuff---
        self.setZValue(1.0)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(0x800) #SIP doesn't know about the ItemSendsGeometryChanges flag yet

        #set the initial position of the GRAPHICAL item
        self.setPos(QtCore.QPointF(*self.graph().graph.node[self.vertex().v]["position"]))

    def notify(self, sender, event):
        #Do cool stuff here
        qtgraphview.Vertex.notify(self, sender, event)


    def announce_view_data(self, *args, **kwargs):
        pass

    def get_view_data(self, *args, **kwargs):
        return self.graph().graph.node[self.vertex().v][args[0]]

    def store_view_data(self, *args, **kwargs):
        """ Store view data is used to put data relative to the view in a place that can be saved """
        #CODE REVIEW why don't we receive a dictionnary of data instead of this unpredictable stuff?
        self.graph().add_vertex(self.vertex().v, **dict([args]))

    # CODE REVIEW : The mixin_method(t1, t2, callName) is easy to use but one must know that it
    # needs to be done. It creates a wrapper method that calls t1.callName and then t2.callName.
    # We do this because the classes used in qtgraphview don't know which QGraphicsItem subclass
    # will be used to implement the actual item in the strategy. Of course you can overload callName
    # yourself.
    mousePressEvent = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsEllipseItem,
                                   "mousePressEvent")
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsEllipseItem,
                              "itemChange")

class GraphicalEdge( qtgraphview.Edge, QtGui.QGraphicsPathItem  ):
    def __init__(self, edge=None, graph=None, src=None, dest=None):
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.Edge.__init__(self, edge, graph, src, dest)
        self.set_edge_path(LinearEdgePath())
        src.notify_update()
        dest.notify_update()
        self.setZValue(0.0)


    def notify(self, sender, event):
        qtgraphview.Edge.notify(self, sender, event)

    store_view_data = None
    get_view_data   = None
    announce_view_data = None

    def announce_view_data_src(self, *args, **kwargs):
        pass

    def announce_view_data_dst(self, *args, **kwargs):
        pass

class GraphicalFloatingEdge(QtGui.QGraphicsPathItem, qtgraphview.FloatingEdge):
    def __init__(self, srcPoint, graph):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.FloatingEdge.__init__(self, srcPoint, graph)
        self.set_edge_path(LinearEdgePath())

# -- the graph strategy --
class Strategy(object):

    @classmethod
    def get_graph_model_type(cls):
        """Returns the classobj defining the graph type"""
        return NXGraph

    @classmethod
    def get_vertex_widget_factory(cls):
        """Returns a factory that instantiates vertices according
        to their types."""
        return GraphicalVertexFactory

    @classmethod
    def get_vertex_widget_types(cls):
        return {"vertex":GraphicalNode}

    @classmethod
    def get_edge_widget_factory(cls):
        """Returns a factory that instantiates edges according
        to their types."""
        return GraphicalEdgeFactory

    @classmethod
    def get_edge_widget_types(cls):
        return {"default":GraphicalEdge,
                "floating-default":GraphicalFloatingEdge}

    @classmethod
    def get_graph_adapter_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return None

    @classmethod
    def get_connector_types(cls):
        return [GraphicalNode]


def GraphicalVertexFactory(vtype, *args, **kwargs):
    VertexClass = Strategy.get_vertex_widget_types().get(vtype)
    if(VertexClass):
        return VertexClass(*args, **kwargs)
    else:
        raise Exception("vtype not found")


def GraphicalEdgeFactory(etype, *args, **kwargs):
    EdgeClass = Strategy.get_edge_widget_types().get(etype)
    if(EdgeClass):
        return EdgeClass(*args, **kwargs)
    else:
        raise Exception("vtype not found")


#we register this strategy
baselisteners.GraphListenerBase.register_strategy(Strategy)



#CUSTOMISING THE GRAPH VIEW FOR THIS PARTICULAR DEMO:
def dropHandler(view, event):
    position = view.mapToScene(event.pos())
    position = [position.x(), position.y()]
    view.scene().graph().new_vertex(position)

View.set_default_drop_handler(dropHandler)
View.set_event_handler("mouseDoubleClickEvent", dropHandler, NXGraph)

def removeNode(view, event):
    nodes = view.scene().get_selected_items(filterType=GraphicalNode)
    vertices = [n.vertex() for n in nodes]
    view.scene().graph().remove_vertices(vertices)

    edges = view.scene().get_selected_items(filterType=GraphicalEdge)
    view.scene().graph().remove_edges(e.edge() for e in edges)
    event.setAccepted(True)

keyPressMapping={ (QtCore.Qt.NoModifier, QtCore.Qt.Key_Delete ):removeNode,}
View.set_keypress_handler_map(keyPressMapping)
View.static_init_handlers(NXGraph)


#THE APPLICATION'S MAIN WINDOW
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtGui.QMainWindow.__init__(self, parent)
        self.__graph = NXGraph()
        self.__graphView = View(self, self.__graph)
        self.setCentralWidget(self.__graphView)


#THE ENTRY POINT
def main(args):
    app = QtGui.QApplication(args)
    QtGui.QApplication.processEvents()
    win = MainWindow()
    win.show()
    return app.exec_()

if __name__=="__main__":
    main(sys.argv)
