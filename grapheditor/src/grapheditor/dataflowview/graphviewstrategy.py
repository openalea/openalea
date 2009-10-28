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

from PyQt4 import QtCore, QtGui
from openalea.core import interface
from openalea.core import compositenode
from openalea.core import node
import strat_node
import strat_edge
import strat_anno
from .. import gengraphview
from .. import qtgraphview


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
        return strat_node.AleaQGraphicalNode

    @classmethod
    def get_edge_widget_type(cls):
        """Return a classobj defining the type of widget 
        that represents an edge"""
        return strat_edge.AleaQGraphicalEdge

    @classmethod
    def get_floating_edge_widget_type(cls):
        """Return a classobj defining the type of widget 
        that represents an edge"""
        return strat_edge.AleaQFloatingEdge


    @classmethod
    def get_annotation_widget_type(cls):
        """Return a classobj defining the type of widget
        that represents an annotation"""
        return strat_anno.AleaQGraphicalAnnotation



#################################
# node state drawing strategies #
#################################

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
    __v_margin__        = 15.0


class PaintNormalNode(object):
    @classmethod
    def get_path(cls, widget):
        rect = QtCore.QRectF( widget.rect() )
            
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
        gradient = QtGui.QLinearGradient(0,0,0,100)
        gradient.setColorAt(0.0, cls.get_first_color(widget))
        gradient.setColorAt(0.8, cls.get_second_color(widget))
        return gradient

    @classmethod
    def get_first_color(cls, widget):
        return DataflowPaintStrategyCommon.not_modified_color

    @classmethod
    def get_second_color(cls, widget):
        return DataflowPaintStrategyCommon.not_selected_color

    @classmethod
    def prepaint(self, widget, paintEvent, painter, state):
        return

    @classmethod
    def postpaint(self, widget, paintEvent, painter, state):
        return


PaintLazyNode=PaintNormalNode


class PaintUserColorNode(PaintNormalNode):
    @classmethod
    def get_first_color(cls, widget):
        return QtGui.QColor(*widget.observed().get_ad_hoc_dict().get_metadata("user_color"))

    @classmethod
    def get_second_color(cls, widget):
        return get_first_color(widget)


class PaintErrorNode(PaintNormalNode):
    @classmethod
    def get_first_color(cls, widget):
        return DataflowPaintStrategyCommon.error_color

    @classmethod
    def get_second_color(cls, widget):
        return QtGui.QColor(255, 144, 0, 200)


class PaintErrorNode(PaintNormalNode):
    @classmethod
    def get_first_color(cls, widget):
        return DataflowPaintStrategyCommon.error_color

    @classmethod
    def get_second_color(cls, widget):
        return DataflowPaintStrategyCommon.not_selected_error_color


class PaintUserAppNode(PaintNormalNode):
    @classmethod
    def get_second_color(cls, widget):
        return QtGui.QColor(255, 144, 0, 200)


class PaintBlockedNode(PaintNormalNode):
    @classmethod
    def postpaint(cls, widget, paintEvent, painter, state):
        painter.setBrush(QtGui.QBrush(QtCore.Qt.BDiagPattern))
        painter.drawPath(cls.get_path(widget))
        return
    
node_drawing_strategies={ "node_normal": PaintNormalNode,
                          "node_lazy": PaintLazyNode, 
                          "use_user_color": PaintUserColorNode, 
                          "node_error": PaintErrorNode, 
                          "node_is_user_app": PaintUserAppNode,
                          "node_blocked": PaintBlockedNode}



if(__name__ != "__main__"):
    #we declare what are the model ad hoc data we require:
    nodeModelAdHocExtension = {"user_color":list, 
                               "use_user_color":bool, 
                               "position":list,
                               "text": str}
    node.Node.extend_ad_hoc_slots(nodeModelAdHocExtension)

    #we register this strategy
    gengraphview.GraphView.register_strategy(GraphViewStrategy)

    #we register the dataflow state drawing strategies
    qtgraphview.QtGraphViewNode.add_drawing_strategies(node_drawing_strategies)
