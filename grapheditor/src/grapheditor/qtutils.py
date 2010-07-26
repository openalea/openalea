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


import weakref
from PyQt4 import QtCore, QtGui


##################################################################################
# Some PYQT versions don't know about some QGraphicsItem flags or enums yet      #
# even though the underlying Qt knows about it (.sip files not up-to-date        #
# when building PyQt). The differences between PYQT_VERSION 4.6.2 and 4.7.3 are: #
##################################################################################
unportableFlags = ['ItemSendsGeometryChanges', 'ItemUsesExtendedStyleOption',
                   'ItemScenePositionHasChanged', 'ItemAcceptsInputMethod', 'ItemSendsScenePositionChanges',
                   'ItemHasNoContents', 'ItemNegativeZStacksBehindParent', 'ItemIsPanel']
unportableEnums = ["ItemScenePositionHasChanged", "ItemPositionHasChanged"]

__dict__ = globals()
for f in unportableFlags+unportableEnums:
    try:
        __dict__[f] = getattr(QtGui.QGraphicsItem, f)
    except Exception, e:
        print "symbol not found:", f
        continue

# if it's just the PyQt Version that is too old we have a hack as
# the qt flag exists but is simply not exposed.
# this is not bug free: if the Qt guys change the enum order, we're wrecked.
if QtCore.PYQT_VERSION < 0x040703 and QtCore.PYQT_VERSION >= 0x040600:
    # -- flags --
    ItemSendsGeometryChanges = 0x800
    ItemSendsScenePositionChanges = 0xffff
    # -- enums --
    ItemScenePositionHasChanged = 0x1b
    ItemPositionHasChanged = 0x9


#####################################################
# A Global to know if using QGraphicsEffect is safe #
#####################################################
safeEffects = QtCore.QT_VERSION >= 0x40600 and QtCore.PYQT_VERSION > 0x40704


#######################################
# A very simple signal implementation #
#######################################
class AleaSignal(object):
    def __init__(self, *types):
        self.types     = types
        self.callbacks = weakref.WeakKeyDictionary()
    def connect(self, callback):
        self.callbacks[callback] = callback
    def emit(self, *args):
        # do type checking?
        callbacks = self.callbacks.values()[:]
        for c in callbacks:
            c(*args)

###############################################
# A Vanishing GraphicsItem mixing. Appears on #
# hover in and vanishes on hover out          #
###############################################
class AleaQGraphicsVanishingMixin(object):
    __baseOpacity = 0.01
    __numFrames   = 24

    def __init__(self, vanishingTime=500):
        self.setAcceptHoverEvents(True)
        self.setOpacity(self.__baseOpacity)
        self.__vanEnabled = True
        self.__vanishingTime = vanishingTime
        self.__timer = QtCore.QTimeLine(vanishingTime)
        self.__timer.setFrameRange(0, self.__numFrames)
        self.__timer.frameChanged.connect(self.__onFrameChanged)
        self.setOpacity(self.__baseOpacity)

    def __onFrameChanged(self, frame):
        frame -= 1
        opacity = (1-self.__baseOpacity)*(self.__numFrames-frame)/self.__numFrames + self.__baseOpacity
        self.setOpacity(opacity)

    def setVanishingEnabled(self, val):
        self.__vanEnabled = val
        if val == True:
            if self.__timer.state() == QtCore.QTimeLine.Running:
                if self.__timer.direction == QtCore.QTimeLine.Backward:
                    self.appear()
                else:
                    self.disappear()
        else:
            self.setOpacity(1)

    def setVanishingTime(self, time):
        self.__vanishingTime = time
        self.__timer.setDuration(time)

    def vanishingTime(self):
        return self.__vanishingTime

    def appear(self):
        if not self.__vanEnabled:
            return
        state = self.__timer.state()
        self.__timer.setDuration(self.__vanishingTime/10)
        if state  == QtCore.QTimeLine.Running:
            self.__timer.setDirection(QtCore.QTimeLine.Backward)
        elif state == QtCore.QTimeLine.NotRunning:
            self.__timer.setCurrentTime(self.__timer.duration())
            self.__timer.setDirection(QtCore.QTimeLine.Backward)
            self.__timer.start()

    def disappear(self):
        if not self.__vanEnabled:
            return
        state = self.__timer.state()
        self.__timer.setDuration(self.__vanishingTime)
        if state  == QtCore.QTimeLine.Running:
            self.__timer.setDirection(QtCore.QTimeLine.Forward)
        elif state == QtCore.QTimeLine.NotRunning:
            self.__timer.setCurrentTime(0)
            self.__timer.setDirection(QtCore.QTimeLine.Forward)
            self.__timer.start()

    def hoverEnterEvent(self, event):
        self.appear()

    def hoverLeaveEvent(self, event):
        self.disappear()

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, event)
        color = QtGui.QColorDialog.getColor(parent=event.widget())
        if color.isValid():
            self.colorChanged.emit(color)


