

"""
This file demonstrates how to create views for graphs from the
`networkx <http://networkx.lanl.gov/_>` toolkit. This toolkit
provides efficient graph structures. We want to create a Qt
widget that allows one to view/create networkx graphs and edit
them.
"""

import networkx as nx
from openalea.grapheditor.all import Observed, GraphAdapterBase

class NXObservedGraph( GraphAdapterBase, Observed ):
    """An adapter to networkx.Graph"""
    def __init__(self):
        GraphAdapterBase.__init__(self)
        Observed.__init__(self)
        self.count = 0
        self.set_graph(nx.Graph())

    def new_vertex(self, **kwargs):
        vtx = self.count#NXObservedNode(self.graph)
        self.count += 1
        self.add_vertex(vtx, **kwargs)
        return vtx

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
        edge = [src_vertex, tgt_vertex]
        edge.sort(lambda x, y: cmp(id(x), id(y)))
        edge = tuple(edge)
        print "add", edge
        if g.has_edge(*edge):
            return
        else:
            g.add_edge(*edge, **kwargs)
            self.notify_listeners(("edge_added", ("default", edge, src_vertex, tgt_vertex)))

    def remove_edge(self, src_vertex, tgt_vertex):
        edge =  [src_vertex, tgt_vertex]
        edge.sort(lambda x, y: cmp(id(x), id(y)))
        edge = tuple(edge)
        print "remove", edge
        self.graph.remove_edge(edge[0], edge[1])
        self.notify_listeners(("edge_removed", ("default",edge)))

    def remove_edges(self, edges):
        GraphAdapterBase.remove_edges(self, (e for e in edges))

    # -- not in the adapter interface (yet): --
    def set_vertex_data(self, vertex, **kwargs):
        if vertex in self.graph:
            self.graph.node[vertex].update(kwargs)
            pos = kwargs.get('position', None)
            if pos:
                self.notify_listeners(("vertex_event",
                                       (vertex,
                                        ("metadata_changed", "position", pos))))

    def set_edge_data(self, edge_proxy, **kwargs):
        #nothing right now"
        pass

#------------------------
# -- the graph qt view --
#------------------------
import sys
from openalea.vpltk.qt import QtGui, QtCore
from openalea.grapheditor.qt import (Vertex, View, mixin_method,
                                     QtGraphStrategyMaker,
                                     DefaultGraphicalEdge,
                                     DefaultGraphicalFloatingEdge,
                                     DefaultGraphicalVertex)
from random import randint as rint # for random colors



class GraphicalNode( DefaultGraphicalVertex  ):
    def initialise_from_model(self):
        self.setPos(QtCore.QPointF(*self.graph().graph.node[self.vertex()]["position"]))
        color = self.graph().graph.node[self.vertex()]["color"]
        brush = QtGui.QBrush(color)
        self.setBrush(brush)

    def store_view_data(self, **kwargs):
        pos = kwargs.get('position', None)
        if pos is not None:
            self.graph().set_vertex_data(self.vertex(), position=pos)
        return None

    def get_view_data(self, key):
        return self.graph().graph.node[self.vertex()][key]

    def store_view_data(self, **kwargs):
        """This call is executed while self is in "deaf" mode to avoid infinite loops"""



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
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtGui.QMainWindow.__init__(self, parent)

        self.setMinimumSize(800,600)
        self.__graph = NXObservedGraph()
        self.__graphView = GraphicalGraph.create_view(self.__graph, parent=self)
        for p in range(100):
            self.__graph.add_vertex(p, position=[rint(0,200), rint(0,200)],
                                   color=QtGui.QColor(rint(0,255),rint(0,255),rint(0,255)))
        for p in range(100):
            self.__graph.add_edge(rint(0,100), rint(0,100))

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
