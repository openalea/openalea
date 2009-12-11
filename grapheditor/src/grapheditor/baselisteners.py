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

import interfaces



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
        self.set_observed(None)
        return

    def initialise_from_model(self):
        adhoc = self.observed().get_ad_hoc_dict()
        self.observed().exclusive_command(self, adhoc.simulate_full_data_change)


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
        assert interfaces.IGraphViewStrategies.check(stratCls)

        graphadapter = stratCls.get_graph_adapter_type()
        vertexWidgetTypes  = stratCls.get_vertex_widget_types()
        edgeWidgetTypes  = stratCls.get_edge_widget_types()
        graphCls = stratCls.get_graph_model_type()
        assert type(graphCls) == types.TypeType

        if graphadapter is None:
            graphadapter = graphCls

        assert interfaces.IGraphAdapter.check(graphadapter)
        
        #checking vertex types
        elTypes = graphadapter.get_vertex_types()
        for vt in elTypes:
            vtype = vertexWidgetTypes.get(vt, None)
            assert interfaces.IGraphViewElement.check(vtype)

        #checking connectable types
        elTypes = stratCls.get_connector_types()
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
        
        cls.__available_strategies__[graphCls]=stratCls
        return        


    def __init__(self, graph):
        observer.AbstractListener.__init__(self)

        #mappings from models to widgets
        self.vertexmap = {}
        self.edgemap = {}

        #obtaining types from the strategy.
        self._vertexWidgetFactory = None
        self._edgeWidgetFactory = None
        self._adapterType = None

        stratCls = self.__available_strategies__.get(graph.__class__,None)
        if(not stratCls):
            raise StrategyError("Could not find matching strategy :" +
                                str(stratCls) +
                                " : " + str(type(graph)))

        self.set_vertex_widget_factory(stratCls.get_vertex_widget_factory())
        self.set_edge_widget_factory(stratCls.get_edge_widget_factory())
        self.set_graph_adapter_type(stratCls.get_graph_adapter_type())
        self.connector_types=stratCls.get_connector_types()
        self.set_graph(graph)

        #low-level detail, during the edge creation we store
        #the connectable graphical item closest to the mice.
        self.currentItem = None
        #an edge currently being drawn,
        self.__newEdge = None

    def graph(self):
        if(isinstance(self.observed, weakref.ref)):
            return self.observed()
        else:
            return self.observed

    def set_graph(self, graph):
        self.initialise(graph) #start listening. Todo: rename this method in
        #the abstract listener class. and make it hold a reference to the observed
        if(self._adapterType):
            ga = self._adapterType(graph)
            self.observed = ga
        else:
            self.observed = weakref.ref(graph) #might not need to be weak.

    # def get_scene(self):
    #     raise NotImplementedError

    #############################################################
    # Observer methods come next. They DO NOT modify the model. #
    #############################################################
    
    def notify(self, sender, data):
        if(data[0]=="vertexAdded") : self.vertex_added(*data[1])
        elif(data[0]=="edgeAdded") : self.edge_added(*data[1])
        elif(data[0]=="vertexRemoved") : self.vertex_removed(*data[1])
        elif(data[0]=="edgeRemoved") : self.edge_removed(*data[1])

    def __element_added(self, element):
        self.post_addition(element)
        return element

    def vertex_added(self, vtype, vertexModel):
        vertexWidget = self._vertexWidgetFactory(vtype, vertexModel, self.graph())
        vertexWidget.add_to_view(self.get_scene())
        self.vertexmap[vertexModel] = weakref.ref(vertexWidget)
        return self.__element_added(vertexWidget)

    def edge_added(self, etype, edgeModel, srcPort, dstPort):
        edgeWidget = self._edgeWidgetFactory(etype, edgeModel, self.graph(),
                                             srcPort, dstPort)
        edgeWidget.add_to_view(self.get_scene())
        self.edgemap[edgeModel] = weakref.ref(edgeWidget)
        return self.__element_added(edgeWidget)

    def vertex_removed(self, vtype, vertexModel):
        vertexWidget = self.vertexmap[vertexModel]
        vertexWidget().remove_from_view(self.get_scene())
        del self.vertexmap[vertexModel]
        return

    def edge_removed(self, vtype, edgeModel):
        edgeWidget = self.edgemap[edgeModel]
        edgeWidget().remove_from_view(self.get_scene())
        del self.edgemap[edgeModel]
        return

    ###########################################################
    # Controller methods come next. They DO MODIFY the model. #
    ###########################################################
    #---Low-Level Edge Interaction---
    def is_creating_edge(self):
        return True if self.__newEdge else False
    
    def new_edge_start(self, srcPt, etype="default"):
        self.__newEdge = self._edgeWidgetFactory("floating-"+etype, srcPt, self.graph())
        self.__newEdge.add_to_view(self.get_scene())

    def new_edge_set_destination(self, *dest):
        if self.currentItem:
            self.currentItem.set_highlighted(False)
        if(self.__newEdge):
            self.currentItem = self.find_closest_connectable(dest)
            if self.currentItem:
                self.currentItem.set_highlighted(True)
                dest = self.currentItem.get_scene_center()
        self.__newEdge.update_line_destination(*dest)


    def new_edge_end(self):
        if(self.__newEdge):
            try:
                self.__newEdge.consolidate(self.graph())
            except Exception, e :
                pass
            finally:
                self.__newEdge.remove_from_view(self.scene())
        if self.currentItem:
            self.currentItem.set_highlighted(False)
            self.currentItem = None
        self.__newEdge = None
            

    #########################
    # Other utility methods #
    #########################

    def set_vertex_widget_factory(self, _fac):
        self._vertexWidgetFactory = _fac

    def set_edge_widget_factory(self, _fac):
        self._edgeWidgetFactory = _fac

    def set_floating_edge_widget_type(self, _type):
        self._floatingEdgeWidgetType = _type

    def set_graph_adapter_type(self, _type):
        self._adapterType = _type

    def is_connectable(self, obj):
        return type(obj) in self.connector_types
