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




class ObservedBlackBox(object):
    def __init__(self, owner, observed):
        self.owner = weakref.ref(owner)
        self.__observed = None
        self.__is_true = False
        self.__call__(observed)

    def __call__(self, *args):
        """If args is provided, sets the args,
        else, returns the observed"""
        if len(args) == 1:
            observed = args[0]
            if observed and self.__observed is not None:
                return #don't overwrite the existing observed
            if observed :
                if isinstance(observed, observer.Observed): self.__patch_true()
                else: self.__patch_fake()
            else : self.__patch_fake()
            self.__set_observed(observed)
        else :
            return self.get_observed()

    def clear_observed(self):
        raise Exception("clear_obs : You first need to set the observed with the () operator")

    def get_observed(self):
        raise Exception("get_obs : You first need to set the observed with the () operator")

    def __set_observed(self, obs):
        raise Exception("set_obs : You first need to set the observed with the () operator")    

    def __patch_true(self):
        self.clear_observed = self.__clear_true_observed
        self.get_observed = self.__get_true_observed
        self.__set_observed = self.__set_true_observed

    def __patch_fake(self):
        self.clear_observed = self.__clear_fake_observed
        self.get_observed = self.__get_fake_observed
        self.__set_observed = self.__set_fake_observed

    def __set_true_observed(self, obs):
        self.owner().initialise(obs)
        self.__observed = weakref.ref(obs, self.clear_observed)

    def __set_fake_observed(self, obs):
        self.__observed = obs

    def __get_true_observed(self):
        return self.__observed()

    def __get_fake_observed(self):
        return self.__observed

    def __clear_true_observed(self, which=None):
        try:
            self.__observed().unregister_listener(self.owner())
        except:
            try: self.__observed.unregister_listener(self.owner())
            except: pass
        finally:
            self.__observed = None

    def __clear_fake_observed(self, which=None):
        self.__observed = None
        

class GraphElementObserverBase(observer.AbstractListener):
    """Base class for elements in a GraphView"""
    
    def __init__(self, observed=None, graph=None):
        observer.AbstractListener.__init__(self)
        self.__obsBBox = ObservedBlackBox(self, observed)
        self.set_graph(graph)
        return

    def set_observed(self, observed):
        if self.get_observed():
            raise Exception("Clear observer before setting a new one")
        self.__obsBBox(observed)
        
    def get_observed(self):
        try: return self.__obsBBox()
        except TypeError: return None

    def clear_observed(self, *args):
        self.__obsBBox.clear_observed()
        
    def change_observer(self, old, new):
        self.__obsBBox.clear_observed()
        self.set_observed(new)

    def set_graph(self, graph):
        if(graph is not None):
            self.__graph = weakref.ref(graph)

    def graph(self):
        return self.__graph()

    def notify(self, sender, event):
        """called by the observed when something happens
        to it."""
        if(event[0] == "metadata_changed"):
            if(event[1]=="position"):
                if(event[2]): 
                    self.position_changed(*event[2])

    def initialise_from_model(self):
        self.announce_view_data(exclusive=self)

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
        self.widgetmap = {}
        # self.vertexmap = {}
        # self.edgemap = {}

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
        if(isinstance(self.__observed, weakref.ref)):
            return self.__observed()
        else:
            return self.__observed

    def set_graph(self, graph):
        self.initialise(graph) #start listening. Todo: rename this method in
        #the abstract listener class. and make it hold a reference to the observed
        if(self._adapterType):
            ga = self._adapterType(graph)
            self.__observed = ga
        else:
            self.__observed = weakref.ref(graph) #might not need to be weak.

    #############################################################
    # Observer methods come next. They DO NOT modify the model. #
    #############################################################
    
    def notify(self, sender, event):
        if(event[0]=="vertex_added") : self.vertex_added(*event[1])
        elif(event[0]=="edge_added") : self.edge_added(*event[1])
        elif(event[0]=="vertex_removed") : self.vertex_removed(*event[1])
        elif(event[0]=="edge_removed") : self.edge_removed(*event[1])
            
    def vertex_added(self, vtype, vertexModel):
        if vertexModel is None : return
        vertexWidget = self._vertexWidgetFactory(vtype, vertexModel, self.graph())
        return self._element_added(vertexWidget, vertexModel)

    def edge_added(self, etype, edgeModel, src, dst):
        if edgeModel is None : return
        edgeWidget = self._edgeWidgetFactory(etype, edgeModel, self.graph(),
                                             src, dst)
        return self._element_added(edgeWidget, edgeModel)

    def vertex_removed(self, vtype, vertexModel):
        if vertexModel is None : return
        return self._element_removed(vertexModel)

    def edge_removed(self, vtype, edgeModel):
        if edgeModel is None : return
        return self._element_removed(edgeModel)
        
    def _element_added(self, widget, model):
        widget.add_to_view(self.get_scene())
        self._register_widget_with_model(widget, model)
        
    def _register_widget_with_model(self, widget, model):
        widgetWeakRef = weakref.ref(widget, self._widget_died)
        modelWidgets = self.widgetmap.get(model, None)
        if not modelWidgets: self.widgetmap[model] = set()
        self.widgetmap[model].add(widgetWeakRef)
        self.widgetmap[widgetWeakRef] = model    
        self.post_addition(widget) #virtual function call
        return widget
        
    def _unregister_widget_from_model(self, widget, model):
        if model is None : return
        widgets = self.widgetmap.get(model, None)
        if(widgets is None): return
        for widgetWeakRef in widgets:
            if widgetWeakRef() == widget : toDiscard = widgetWeakRef
        widgets.discard(toDiscard)
        
    def _element_removed(self, model):
        if model is None : return
        widgets = self.widgetmap.pop(model, None)
        if(widgets is None): return
        for widgetWeakRef in widgets:
            self.widgetmap.pop(widgetWeakRef, None)
            widget = widgetWeakRef(); widget.remove_from_view(self.get_scene()) 
            del widgetWeakRef
    
    def _widget_died(self, widgetWeakRef):
        model = self.widgetmap.pop(widgetWeakRef, None)
        if not model: return
            # raise Exception("__widget_died without associated model")
        modelWidgets = self.widgetmap.get(model, None)
        if not modelWidgets : return
        modelWidgets.discard(widgetWeakRef)
            

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
