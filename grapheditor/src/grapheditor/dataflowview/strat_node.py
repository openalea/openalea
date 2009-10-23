
import sys, numpy, weakref
from PyQt4 import QtCore, QtGui

from .. import gengraphview 
from .. import qtgraphview 

from openalea.core.observer import lock_notify


"""
This module implements a graphical node in several layers.
It was meant to try to use Qt at most and not to layout everything
by hand. It became a bit more complicated than expected.
"""


class AleaQtGraphicalNode(QtGui.QGraphicsItem, qtgraphview.QtGraphViewNode):

    #color of the small box that indicates evaluation
    eval_color = QtGui.QColor(255, 0, 0, 200)

    def __init__(self, node, parent=None):
        QtGui.QGraphicsItem.__init__(self, parent)
        qtgraphview.QtGraphViewNode.__init__(self, node)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(1)

        self.__child=AleaQtGraphicalNodeProxy(node, self)

        # ---Small box when the node is being evaluated---
        self.modified_item = QtGui.QGraphicsRectItem(5,5,7,7, self)
        self.modified_item.setBrush(self.eval_color)
        self.modified_item.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.modified_item.setVisible(False)

        # ---read existing data---
        self.initialise_from_model()


    def boundingRect(self):
        return self.__child.boundingRect()

    def paint(self, painter, paintOptions, widget):
        return self.__child.paint(painter, paintOptions, widget)


    ####################
    # Observer methods #
    ####################
    def notify(self, sender, event): 
        """ Notification sent by the node associated to the item """

        if(event and event[0] == "start_eval"):
            self.modified_item.setVisible(self.isVisible())
            self.modified_item.update()
            self.update()
            QtGui.QApplication.processEvents()

        elif(event and event[0] == "stop_eval"):
            self.modified_item.setVisible(False)
            self.modified_item.update()
            self.update()
            QtGui.QApplication.processEvents()

        qtgraphview.QtGraphViewNode.notify(self, sender, event)

    ###############
    # Controllers #
    ###############
    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """

        ret = QtGui.QGraphicsItem.itemChange(self, change, value)
        
        if (change == QtGui.QGraphicsItem.ItemPositionChange):                    
            point = value.toPointF()
            self.observed().get_ad_hoc_dict().set_metadata('position', 
                                                        [point.x(), point.y()],
                                                        False)
        try:
             #make the ports update their positions and
             #so make the edges update their drawing
            self.__child.widget().update_layout() 
        except:
            pass

        return ret


class AleaQtGraphicalNodeProxy(QtGui.QGraphicsProxyWidget):
    """ A proxy QGraphicsItem holding a QWidget. The actual widget is coded
    in AleaQtGraphicalNoderaphicalNodeWidget. """

    def __init__(self, node, parent=None):
        QtGui.QGraphicsProxyWidget.__init__(self, parent)
        self.observed = weakref.ref(node)
        widget = AleaQtGraphicalNodeWidget(node, None, self)
        widget.set_caption( node.internal_data["caption"] )
        self.setWidget(widget)

    ############
    # QT WORLD #
    ############
    def paint(self, painter, paintOptions, widget):
        #NEEDED TO OVERLOAD THIS TO GET RID OF THE UGLY BACKGROUND
        #AROUND THE WIDGET.
        self.widget().render(painter, QtCore.QPoint(), QtGui.QRegion(), 
                             QtGui.QWidget.RenderFlags()|QtGui.QWidget.DrawChildren)

    def polishEvent(self):
        self.widget().update_layout()



class AleaQtGraphicalNodeWidget(QtGui.QWidget):
    """ Represents a node in the graph widget. """
    
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

    def __init__(self, vertex, parent=None, container=None):
        QtGui.QWidget.__init__(self, parent)

        #pointer to the QGraphicsItem needed for absolute position computation.
        self._container = weakref.ref(container) 
        self.observed = weakref.ref(vertex)

        # ---Qt stuff---        
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setSpacing(2)

        self._inConnectorLayout = QtGui.QHBoxLayout()
        self._outConnectorLayout = QtGui.QHBoxLayout()
        self._caption = QtGui.QLabel()
        self._caption.setSizePolicy(QtGui.QSizePolicy.Fixed, 
                                    QtGui.QSizePolicy.Fixed)

        self.layout().addLayout(self._inConnectorLayout)
        self.layout().addWidget(self._caption)
        self.layout().addLayout(self._outConnectorLayout)

        self._inConnectorLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self._outConnectorLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self._inConnectorLayout.setSpacing(8)
        self._outConnectorLayout.setSpacing(8)

        self.layout().setAlignment(self._caption, QtCore.Qt.AlignHCenter)

        #do the port layout
        self.__layout_ports()


    def update_layout(self):
        for cId in range(self._inConnectorLayout.count()):
            self._inConnectorLayout.itemAt(cId).widget().update_meta_canvas_position()
        for cId in range(self._outConnectorLayout.count()):
            self._outConnectorLayout.itemAt(cId).widget().update_meta_canvas_position()

    def __layout_ports(self):
        """ Add connectors """
        self.nb_cin = 0
        for i,desc in enumerate(self.observed().input_desc):
            self.add_in_connection(i, desc)
                
        for i,desc in enumerate(self.observed().output_desc):
            self.add_out_connection(i, desc)

    def get_container(self):
        return self._container()

    def set_caption(self, caption):
        self._caption.setText(caption)

    def add_in_connection(self, index, connector):
        self._inConnectorLayout.addWidget(AleaQtGraphicalConnector(self, index, connector))

    def add_out_connection(self, index, connector):
        self._outConnectorLayout.addWidget(AleaQtGraphicalConnector(self, index, connector))

    def remove_in_connection(self, index):
        pass

    def remove_out_connection(self, index):
        pass

    def paintEvent(self, paintEvent):
        size = self.size()
        painter = QtGui.QPainter(self)
        
        rect = QtCore.QRectF( self.rect() )

        #the drawn rectangle is smaller than
        #the actual widget size
        rect.setX( rect.x()+self.__margin__ )
        rect.setY( rect.y()+self.__v_margin__ )
        rect.setWidth( rect.width()-self.__margin__ )
        rect.setHeight( rect.height()-self.__v_margin__ )

        painter.setBackgroundMode(QtCore.Qt.TransparentMode)

        #let's figure out how to paint our box:
        color = self.not_selected_color
        secondColor = self.not_modified_color

        #user defined colors
        if self.observed().get_ad_hoc_dict().get_metadata("use_user_color"):
            color = QtGui.QColor(*self.observed().get_ad_hoc_dict().get_metadata("user_color"))
            secondColor = color

        #error state colors
        elif self.observed().internal_data.get("is_in_error_state", False):
            color = self.error_color
            if(self._container().isSelected()):
                secondColor = self.selected_error_color
            else:
                secondColor = self.not_selected_error_color

        #non error state colors
        elif self._container().isSelected():
            color = self.selected_color
        elif self.observed().internal_data.get("is_user_application", False):
            secondColor = QtGui.QColor(255, 144, 0, 200)
            

        # Shadow
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(100, 100, 100, 50))
        painter.drawRoundedRect(rect,
                                self.__corner_radius__,
                                self.__corner_radius__)

        # Draw Box
        gradient = QtGui.QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, color)
        gradient.setColorAt(0.8, secondColor)
        painter.setBrush(QtGui.QBrush(gradient))
        
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.drawRoundedRect(rect,
                                self.__corner_radius__,
                                self.__corner_radius__)


        if self.observed().internal_data.get("block", False):
            painter.setBrush(QtGui.QBrush(QtCore.Qt.BDiagPattern))
            painter.drawRoundedRect(rect,
                                    self.__corner_radius__,
                                    self.__corner_radius__)

        QtGui.QWidget.paintEvent(self, paintEvent)




    











class AleaQtGraphicalConnector(QtGui.QWidget):
    """ A node connector """
    WIDTH =  10
    HEIGHT = 10

    def __init__(self, parent, index, connector):
        """
        """
        
        QtGui.QWidget.__init__(self, parent)
        self.__index = index

        self.observed = weakref.ref(connector)
        self.edge_list = [] #used to refresh edges when connector moves.
        connector.get_ad_hoc_dict().add_metadata("canvasPosition", list)
        connector.set_id(index)

    def canvas_position(self):
        pos = QtCore.QPointF(self.rect().center()) + QtCore.QPointF(self.pos()) + \
            QtCore.QPointF(self.parent().get_container().scenePos())
        return[pos.x(), pos.y()]
        
    def update_meta_canvas_position(self):
        self.observed().get_ad_hoc_dict().set_metadata("canvasPosition", 
                                                    self.canvas_position())
        
    def get_index(self):
        return self.__index

    ##################
    # QtWorld-Layout #
    ##################

    def size(self):
        return QtCore.QSize(self.WIDTH, self.HEIGHT)

    def sizeHint(self):
        return QtCore.QSize(self.WIDTH, self.HEIGHT)

    def minimumSizeHint(self):
        return QtCore.QSize(self.WIDTH, self.HEIGHT)

    def sizePolicy(self):
        return QtGui.QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    ##################
    # QtWorld-Events #
    ##################

    def mousePressEvent(self, event):
        graphview = self.parent().get_container().scene().views()[0]
        if (graphview and event.buttons() & QtCore.Qt.LeftButton):
            graphview.new_edge_start(self.canvas_position())
            return
        #QtGui.QWidget.mousePressEvent(self, event)
        #event.setAccepted(False)

    def mouseMoveEvent(self, event):
        "connector mouseMoveEvent"


    def paintEvent(self, paintEvent):
        size = self.size()
        painter = QtGui.QPainter(self)
        
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        gradient = QtGui.QLinearGradient(0, 0, 10, 0)
        gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
        gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        painter.drawEllipse(1,1,size.width()-2,size.height()-2)
