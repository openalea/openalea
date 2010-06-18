

"""
This file demonstrates how to create views for graphs from the
`networkx <http://networkx.lanl.gov/_>` toolkit. This toolkit
provides efficient graph structures. We want to create a Qt
widget that allows one to view/create networkx graphs and edit
them.
"""

import networkx as nx
import weakref
from openalea.core import observer
import grapheditor.base

#These variables are shared by both the model
#and the Views. Conceptually, this is not good.
circleSize = 10.0*2
halfCircleSize = circleSize/2

#----------------------
# -- the graph model --
#----------------------
class NXObservedProxyNode( observer.Observed ):
    """ Proxy on networkx nodes """
    def __init__(self, vertex, graph):
        observer.Observed.__init__(self)
        self.v = vertex
        self.g = weakref.ref(graph)

    def notify_update(self, **kwargs):
        for item in kwargs.iteritems():
            self.notify_listeners(item)
        self.notify_position()

    def notify_position(self):
        pos = self.g().node[self.v]["position"]
        self.notify_listeners(("metadata_changed", "position", pos))

class NXObservedProxyEdge( observer.Observed ):
    """ Proxy on networkx edges. """
    def __init__(self, edge, graph):
        observer.Observed.__init__(self)
        self.e = edge
        self.g = weakref.ref(graph)

    def notify_update(self):
        pass

class NXObservedGraph( grapheditor.base.GraphAdapterBase, observer.Observed ):
    """An adapter to networkx.Graph"""
    def __init__(self):
        grapheditor.base.GraphAdapterBase.__init__(self)
        observer.Observed.__init__(self)
        self.set_graph(nx.Graph())
        self.__curVtx = 0

#    def new_vertex(self, position=None):
    def new_vertex(self, **kwargs):
        self.add_vertex(self.__curVtx, **kwargs)
        self.__curVtx += 1

    def add_vertex(self, vertex, **kwargs):
        if vertex in self.graph:
            return
        else:
            if "position" not in kwargs : kwargs["position"] = [0,0,0]
            proxy = NXObservedProxyNode(vertex, self.graph)
            kwargs["proxy"] = proxy
            self.graph.add_node(vertex, **kwargs)
            self.notify_listeners(("vertex_added", ("vertex", proxy)))

    #not in the adapter interface (yet):
    def set_vertex_data(self, vertex_proxy, **kwargs):
        vertex = vertex_proxy.v
        if vertex in self.graph:
            proxy = self.graph.node[vertex]["proxy"]
            self.graph.add_node(vertex, **kwargs)
            proxy.notify_update(**kwargs)

    def remove_vertex(self, vertex_proxy):
        n = vertex_proxy.v
        edges = self.graph.edges([n])
        print 'edges : ', edges
        for src, tgt in edges:
            self.remove_edge(src, tgt)
        self.graph.remove_node(n)
        self.notify_listeners(("vertex_removed", ("vertex",vertex_proxy)))

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
            proxy = NXObservedProxyEdge(edge, g)
            g.add_edge(*edge, proxy=proxy, **kwargs)
            self.notify_listeners(("edge_added", ("default", proxy, src_proxy, tgt_proxy)))

        print 'edges ', self.graph.edges()

    def remove_edge(self, source, target):
        proxy = self.graph.edge[source][target]["proxy"]
        self.graph.remove_edge(source, target)
        self.notify_listeners(("edge_removed", ("default",proxy)))


    def remove_edges(self, edge_proxies):
        grapheditor.base.GraphAdapterBase.remove_edges(self, (ep.e for ep in edge_proxies))

