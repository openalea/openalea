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

try:
    from openalea.core import observer
except ImportError:
    # This will fail.
    # Please, have a local copy to remove the dependency on core.
    import observer

import interfaces



class StrategyError( Exception ):
    def __init__(self, msg):
        Exception.__init__(self)
        self._msg = msg
        return

    def get_message(self):
        return self._msg



class GraphElementListenerBase(observer.AbstractListener):
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
        try:
            return self.__obsBBox()
        except TypeError:
            return None

    def clear_observed(self, *args):
        self.__obsBBox.clear_observed()

    def change_observed(self, old, new):
        self.clear_observed()
        self.set_observed(new)
        #currently, the grapheditor widget maps models with graphical items
        #to track which graphic item to delete when something is being
        #deleted in the model:
        self.get_view()._unregister_widget_from_model(self, old)
        self.get_view()._register_widget_with_model(self, new)

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


class GraphListenerBase(observer.AbstractListener):
    """This object strictly watches the given graph.
    It deduces the correct representation out
    of a known list of representations.

    It is MVC oriented.
    """

    __available_strategies__ = {}

    @classmethod
    def register_strategy(cls, strat):
        graphCls = strat.get_graph_model_type()
        cls.__available_strategies__[graphCls]=strat
        return


    def __init__(self, graph):
        observer.AbstractListener.__init__(self)

        #mappings from models to widgets
        self.widgetmap = {}

        #obtaining types from the strategy.
        self._vertexWidgetFactory = None
        self._edgeWidgetFactory = None
        self._adapterType = None
        self._interactionFlag = 0

        strat = self.__available_strategies__.get(graph.__class__,None)
        if(not strat):
            raise StrategyError("Could not find matching strategy :" +
                                str(strat) +
                                " : " + str(type(graph)))
        self.__strategy=strat
        self.connector_types=set(strat.get_connector_types())
        self.set_graph(graph)

        #low-level detail, during the edge creation we store
        #the connectable graphical item closest to the mice.
        self.currentItem = None
        #an edge currently being drawn,
        self.__newEdge = None
        self.__newEdgeSource = None

    def get_strategy(self):
        return self.__strategy

    def graph(self):
        if(isinstance(self.__observed, weakref.ref)):
            return self.__observed()
        else:
            return self.__observed

    def set_graph(self, graph):
        self.initialise(graph) #start listening. Todo: rename this method in
        #the abstract listener class. and make it hold a reference to the observed
        if(self.__strategy.has_adapter()):
            ga = self.__strategy.adapt_graph(graph)
            self.__observed = ga
        else:
            self.__observed = weakref.ref(graph) #might not need to be weak.

    def initialise_from_model(self):
        self.__strategy.initialise_graph_view(self, self.graph())

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
        vertexWidget = self.__strategy.create_vertex_widget(vtype, vertexModel, self.graph())
        return self._element_added(vertexWidget, vertexModel)

    def edge_added(self, etype, edgeModel, src, dst):
        if edgeModel is None : return
        edgeWidget = self.__strategy.create_edge_widget(etype, edgeModel, self.graph(),
                                                        src, dst)
        return self._element_added(edgeWidget, edgeModel)

    def vertex_removed(self, vtype, vertexModel):
        if vertexModel is None : return
        return self._element_removed(vertexModel)

    def edge_removed(self, vtype, edgeModel):
        if edgeModel is None : return
        return self._element_removed(edgeModel)

    def clear(self):
        self.widgetmap = {}


    ###############################################################
    # Internal book-keeping methods to make all system's gc happy #
    ###############################################################
    def _element_added(self, widget, model):
        widget.add_to_view(self.get_scene())
        self._register_widget_with_model(widget, model)

    def _register_widget_with_model(self, widget, model):
        """
        This method maps widgets to models. A single model
        can be viewed be many widgets.
        Because it is very difficult to track ownership of
        widgets or models, GraphEditor tries to create only
        weak references to the widgets to reduce the risk of leaks
        comming from OS-specific memory management issues.
        The resulting mapping is used to cleanly remove widgets from
        the views when the model has been deleted.
        It uses the weakref callback to maintain the mapping up-to-date.
        """
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
        toDiscard = None
        for widgetWeakRef in widgets:
            if widgetWeakRef() == widget : toDiscard = widgetWeakRef; break
        if toDiscard:
            widgets.discard(toDiscard)

    def _element_removed(self, model):
        if model is None : return
        widgets = self.widgetmap.pop(model, None)
        if(widgets is None): return
        for widgetWeakRef in widgets:
            self.widgetmap.pop(widgetWeakRef, None)
            widget = widgetWeakRef()
            widget.remove_from_view(self.get_scene())
            del widgetWeakRef

    def _widget_died(self, widgetWeakRef):
        model = self.widgetmap.pop(widgetWeakRef, None)
        if not model: return
            # raise Exception("__widget_died without associated model")
        modelWidgets = self.widgetmap.get(model, None)
        if not modelWidgets : return
        modelWidgets.discard(widgetWeakRef)


    ########################################################
    # Controller methods come next. They MODIFY the model. #
    ########################################################
    def set_interaction_flag(self, val):
        self._interactionFlag = val

    def get_interaction_flag(self):
        return self._interactionFlag

    #---Low-Level Edge Interaction---
    def is_creating_edge(self):
        return True if self.__newEdge else False

    def new_edge_start(self, srcPt, etype="default", source=None):
        self.__newEdge = self.__strategy.create_edge_widget("floating-"+etype, srcPt, self.graph())
        self.__newEdge.add_to_view(self.get_scene())
        if  source:
            self.__newEdgeSource = source
            self.__newEdgeSource.lock_position(True)

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
                self.__newEdge.remove_from_view(self.get_scene())
        if self.currentItem:
            self.currentItem.set_highlighted(False)
            self.currentItem = None
        self.__newEdge = None
        if self.__newEdgeSource:
            self.__newEdgeSource.lock_position(False)
            self.__newEdgeSource = None


    #########################
    # Other utility methods #
    #########################
    def is_connectable(self, obj):
        for ct in self.connector_types:
            if isinstance(obj, ct):
                return True
        return False

