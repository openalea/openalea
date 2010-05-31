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

from openalea.core import compositenode
from openalea.core import node
from openalea.core import system
from openalea.core.system import systemnodes
import vertex
import edge
import anno
import adapter
from openalea.grapheditor import baselisteners
from openalea.grapheditor import qtgraphview


class Strategy(object):

    @classmethod
    def get_graph_model_type(cls):
        """Returns the classobj defining the graph type"""
        return compositenode.CompositeNode

    @classmethod
    def get_vertex_widget_factory(cls):
        """Returns a factory that instantiates vertices according
        to their types."""
        return GraphicalVertexFactory

    @classmethod
    def get_vertex_widget_types(cls):
        return {"vertex":vertex.GraphicalVertex,
                "annotation":anno.GraphicalAnnotation,
                "inNode":vertex.GraphicalInVertex,
                "outNode":vertex.GraphicalOutVertex}

    @classmethod
    def get_edge_widget_factory(cls):
        """Returns a factory that instantiates edges according
        to their types."""
        return GraphicalEdgeFactory

    @classmethod
    def get_edge_widget_types(cls):
        return {"default":edge.GraphicalEdge,
                "floating-default":edge.FloatingEdge}

    @classmethod
    def get_graph_adapter_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return adapter.GraphAdapter

    @classmethod
    def get_connector_types(cls):
        return [vertex.GraphicalPort]

    @classmethod
    def initialise_graph_view(cls, graphView, graphModel):
        # -- do the base node class initialisation --
        mdict  = graphModel.get_ad_hoc_dict()

        #graphical data init.
        mdict.simulate_full_data_change(graphView, graphModel)

        #other attributes init
        for i in graphModel.input_desc:
            graphView.notify(graphModel, ("input_port_added", i))
        for i in graphModel.output_desc:
            graphView.notify(graphModel, ("output_port_added", i))
        for i in graphModel.map_index_in:
            graphView.notify(graphModel, ("input_modified", i))
        graphView.notify(graphModel, ("caption_modified", graphModel.internal_data["caption"]))
        graphView.notify(graphModel, ("tooltip_modified", graphModel.get_tip()))
        graphView.notify(graphModel, ("internal_data_changed",))

        # -- then the composite node class initialisation --
        ids = graphModel.vertices()
        for eltid in ids:
            vtype = "vertex"
            doNotify = True
            vertex = graphModel.node(eltid)
            if(vertex.__class__.__dict__.has_key("__graphitem__")): vtype = "annotation"
            elif isinstance(vertex, compositenode.CompositeNodeOutput):
                vtype = "outNode"
                doNotify = True if len(vertex.input_desc) else False
            elif isinstance(vertex, compositenode.CompositeNodeInput) :
                vtype = "inNode"
                doNotify = True if len(vertex.output_desc) else False
            else: pass
            if doNotify:
                graphView.notify(graphModel, ("vertex_added", (vtype, vertex)))

        for eid in graphModel.edges():
            (src_id, dst_id) = graphModel.source(eid), graphModel.target(eid)
            etype=None
            src_port_id = graphModel.local_id(graphModel.source_port(eid))
            dst_port_id = graphModel.local_id(graphModel.target_port(eid))

            nodeSrc = graphModel.node(src_id)
            nodeDst = graphModel.node(dst_id)
            src_port = nodeSrc.output_desc[src_port_id]
            dst_port = nodeDst.input_desc[dst_port_id]

            #don't notify if the edge is connected to the input or
            #output nodes.
            # if(src_id == graphModel.id_in or dst_id == graphModel.id_out):
                # continue

            edgedata = "default", eid, src_port, dst_port
            graphView.notify(graphModel, ("edge_added", edgedata))


def GraphicalVertexFactory(vtype, *args, **kwargs):
    VT = Strategy.get_vertex_widget_types().get(vtype)
    if(VT):
        return VT(*args, **kwargs)
    else:
        raise Exception("vtype not found")


def GraphicalEdgeFactory(etype, *args, **kwargs):
    ET = Strategy.get_edge_widget_types().get(etype)
    if(ET):
        return ET(*args, **kwargs)
    else:
        raise Exception("vtype not found")


if(__name__ != "__main__"):
    #we register this strategy
    baselisteners.GraphListenerBase.register_strategy(Strategy)