#------------------------
# -- the graph qt view --
#------------------------
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
        qtgraphview.Vertex.__init__(self, vertex, graph, defaultCenterConnector=True)
        self.initialise_from_model()

    def initialise_from_model(self):
        self.setPos(QtCore.QPointF(*self.graph().graph.node[self.vertex().v]["position"]))
        color = self.graph().graph.node[self.vertex().v]["color"]
        brush = QtGui.QBrush(color)
        self.setBrush(brush)

    def notify(self, sender, event):
        qtgraphview.Vertex.notify(self, sender, event)

    def get_view_data(self, *args, **kwargs):
        return self.graph().graph.node[self.vertex().v][args[0]]

    def store_view_data(self, **kwargs):
        """This call is executed while self is in "deaf" mode to avoid infinite loops"""
        pos = kwargs.get('position', None)
        if pos is not None:
            self.graph().set_vertex_data(self.vertex(), position=pos)

    mousePressEvent = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsEllipseItem,
                                   "mousePressEvent")
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsEllipseItem,
                              "itemChange")

    paint = mixin_method(QtGui.QGraphicsEllipseItem, None,
                         "paint")

class GraphicalEdge( qtgraphview.Edge, QtGui.QGraphicsPathItem  ):
    def __init__(self, edge=None, graph=None, src=None, dest=None):
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.Edge.__init__(self, edge, graph, src, dest)
        self.set_edge_creator(LinearEdgePath())

    def initialise_from_model(self):
        pass

    def notify(self, sender, event):
        qtgraphview.Edge.notify(self, sender, event)

    store_view_data = None
    get_view_data   = None


class GraphicalFloatingEdge(QtGui.QGraphicsPathItem, qtgraphview.FloatingEdge):
    def __init__(self, srcPoint, graph):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.FloatingEdge.__init__(self, srcPoint, graph)
        self.set_edge_creator(LinearEdgePath())


#-------------------------
# -- the graph strategy --
#-------------------------
Strategy = grapheditor.base.GraphStrategy(graphModelType = NXObservedGraph,
                                          vertexWidgetMap= {"vertex":GraphicalNode},
                                          edgeWidgetMap  = {"default":GraphicalEdge,
                                                            "floating-default":GraphicalFloatingEdge},
                                          #[GraphicalNode], not necessary since use the default invisible connector
                                          connectorTypes = [],
                                          #of vertices
                                          adapterType    = None)


#we register this strategy
baselisteners.GraphListenerBase.register_strategy(Strategy)


#CUSTOMISING THE GRAPH VIEW FOR THIS PARTICULAR DEMO:
from random import randint as rint
def dropHandler(view, event):
    position = view.mapToScene(event.pos())
    position = [position.x(), position.y()]
    view.scene().graph().new_vertex(position=position,
                                    color=QtGui.QColor(rint(0,255),rint(0,255),rint(0,255)))

View.set_default_drop_handler(dropHandler)
View.set_event_handler("mouseDoubleClickEvent", dropHandler, NXObservedGraph)

def removeNode(view, event):
    graphAdapter = view.scene().graph()
    vertices = view.scene().get_selected_items(filterType=GraphicalNode, subcall=lambda x:x.vertex())
    graphAdapter.remove_vertices(vertices)
    edges = view.scene().get_selected_items(filterType=GraphicalEdge)
    graphAdapter.remove_edges(e.edge() for e in edges)
    event.setAccepted(True)

keyPressMapping={ (QtCore.Qt.NoModifier, QtCore.Qt.Key_Delete ):removeNode,}
View.set_keypress_handler_map(keyPressMapping)
View.static_init_handlers(NXObservedGraph)


#THE APPLICATION'S MAIN WINDOW
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtGui.QMainWindow.__init__(self, parent)
        self.setMinimumSize(800,600)
        self.__graph = NXObservedGraph()
        self.__graphView = View(self, self.__graph)
        self.setCentralWidget(self.__graphView)


#THE ENTRY POINT
def main(argv):
    app = QtGui.QApplication(["GraphEditor and Networkx Demo"])
    QtGui.QApplication.processEvents()
    win = MainWindow()
    win.show()
    return app.exec_()

if __name__=="__main__":
    main(sys.argv)
