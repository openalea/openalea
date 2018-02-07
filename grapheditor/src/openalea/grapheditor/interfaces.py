# -*- python -*-
#
#       OpenAlea.GraphEditor: OpenAlea graphical user interface
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
"""Interfaces for the generic graph view module. The graph view widget
won't check for inheritance of the object's it is passed. Instead, it
will check the interfaces match more or less."""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

class IInterfaceMetaClass(type):
    """
    Adds a method to the interface class that checks
    that the given object implements the class' interface.
    Allows some sort of safe-ducktyping"""

    def __new__(cls, name, bases, dict):
        newCls = type.__new__(cls, name, bases, dict)

        ###--CONTRACT CHECKING INFRASTRUCTURE---
        newCls.__interface_decl__ = [i for i in dict.keys()]
        for base in bases:
            if(hasattr(base, "__interface_decl__")):
                   newCls.__interface_decl__ += base.__interface_decl__

        #removing some objects that aren't part of the interface
        if("__metaclass__" in newCls.__interface_decl__):
            newCls.__interface_decl__.remove("__metaclass__")
        if("__module__" in newCls.__interface_decl__):
            newCls.__interface_decl__.remove("__module__")
        if("__doc__" in newCls.__interface_decl__):
            newCls.__interface_decl__.remove("__doc__")
        if("check" in newCls.__interface_decl__):
            newCls.__interface_decl__.remove("check")
        ###--!!CONTRACT CHECKING INFRASTRUCTURE---
        return newCls

    def __init__(cls, name, bases, dic):
        super(IInterfaceMetaClass, cls).__init__(name, bases, dic)

    def check(cls, obj):
        """ Check if obj matches this interface. """
        objMem = dir(obj)
        notImp = []

        stop = False
        for i in cls.__interface_decl__:
            if i not in objMem:
                notImp.append(i)
                stop = True
            else :
                continue

        if stop:
            # The check failed.
            stri = "Unimplemented : \n"
            for i in notImp:
                stri += "\t"+i+"\n"
            raise UserWarning('Object %s does not belong to the Interface %s \n%s '%(str(obj),cls.__name__,stri))

        return not stop


class IGraphViewStrategies(object):
    """Define implementations of this trait
    class to define the behaviour of the graph.
    For example : DataFlowGraphViewTrait, TreeGraphViewTrait,
    NetworkGraphViewTrait..."""
    __metaclass__ = IInterfaceMetaClass


    def get_graph_model_type(cls):
        """Returns the classobj defining the graph type"""
        raise NotImplementedError

    def create_view(self, parent, graph, *args, **kwargs):
        """Instanciates the view"""
        raise NotImplementedError

    def create_vertex_widget(self, vtype, *args, **kwargs):
        """Instanciates a node matching vtype"""
        raise NotImplementedError

    def create_edge_widget(self, etype, *args, **kwargs):
        """Instanciates an edge matching etype"""
        raise NotImplementedError

    # def get_vertex_widget_types(cls):
    #     """Return a dict mapping vertex type names (a str) to the
    #     graphical representation of it (a class)"""
    #     raise NotImplementedError

    # def get_edge_widget_types(cls):
    #     """Return a dict mapping edge type names (a str) to the
    #     graphical representation of it (a class)"""
    #     raise NotImplementedError


    # def get_graph_or_adapter_type(cls):
    #     """Return a classobj defining the type of widget
    #     that represents an annotation"""
    #     raise NotImplementedError


    def get_connector_types(cls):
        raise NotImplementedError


    def initialise_graph_view(cls, graphView, graphModel):
        """intialise graph view from model"""
        raise NotImplementedError


#------*************************************************------#
class IGraphListener(object):
    __metaclass__ = IInterfaceMetaClass

    def vertex_added(self, vtype, vertexModel):
        raise NotImplementedError

    def edge_added(self, edgeModel, srcPort, dstPort):
        raise NotImplementedError

    def vertex_removed(self, vtype,  vertexModel):
        raise NotImplementedError

    def edge_removed(self, edgeModel):
        raise NotImplementedError

    def _new_edge_start(self, srcPt, etype, source):
        raise NotImplementedError

    def _new_edge_set_destination(self, *dest):
        raise NotImplementedError

    def _new_edge_end(self):
        raise NotImplementedError

    def find_closest_connectable(self, *args, **kwargs):
        raise NotImplementedError

    def post_addition(self, *args, **kwargs):
        raise NotImplementedError

    def is_connectable(self, *args, **kwargs):
        raise NotImplementedError

    def clear(self, *args, **kwargs):
        raise NotImplementedError

    def initialise_from_model(self):
        raise NotImplementedError



