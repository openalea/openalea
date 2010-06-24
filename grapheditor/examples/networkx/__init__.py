

"""
This file demonstrates how to create views for graphs from the
`networkx <http://networkx.lanl.gov/_>` toolkit. This toolkit
provides efficient graph structures. We want to create a Qt
widget that allows one to view/create networkx graphs and edit
them.
"""

import networkx as nx
from openalea.grapheditor import Observed, GraphAdapterBase
import weakref

#These variables are shared by both the model
#and the Views. Conceptually, this is not good.
circleSize = 10.0*2
halfCircleSize = circleSize/2

#----------------------
# -- the graph model --
#----------------------
class NXObservedNode( Observed ):
    """ Proxy on networkx nodes """
    def __init__(self, graph):
        Observed.__init__(self)
        self.g = weakref.ref(graph)

    def notify_update(self, **kwargs):
        for item in kwargs.iteritems():
            self.notify_listeners(item)
        self.notify_position()

    def notify_position(self):
        pos = self.g().node[self]["position"]
        self.notify_listeners(("metadata_changed", "position", pos))

class NXObservedProxyEdge( Observed ):
    """ Proxy on networkx edges. """
    def __init__(self, edge, graph):
        Observed.__init__(self)
        self.e = edge
        self.g = weakref.ref(graph)

    def notify_update(self):
        pass

class NXObservedGraph( GraphAdapterBase, Observed ):
    """An adapter to networkx.Graph"""
    def __init__(self):
        GraphAdapterBase.__init__(self)
        Observed.__init__(self)
        self.set_graph(nx.Graph())
        self.__curVtx = 0

    def new_vertex(self, **kwargs):
        vtx = NXObservedNode(self.graph)
        self.add_vertex(vtx, **kwargs)

    def add_vertex(self, vertex, **kwargs):
        if vertex in self.graph:
            return
        else:
            position = kwargs.pop("position", [0,0,0])
            self.graph.add_node(vertex, position=position, **kwargs)
            self.notify_listeners(("vertex_added", ("vertex", vertex)))

    def remove_vertex(self, vertex):
        g = self.graph
        edges = g.edges([vertex])
        for src, tgt in edges:
            self.remove_edge(src, tgt)
        g.remove_node(vertex)
        self.notify_listeners(("vertex_removed", ("vertex",vertex)))

    def add_edge(self, src_vertex, tgt_vertex, **kwargs):
        g = self.graph
        edge = (src_vertex, tgt_vertex)
        if g.has_edge(*edge):
            return
        else:
            proxy = NXObservedProxyEdge(edge, g)
            g.add_edge(*edge, proxy=proxy, **kwargs)
            self.notify_listeners(("edge_added", ("default", proxy, src_vertex, tgt_vertex)))

    def remove_edge(self, src_vertex, tgt_vertex):
        proxy = self.graph.edge[src_vertex][tgt_vertex]["proxy"]
        self.graph.remove_edge(src_vertex, tgt_vertex)
        self.notify_listeners(("edge_removed", ("default",proxy)))

    def remove_edges(self, edge_proxies):
        GraphAdapterBase.remove_edges(self, (ep.e for ep in edge_proxies))

    # -- not in the adapter interface (yet): --
    def set_vertex_data(self, vertex, **kwargs):
        if vertex in self.graph:
            self.graph.node[vertex].update(kwargs)
            vertex.notify_update(**kwargs)

    def set_edge_data(self, edge_proxy, **kwargs):
        if g.has_edge(*edge):
            v1, v2 = edge_proxy.edge
            self.graph.edge[v1][2].update(kwargs)
            edge_proxy.notify_update(**kwargs)

#------------------------
# -- the graph qt view --
#------------------------
import sys
from PyQt4 import QtGui, QtCore
from openalea.grapheditor import GraphStrategyMaker
from openalea.grapheditor import Edge, FloatingEdge, Vertex, Scene, View, mixin_method, LinearEdgePath
from random import randint as rint # for random colors

