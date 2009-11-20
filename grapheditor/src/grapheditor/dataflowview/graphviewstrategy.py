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

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from PyQt4 import QtCore, QtGui
from openalea.core import compositenode
from openalea.core import node
import strat_vertex
import strat_edge
import strat_anno
import graph_adapter
from .. import grapheditor_baselisteners
from .. import qtgraphview


def GraphicalVertexFactory(vtype, *args, **kwargs):
    VT = GraphViewStrategy.get_vertex_widget_types().get(vtype)
    if(VT):
        return VT(*args, **kwargs)
    else:
        raise Exception("vtype not found")


def GraphicalEdgeFactory(etype, *args, **kwargs):
    ET = GraphViewStrategy.get_edge_widget_types().get(etype)
    if(ET):
        return ET(*args, **kwargs)
    else:
        raise Exception("vtype not found")


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
    def get_vertex_widget_factory(cls):
        """Returns a factory that instantiates vertices according
        to their types."""
        return GraphicalVertexFactory

    @classmethod
    def get_vertex_widget_types(cls):
        return {"vertex":strat_vertex.GraphicalVertex,
                "annotation":strat_anno.GraphicalAnnotation}

    @classmethod
    def get_edge_widget_factory(cls):
        """Returns a factory that instantiates edges according
        to their types."""
        return GraphicalEdgeFactory

    @classmethod
    def get_edge_widget_types(cls):
        return {"default":strat_edge.GraphicalEdge,
                "floating-default":strat_edge.FloatingEdge}

    @classmethod
    def get_graph_adapter_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return graph_adapter.GraphAdapter
    
    @classmethod
    def get_connector_types(cls):
        return [strat_vertex.GraphicalPort]

###################################
# vertex state drawing strategies #
###################################

class DataflowPaintStrategyCommon:
    # Color Definition
    not_modified_color = QtGui.QColor(0, 0, 255, 200)
    modified_color = QtGui.QColor(255, 0, 0, 200)        
    
    selected_color = QtGui.QColor(180, 180, 180, 180)
    not_selected_color = QtGui.QColor(255, 255, 255, 100)
    
    error_color = QtGui.QColor(255, 0, 0, 255)    
    selected_error_color = QtGui.QColor(0, 0, 0, 255)
    not_selected_error_color = QtGui.QColor(100, 0, 0, 255)
    
    __corner_radius__ = 5.0
    __margin__        = 5.0
    __v_margin__      = 15.0


class PaintNormalVertex(object):
    @classmethod
    def paint(cls, item, painter, option, widget):
        return False

    @classmethod
    def get_path(cls, widget):
        rect = widget.rect()
            
        #the drawn rectangle is smaller than
        #the actual widget size
        rect.setX( rect.x()+DataflowPaintStrategyCommon.__margin__ )
        rect.setY( rect.y()+DataflowPaintStrategyCommon.__v_margin__ )
        rect.setWidth( rect.width()-DataflowPaintStrategyCommon.__margin__ )
        rect.setHeight( rect.height()-DataflowPaintStrategyCommon.__v_margin__ )
        
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect,
                            DataflowPaintStrategyCommon.__corner_radius__,
                            DataflowPaintStrategyCommon.__corner_radius__)
        return path

    @classmethod
    def get_gradient(cls, widget):
        rect = widget.rect()
        margin = DataflowPaintStrategyCommon.__v_margin__
        gradient = QtGui.QLinearGradient(0,margin,
                                         0,rect.height()-margin )

        gradient.setColorAt(0.0, cls.get_first_color(widget))
        gradient.setColorAt(0.8, cls.get_second_color(widget))
        return gradient

    @classmethod
    def get_first_color(cls, widget):
        return DataflowPaintStrategyCommon.not_selected_color

    @classmethod
    def get_second_color(cls, widget):
        return DataflowPaintStrategyCommon.not_modified_color

    @classmethod
    def prepaint(self, widget, paintEvent, painter, state):
        return

    @classmethod
    def postpaint(self, widget, paintEvent, painter, state):
        return


PaintLazyVertex=PaintNormalVertex


class PaintUserColorVertex(PaintNormalVertex):
    @classmethod
    def get_first_color(cls, widget):
        return QtGui.QColor(*widget.observed().get_ad_hoc_dict().get_metadata("user_color"))

    @classmethod
    def get_second_color(cls, widget):
        return cls.get_first_color(widget)


class PaintErrorVertex(PaintNormalVertex):
    @classmethod
    def get_first_color(cls, widget):
        return DataflowPaintStrategyCommon.error_color

    @classmethod
    def get_second_color(cls, widget):
        return QtGui.QColor(255, 144, 0, 200)


class PaintErrorVertex(PaintNormalVertex):
    @classmethod
    def get_first_color(cls, widget):
        return DataflowPaintStrategyCommon.error_color

    @classmethod
    def get_second_color(cls, widget):
        return DataflowPaintStrategyCommon.not_selected_error_color


class PaintUserAppVertex(PaintNormalVertex):
    @classmethod
    def get_second_color(cls, widget):
        return QtGui.QColor(255, 144, 0, 200)


class PaintBlockedVertex(PaintNormalVertex):
    @classmethod
    def postpaint(cls, widget, paintEvent, painter, state):
        painter.setBrush(QtGui.QBrush(QtCore.Qt.BDiagPattern))
        painter.drawPath(cls.get_path(widget))
        return
    
vertex_drawing_strategies={ "node_normal": PaintNormalVertex,
                            "node_lazy": PaintLazyVertex, 
                            "use_user_color": PaintUserColorVertex, 
                            "node_error": PaintErrorVertex, 
                            "node_is_user_app": PaintUserAppVertex,
                            "node_blocked": PaintBlockedVertex}



if(__name__ != "__main__"):
    #we declare what are the node model ad hoc data we require:
    vertexModelAdHocExtension = {"user_color":list, 
                                 "use_user_color":bool, 
                                 "position":list,
                                 "text": str}
    node.Node.extend_ad_hoc_slots(vertexModelAdHocExtension)

    #we declare what are the node model ad hoc data we require:
    portModelAdHocExtension = {"hide":bool,
                               "canvasPosition": list}
    node.AbstractPort.extend_ad_hoc_slots(portModelAdHocExtension)

    
    #we register this strategy
    grapheditor_baselisteners.GraphListenerBase.register_strategy(GraphViewStrategy)
    
    #we register the dataflow state drawing strategies
    qtgraphview.QtGraphViewVertex.add_drawing_strategies(vertex_drawing_strategies)
