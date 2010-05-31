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


class GraphAdapterBase(object):
    """Base class for adapter to graph"""
    def __init__(self, graph=None):
        if graph:
            self.set_graph(graph)

    def set_graph(self, graph):
        self.graph = graph

    def new_vertex(self, position=None):
        """Create a new vertex at the defined position and add it to the model"""
        raise NotImplementedError

    def add_vertex(self, vertex, *args, **kwargs):
        """Add an existing vertex to the model.

        Upon succes it must emit the following event tuple:
        ("vertex_added", ("vertex_type", vertex)).
        * "vertex-type" is a vertex-type string defined in the strategy
        used for a particular graph type.
        * vertex is the observable object representing a vertex.
        """
        raise NotImplementedError

    def get_vertex(self, vid=None):
        """Return the vertex object matching vid. By default this is just vid!"""
        return vid

    def remove_vertex(self, vertex):
        """Removes the specified vertex from the model.

        Upon success it must emit the following event tuple:
        ("vertex_removed", (vertex,)).
        *vertex if the observable object representing a vertex.
        """
        raise NotImplementedError

    def remove_vertices(self, vertexList):
        """Removes a list of vertices by forwarding
        them to self.remove_vertex"""
        for vertex in vertexList:
            self.remove_vertex(vertex)

    def add_edge(self, source, target, *args, **kwargs):
        """Create an edge in the model between source and target.

        Upon succes it must emit the following event tuple:
        ("edge_added", ("edge_type", edge, sourceObs, targetObs)).
        * "edge-type" is a edge-type string defined in the strategy
        used for a particular graph type.
        * edge, sourceObs and targetObs are the observable objects
        representing an egde and its two anchors.
        """
        raise NotImplementedError

    def remove_edge(self, source, target):
        """Removes the specified vertex from the model.

        Upon success it must emit the following event tuple:
        ("edge_removed", (edge,)).
        *edge if the observable object representing a edge.
        """
        raise NotImplementedError

    def remove_edges(self, edgeList):
        """Removes a list of vertices by forwarding
        them to self.remove_vertex"""
        for edge in edgeList:
            self.remove_edge(*edge)

    # -- Utility methods, not always useful/relevant.
    def replace_vertex(self, oldVertex, newVertex):
        return

    def get_vertex_inputs(self, graphicalV):
        return

    def get_vertex_outputs(self, graphicalV):
        return

    def get_vertex_input(self, graphicalV, pid):
        return

    def get_vertex_output(self, graphicalV, pid):
        return

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
        """Used by the GraphListenerBase class to
        check if the types declared here are really
        implemented in the strategy"""
        return ["vertex"]

    @classmethod
    def get_edge_types(cls):
        """Used by the GraphListenerBase class to
        check if the types declared here are really
        implemented in the strategy"""
        return ["default"]
