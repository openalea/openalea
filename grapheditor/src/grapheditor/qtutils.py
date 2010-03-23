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

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from PyQt4 import QtCore, QtGui


class AleaQGraphicsLabelWidget(QtGui.QGraphicsWidget):
    def __init__(self, label, parent=None):
        QtGui.QGraphicsWidget.__init__(self, parent)
        self.__label = QtGui.QGraphicsSimpleTextItem(self)
        font = self.__label.font()
        font.setBold(True)
        self.__label.setText(label)

    def boundingRect(self):
        return self.__label.boundingRect()

    def shape(self):
        return self.__label.shape()

    def size(self):
        return self.boundingRect().size()

    def sizeHint(self, blop, blip):
        return self.size()

    def setText(self, text):
        self.__label.setText(text)
        self.updateGeometry()

    def paint(self, painter, paintOpts, widget):
        self.__label.paint(painter, paintOpts, widget)

class AleaQGraphicsProxyWidget(QtGui.QGraphicsProxyWidget):
    """Embed a QWidget in a QGraphicsItem without the ugly background.

    When embedding for ex. a QLabel in a QGraphicsLayout using the normal
    QGraphicsProxyWidget, the QLabel is rendered with its ugly background
    and the custom drawing of the QGraphicsItem is hidden.
    This class overrides the painting routine or the QGraphicsProxyWidget
    to paint the child widget without the background.
    """
    def __init__(self, widget, parent=None):
        """
        Ctor.

        :Parameters:
	 - widget (QtGui.QWidget) - The QWidget to embed
	 - parent (QtGui.QGraphicsItem) - Reference to the parent.

        """
        QtGui.QGraphicsProxyWidget.__init__(self, parent)
        self.setWidget(widget)
        self.__noMouseEventForward = True

    def event(self, event):
        #needed or else it catches events before getting to the nodes in dataflowviews and
        #makes tooltips invisible.
        if(event.type()==QtCore.QEvent.GraphicsSceneHoverMove and self.__noMouseEventForward):
            event.ignore()
            return True
        return QtGui.QGraphicsProxyWidget.event(self, event)

    def setMouseEventForward(self, val):
        self.__noMouseEventForward = val

    def setWidget(self, widget):
        widget.setBackgroundRole(QtGui.QPalette.Background)
        widget.setAutoFillBackground(True)
        widget.setStyleSheet("background-color: transparent")
        QtGui.QGraphicsProxyWidget.setWidget(self, widget)


class AleaQMenu(QtGui.QMenu):
    def __init__(self, arg1=None, arg2=None):
        if isinstance(arg1, QtGui.QWidget):
            QtGui.QMenu.__init__(self, arg1)
        else:
            QtGui.QMenu.__init__(self, arg1, arg2)

    def move(self, pos):
        QtGui.QMenu.move(self, pos)
        rect = self.rect(); rect.moveTo(pos)
        #fix the position of the menu if it tries to popup too close to the lower & right edges.
        #bad fixing strategy probably: what if we were create arabian menus?
        #We should maube sublcass QMenu to handle screen real estate and reuse it.
        desktopGeom = QtGui.QApplication.desktop().availableGeometry(self.parent())
        contained, edges = qrect_contains(desktopGeom, rect, True)
        if not contained and edges.count(0) > 2:
            dx = edges[0] if edges[0] else edges[1]
            dy = edges[2] if edges[2] else edges[3]
            rect.translate(dx, dy)
            QtGui.QMenu.move(self,rect.topLeft())

def qrect_contains(r1, r2, proper):
    assert r1 is not None
    assert r2 is not None
    dl,dr,dt,db = [0]*4
    contains = False

    if r1.contains(r2, proper):
        contains = True
    elif r1.intersects(r2):
        if r2.left() < r1.left():
            dl = r1.left() - r2.left()
        if r2.right() > r1.right():
            dr = r1.right() - r2.right()
        if r2.top() < r1.top():
            dt = r1.top() - r2.top()
        if r2.bottom() > r1.bottom():
            db = r1.bottom() - r2.bottom()

    return contains, (dl,dr,dt,db)


def mixin_method(mixinOne, mixinTwo, methodname, firstWins = False, invert=False, caller=None):
    """A function that returns a method calling method \"methodname\"
    from mixinOne and then from mixinTwo, or the reverse order
    if invert is True.
    Can be used to quickly reimplement simple overloads.
    """

    first =  None
    second = None

    if(not invert):
        first = None if (mixinOne is None) else getattr(mixinOne, methodname, None)
        second = None if (mixinTwo is None) else getattr(mixinTwo, methodname, None)
    else:
        second = None if (mixinOne is None) else getattr(mixinOne, methodname, None)
        first = None if (mixinTwo is None) else getattr(mixinTwo, methodname, None)

    def simple_call(self, *args, **kwargs):
        return first(self, *args, **kwargs)

    def mixin_call(self, *args, **kwargs):
        v1 = first(self, *args, **kwargs)
        v2 = second(self, *args, **kwargs)
        if(firstWins): return v1
        else: return v2

    if(second and first is None):
        first = second
        second = None

    if(first and second is None):
        return simple_call
    else:
        return mixin_call


def extend_qt_scene_event(qtcls):
    def event_handler(self, event):
        t = event.type()
        if t == QtCore.QEvent.GraphicsSceneMouseMove:
            self.moveEvent(event)
        elif t == QtCore.QEvent.Show:
            self.polishEvent()
        return qtcls.sceneEvent(self, event)

    return event_handler
