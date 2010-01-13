# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
##############################################################################
"""This module provide a set of graph concepts to form a graph interface"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

class GraphError(Exception):
    """
    base class of all graph exceptions
    """

class InvalidEdge(GraphError, KeyError) :
    """
    exception raised when a wrong edge id is provided
    """

class InvalidVertex(GraphError, KeyError) :
    """
    exception raised when a wrong vertex id is provided
    """

class IGraph(object):
    """
    Directed graph definition
    """
    def source(self, eid):
        """
        retrieve the source of an edge
        
        :param eid: id of the edge
        :type eid: eid
        :rtype: vid
        """
        raise NotImplementedError
    
    def target(self, eid):
        """
        retrieve the target of an edge
        
        :param eid: id of the edge
        :type eid: eid
        :rtype: vid
        """
        raise NotImplementedError
    
    def edge(self, source, target):
        """
        find the matching edges with same source and same target
        return None if it don't succeed
        
        :Parameters:
            - `source` : id of the source vertex
            - `target` : id of the target vertex
        :Types:
            - `source` : vid
            - `target` : vid
        :rtype: eid|iter of eid|None
        """
        raise NotImplementedError
    
    def __contains__(self, vid):
        """
        test wether a vertex belong to the graph, see `has_vertex`
        
        :param vid: vertex id to test
        :type vid: vid
        :rtype: bool
        """
        raise NotImplementedError
    
    def has_vertex(self, vid):
        """
        test wether a vertex belong to the graph
        
        :param vid: vertex id to test
        :type vid: vid
        :rtype: bool
        """
        raise NotImplementedError
    
    def has_edge(self, eid):
        """
        test wether an edge belong to the graph
        
        :param eid: edge id to test
        :type eid: eid
        :rtype: bool
        """
        raise NotImplementedError
    
    def is_valid(self):
        """
        test the validity of the graph
        
        :rtype: bool
        """
        raise NotImplementedError

class IVertexListGraph(object):
    """
    interface of a graph seen as a vertex list
    """
    def vertices(self):
        """
        iterator on vertices
        
        :rtype: iter of vid
        """
        raise NotImplementedError
    
    def __iter__ (self) :
        """
        magic function for `vertices`
        
        :rtype: iter of vid
        """
        raise NotImplementedError
    
    def nb_vertices(self):
        """
        return the total number of vertices
        
        :rtype: int
        """
        raise NotImplementedError
    
    def __len__(self):
        """
        magic function for `nb_vertices`
        
        :rtype: int
        """
        raise NotImplementedError
    
    def in_neighbors(self, vid):
        """
        iterator on the neighbors of vid
        where edges are directed from neighbor to vid
        
        :param vid: id of the reference vertex
        :type vid: vid
        :rtype: iter of vid
        """
        raise NotImplementedError
    
    def out_neighbors(self, vid):
        """
        iterator on the neighbors of vid
        where edges are directed from vid to neighbor
        
        :param vid: id of the reference vertex
        :type vid: vid
        :rtype: iter of vid
        """
        raise NotImplementedError
    
    def neighbors(self, vid):
        """
        iterator on the neighbors of vid
        regardless of the orientation of the edge
        
        :param vid: id of the reference vertex
        :type vid: vid
        :rtype: iter of vid
        """
        raise NotImplementedError
    
    def nb_in_neighbors(self, vid):
        """
        number of neighbors such as edges are directed from neighbor to vid
        
        :param vid: id of the reference vertex
        :type vid: vid
        :rtype: int
        """
        raise NotImplementedError
    
    def nb_out_neighbors(self, vid):
        """
        number of neighbors such as edges are directed from vid to neighbor
        
        :param vid: id of the reference vertex
        :type vid: vid
        :rtype: int
        """
        raise NotImplementedError
    
    def nb_neighbors(self, vid):
        """
        number of neighbors regardless of the orientation of the edge
        
        :param vid: id of the reference vertex
        :type vid: vid
        :rtype: int
        """
        raise NotImplementedError

class IEdgeListGraph(object) :
    """
    Definition of a graph seen as a list of edges
    """
    def edges(self, vid= None):
        """
        retrieve the edges linked to a specified vertex,
        all if vid is None
        
        :param vid: id of the reference vertex, default=None
        :type vid: vid
        :rtype: iter of eid
        """
        raise NotImplementedError
    
    def nb_edges(self, vid= None):
        """
        number of edges linked to a specified vertex,
        total number if vid is None
        
        :param vid: id of the reference vertex, default=None
        :type vid: vid
        :rtype: iter of eid
        """
        raise NotImplementedError
    
    def in_edges(self, vid):
        """
        retrieve the edges linked to a specified vertex,
        oriented inside the vertex
        
        :param vid: id of the reference vertex, default=None
        :type vid: vid
        :rtype: iter of eid
        """
        raise NotImplementedError
    
    def out_edges(self, vid):
        """
        retrieve the edges linked to a specified vertex,
        oriented outside the vertex
        
        :param vid: id of the reference vertex, default=None
        :type vid: vid
        :rtype: iter of eid
        """
        raise NotImplementedError
    
    def nb_in_edges(self, vid):
        """
        number of edges linked to a specified vertex,
        oriented inside vertex
        
        :param vid: id of the reference vertex, default=None
        :type vid: vid
        :rtype: iter of eid
        """
        raise NotImplementedError
    
    def nb_out_edges(self, vid):
        """
        number of edges linked to a specified vertex,
        oriented outside vertex
        
        :param vid: id of the reference vertex, default=None
        :type vid: vid
        :rtype: iter of eid
        """
        raise NotImplementedError

class IMutableVertexGraph(object) :
    """
    definition of graph edition methods for vertices
    """
    def add_vertex(self, vid=None):
        """
        add a vertex to the graph, if vid is not provided create a new vid
        
        :param vid: the id of the vertex to add, default=None
        :type vid: vid
        :return: the id of the created vertex
        :rtype: vid
        """
        raise NotImplementedError
    
    def remove_vertex(self, vid):
        """
        remove a specified vertex of the graph
        remove all the edges attached to it
        
        :param vid: the id of the vertex to remove
        :type vid: vid
        """
        raise NotImplementedError
    
    def clear(self):
        """
        remove all vertices and edges
        don't change references to objects
        """
        raise NotImplementedError

class IMutableEdgeGraph(object) :
    """
    definition of graph edition methods for edges
    """
    def add_edge(self, edge=(None, None), eid= None):
        """
        add an edge to the graph, if eid is not provided create a new eid
        
        :Parameters:
            - `edge` : a tuple (vertex source,vertex target)
            - `eid` : the id of the created edge
        :Types:
            - `edge` : (vid,vid)
            - `eid` : eid
        :return: the id of the newly created edge
        :rtype: eid
        """
        raise NotImplementedError
    
    def remove_edge(self, eid):
        """
        remove a specified edge from the graph
        
        :param eid: id of the edge to remove
        :type eid: eid
        """
        raise NotImplementedError
    
    def clear_edges(self):
        """
        remove all the edges of the graph
        don't change references to objects
        """
        raise NotImplementedError

class IExtendGraph(object) :
    """
    allow the graph to be extended by another graph
    """
    
    def extend(self, graph):
        """
        add the specified graph to self, create new vid and eid
        
        :param graph: the graph to add
        :type graph: Graph
        :return: two dictionnary specifying correspondence between graph id and self id
        :rtype: ({vid:vid},{eid:eid})
        """
        raise NotImplementedError

class ICopyGraph(object) :
    """
    allow the graph to be copied
    """
    def copy(self):
        """
        make a shallow copy of the graph,
        for a deep copy use the constructor `__init__`
        """
        raise NotImplementedError

