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
"""Generic Graph Widget"""


__all__=["GraphView", "GraphViewMetaData"]

import types
import weakref

from openalea.core import observer
from openalea.visualea import node_widget

import gengraphview_interfaces



class StrategyError( Exception ):
    def __init__(self, msg):
        Exception.__init__(self)
        self._msg = msg
        return

    def get_message(self):
        return self._msg



class GraphViewElement(observer.AbstractListener):
    """Base class for elements in a GraphView"""
    
    def __init__(self, observed=None):
        observer.AbstractListener.__init__(self)
        if(observed and isinstance(observed, observer.Observed)):
            self.initialise(observed)
            self.observed = weakref.ref(observed, self.clear_observed)
        else:
            self.observed = None
        return

    def clear_observed(self, observed):
        """called when the observed dies."""
        if observed == self.observed() : self.observed = None
        return

    def add_to_view(self, view):
        """insert the graphical element into a scene"""
        raise NotImplementedError

    def remove_from_view(self, view):
        """remove the graphical element from a scene"""
        raise NotImplementedError

    def position_changed(self):
        """called when the position of an item changes
        in the model"""
        raise NotImplementedError

    def initialise_from_model(self):
        self.observed().get_ad_hoc_dict().simulate_full_data_change()





class GraphView(node_widget.SignalSlotListener):
    """This widget strictly watches the given graph.
    It deduces the correct representation out
    of a known list of representations.
    
    It is MVC oriented with both views and controllers
    represented by distinct methods.
    """

    __available_strategies__ = {}
    
    @classmethod
    def register_strategy(cls, stratCls):
        assert isinstance(stratCls, types.TypeType)
        assert gengraphview_interfaces.IGraphViewStrategies.check(stratCls)
        assert gengraphview_interfaces.IGraphViewNode.check(stratCls.get_node_widget_type())
        assert gengraphview_interfaces.IGraphViewEdge.check(stratCls.get_edge_widget_type())
        assert gengraphview_interfaces.IGraphFloatingViewEdge.check(stratCls.get_floating_edge_widget_type())
        assert gengraphview_interfaces.IGraphViewAnnotation.check(stratCls.get_annotation_widget_type())

        graphCls = stratCls.get_graph_model_type()
        assert type(graphCls) == types.TypeType
        
        GraphView.__available_strategies__[graphCls]=stratCls
        return        


    def __init__(self, graph):
        node_widget.SignalSlotListener.__init__(self)

        self.initialise(graph) #start listening. Todo: rename this method in
        #the abstract listener class. and make it hold a reference to the observed
        self.observed = weakref.ref(graph)

        #mappings from models to widgets
        self.nodemap = {}
        self.edgemap = {}
        self.annomap = {}

        self._type = None
        self._cosineMatrix = None

        stratCls = GraphView.__available_strategies__.get(graph.__class__,None)
        if(not stratCls): raise StrategyError("Could not find matching strategy")

        self.set_node_widget_type(stratCls.get_node_widget_type())
        self.set_edge_widget_type(stratCls.get_edge_widget_type())
        self.set_floating_edge_widget_type(stratCls.get_floating_edge_widget_type())
        self.set_annotation_widget_type(stratCls.get_annotation_widget_type())
        self.set_direction_vector(stratCls.get_direction_vector())

        #an edge currently being drawn, low-level detail.
        self.__newEdge = None


    def get_scene(self):
        raise NotImplementedError

    #############################################################
    # Observer methods come next. They DO NOT modify the model. #
    #############################################################
    
    def notify(self, sender, data):
        if(data[0]=="nodeAdded") : self.node_added(data[1])
        elif(data[0]=="edgeAdded") : self.edge_added(*data[1]) 
        elif(data[0]=="annotationAdded") : self.annotation_added(data[1])
        elif(data[0]=="nodeRemoved") : self.node_removed(data[1])
        elif(data[0]=="edgeRemoved") : self.edge_removed(data[1]) 
        elif(data[0]=="annotationRemoved") : self.annotation_removed(data[1])

    def node_added(self, nodeModel):
        nodeWidget = self._nodeWidgetType(nodeModel)
        nodeWidget.add_to_view(self.get_scene())
        self.nodemap[nodeModel] = weakref.ref(nodeWidget)
        return

    def edge_added(self, edgeModel, srcPort, dstPort):
        edgeWidget = self._edgeWidgetType(edgeModel, srcPort, dstPort)
        edgeWidget.add_to_view(self.get_scene())
        self.edgemap[edgeModel] = weakref.ref(edgeWidget)
        return

    def annotation_added(self, annotation):
        annoWidget = self._annoWidgetType(annotation)
        annoWidget.add_to_view(self.get_scene())
        self.annomap[annotation] = weakref.ref(annoWidget)
        return

    def node_removed(self, nodeModel):
        nodeWidget = self.nodemap[nodeModel]
        nodeWidget().remove_from_view(self.get_scene())
        del self.nodemap[nodeModel]
        return

    def edge_removed(self, edgeModel):
        edgeWidget = self.edgemap[edgeModel]
        edgeWidget().remove_from_view(self.get_scene())
        del self.edgemap[edgeModel]
        return

    def annotation_removed(self, annotation):
        annoWidget = self.annomap[annotation]
        annoWidget().remove_from_view(self.get_scene())
        del self.annomap[annotation]
        return

    ###############################################################
    # Controller methods come next. They DO NOT modify the model. #
    ###############################################################
    def add_node(self, node, position=None):
        self.observed().add_node(node)
        if(position):
            node.get_ad_hoc_dict().set_metadata("position", position)

    def remove_nodes(self, nodes):
        for node in nodes:
            self.observed().remove_node(node)

    #---Low-Level Edge Interaction---
    def is_creating_edge(self):
        return True if self.__newEdge else False
    
    def new_edge_start(self, srcPt):
        self.__newEdge = self._floatingEdgeWidgetType(srcPt)
        self.new_edge_scene_init(self.__newEdge)
    
    def new_edge_scene_init(self, edge):
        raise NotImplementedError

    def new_edge_set_destination(self, *dest):
        if(self.__newEdge):
            self.__newEdge.update_line_destination(*dest)

    def new_edge_end(self):
        if(self.__newEdge):
            try:
                self.__newEdge.consolidate(self.observed())
            except Exception, e :
                pass
            finally:
                self.new_edge_scene_cleanup(self.__newEdge)
        self.__newEdge = None

    def new_edge_scene_cleanup(self, edge):
        raise NotImplementedError
            

    #########################
    # Other utility methods #
    #########################

    def set_node_widget_type(self, _type):
        self._nodeWidgetType = _type

    def set_edge_widget_type(self, _type):
        self._edgeWidgetType = _type

    def set_floating_edge_widget_type(self, _type):
        self._floatingEdgeWidgetType = _type

    def set_annotation_widget_type(self, _type):
        self._annoWidgetType = _type

    def set_direction_vector(self, vector):
        """precompute the cosines matrix from
        a vector giving the Y direction. The matrix 
        will be used to place graph nodes on the screen."""
        assert type(vector) == types.TupleType