###########################################
# A button like mixin for qgraphics items #
###########################################
class AleaQGraphicsButtonMixin(object):
    def __init__(self):
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.pressed = AleaSignal()

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, event)
        self.pressed.emit()

########################
# A horizontal toolbar #
########################
class AleaQGraphicsToolbar(QtGui.QGraphicsRectItem, AleaQGraphicsVanishingMixin):
    def __init__(self, parent=None):
        QtGui.QGraphicsRectItem.__init__(self, parent)
        AleaQGraphicsVanishingMixin.__init__(self)
        self.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True)
        self.__layout = HorizontalLayout(parent=None, margins=(2.,2.,2.,2.),
                                         innerMargins=(1.,1.), center=True,
                                         mins=(20.,20.))

    def refreshGeometry(self):
        rect = self.__layout.boundingRect(force=True)

        self.__layout.setPos(QtCore.QPointF(0.,0.))
        self.setRect(rect)

    def addItem(self, item):
        self.__layout.addItem(item)


#############################################################
# Customized Qt Classes that can be reused in other places. #
#############################################################
class AleaQGraphicsEmitingTextItem(QtGui.QGraphicsTextItem):
    """A QtGui.QGraphicsTextItem that emits geometryModified whenever
    its geometry can have changed."""

    ######################
    # The Missing Signal #
    ######################
    geometryModified = QtCore.pyqtSignal(QtCore.QRectF)

    def __init__(self, *args, **kwargs):
        QtGui.QGraphicsTextItem.__init__(self, *args, **kwargs)
        self.document().contentsChanged.connect(self.__onDocumentChanged)

    def __onDocumentChanged(self):
        self.geometryModified.emit(self.boundingRect())



###########
# Buttons #
###########
class AleaQGraphicsFontButton(QtGui.QGraphicsSimpleTextItem, AleaQGraphicsButtonMixin):
    def __init__(self, parent=None):
        QtGui.QGraphicsSimpleTextItem.__init__(self, "A", parent)
        AleaQGraphicsButtonMixin.__init__(self)
        print "ooooooooookay"

class AleaQGraphicsColorWheel(QtGui.QGraphicsEllipseItem, AleaQGraphicsVanishingMixin, AleaQGraphicsButtonMixin):
    __stopHues    = xrange(0,360,360/12)
    __stopPos     = [i*1.0/12 for i in xrange(12)]

    ######################
    # The Missing Signal #
    ######################

    def __init__(self, radius=3.0, parent=None):
        QtGui.QGraphicsEllipseItem.__init__(self, 0,0,radius*2, radius*2, parent)
        AleaQGraphicsVanishingMixin.__init__(self)
        AleaQGraphicsButtonMixin.__init__(self)
        self.colorChanged = AleaSignal(QtGui.QColor)
        gradient = QtGui.QConicalGradient()
        gradient.setCenter(radius, radius)
        for hue, pos in zip(self.__stopHues, self.__stopPos):
            gradient.setColorAt(pos, QtGui.QColor.fromHsv(hue, 255, 255, 255))
        self.setBrush(QtGui.QBrush(gradient))

    def __onButtonPressed(self):
        color = QtGui.QColorDialog.getColor(parent=event.widget())
        if color.isValid():
            self.colorChanged.emit(color)




#####################################
# Simple layouts for QGraphicsItems #
#####################################
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

    def visibleItems(self, subcall=None):
        return [ i if subcall is None else subcall(i) for i in self._items if i.isVisible() ]

class HorizontalLayout(Layout):
    def _boundingRect(self):
        width = self._x1 + self._x2
        height = self._y1 + self._y2
        geoms = self.visibleItems(lambda x:x.boundingRect())
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
        items = self.visibleItems()
        selfHeight = self.boundingRect(force=False).height()
        for it in items:
            itRect = it.boundingRect()
            if self._center:
                offset.setY(pos.y()+(selfHeight - itRect.height())/2.)
            it.setPos(offset)
            offset += QtCore.QPointF(itRect.width(), 0.) + innerOffset
        if self._final and self._final.isVisible():
            if self._center:
                offset.setY(pos.y()+(selfHeight - self._final.boundingRect().height())/2.)
            self._final.setPos(offset)

