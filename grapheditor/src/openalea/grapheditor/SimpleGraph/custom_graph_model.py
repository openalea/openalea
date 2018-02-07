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

from openalea.core.observer import Observed, AbstractListener
from openalea.core.metadatadict import MetaDataDict, HasAdHoc
import weakref

class Graph(Observed):
    """An adapter to openalea.core.compositenode"""
    def __init__(self):
        Observed.__init__(self)
        self.__vidCounter = 0
        self.__eidCounter = 0
        self.__vertices   = {}
        self.__edges      = {}

    def simulate_construction_notifications(self):
        for v in self.__vertices.values():
            self.notify_listeners( ("vertex_added", ("vertex", v)) )
        for e in self.__edges.values():
            self.notify_listeners( ("edge_added", ("default", v)) )

    #todo : add this to the graph_adapter interface?
    def new_vertex(self, position=None):
        v = Vertex()
        self.add_vertex(v, position)

    def add_vertex(self, vertex, position=None):
        if vertex is None:
            return

        self.__vertices[self.__vidCounter] = vertex
        vertex.set_id(self.__vidCounter)
        self.__vidCounter += 1
        self.notify_listeners( ("vertex_added", ("vertex", vertex)) )
        if(position is None):
            position = [0.0,0.0]
        vertex.get_ad_hoc_dict().set_metadata("position", position)
        
    def get_vertex(self, vid):
        return self.__vertices.get(vid)

    def remove_vertex(self, vertex):
        del self.__vertices[vertex.get_id()]
        for con in vertex.get_connections():
            self.remove_edge(con().src(), con().dst())
        self.notify_listeners( ("vertex_removed", ("vertex", vertex)) )

    def remove_vertices(self, vertexList):
        for vert in vertexList:
            self.remove_vertex(vert)

    def get_vertex_inputs(self, vertex):
        return vertex

    def get_vertex_outputs(self, vertex):
        return vertex

    def get_vertex_input(self, vertex):
        return vertex

    def get_vertex_output(self, vertex):
        return vertex

    #todo : add this to the graph_adapter interface?
    def new_edge(src, dst):
        edge = Edge(src, dst)
        self.add_edge(src, dst, edge)
        
    def add_edge(self, src, dst, edge=None):
        if src is None or dst is None:
            return None
        
        if (src, dst) in self.__edges:
            return
        
        if edge is None:
            edge = Edge(src, dst)
        
        self.__edges[(src,dst)] = edge
        src.add_connection(edge)
        dst.add_connection(edge)
        edge.set_id(self.__eidCounter)
        self.__eidCounter += 1
        self.notify_listeners( ("edge_added", ("default", edge, src, dst)) )

    def remove_edge(self, src, dst):
        edge = self.__edges.get((src, dst))
        if edge is None:
            return

        del self.__edges[(src,dst)]
        self.notify_listeners( ("edge_removed", ("default", edge)) )

    #type checking
    def is_input(self, input):
        return isinstance(input, Vertex)

    def is_output(self, output):
        return isinstance(output, Vertex)

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



class Vertex(Observed, HasAdHoc):
    def __init__(self):
        Observed.__init__(self)
        HasAdHoc.__init__(self)
        self.__connections = set()
        self.__id = 0

    def add_connection(self, edge):
        self.__connections.add( weakref.ref(edge, self.discard_connection) )

    def discard_connection(self, edgeref):
        self.__connections.discard(edgeref)

    def get_connections(self):
        return self.__connections
        
    def set_id(self, _id):
        self.__id = _id

    def get_id(self):
        return self.__id

Vertex.extend_ad_hoc_slots("position", list, [0,0])

class Edge(Observed, HasAdHoc):
    def __init__(self, src, dst):
        Observed.__init__(self)
        HasAdHoc.__init__(self)
        self.__id = 0
        self.src = weakref.ref(src)
        self.dst = weakref.ref(dst)

    def get_ad_hoc_dict(self):
        return self.__metadata_dict

    def set_id(self, _id):
        self.__id = _id

    def get_id(self):
        return self.__id

