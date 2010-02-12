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
"""Interfaces for the generic graph view module. The graph view widget
won't check for inheritance of the object's it is passed. Instead, it
will check the interfaces match more or less."""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from openalea.core import interface


class IGraphViewStrategies(object):
    """Define implementations of this trait 
    class to define the behaviour of the graph.
    For example : DataFlowGraphViewTrait, TreeGraphViewTrait, 
    NetworkGraphViewTrait..."""
    __metaclass__ = interface.IInterfaceMetaClass

    @classmethod
    def get_graph_model_type(cls):
        """Returns the classobj defining the graph type"""
        raise NotImplementedError

    @classmethod
    def get_vertex_widget_factory(cls):
        """Returns a factory that creates vertices
        according to a type argument"""
        raise NotImplementedError

    @classmethod
    def get_vertex_widget_types(cls):
        """Return a dict mapping vertex type names (a str) to the
        graphical representation of it (a class)"""
        raise NotImplementedError

    @classmethod
    def get_edge_widget_factory(cls):
        """Returns a factory that creates edges
        according to a type argument"""
        raise NotImplementedError

    @classmethod
    def get_edge_widget_types(cls):
        """Return a dict mapping edge type names (a str) to the
        graphical representation of it (a class)"""
        raise NotImplementedError

    @classmethod
    def get_graph_adapter_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        raise NotImplementedError

    @classmethod
    def get_connector_types(cls):
        raise NotImplementedError
    

#------*************************************************------#
class IGraphListener(object):
    __metaclass__ = interface.IInterfaceMetaClass

    def vertex_added(self, vtype, vertexModel):
        raise NotImplementedError

    def edge_added(self, edgeModel, srcPort, dstPort):
        raise NotImplementedError

    def vertex_removed(self, vtype,  vertexModel):
        raise NotImplementedError

    def edge_removed(self, edgeModel):
        raise NotImplementedError

    def new_edge_scene_init(self, *args, **kwargs):
        raise NotImplementedError
    
    def new_edge_scene_cleanup(self, *args, **kwargs):
        raise NotImplementedError

    def find_closest_connectable(self, *args, **kwargs):
        raise NotImplementedError

    def post_addition(self, *args, **kwargs):
        raise NotImplementedError

    def is_connectable(self, *args, **kwargs):
        raise NotImplementedError

#------*************************************************------#
class IGraphAdapter(object):
    __metaclass__ = interface.IInterfaceMetaClass

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

    @classmethod
    def get_vertex_types(cls):
        raise NotImplementedError

    @classmethod
    def get_edge_types(cls):
        raise NotImplementedError

#------*************************************************------#
class IGraphViewConnectable(object):
    """Interface for connectable objects"""
    __metaclass__ = interface.IInterfaceMetaClass

    def set_highlighted(self, *args, **kwargs):
        raise NotImplementedError

    def get_scene_center(self):
        raise NotImplementedError

#------*************************************************------#
class IGraphViewElement(object):
    """Base class for elements in a GraphView"""
    __metaclass__ = interface.IInterfaceMetaClass

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

    def store_view_data(self, key, value, notify=True):
        raise NotImplementedError

    def get_view_data(self, key):
        raise NotImplementedError

    def announce_view_data(self, exclusive=False):
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

    def announce_view_data_src(self, exclusive=False):
        raise NotImplementedError        

    def announce_view_data_dst(self, exclusive=False):
        raise NotImplementedError        


#------*************************************************------#
class IGraphViewFloatingEdge(object):
    """Interface for edges to be drawn during
    creation time, ie while the user drags."""
    __metaclass__ = interface.IInterfaceMetaClass

    def __init__(self, src):
        raise NotImplementedError

    def consolidate(self, model):
        """returns whatever object is under the mouse
        pointer at the time the button was released"""
        raise NotImplementedError

    def get_connections(self, *args):
        raise NotImplementedError


#------*************************************************------#
class IGraphViewVertexPaintStrategy(object):
    __metaclass__ = interface.IInterfaceMetaClass

    @classmethod
    def paint(cls, item, painter, option, widget):
        """
        Implement this to completely override the drawing
        process.

        :Returns:
        True if the method did the complete painting
        or False if it doesn't want to override the
        caller's painting routine.

        :Parameters:
            - item - the graphical item calling this function.
            - painter - the painter object used to draw the view.
            - option - options to tweak the drawing of the item.
            - widget - the widget being painted on.
         
        """
        raise NotImplementedError
    
    @classmethod
    def get_path(cls, widget):
        """ 
	Path representing the object.
        
	:Returns: The path that will draw the
        boundary of the item.
        """
        raise NotImplementedError
    
    @classmethod
    def get_gradient(cls, widget):
        """ 
	Gradient to fill the object with.
        
        :Returns: The gradient to brush the item
        with. It can return None and let the gradient
        be defined by the first and second color. The
        direction of the gradient will be determined
        by the caller.
        """
        raise NotImplementedError
    
    @classmethod
    def get_first_color(cls, widget):
        """
	Returns the first color of the gradient.
	"""
        raise NotImplementedError
    
    @classmethod
    def get_second_color(cls, widget):
        """
	Returns the second color of the gradient.
	"""
        raise NotImplementedError
    
    @classmethod
    def prepaint(self, widget, paintEvent, painter, state):
        """A routine to do things before the actual painting happens.

        :Parameters:
            - item - the graphical item calling this function.
            - painter - the painter object used to draw the view.
            - option - options to tweak the drawing of the item.
            - widget - the widget being painted on.

         """
        raise NotImplementedError

    @classmethod
    def postpaint(self, widget, paintEvent, painter, state):
        """A routine to do things after the actual painting occured.

        :Parameters:
            - item - the graphical item calling this function.
            - painter - the painter object used to draw the view.
            - option - options to tweak the drawing of the item.
            - widget - the widget being painted on.

         """
        raise NotImplementedError
