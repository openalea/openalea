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



import weakref
from PyQt4 import QtGui, QtCore
from openalea.core.settings import Settings

import gengraphview
import edgefactory


#------*************************************************------#
class QtGraphViewElement(gengraphview.GraphViewElement):
    """Base class for elements in a GraphView"""

    ####################################
    # ----Instance members follow----  #
    ####################################    
    def __init__(self, observed=None):
        """Ctor"""
        gengraphview.GraphViewElement.__init__(self, observed)

    #################################
    # IGraphViewElement realisation #
    #################################       
    def add_to_view(self, view):
        view.addItem(self)

    def remove_from_view(self, view):
        view.removeItem(self)

    def notify(self, sender, event):
        """called by the observed when something happens
        to it."""
        if(event[0] == "MetaDataChanged"):
            if(event[1]=="position"):
                if(event[2]): 
                    self.position_changed(event[2][0], event[2][1])

    def position_changed(self, *args):
        """called when the position of the widget changes"""
        point = QtCore.QPointF(args[0], args[1])
        self.setPos(point)




#------*************************************************------#
class QtGraphViewNode(QtGraphViewElement):
    """A Node widget should implement this interface"""
    ####################################
    # ----Class members come first---- #
    ####################################
    __state_drawing_strategies__={}

    @classmethod
    def add_drawing_strategies(cls, d):
        cls.__state_drawing_strategies__.update(d)

    @classmethod
    def get_drawing_strategy(cls, state):
        return cls.__state_drawing_strategies__.get(state)


    ####################################
    # ----Instance members follow----  #
    ####################################    
    def __init__(self, vertex):
        QtGraphViewElement.__init__(self, vertex)
        return

    #####################
    # ----Qt World----  #
    #####################
    # ---> state-based painting
    def select_drawing_strategy(self, state):
        return self.get_drawing_strategy(state)

    def paint(self, painter, option, widget):
        paintEvent=None #remove this
        path=None
        firstColor=None
        secondColor=None
        gradient=None

        state = self.observed().get_state()

        #try to get a strategy for this state ...
        strategy = self.select_drawing_strategy(state)
        if(strategy):
            path = strategy.get_path(self)
            gradient=strategy.get_gradient(self)
            #the gradient is already defined, no need for colors
            if(not gradient):
                firstColor=strategy.get_first_color(self)
                secondColor=strategy.get_second_color(self)
        else: #...or fall back on defaults
            rect = QtCore.QRectF( self.rect() )

            #the drawn rectangle is smaller than
            #the actual widget size
            rect.setX( rect.x()+self.__margin__ )
            rect.setY( rect.y()+self.__v_margin__ )
            rect.setWidth( rect.width()-self.__margin__ )
            rect.setHeight( rect.height()-self.__v_margin__ )

            path = QtGui.QPainterPath()
            path.addRoundedRect(rect,
                                self.__corner_radius__,
                                self.__corner_radius__)
            firstColor = self.not_selected_color
            secondColor = self.not_modified_color

        if(not gradient):
            gradient = QtGui.QLinearGradient(0, 0, 0, 100)
            gradient.setColorAt(0.0, firstColor)
            gradient.setColorAt(0.8, secondColor)


        #PAINTING
        #painter = QtGui.QPainter(self)
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        if(strategy):
            strategy.prepaint(self, paintEvent, painter, state)
        #shadow drawing:
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(100, 100, 100, 50))
        painter.drawPath(path)
        #item drawing
        painter.setBrush(QtGui.QBrush(gradient))        
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.drawPath(path)

        if(strategy):
            strategy.postpaint(self, paintEvent, painter, state)

        #selection marker is drawn at the end
        if(self.isSelected()):
            painter.setPen(QtCore.Qt.DashLine)
            painter.setBrush(QtGui.QBrush())
            painter.drawRect(self.rect())

    # ---> other events
    def polishEvent(self):
        point = self.scenePos()
        self.observed().get_ad_hoc_dict().set_metadata('position', 
                                                        [point.x(), point.y()], False)
        QtGui.QGraphicsWidget.polishEvent(self)

    def moveEvent(self, event):
        point = event.newPos()
        self.observed().get_ad_hoc_dict().set_metadata('position', 
                                                        [point.x(), point.y()], False)
        QtGui.QGraphicsWidget.moveEvent(self, event)    

    def mousePressEvent(self, event):
        graphview = self.scene().views()[0]
        if (graphview and event.buttons() & QtCore.Qt.LeftButton):
            pos = event.posF().x(), event.posF.y()
            graphview.new_edge_start(pos)
            return



