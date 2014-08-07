"""A graph Interface."""


# errors definition
class GraphError(Exception):
    """todo"""
    pass

class InvalidVertex(GraphError, KeyError):
    """todo"""
    pass

class InvalidEdge(GraphError, KeyError):
    """todo"""
    pass

class InvalidGraph(GraphError):
    """todo"""
    pass

class InexistingVertex(GraphError):
    """todo"""
    pass

class GraphConcept(object): 
    """
    Graph concept or graph interface.
    To separate algo and data structures.
    """
    def source(self, edge_id):
        """Return the source vertex of the edge.
    
        :Parameters:
         - `edge_id`: The edge identifier.

        :Types:
         - `edge_id`: id

        :Return: vertex identifier
        """
        raise NotImplementedError


    def target(self, edge_id):
        """Return the target vertex of the edge.

        :Parameters:
         - `edge_id`: The edge identifier.

        :Return: vertex identifier
        """
        raise NotImplementedError


    def edge(self, source, target):
        """Return the edge identifier or an iterator if the graph is a  
        multiplegraph.
        
        :Parameters:
         - `source`: vtx_id 
         - `target`: vtx_id

        :Return: iter of edge_id
        """
        raise NotImplementedError


    def __contains__(self, vtx_id): 
        return self.has_vertex(vtx_id)


    def has_vertex(self, vtx_id):
        """
        Test the existence of a vertex in the graph.

        :Parameters:
         - `vtx_id`: The vertex identifier.

        :Return: bool
        """
        raise NotImplementedError


    def has_edge(self, edge_id):
        """
        Test the existence of an edge in the graph.

        :Parameters:
         - `edge_id`: The edge identifier.

        :Return: bool
        """
        raise NotImplementedError


    def is_valid(self):
        """
        Is the graph valid?

        :Return: bool
        """
        raise NotImplementedError


class VertexListGraphConcept(GraphConcept):
    """
    Vertex List Graph Concept.
    """

    def __len__(self):
        return self.nb_vertices()

    def nb_vertices(self):
        """
        Return the number of vertices.

        :Return: int
        """
        raise NotImplementedError

    def vertices(self):
        """
        :Return: iter of vertex_id
        """
        raise NotImplementedError

    def nb_in_neighbors(self, vtx_id):
        """
        :Return: int
        """
        raise NotImplementedError

    def in_neighbors(self, vtx_id):
        """
        :Return: iter of vertex_id
        """
        raise NotImplementedError

    def nb_out_neighbors(self, vtx_id): 
        """
        :Return: int
        """
        raise NotImplementedError

    def out_neighbors(self, vtx_id): 
        """
        :Return: iter of vertex_id
        """
        raise NotImplementedError

    def nb_neighbors(self, vtx_id): 
        """
        :Return: int
        """
        raise NotImplementedError

    def neighbors(self, vtx_id): 
        """
        :Return: iter of vertex_id
        """
        raise NotImplementedError


class EdgeListGraphConcept(GraphConcept):
    """
    Edge List Graph Concept
    """

    def nb_edges(self, vid= None):
        """
        :Return: int
        """
        raise NotImplementedError

    def edges(self, vtx_id= None):
        """
        Return an iterator of edge identifier.
        If `vtx_id` is specified, return input and output edges of `vtx_id`

        :Parameters:
         - `vtx_id` 
        :Return: iter of edge id
        """
        raise NotImplementedError  


    def nb_in_edges(self, vtx_id):
        """
        :Return: int
        """
        raise NotImplementedError

    def in_edges(self, vtx_id):
        """
        Return input edges of `vtx_id`

        :Parameters:
         - `vtx_id` 

        :Return: iter of edges
        """
        raise NotImplementedError

    def nb_out_edges(self, vtx_id):
        """
        :Return: int
        """
        raise NotImplementedError

    def out_edges(self, vtx_id):
        """
        Return output edges of `vtx_id`

        :Parameters:
         - `vtx_id` 

        :Return: iter of edges
        """
        raise NotImplementedError


class MutableVertexGraphConcept(VertexListGraphConcept):
    """
    Mutable Vertex Graph Concept
    """

    def vertex_id(self):
        """
        Return a free vertex identifier

        :returns: vtx_id
        """
        raise NotImplementedError


    def add_vertex(self, vtx_id= None): 
        """
        Add a vertex to the graph.

        :param vtx_id: optional vertex identifier
        """
        raise NotImplementedError

    def remove_vertex(self, vtx_id): 
        """
        Remove vertex from the graph

        :param vtx_id: todo
        """
        raise NotImplementedError

    def clear(self): 
        """
        Clear vertices and edges of the graph.
        """
        raise NotImplementedError


class MutableEdgeGraphConcept(EdgeListGraphConcept):
    """
    Mutable Edge Graph Concept.
    """

    def edge_id(self):
        """
        Return a free edge identifier

        :Return: edge_id
        """
        raise NotImplementedError

    def add_edge(self, edge, edge_id= None, create_vertex= False): 
        """
        Add an edge to the graph.

        :Parameters:
         - `edge`: (vertex id, vertex id)
         - `edge_id`: optional edge identifier
         - `create_vertex`: optional flag for automatic vertices creation
         """
        raise NotImplementedError

    def remove_edge(self, edge_id): 
        """
        Remove `edge_id` from the graph
   
        :Parameters:
         - `edge_id` : edge identifier
        """
        raise NotImplementedError

    def clear_edges(self): 
        """
        Remove all edges.
        """
        raise NotImplementedError


class CopyConcept:
    """
    Copy Concept.
    """
    def copy(self): 
        """
        Make a shallow copy
        """
        raise NotImplementedError


class ExtendConcept:
    """
    Extend the actul data structure with an other.
    """
    def extend(self, graph):
        """
        Extend the actual graph with `graph`
        PB: shift vertex id & edge id?

        :Parameters:
         - `graph` : a valid graph
        """
        raise NotImplementedError
