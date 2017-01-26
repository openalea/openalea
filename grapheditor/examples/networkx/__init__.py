"""
This file demonstrates how to create views for graphs from the
`networkx <http://networkx.lanl.gov/_>` toolkit. This toolkit
provides efficient graph structures. We want to create a Qt
widget that allows one to view/create networkx graphs and edit
them.
"""

import networkx as nx
from openalea.grapheditor.all import  Observed, GraphAdapterBase
import weakref

from Qt import QtGui, QtCore, QtWidgets

class NxObservedVertex(Observed):

    def __init__(self, graph, identifier):
        Observed.__init__(self)
        self.identifier = identifier
        self.g = weakref.ref(graph)

    def notify_position(self, pos):
        self.notify_listeners(("metadata_changed", "position", pos))

    def notify_update(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.notify_listeners(("metadata_changed", k, v))

        pos = self.g().node[self]["position"]
        self.notify_position(pos)

    def __setitem__(self, key, value):
        self.g().node[self][key] = value
        self.notify_update()

    def __getitem__(self, key):
        return self.g().node[self][key]

class NXObservedGraph( GraphAdapterBase, Observed ):
    """An adapter to networkx.Graph"""
    def __init__(self):
        GraphAdapterBase.__init__(self)
        Observed.__init__(self)
        self.set_graph(nx.Graph())

    def new_vertex(self, vid=None, **kwargs):
        vtx = NxObservedVertex(self.graph, vid)
        self.add_vertex(vtx, **kwargs)
        return vtx

    def add_vertex(self, vertex, **kwargs):
        if vertex in self.graph:
            return
        else:
            if "position" not in kwargs :
                kwargs["position"] = [0., 0.]
            else:
                kwargs["position"] = map(float, kwargs["position"])
            if "color" not in kwargs :
                kwargs["color"] = QtGui.QColor(0, 0, 0)

            self.graph.add_node(vertex, **kwargs)
            self.notify_listeners(("vertex_added", ("vertex", vertex)))

    def remove_vertex(self, vertex):
        edges = self.graph.edges([vertex])
        for src, tgt in edges:
            self.remove_edge(src, tgt)
        self.graph.remove_node(vertex)
        self.notify_listeners(("vertex_removed", ("vertex",vertex)))

    def add_edge(self, src_vertex, tgt_vertex, **kwargs):
        edge = [src_vertex, tgt_vertex]
        edge.sort(lambda x, y: cmp(id(x), id(y)))
        edge = tuple(edge)
        if self.graph.has_edge(*edge):
            return
        else:
            self.graph.add_edge(*edge, **kwargs)
            self.notify_listeners(("edge_added", ("default", edge, src_vertex, tgt_vertex)))

    def remove_edge(self, src_vertex, tgt_vertex):
        edge =  [src_vertex, tgt_vertex]
        edge.sort(lambda x, y: cmp(id(x), id(y)))
        edge = tuple(edge)
        self.graph.remove_edge(edge[0], edge[1])
        self.notify_listeners(("edge_removed", ("default",edge)))

    def remove_edges(self, edges):
        GraphAdapterBase.remove_edges(self, (e for e in edges))

    # -- not in the adapter interface (yet): --
    def set_vertex_data(self, vertex, **kwargs):
        if vertex in self.graph:
            for k, v in kwargs.iteritems():
                self.graph.node[vertex][k]=v

    def set_edge_data(self, edge_proxy, **kwargs):
        #nothing right now"
        pass

#------------------------
# -- the graph qt view --
#------------------------
from openalea.grapheditor.qt import (Vertex, View, mixin_method,
                                     QtGraphStrategyMaker,
                                     DefaultGraphicalEdge,
                                     DefaultGraphicalFloatingEdge,
                                     DefaultGraphicalVertex)
from random import randint as rint # for random colors

class GraphicalNode( DefaultGraphicalVertex ):
    def initialise_from_model(self):
        self.setPos(QtCore.QPointF(*self.graph().graph.node[self.vertex()]["position"]))
        color = self.graph().graph.node[self.vertex()]["color"]
        brush = QtGui.QBrush(color)
        self.setBrush(brush)

    def store_view_data(self, **kwargs):
        self.graph().set_vertex_data(self.vertex(), **kwargs)

    def get_view_data(self, key):
        return self.graph().graph.node[self.vertex()][key]

class GraphicalView( View ):
    def __init__(self, parent):
        View.__init__(self, parent)
        self.set_default_drop_handler(self.dropHandler)
        keyPressMapping={ (QtCore.Qt.NoModifier, QtCore.Qt.Key_Delete ):self.removeElement,}
        self.set_keypress_handler_map(keyPressMapping)

    def mouseDoubleClickEvent(self, event):
        self.dropHandler(event)

    def dropHandler(self, event):
        position = self.mapToScene(event.pos())
        position = [position.x(), position.y()]
        self.scene().new_vertex(position=position,
                                color=QtGui.QColor(rint(0,255),rint(0,255),rint(0,255)))

    def removeElement(self, event):
        scene = self.scene()
        edges = scene.get_selected_items(filterType=DefaultGraphicalEdge)
        scene.remove_edges(e.edge() for e in edges)
        vertices = scene.get_selected_items(filterType=GraphicalNode, subcall=lambda x:x.vertex())
        scene.remove_vertices(vertices)
        event.setAccepted(True)


#-------------------------
# -- the graph strategy --
#-------------------------
GraphicalGraph = QtGraphStrategyMaker( graphView       = GraphicalView,
                                       vertexWidgetMap = {"vertex":GraphicalNode},
                                       edgeWidgetMap   = {"default":DefaultGraphicalEdge,
                                                          "floating-default":DefaultGraphicalFloatingEdge} )

#THE APPLICATION'S MAIN WINDOW
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtWidgets.QMainWindow.__init__(self, parent)

        self.setMinimumSize(800,600)

        self.graph = NXObservedGraph()
        self.graphView = GraphicalGraph.create_view(self.graph, parent=self)
        nodes = []
        nmax = 100
        emax = 100
        for p in range(nmax):
            node = self.graph.new_vertex(p, position=[rint(0,200), rint(0,200)],
                                   color=QtGui.QColor(rint(0,255),rint(0,255),rint(0,255)))
            nodes.append(node)
        for p in range(emax):
            self.graph.add_edge(nodes[rint(0,nmax-1)], nodes[rint(0,nmax-1)])

        self.setCentralWidget(self.graphView)


if __name__=="__main__":

    instance = QtWidgets.QApplication.instance()
    if instance is None :
        app = QtWidgets.QApplication([])
    else :
        app = instance

    win = MainWindow()
    win.show()


    graph = win.graph
    nxgraph = graph.graph
    view = win.graphView

    if instance is None :
        app.exec_()