#------*************************************************------#
class QtGraphViewAnnotation(QtGraphViewElement):
    """A Node widget should implement this interface"""

    def __init__(self, annotation):
        QtGraphViewElement.__init__(self, annotation)
        return

    def set_text(self, text):
        """to change the visible text, not the model text"""
        raise NotImplementedError

    def notify(self, sender, event):
        if(event[0] == "MetaDataChanged"):
            if(event[1]=="text"):
                if(event[2]): self.set_text(event[2])

        QtGraphViewElement.notify(self, sender, event)

    ############
    # Qt World #
    ############
    # ---->controllers
    def mouseDoubleClickEvent(self, event):
        """ todo """
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setSelected(True)
        self.setFocus()
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        self.setTextCursor(cursor)

    def focusOutEvent(self, event):
        """ todo """
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, False)

        # unselect text
        cursor = self.textCursor ()
        if(cursor.hasSelection()):
            cursor.clearSelection()
            self.setTextCursor(cursor)
            
        self.observed().get_ad_hoc_dict().set_metadata('text', str(self.toPlainText()))

        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)


#------*************************************************------#
class QtGraphViewEdge(QtGraphViewElement):
    """Base class for Qt based edges."""

    def __init__(self, edge=None, src=None, dest=None):
        QtGraphViewElement.__init__(self, edge)

        self.setFlag(QtGui.QGraphicsItem.GraphicsItemFlag(
            QtGui.QGraphicsItem.ItemIsSelectable))
        
        self.src = None
        self.dst = None

        if(src)  : 
            self.initialise(src)
            self.src = weakref.ref(src)
        if(dest) : 
            self.initialise(dest)
            self.dst = weakref.ref(dest)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()

        self.edge_path = edgefactory.EdgeFactory()
        path = self.edge_path.get_path(self.sourcePoint, self.destPoint)
        self.setPath(path)

        self.setPen(QtGui.QPen(QtCore.Qt.black, 3,
                               QtCore.Qt.SolidLine,
                               QtCore.Qt.RoundCap,
                               QtCore.Qt.RoundJoin))

    def shape(self):
        path = self.edge_path.shape()
        if not path:
            return QtGui.QGraphicsPathItem.shape(self)
        else:
            return path
        
    def __update_line(self):
        path = self.edge_path.get_path(self.sourcePoint, self.destPoint)
        self.setPath(path)

    def update_line_source(self, *pos):
        self.sourcePoint = QtCore.QPointF(*pos)
        self.__update_line()

    def update_line_destination(self, *pos):
        self.destPoint = QtCore.QPointF(*pos)
        self.__update_line()

    def notify(self, sender, event):
        if(event[0] == "MetaDataChanged"):
            if(event[1]=="canvasPosition" or event[1]=="position"):
                    pos = event[2]
                    if(sender==self.src()): 
                        self.update_line_source(*pos)
                    elif(sender==self.dst()):
                        self.update_line_destination(*pos)

    def initialise_from_model(self):
        self.src().get_ad_hoc_dict().simulate_full_data_change()
        self.dst().get_ad_hoc_dict().simulate_full_data_change()


    def remove(self):
        view = self.scene().views()[0]
        view.observed().disconnect(self.src().node().get_id(), self.src().get_id(),
                                   self.dst().node().get_id(), self.dst().get_id())
        

    ############
    # Qt World #
    ############
    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """

        if (change == QtGui.QGraphicsItem.ItemSelectedChange):
            if(value.toBool()):
                color = QtCore.Qt.blue
            else:
                color = QtCore.Qt.black

            self.setPen(QtGui.QPen(color, 3,
                                   QtCore.Qt.SolidLine,
                                   QtCore.Qt.RoundCap,
                                   QtCore.Qt.RoundJoin))
                
        return QtGui.QGraphicsItem.itemChange(self, change, value)



class QtGraphViewFloatingEdge( QtGraphViewEdge ):
    def __init__(self, srcPoint):
        QtGraphViewEdge.__init__(self, None, None, None)
        self.sourcePoint = QtCore.QPointF(*srcPoint)

    def notify(self, sender, event):
        return

    def consolidate(self, model):
        try:
            srcNode, dstNode = self.get_connections()
            model.connect(srcNode, dstNode)
        except Exception, e:
            print "consolidation failed :", e
        return
        
    def get_connections(self):
        #find the node items that were activated
        srcNodeItem = self.scene().itemAt( self.sourcePoint )
        dstNodeItem = self.scene().itemAt( self.destPoint   )

        #if the input and the output are on the same node...
        if(srcNodeItem == dstNodeItem):
            raise Exception("Nonsense connection : plugging self to self.")            

        return srcNodeItem.observed(), dstNodeItem.observed()




#------*************************************************------#
class QtGraphView(QtGui.QGraphicsView, gengraphview.GraphView):
    """A Qt implementation of GraphView    """

    def __init__(self, parent, graph):
        QtGui.QGraphicsView.__init__(self, parent)
        gengraphview.GraphView.__init__(self, graph)

        scene = QtGui.QGraphicsScene(self)
        #scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.setScene(scene)

        # ---Qt Stuff---
        #self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.rebuild_scene()

        # ---Other stuff used for the user experience---
        self.__mimeHandlers={}
        self.__pressHotkeyMap={}
        self.__releaseHotkeyMap={}

    def get_scene(self):
        return self.scene()

    ##################
    # QtWorld-Events #
    ##################
    def wheelEvent(self, event):
        self.centerOn(QtCore.QPointF(event.pos()))
        delta = -event.delta() / 2400.0 + 1.0
        self.scale_view(delta)

    def mouseMoveEvent(self, event):
        if(self.is_creating_edge()):
            pos = self.mapToScene(event.pos())
            self.new_edge_set_destination(pos.x(), pos.y())
            return
        QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if(self.is_creating_edge()):
            self.new_edge_end()
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)

    def acceptEvent(self, event):
        """ Return True if event is accepted """
        for format in self.__mimeHandlers.keys():
            if event.mimeData().hasFormat(format): return True
        return False

    def dragEnterEvent(self, event):
        event.setAccepted(self.acceptEvent(event))
            
    def dragMoveEvent(self, event):
        if (self.acceptEvent(event)):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for format in event.mimeData().formats():
            format = format.toUtf8().data()
            handler = self.__mimeHandlers.get(format)
            if(handler):
                handler(self, event)
                return
            else:
                continue
        QtGui.QGraphicsView.dropEvent(self, event)

    def keyPressEvent(self, e):
        combo = e.modifiers().__int__(), e.key()
        action = self.__pressHotkeyMap.get(combo)
        if(action):
            action.press(self, event)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, e)

    def keyReleaseEvent(self, e):
        combo = e.modifiers().__int__(), e.key()
        action = self.__releaseHotkeyMap.get(combo)
        if(action):
            action.release(self, event)
        else:
            QtGui.QGraphicsView.keyReleaseEvent(self, e)


    #########################
    # Other utility methods #
    #########################
    def set_mime_handler_map(self, mapping):
        self.__mimeHandlers = mapping

    def get_mime_handler_map(self):
        return self.__mimeHandlers

    def set_keypress_handler_map(self, mapping):
        self.__pressHotkeyMap = mapping

    def get_keypress_handler_map(self):
        return self.__pressHotkeyMap

    def set_keyrelease_handler_map(self, mapping):
        self.__releaseHotkeyMap = mapping

    def get_keyrelease_handler_map(self):
        return self.__releaseHotkeyMap

    def scale_view(self, factor):
        self.scale(factor, factor)

    def rebuild_scene(self):
        """ Build the scene with graphic node and edge"""
        self.clear_scene()
        self.observed().simulate_construction_notifications()

    def clear_scene(self):
        """ Remove all items from the scene """
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.setScene(scene)

    def new_edge_scene_cleanup(self, graphicalEdge):
        self.scene().removeItem(graphicalEdge)

    def new_edge_scene_init(self, graphicalEdge):
        self.scene().addItem(graphicalEdge)
