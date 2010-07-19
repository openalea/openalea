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


import weakref, traceback
from PyQt4 import QtCore, QtGui




#-- Simple layouts for QGraphicsItems --
class Layout(object):
    def __init__(self, parent=None, final=None, margins=(0.,0.,0.,0.),
                 innerMargins=(0.,0.), center=False, mins=(0.,0.)):
        self._parent = parent
        self._final = final
        self._x1, self._x2, self._y1, self._y2 = margins
        self._ix1, self._iy1 = innerMargins
        self._center = center
        self._minWidth, self._minHeight = mins
        self._boundCache = None
        self._items = []
        if parent:
            parent.addItem(self)

    def clear(self):
        self._items = []
        self._final = None

    def __add__(self, other):
        return self._items + other._items

    def __iter__(self):
        return self._items.__iter__()

    def __contains__(self, item):
        return self._items.__contains__(item)

    def center(self, val):
        self._center = val

    def sort(self, cmp):
        self._items.sort(cmp)

    def addFinalItem(self, item):
        self._final = item

    def addItem(self, item):
        self._items.append(item)

    def removeItem(self, item):
        self._items.remove(item)

    def boundingRect(self, force=True):
        if force or self._boundCache is None:
            x, y, w, h = self._boundingRect()
            w = max(w, self._minWidth)
            h = max(h, self._minHeight)
            self._boundCache = QtCore.QRectF(x, y, w, h)
            if self._parent:
                self._parent.boundCache = None
        return self._boundCache

    def _boundingRect(self):
        raise NotImplementedError

    def setPos(self, pos):
        raise NotImplementedError

    def setMinimumSize(width=None, height=None):
        if width: self._minWidth = width
        if height: self._minHeight = height

    def setMargins(self, x1=None, x2=None,
                   y1=None, y2=None):
        if x1: self._x1=x1
        if x2: self._x2=x2,
        if y1: self._y1=y1
        if y2: self._y2=y2

    def setInnerMargins(self, ix1=None,
                        iy1=None):
        if ix1: self._ix1=ix1
        if iy1: self._iy1=iy1

    def isVisible(self):
        return True

class HorizontalLayout(Layout):
    def _boundingRect(self):
        width = self._x1 + self._x2
        height = self._y1 + self._y2
        geoms = [i.boundingRect() for i in self._items if i.isVisible()]
        lenGeoms = len(geoms)
        if lenGeoms>0:
            width  += sum( g.width() for g in geoms ) + (lenGeoms-1)*self._ix1
            height += max( g.height() for g in geoms )
        if self._final and self._final.isVisible():
            width  += self._final.boundingRect().width()
            height = max( height, self._final.boundingRect().height() )
        return 0., 0., width, height

    def setPos(self, pos):
        offset = pos + QtCore.QPointF(self._x1, self._y1)
        innerOffset = QtCore.QPointF(self._ix1, self._iy1)
        items = (i for i in self._items if i.isVisible())
        selfHeight = self.boundingRect(force=False).height()
        for it in items:
            itRect = it.boundingRect()
            if self._center:
                offset.setY(offset.y() + (selfHeight - itRect.height())/2.)
            it.setPos(offset)
            offset += QtCore.QPointF(itRect.width(), 0.) + innerOffset
        if self._final and self._final.isVisible():
            if self._center:
                offset.setY((selfHeight - self._final.boundingRect().height())/2.)
            self._final.setPos(offset)

class VerticalLayout(Layout):
    def _boundingRect(self):
        width = self._x1 + self._x2
        height = self._y1 + self._y2
        geoms = [i.boundingRect() for i in self._items if i.isVisible()]
        lenGeoms = len(geoms)
        if lenGeoms>0:
            width  += max( g.width() for g in geoms )
            height += sum( g.height() for g in geoms ) + (lenGeoms-1)*self._iy1
        if self._final and self._final.isVisible():
            width  = max(width, self._final.boundingRect().width())
            height += self._final.boundingRect().height()
        return 0., 0., width, height

    def setPos(self, pos):
        offset = pos + QtCore.QPointF(self._x1, self._y1)
        innerOffset = QtCore.QPointF(self._ix1, self._iy1)
        items = (i for i in self._items if i.isVisible())
        selfWidth = self.boundingRect(force=False).width()
        for it in items:
            itRect = it.boundingRect()
            if self._center:
                offset.setX((selfWidth - itRect.width())/2.)
            it.setPos(offset)
            offset += QtCore.QPointF(0., itRect.height()) + innerOffset
        if self._final and self._final.isVisible():
            if self._center:
                offset.setX((selfWidth - self._final.boundingRect().width())/2.)
            self._final.setPos(offset)



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
        rect = QtCore.QRect(pos, self.sizeHint())
        #fix the position of the menu if it tries to popup too close to the lower & right edges.
        #bad fixing strategy probably: what if we were create arabian menus?
        #We should maube sublcass QMenu to handle screen real estate and reuse it.
        desktopGeom = QtGui.QApplication.desktop().availableGeometry(self.parent())
        contained, edges = qrect_contains(desktopGeom, rect, True)
        if not contained and edges.count(0) > 0:
            dx = edges[0] if edges[0] else edges[1]
            dy = edges[2] if edges[2] else edges[3]
            rect.translate(dx, dy)
            QtGui.QMenu.move(self,rect.topLeft())
            return
        else:
            QtGui.QMenu.move(self, pos)


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
