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

class QtGraphViewElement(gengraphview.GraphViewElement):
    """Base class for elements in a GraphView"""

    ############################
    # Class members come first #
    ############################
    __state_drawing_strategies__={}

    @classmethod
    def add_drawing_strategies(cls, d):
        cls.__state_drawing_strategies__.update(d)

    @classmethod
    def get_drawing_strategy(cls, state):
        return cls.__state_drawing_strategies__.get(state)

    ############################
    # Instance members follow  #
    ############################    
    def __init__(self, observed=None):
        """Ctor"""
        gengraphview.GraphViewElement.__init__(self, observed)

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

    def initialise_from_model(self):
        self.observed().get_ad_hoc_dict().simulate_full_data_change()

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



class QtGraphViewNode(QtGraphViewElement):
    """A Node widget should implement this interface"""

    def __init__(self, vertex):
        QtGraphViewElement.__init__(self, vertex)
        return



class QtGraphViewAnnotation(QtGraphViewElement):
    """A Node widget should implement this interface"""

    def __init__(self, annotation):
        QtGraphViewElement.__init__(self, annotation)
        return

    def set_text(self, text):
        """to change the visible text"""
        raise NotImplementedError

    def notify(self, sender, event):
        if(event[0] == "MetaDataChanged"):
            if(event[1]=="text"):
                if(event[2]): self.set_text(event[2])

        QtGraphViewElement.notify(self, sender, event)

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

        return

    def update_line_source(self, *pos):
        """updates this edge's starting point. Called when
        source point is moved"""
        raise NotImplementedError

    def update_line_destination(self, *pos):
        """updates this edge's ending point. Called when
        dest point is moved"""
        raise NotImplementedError

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
        #self.setViewportUpdateMode(QtGui.QGraphicsView.SmartViewportUpdate)

    def clear_scene(self):
        """ Remove all items from the scene """
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.setScene(scene)

    def new_edge_scene_cleanup(self, graphicalEdge):
        self.scene().removeItem(graphicalEdge)

    def new_edge_scene_init(self, graphicalEdge):
        self.scene().addItem(graphicalEdge)

        





#################
# MOVE THIS OUT #
#################
def edge_factory():
    try:
        settings = Settings()
        style = settings.get('UI', 'EdgeStyle')
    except:
        style = 'Spline'

    if style == 'Line':
        return LinearEdgePath()
    elif style == 'Polyline':
        return PolylineEdgePath()
    else:
        return SplineEdgePath()


class LinearEdgePath(object):
    """ Draw edges as line. """
    def __init__(self): 
        self.p1 = QtCore.QPointF()
        self.p2 = QtCore.QPointF()

    def shape(self):
        path = QtGui.QPainterPath()

        # Enlarge selection zone
        diff = self.p2 - self.p1

        if( abs(diff.x()) > abs(diff.y())):
            dp = QtCore.QPointF(0, 10)
        else:
            dp = QtCore.QPointF(10, 0)
        
        p1 = self.p1 - dp
        p2 = self.p1 + dp
        p3 = self.p2 + dp
        p4 = self.p2 - dp
        poly = QtGui.QPolygonF([p1, p2, p3, p4])
        path.addPolygon(poly)
        
        return path

    def get_path( self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        path = QtGui.QPainterPath(self.p1)
        path.lineTo(self.p2)
        return path

        
class PolylineEdgePath(LinearEdgePath):
    """ Edge as Polyline """
    WIDTH = 30
    def __init__(self): 
        LinearEdgePath.__init__(self)

    def shape(self):
        return None

    def get_path( self, p1, p2 ):
        self.p1 = p1
        self.p2 = p2
        path = QtGui.QPainterPath(self.p1)

        points = []

        sd= self.p2 - self.p1
        if abs(sd.x()) <= self.WIDTH: # draw a line
            pass
        elif sd.y() < 2 * self.WIDTH:
            s1 = self.p1 + QtCore.QPointF(0,self.WIDTH)
            d1 = self.p2 - QtCore.QPointF(0,self.WIDTH)

            s1d1= d1 -s1
            s2 = s1 + QtCore.QPointF(s1d1.x() / 2., 0)
            d2 = s2 + QtCore.QPointF(0, s1d1.y())
            points.extend([s1, s2, d2, d1])
        else:
            s1 = self.p1 + QtCore.QPointF(0, sd.y() / 2.)
            d1= self.p2 - QtCore.QPointF(0, sd.y() / 2.)
            points.extend([s1, d1])
        
        points.append(self.p2)
        for pt in points:
            path.lineTo(pt)

        return path


class SplineEdgePath(PolylineEdgePath):
    """ Edge as Spline """
    
    def __init__(self): 
        PolylineEdgePath.__init__(self)

    def get_path( self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        path = QtGui.QPainterPath(self.p1)

        sd= self.p2- self.p1
        if abs(sd.x()) <= self.WIDTH: # draw a line
            path.lineTo(self.p2)
        elif sd.y() < self.WIDTH: 
            py = QtCore.QPointF(0, max(self.WIDTH, - sd.y()))
            path.cubicTo(self.p1 + py, self.p2 - py, self.p2)

        else:
            py = QtCore.QPointF(0, sd.y() / 2.)
            pm = (self.p1 + self.p2) / 2.
            path.quadTo(self.p1 + py, pm)
            path.quadTo(self.p2 - py, self.p2)

        return path