#------*************************************************------#
class IGraphAdapter(object):
    __metaclass__ = IInterfaceMetaClass

    def add_vertex(self, *args, **kargs):
        NotImplementedError

    def get_vertex(self, *args, **kargs):
        raise NotImplementedError

    def remove_vertex(self, *args, **kargs):
        raise NotImplementedError

    def remove_vertices(self, *args, **kargs):
        raise NotImplementedError

    def get_vertex_inputs(self, *args, **kargs):
        raise NotImplementedError

    def get_vertex_outputs(self, *args, **kargs):
        raise NotImplementedError

    def get_vertex_input(self, *args, **kargs):
        raise NotImplementedError

    def get_vertex_output(self, *args, **kargs):
        raise NotImplementedError

    def add_edge(self, *args, **kargs):
        raise NotImplementedError

    def remove_edge(self, *args, **kargs):
        raise NotImplementedError

    def is_input(self, *args, **kargs):
        raise NotImplementedError

    def is_output(self, *args, **kargs):
        raise NotImplementedError

    def get_vertex_types(self):
        raise NotImplementedError

    def get_edge_types(self):
        raise NotImplementedError

#------*************************************************------#
class IGraphViewConnectable(object):
    """Interface for connectable objects"""
    __metaclass__ = IInterfaceMetaClass

    def set_highlighted(self, *args, **kwargs):
        raise NotImplementedError

    def get_scene_center(self):
        raise NotImplementedError

#------*************************************************------#
class IGraphViewElement(object):
    """Base class for elements in a GraphView"""
    __metaclass__ = IInterfaceMetaClass

    def position_changed(self, *args):
        """Place the element's representation in
        the view space"""
        raise NotImplementedError

    def add_to_view(self, view):
        """add this element to the graphical view"""
        raise NotImplementedError

    def remove_from_view(self, view):
        """remove this element from the graphical view"""
        raise NotImplementedError

    def notify(self, sender, event):
        """called by the observed objects
        Expected event = (\"metadata_changed\", "position", [x,x], list)
        """
        raise NotImplementedError

    def store_view_data(self, **kwargs):
        raise NotImplementedError

    def get_view_data(self, key):
        raise NotImplementedError

    def initialise_from_model(self):
        raise NotImplementedError

#------*************************************************------#
class IGraphViewVertex (IGraphViewElement):
    def lock_position(self, val=True):
        raise NotImplementedError

#------*************************************************------#
class IGraphViewAnnotation(IGraphViewElement):
    """Interface for Annotations"""
    def set_text(self, text):
        """to change the visible text"""
        raise NotImplementedError

    def notify(self, sender, event):
        """(\"metadata_changed\", \"text\", \"a string\", str)"""
        raise NotImplementedError

#------*************************************************------#
class IGraphViewEdge(IGraphViewElement):
    """Interface for edges between two vertexs."""
    def update_line_source(self, *pos):
        """updates this edge's starting point. Called when
        source point is moved"""
        raise NotImplementedError

    def update_line_destination(self, *pos):
        """updates this edge's ending point. Called when
        dest point is moved"""
        raise NotImplementedError

    def notify(self, sender, event):
        """(\"metadata_changed\", \"canvasPosition\", [x,x], list)"""
        raise NotImplementedError


#------*************************************************------#
class IGraphViewFloatingEdge(object):
    """Interface for edges to be drawn during
    creation time, ie while the user drags."""
    __metaclass__ = IInterfaceMetaClass

    def __init__(self, src):
        raise NotImplementedError

    def consolidate(self, model):
        """returns whatever object is under the mouse
        pointer at the time the button was released"""
        raise NotImplementedError

    def get_connections(self, *args):
        raise NotImplementedError


