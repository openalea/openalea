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
import vertex
import edge
import anno
import adapter
from .. import baselisteners
from .. import qtgraphview


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
                "annotation":anno.GraphicalAnnotation}

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

print "ha"

if(__name__ != "__main__"):
    #we declare what are the node model ad hoc data we require:
    vertexModelAdHocExtension = {"user_color":list, 
                                 "use_user_color":bool, 
                                 "position":list,
                                 "text": str,
                                 "connectorPosition":list}
    node.Node.extend_ad_hoc_slots(vertexModelAdHocExtension)

    #we declare what are the node model ad hoc data we require:
    portModelAdHocExtension = {"hide":bool,
                               "connectorPosition": list}
    node.AbstractPort.extend_ad_hoc_slots(portModelAdHocExtension)

    
    #we register this strategy
    baselisteners.GraphListenerBase.register_strategy(Strategy)
