# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
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
        self.set_graph(graph if graph else self)

    def set_graph(self, graph):
        self.graph = graph

    def new_vertex(self, vtype=None, position=None):
        """Create a new vertex at the defined position and add it to the model"""
        raise NotImplementedError

    def add_vertex(self, vertex, *args, **kwargs):
        """Add an existing vertex to the model.

        Upon succes it must emit the following event tuple:
        ("vertex_added", ("vertex_type", vertex)).
          * "vertex-type" is a vertex-type string defined in the strategy 
            used for a particular graph type.
          * "vertex" is the **observable** object representing a vertex.
        """
        raise NotImplementedError

    def get_vertex(self, vid=None):
        """Return the vertex object matching vid. By default this is just vid!"""
        return vid

    def remove_vertex(self, vertex):
        """Removes the specified vertex from the model.

        Upon success it must emit the following event tuple:
        ("vertex_removed", (vertex,)).
          * vertex is the **observable** object representing a vertex.
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
          * edge, sourceObs and targetObs are the **observable** objects
        representing an egde and its two anchors.
        """
        raise NotImplementedError

    def remove_edge(self, source, target):
        """Removes the specified vertex from the model.

        Upon success it must emit the following event tuple:
        ("edge_removed", (edge,)).
          * edge is the observable object representing an edge.
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




def GraphStrategyMaker(graphView, vertexWidgetMap, edgeWidgetMap,
                       connectorTypes=[], graphViewInitialiser=None,
                       adapterType=None):

    class __GraphStrategy(object):
        __sceneType__            = None
        __graphViewType__        = graphView
        __vertexWidgetMap__      = vertexWidgetMap
        __edgeWidgetMap__        = edgeWidgetMap
        __connectorTypes__       = connectorTypes
        __graphViewInitialiser__ = staticmethod(graphViewInitialiser \
                                                if graphViewInitialiser \
                                                else lambda x,y:x)
        __adapterType__          = adapterType

        @classmethod
        def create_view(cls, graph, observableGraph=None, parent=None,
                        clone=False, *args, **kwargs):
            """Instanciates the view"""
            view = cls.__graphViewType__(parent, *args,**kwargs)
            scene = cls.__sceneType__._make_scene(cls, graph, observableGraph, clone)
            scene.initialise_from_model()
            view.set_canvas(scene)
            return view

        @classmethod
        def create_vertex_widget(cls, vtype, *args, **kwargs):
            VertexClass = cls.__vertexWidgetMap__.get(vtype)
            if(VertexClass):
                return VertexClass(*args, **kwargs)
            else:
                raise Exception("vtype not found")

        @classmethod
        def create_edge_widget(cls, etype, *args, **kwargs):
            VertexClass = cls.__edgeWidgetMap__.get(etype)
            if(VertexClass):
                return VertexClass(*args, **kwargs)
            else:
                raise Exception("etype not found")

        @classmethod
        def get_connector_types(cls):
            return cls.__connectorTypes__

        @classmethod
        def initialise_graph_view(cls, graphView, graphModel):
            if cls.__graphViewInitialiser__ is not None:
                cls.__graphViewInitialiser__(graphView, graphModel)

    return __GraphStrategy
