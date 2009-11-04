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
    
    def __init__(self, observed=None, graphadapter=None):
        observer.AbstractListener.__init__(self)
        self.set_observed(observed)
        self.set_graph_adapter(graphadapter)
        return

    def set_observed(self, observed):
        if(observed and isinstance(observed, observer.Observed)):
            self.initialise(observed)
            self.observed = weakref.ref(observed, self.clear_observed)
        else:
            self.observed = observed

    def set_graph_adapter(self, adapter):
        self.__adapter = weakref.ref(adapter)

    def get_graph_adapter(self):
        return self.__adapter()

    graph = property(get_graph_adapter)

    def notify(self, sender, event):
        """called by the observed when something happens
        to it."""
        if(event[0] == "MetaDataChanged"):
            if(event[1]=="position"):
                if(event[2]): 
                    self.position_changed(*event[2])

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
        self.set_graph(graph)

        #mappings from models to widgets
        self.vertexmap = {}
        self.edgemap = {}
        self.annomap = {}

        self._type = None

        stratCls = self.__available_strategies__.get(graph.__class__,None)
        if(not stratCls): raise StrategyError("Could not find matching strategy")

        self.set_vertex_widget_type(stratCls.get_vertex_widget_type())
        self.set_edge_widget_type(stratCls.get_edge_widget_type())
        self.set_floating_edge_widget_type(stratCls.get_floating_edge_widget_type())
        self.set_annotation_widget_type(stratCls.get_annotation_widget_type())
        self.set_graph_adapter(stratCls.get_graph_adapter_type()(graph))
        self.set_direction_vector(stratCls.get_direction_vector())

        #an edge currently being drawn, low-level detail.
        self.__newEdge = None

    def set_graph(self, graph):
        self.observed = weakref.ref(graph)

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

    def post_addition(self, element):
        """defining virtual bases makes the program start
        but crash during execution if the method is not implemented, where
        the interface checking system could prevent the application from
        starting, with a die-early behaviour."""
        raise NotImplementedError

    def element_added(self, element):
        self.post_addition(element)
        return element

    def vertex_added(self, vertexModel):
        vertexWidget = self._vertexWidgetType(vertexModel, self.__adapter)
        vertexWidget.add_to_view(self.get_scene())
        self.vertexmap[vertexModel] = weakref.ref(vertexWidget)
        return self.element_added(vertexWidget)

    def edge_added(self, edgeModel, srcPort, dstPort):
        edgeWidget = self._edgeWidgetType(edgeModel, self.__adapter, srcPort, dstPort)
        edgeWidget.add_to_view(self.get_scene())
        self.edgemap[edgeModel] = weakref.ref(edgeWidget)
        return self.element_added(edgeWidget)

    def annotation_added(self, annotation):
        annoWidget = self._annoWidgetType(annotation, self.__adapter)
        annoWidget.add_to_view(self.get_scene())
        self.annomap[annotation] = weakref.ref(annoWidget)
        return self.element_added(annoWidget)

    def vertex_removed(self, vertexModel):
        print "vertexModel : ", vertexModel
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
        self.__newEdge = self._floatingEdgeWidgetType(srcPt, self.__adapter)
        self.new_edge_scene_init(self.__newEdge)
    
    def new_edge_scene_init(self, edge):
        raise NotImplementedError

    def new_edge_set_destination(self, *dest):
        if(self.__newEdge):
            self.__newEdge.update_line_destination(*dest)

    def new_edge_end(self):
        if(self.__newEdge):
            try:
                self.__newEdge.consolidate(self.__adapter)
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

    def set_vertex_widget_type(self, _type):
        self._vertexWidgetType = _type

    def set_edge_widget_type(self, _type):
        self._edgeWidgetType = _type

    def set_floating_edge_widget_type(self, _type):
        self._floatingEdgeWidgetType = _type

    def set_annotation_widget_type(self, _type):
        self._annoWidgetType = _type

    def set_direction_vector(self, vector):
        """precompute the cosines matrix from
        a vector giving the Y direction. The matrix 
        will be used to place graph verticess on the screen."""
        assert type(vector) == types.TupleType

    def set_graph_adapter(self, adapter):
        assert grapheditor_interfaces.IGraphAdapter.check(adapter)
        self.__adapter = adapter

    def get_graph_adapter(self):
        return self.__adapter

    graph = property(get_graph_adapter)
    
