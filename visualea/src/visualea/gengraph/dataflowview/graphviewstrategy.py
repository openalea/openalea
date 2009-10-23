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
"""Trait to create a DataFlow, similar to what currently exists in OpenAlea"""


from openalea.core import interface
from openalea.core import compositenode
from openalea.core import node
import strat_node
import strat_edge
import strat_anno
from .. import gengraphview as gengraphview


class GraphViewStrategy(object):

    @classmethod
    def get_graph_model_type(cls):
        """Returns the classobj defining the graph type"""
        return compositenode.CompositeNode

    @classmethod
    def get_direction_vector(cls):
        """Returns an (x,y) vector defining the Y direction of the tree.
        (0,-1) is upward, (0,1) is downward."""
        return (0,1)

    @classmethod
    def get_node_widget_type(cls):
        """Return a classobj defining the type of widget 
        that represents a node"""
        return strat_node.AleaQtGraphicalNode

    @classmethod
    def get_edge_widget_type(cls):
        """Return a classobj defining the type of widget 
        that represents an edge"""
        return strat_edge.AleaQtGraphicalEdge

    @classmethod
    def get_floating_edge_widget_type(cls):
        """Return a classobj defining the type of widget 
        that represents an edge"""
        return strat_edge.AleaQtFloatingEdge


    @classmethod
    def get_annotation_widget_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return strat_anno.AleaQtGraphicalAnnotation


if(__name__ != "__main__"):
    #we declare what are the model ad hoc data we require:
    nodeModelAdHocExtension = {"user_color":list, 
                               "use_user_color":bool, 
                               "position":list,
                               "text": str}
    node.Node.extend_ad_hoc_slots(nodeModelAdHocExtension)

    #we register this strategy
    gengraphview.GraphView.register_strategy(GraphViewStrategy)
