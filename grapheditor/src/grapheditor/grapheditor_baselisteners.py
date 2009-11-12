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

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import types
import weakref

from openalea.core import observer

import grapheditor_interfaces



class StrategyError( Exception ):
    def __init__(self, msg):
        Exception.__init__(self)
        self._msg = msg
        return

    def get_message(self):
        return self._msg



class GraphElementObserverBase(observer.AbstractListener):
    """Base class for elements in a GraphView"""
    
    def __init__(self, observed=None, graph=None):
        observer.AbstractListener.__init__(self)
        self.set_observed(observed)
        self.set_graph(graph)
        return

    def set_observed(self, observed):
        if(observed and isinstance(observed, observer.Observed)):
            self.initialise(observed)
            self.observed = weakref.ref(observed, self.clear_observed)
        else:
            self.observed = observed

    def set_graph(self, graph):
        self.__graph = weakref.ref(graph)

    def graph(self):
        return self.__graph()

    def notify(self, sender, event):
        """called by the observed when something happens
        to it."""
        if(event[0] == "MetaDataChanged"):
            if(event[1]=="position"):
                if(event[2]): 
                    self.position_changed(*event[2])

    def clear_observed(self, observed):
        if observed == self.observed() : self.observed = None
        return

    def initialise_from_model(self):
        self.observed().get_ad_hoc_dict().simulate_full_data_change()



import traceback

class GraphListenerBase(observer.AbstractListener):
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
        assert grapheditor_interfaces.IGraphViewStrategies.check(stratCls)
        assert grapheditor_interfaces.IGraphViewVertex.check(stratCls.get_vertex_widget_type())
        assert grapheditor_interfaces.IGraphViewEdge.check(stratCls.get_edge_widget_type())
        assert grapheditor_interfaces.IGraphViewFloatingEdge.check(stratCls.get_floating_edge_widget_type())
        assert grapheditor_interfaces.IGraphViewAnnotation.check(stratCls.get_annotation_widget_type())
        assert grapheditor_interfaces.IGraphAdapter.check(stratCls.get_graph_adapter_type())

        graphCls = stratCls.get_graph_model_type()
        assert type(graphCls) == types.TypeType
        
        cls.__available_strategies__[graphCls]=stratCls
        return        


    def __init__(self, graph):
        observer.AbstractListener.__init__(self)

        self.initialise(graph) #start listening. Todo: rename this method in
        #the abstract listener class. and make it hold a reference to the observed

        #mappings from models to widgets
        self.vertexmap = {}
        self.edgemap = {}
        self.annomap = {}

        #types
        self._vertexWidgetType = None
        self._edgeWidgetType = None
        self._floatingEdgeWidgetType = None
        self._annoWidgetType = None
        self._adapterType = None

        #an edge currently being drawn, low-level detail.
        self.__newEdge = None

        stratCls = self.__available_strategies__.get(graph.__class__,None)
        if(not stratCls): raise StrategyError("Could not find matching strategy")

        self.set_vertex_widget_type(stratCls.get_vertex_widget_type())
        self.set_edge_widget_type(stratCls.get_edge_widget_type())
        self.set_floating_edge_widget_type(stratCls.get_floating_edge_widget_type())
        self.set_annotation_widget_type(stratCls.get_annotation_widget_type())
        self.set_graph_adapter_type(stratCls.get_graph_adapter_type())
        self.set_direction_vector(stratCls.get_direction_vector())
        self.set_graph(graph)
        self.connector_types=stratCls.get_connector_types()
        self.currentItem = None

    def graph(self):
        if(isinstance(self.observed, weakref.ref)):
            return self.observed()
        else:
            return self.observed

    def set_graph(self, graph):
        self.clear_scene()
        if(self._adapterType):
            ga = self._adapterType(graph)
            self.observed = ga
        else:
            self.observed = weakref.ref(graph) #might not need to be weak.

    def get_scene(self):
        raise NotImplementedError

    #############################################################
    # Observer methods come next. They DO NOT modify the model. #
    #############################################################
    
    def notify(self, sender, data):
        if(data[0]=="vertexAdded") : self.vertex_added(data[1])
        elif(data[0]=="edgeAdded") : self.edge_added(*data[1]) 
        elif(data[0]=="annotationAdded") : self.annotation_added(data[1])
        elif(data[0]=="vertexRemoved") : self.vertex_removed(data[1])
        elif(data[0]=="edgeRemoved") : self.edge_removed(data[1]) 
        elif(data[0]=="annotationRemoved") : self.annotation_removed(data[1])

    def element_added(self, element):
        self.post_addition(element)
        return element

    def vertex_added(self, vertexModel):
        vertexWidget = self._vertexWidgetType(vertexModel, self.graph())
        vertexWidget.add_to_view(self.get_scene())
        self.vertexmap[vertexModel] = weakref.ref(vertexWidget)
        return self.element_added(vertexWidget)

    def edge_added(self, edgeModel, srcPort, dstPort):
        edgeWidget = self._edgeWidgetType(edgeModel, self.graph(), srcPort, dstPort)
        edgeWidget.add_to_view(self.get_scene())
        self.edgemap[edgeModel] = weakref.ref(edgeWidget)
        return self.element_added(edgeWidget)

    def annotation_added(self, annotation):
        annoWidget = self._annoWidgetType(annotation, self.graph())
        annoWidget.add_to_view(self.get_scene())
        self.annomap[annotation] = weakref.ref(annoWidget)
        return self.element_added(annoWidget)

    def vertex_removed(self, vertexModel):
        vertexWidget = self.vertexmap[vertexModel]
        vertexWidget().remove_from_view(self.get_scene())
        del self.vertexmap[vertexModel]
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

    ###########################################################
    # Controller methods come next. They DO MODIFY the model. #
    ###########################################################
    #---Low-Level Edge Interaction---
    def is_creating_edge(self):
        return True if self.__newEdge else False
    
    def new_edge_start(self, srcPt):
        self.__newEdge = self._floatingEdgeWidgetType(srcPt, self.graph())
        self.new_edge_scene_init(self.__newEdge)

    def new_edge_set_destination(self, *dest):
        if self.currentItem:
            self.currentItem.set_highlighted(False)
        if(self.__newEdge):
            self.currentItem = self.find_closest_connectable(dest)
            if self.currentItem:
                self.currentItem.set_highlighted(True)
                dest = self.currentItem.get_center()
            self.__newEdge.update_line_destination(*dest)

    def new_edge_end(self):
        if(self.__newEdge):
            try:
                self.__newEdge.consolidate(self.graph())
            except Exception, e :
                pass
            finally:
                self.new_edge_scene_cleanup(self.__newEdge)
        self.__newEdge = None
            

    #########################
    # Other utility methods #
    #########################

    def set_vertex_widget_type(self, _type):
        self._vertexWidgetType = _type

    def set_edge_widget_type(self, _type):
        self._edgeWidgetType = _type

    def set_floating_edge_widget_type(self, _type):
        self._floatingEdgeWidgetType = _type

    def set_annotation_widget_type(self, _type):
        self._annoWidgetType = _type

    def set_graph_adapter_type(self, _type):
        self._adapterType = _type

    def set_direction_vector(self, vector):
        """precompute the cosines matrix from
        a vector giving the Y direction. The matrix 
        will be used to place graph verticess on the screen."""
        assert type(vector) == types.TupleType
    