class ObservedBlackBox(object):
    def __init__(self, owner, observed):
        self.owner = weakref.ref(owner)
        self.__observed = None
        self.__is_true = False
        self.__call__(observed)

    def is_true(self):
        return self.__is_true

    def __call__(self, *args):
        """If args is provided, sets the args,
        else, returns the observed"""
        if len(args) == 1:
            observed = args[0]
            if observed:
                if self.__observed is not None:
                    return #don't overwrite the existing observed
                else :
                    if isinstance(observed, observer.Observed):
                        self.__patch_true()
                    else:
                        self.__patch_fake()
            else :
                self.__patch_fake()
            self.__set_observed(observed)
        else :
            return self.get_observed()

    def clear_observed(self):
        raise Exception("clear_obs : You first need to set the observed with the () operator")

    def get_observed(self):
        raise Exception("get_obs : You first need to set the observed with the () operator")

    def __set_observed(self, obs):
        raise Exception("set_obs : You first need to set the observed with the () operator")

    def get_observers(self):
        raise Exception("get_observers : You first need to set the observed with the () operator")

    def __patch_true(self):
        self.__is_true = True
        self.clear_observed = self.__clear_true_observed
        self.get_observed = self.__get_true_observed
        self.get_observers = self.__get_true_observers
        self.__set_observed = self.__set_true_observed

    def __patch_fake(self):
        self.__is_true = False
        self.clear_observed = self.__clear_fake_observed
        self.get_observed = self.__get_fake_observed
        self.get_observers = self.__get_fake_observers
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
        if (self.__observed()):
            self.__observed().unregister_listener(self.owner())
        self.__observed = None

    def __clear_fake_observed(self, which=None):
        self.__observed = None

    def __get_true_observers(self):
        return self.__observed().listeners

    def __get_fake_observers(self):
        return 0 #ugh... don't know how to do anything smart here yet.

