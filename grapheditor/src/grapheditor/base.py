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

import types
from openalea.grapheditor import interfaces


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






class GraphStrategy(object):
    def __init__(self, graphModelType, vertexWidgetMap, edgeWidgetMap, connectorTypes=[], adapterType=None, graphViewInitialiser=None):

        assert interfaces.IGraphViewStrategies.check(self)
        self.__graphModelType = graphModelType
        self.__vertexWidgetMap = vertexWidgetMap
        self.__edgeWidgetMap = edgeWidgetMap
        self.__adapterType = adapterType
        self.__connectorTypes = connectorTypes
        self.__graphViewInitialiser = graphViewInitialiser

        graphadapter = self.get_graph_or_adapter_type()
        vertexWidgetTypes  = self.get_vertex_widget_types()
        edgeWidgetTypes  = self.get_edge_widget_types()

        graphCls = self.get_graph_model_type()
        assert type(graphCls) == types.TypeType

        if graphadapter is None:
            graphadapter = graphCls

        assert interfaces.IGraphAdapter.check(graphadapter)

        #checking vertex types
        elTypes = graphadapter.get_vertex_types()
        for vt in elTypes:
            vtype = vertexWidgetTypes.get(vt, None)
            assert interfaces.IGraphViewVertex.check(vtype)

        #checking connectable types
        elTypes = self.get_connector_types()
        for ct in elTypes:
            assert interfaces.IGraphViewConnectable.check(ct)

        #checking edge types
        elTypes = graphadapter.get_edge_types()
        for et in elTypes:
            etype = edgeWidgetTypes.get(et, None)
            assert interfaces.IGraphViewEdge.check(etype)

        #checking floating edge types
        elTypes = edgeWidgetTypes.keys()
        elTypes = [i for i in elTypes if i.startswith("floating")]
        for et in elTypes:
            assert interfaces.IGraphViewFloatingEdge.check(edgeWidgetTypes[et])

    def get_graph_model_type(self):
        """Returns the classobj defining the graph type"""
        return self.__graphModelType

    def create_vertex_widget(self, vtype, *args, **kwargs):
        VertexClass = self.get_vertex_widget_types().get(vtype)
        if(VertexClass):
            return VertexClass(*args, **kwargs)
        else:
            raise Exception("vtype not found")

    def create_edge_widget(self, etype, *args, **kwargs):
        VertexClass = self.get_edge_widget_types().get(etype)
        if(VertexClass):
            return VertexClass(*args, **kwargs)
        else:
            raise Exception("etype not found")

    def get_vertex_widget_types(self):
        return self.__vertexWidgetMap

    def get_edge_widget_types(self):
        return self.__edgeWidgetMap

    def has_adapter(self):
        return self.__adapterType is not None

    def adapt_graph(self, graph):
        return self.__adapterType(graph) if self.has_adapter() else graph

    def get_graph_or_adapter_type(self):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return self.__adapterType if self.has_adapter() else self.__graphModelType

    def get_connector_types(self):
        return self.__connectorTypes

    def initialise_graph_view(self, graphView, graphModel):
        if self.__graphViewInitialiser is not None:
            self.__graphViewInitialiser(graphView, graphModel)
