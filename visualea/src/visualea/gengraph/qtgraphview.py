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
    
    def __init__(self, observed=None):
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
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
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


    def get_scene(self):
        return self.scene()

    ##################
    # QtWorld-Events #
    ##################
    def wheelEvent(self, event):
        self.centerOn(self.mapToScene(event.globalPos()))
        delta = -event.delta() / 1200.0 + 1.0
        self.scale(delta, delta)
        QtGui.QGraphicsView.wheelEvent(self, event)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsView.mouseMoveEvent(self, event)
        if(self.is_creating_edge()):
            pos = self.mapToScene(event.pos())
            self.new_edge_set_destination(pos.x(), pos.y())
            return

    def mouseReleaseEvent(self, event):
        if(self.is_creating_edge()):
            self.new_edge_end()
        QtGui.QGraphicsView.mouseReleaseEvent(self, event)

    #########################
    # Other utility methods #
    #########################
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

    def new_edge_scene_cleanup(self, edge):
        self.scene().removeItem(edge)

    def new_edge_scene_init(self, edge):
        self.scene().addItem(edge)

        





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