class GraphicalNode( Vertex, QtGui.QGraphicsEllipseItem  ):
    def __init__(self, vertex, graph):
        QtGui.QGraphicsEllipseItem .__init__(self, 0, 0, circleSize, circleSize, None)
        Vertex.__init__(self, vertex, graph, defaultCenterConnector=True)
        self.initialise_from_model()

    def initialise_from_model(self):
        self.setPos(QtCore.QPointF(*self.graph().graph.node[self.vertex()]["position"]))
        color = self.graph().graph.node[self.vertex()]["color"]
        brush = QtGui.QBrush(color)
        self.setBrush(brush)

    def notify(self, sender, event):
        Vertex.notify(self, sender, event)

    def get_view_data(self, *args, **kwargs):
        return self.graph().graph.node[self.vertex()][args[0]]

    def store_view_data(self, **kwargs):
        """This call is executed while self is in "deaf" mode to avoid infinite loops"""
        pos = kwargs.get('position', None)
        if pos is not None:
            self.graph().set_vertex_data(self.vertex(), position=pos)

    mousePressEvent = mixin_method(Vertex, QtGui.QGraphicsEllipseItem,
                                   "mousePressEvent")
    itemChange = mixin_method(Vertex, QtGui.QGraphicsEllipseItem,
                              "itemChange")

    paint = mixin_method(QtGui.QGraphicsEllipseItem, None,
                         "paint")

class GraphicalEdge( Edge, QtGui.QGraphicsPathItem  ):
    def __init__(self, edge=None, graph=None, src=None, dest=None):
        QtGui.QGraphicsPathItem.__init__(self, None)
        Edge.__init__(self, edge, graph, src, dest)
        self.set_edge_creator(LinearEdgePath())

    store_view_data = None
    get_view_data   = None


class GraphicalFloatingEdge(QtGui.QGraphicsPathItem, FloatingEdge):
    def __init__(self, srcPoint, graph):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, None)
        FloatingEdge.__init__(self, srcPoint, graph)
        self.set_edge_creator(LinearEdgePath())

class GraphicalView( View ):
    def __init__(self, parent, graph, strategy, clone=False):
        View.__init__(self, parent, graph, strategy, clone)
        self.set_default_drop_handler(self.dropHandler)
        keyPressMapping={ (QtCore.Qt.NoModifier, QtCore.Qt.Key_Delete ):self.removeNode,}
        self.set_keypress_handler_map(keyPressMapping)

    def mouseDoubleClickEvent(self, event):
        self.dropHandler(event)

    def dropHandler(self, event):
        position = self.mapToScene(event.pos())
        position = [position.x(), position.y()]
        self.scene().new_vertex(position=position,
                                color=QtGui.QColor(rint(0,255),rint(0,255),rint(0,255)))

    def removeNode(self, event):
        scene = self.scene()
        vertices = scene.get_selected_items(filterType=GraphicalNode, subcall=lambda x:x.vertex())
        scene.remove_vertices(vertices)
        edges = scene.get_selected_items(filterType=GraphicalEdge)
        scene.remove_edges(e.edge() for e in edges)
        event.setAccepted(True)



#-------------------------
# -- the graph strategy --
#-------------------------
GraphicalGraph = GraphStrategyMaker( graphView       = GraphicalView,
                                vertexWidgetMap = {"vertex":GraphicalNode},
                                edgeWidgetMap   = {"default":GraphicalEdge,
                                                   "floating-default":GraphicalFloatingEdge},
                                adapterType     = None)


#THE APPLICATION'S MAIN WINDOW
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtGui.QMainWindow.__init__(self, parent)


        self.setMinimumSize(800,600)
        self.__graph = NXObservedGraph()
        noodles = GraphicalGraph(self.__graph)
        self.__graphView = noodles.create_view(parent=self)
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