class VerticalLayout(Layout):
    def _boundingRect(self):
        width = self._x1 + self._x2
        height = self._y1 + self._y2
        geoms = self.visibleItems(lambda x:x.boundingRect())
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
        items = self.visibleItems()
        selfWidth = self.boundingRect(force=False).width()
        for it in items:
            itRect = it.boundingRect()
            if self._center:
                offset.setX(pos.x()+(selfWidth - itRect.width())/2.)
            it.setPos(offset)
            offset += QtCore.QPointF(0., itRect.height()) + innerOffset
        if self._final and self._final.isVisible():
            if self._center:
                offset.setX(pos.x()+(selfWidth - self._final.boundingRect().width())/2.)
            self._final.setPos(offset)



#########################################################################################################
# class AleaQGraphicsLabelWidget(QtGui.QGraphicsWidget):                                                #
#     def __init__(self, label, parent=None):                                                           #
#         QtGui.QGraphicsWidget.__init__(self, parent)                                                  #
#         self.__label = QtGui.QGraphicsSimpleTextItem(self)                                            #
#         font = self.__label.font()                                                                    #
#         font.setBold(True)                                                                            #
#         self.__label.setText(label)                                                                   #
#                                                                                                       #
#     def boundingRect(self):                                                                           #
#         return self.__label.boundingRect()                                                            #
#                                                                                                       #
#     def shape(self):                                                                                  #
#         return self.__label.shape()                                                                   #
#                                                                                                       #
#     def size(self):                                                                                   #
#         return self.boundingRect().size()                                                             #
#                                                                                                       #
#     def sizeHint(self, blop, blip):                                                                   #
#         return self.size()                                                                            #
#                                                                                                       #
#     def setText(self, text):                                                                          #
#         self.__label.setText(text)                                                                    #
#         self.updateGeometry()                                                                         #
#                                                                                                       #
#     def paint(self, painter, paintOpts, widget):                                                      #
#         self.__label.paint(painter, paintOpts, widget)                                                #
#                                                                                                       #
# class AleaQGraphicsProxyWidget(QtGui.QGraphicsProxyWidget):                                           #
#     """Embed a QWidget in a QGraphicsItem without the ugly background.                                #
#                                                                                                       #
#     When embedding for ex. a QLabel in a QGraphicsLayout using the normal                             #
#     QGraphicsProxyWidget, the QLabel is rendered with its ugly background                             #
#     and the custom drawing of the QGraphicsItem is hidden.                                            #
#     This class overrides the painting routine or the QGraphicsProxyWidget                             #
#     to paint the child widget without the background.                                                 #
#     """                                                                                               #
#     def __init__(self, widget, parent=None):                                                          #
#         """                                                                                           #
#         Ctor.                                                                                         #
#                                                                                                       #
#         :Parameters:                                                                                  #
# 	 - widget (QtGui.QWidget) - The QWidget to embed                                                #
# 	 - parent (QtGui.QGraphicsItem) - Reference to the parent.                                      #
#                                                                                                       #
#         """                                                                                           #
#         QtGui.QGraphicsProxyWidget.__init__(self, parent)                                             #
#         self.setWidget(widget)                                                                        #
#         self.__noMouseEventForward = True                                                             #
#                                                                                                       #
#     def event(self, event):                                                                           #
#         #needed or else it catches events before getting to the nodes in dataflowviews and            #
#         #makes tooltips invisible.                                                                    #
#         if(event.type()==QtCore.QEvent.GraphicsSceneHoverMove and self.__noMouseEventForward):        #
#             event.ignore()                                                                            #
#             return True                                                                               #
#         return QtGui.QGraphicsProxyWidget.event(self, event)                                          #
#                                                                                                       #
#     def setMouseEventForward(self, val):                                                              #
#         self.__noMouseEventForward = val                                                              #
#                                                                                                       #
#     def setWidget(self, widget):                                                                      #
#         widget.setBackgroundRole(QtGui.QPalette.Background)                                           #
#         widget.setAutoFillBackground(True)                                                            #
#         widget.setStyleSheet("background-color: transparent")                                         #
#         QtGui.QGraphicsProxyWidget.setWidget(self, widget)                                            #
#########################################################################################################


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
