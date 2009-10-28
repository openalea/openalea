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

from PyQt4 import QtCore, QtGui
from openalea.core.pkgmanager import PackageManager

#Drag and drop handlers
def OpenAleaNodeFactoryHandler(view, event):
    """ Drag and Drop from the PackageManager """
    if (event.mimeData().hasFormat("openalea/nodefactory")):
        pieceData = event.mimeData().data("openalea/nodefactory")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
        
        package_id = QtCore.QString()
        factory_id = QtCore.QString()
        
        dataStream >> package_id >> factory_id
        
        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager[str(package_id)]
        factory = pkg.get_factory(str(factory_id))
        
        position = view.mapToScene(event.pos())
        try:
            node = factory.instantiate([view.observed().factory.get_id()])
            view.add_node(node, [position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return
        
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


def OpenAleaNodeDataPoolHandler(view, event):
    # Drag and Drop from the DataPool
    if(event.mimeData().hasFormat("openalea/data_instance")):
        pieceData = event.mimeData().data("openalea/data_instance")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)

        data_key = QtCore.QString()

        dataStream >> data_key
        data_key = str(data_key)

        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager["system"]
        factory = pkg.get_factory("pool reader")

        position = view.mapToScene(event.pos())

        # Set key val
        try:
            node = factory.instantiate([view.observed().factory.get_id()])
            view.add_node(node, [position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return

        node.set_input(0, data_key)
        node.set_caption("pool ['%s']"%(data_key,))

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


mimeFormats = ["openalea/nodefactory", "openalea/data_instance"]
mimeDropHandlers = [OpenAleaNodeFactoryHandler, OpenAleaNodeDataPoolHandler]
def get_drop_mime_handlers():
    return dict(zip(mimeFormats, mimeDropHandlers))



#################################
# node state drawing strategies #
#################################

class VisualeaPaintStrategyCommon:
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
        rect.setX( rect.x()+VisualeaPaintStrategyCommon.__margin__ )
        rect.setY( rect.y()+VisualeaPaintStrategyCommon.__v_margin__ )
        rect.setWidth( rect.width()-VisualeaPaintStrategyCommon.__margin__ )
        rect.setHeight( rect.height()-VisualeaPaintStrategyCommon.__v_margin__ )
        
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect,
                            VisualeaPaintStrategyCommon.__corner_radius__,
                            VisualeaPaintStrategyCommon.__corner_radius__)
        return path

    @classmethod
    def get_gradient(cls, widget):
        gradient = QtGui.QLinearGradient(0,0,0,100)
        gradient.setColorAt(0.0, cls.get_first_color(widget))
        gradient.setColorAt(0.8, cls.get_second_color(widget))
        return gradient

    @classmethod
    def get_first_color(cls, widget):
        return VisualeaPaintStrategyCommon.not_modified_color

    @classmethod
    def get_second_color(cls, widget):
        return VisualeaPaintStrategyCommon.not_selected_color

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
        return VisualeaPaintStrategyCommon.error_color

    @classmethod
    def get_second_color(cls, widget):
        return QtGui.QColor(255, 144, 0, 200)

class PaintErrorNode(PaintNormalNode):
    @classmethod
    def get_first_color(cls, widget):
        return VisualeaPaintStrategyCommon.error_color

    @classmethod
    def get_second_color(cls, widget):
        return VisualeaPaintStrategyCommon.not_selected_error_color
#         if(widget.isSelected()):
#             return VisualeaPaintStrategyCommon.selected_error_color
#         else:
#             return VisualeaPaintStrategyCommon.not_selected_error_color

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
    
