# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#       Original code from visualea.compositenode_widget
#       (Samuel Dufour Kowalski, Christophe Pradal)
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from Qt import QtCore, QtGui, QtWidgets

# def EdgeFactory():
#     try:
#         settings = Settings()
#         style = settings.get('UI', 'EdgeStyle')
#     except:
#         style = 'Spline'

#     if style == 'Line':
#         return LinearEdgePath()
#     elif style == 'Polyline':
#         return PolylineEdgePath()
#     else:
#         return SplineEdgePath()


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
