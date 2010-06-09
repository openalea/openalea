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
import openalea.grapheditor.base as grapheditorbase


def initialise_graph_view_from_model(graphView, graphModel):
    # -- do the base node class initialisation --
    mdict  = graphModel.get_ad_hoc_dict()

    #graphical data init.
    mdict.simulate_full_data_change(graphView, graphModel)

    #other attributes init (composite node is subclass of node)
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

        edgedata = "default", eid, src_port, dst_port
        graphView.notify(graphModel, ("edge_added", edgedata))


Strategy = grapheditorbase.GraphStrategy( graphModelType       = compositenode.CompositeNode,
                                          vertexWidgetMap      = {"vertex":vertex.GraphicalVertex,
                                                                  "annotation":anno.GraphicalAnnotation,
                                                                  "inNode":vertex.GraphicalInVertex,
                                                                  "outNode":vertex.GraphicalOutVertex},
                                          edgeWidgetMap        = {"default":edge.GraphicalEdge,
                                                                  "floating-default":edge.FloatingEdge},
                                          connectorTypes       = [], #[vertex.GraphicalPort] not necessary if we derive from qtgraphview.Connector
                                          adapterType          = adapter.GraphAdapter,
                                          graphViewInitialiser = initialise_graph_view_from_model )

if(__name__ != "__main__"):
    #we register this strategy
    baselisteners.GraphListenerBase.register_strategy(Strategy)
