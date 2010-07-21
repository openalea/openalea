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

from PyQt4 import QtGui, QtCore
from openalea.grapheditor import qtgraphview, baselisteners
from openalea.grapheditor.qtutils import mixin_method, safeEffects




class MemoRects(QtGui.QGraphicsRectItem):

    __handleSize   = 7.5

    def __init__(self, rect, parent=None):
        QtGui.QGraphicsRectItem.__init__(self, rect, parent)
        self.__resizing   = False
        self.__handlePoly = QtGui.QPolygonF([QtCore.QPointF(0, -self.__handleSize),
                                             QtCore.QPointF(0, 0),
                                             QtCore.QPointF(-self.__handleSize,0)])
        self.__handlePos  = QtCore.QPointF(0,0)
        self.setFlag(QtGui.QGraphicsItem.ItemStacksBehindParent)
        self.__headerContentRect = None
        self.__headerRect = None

        if safeEffects:
            fx = QtGui.QGraphicsDropShadowEffect()
            fx.setOffset(2,2)
            fx.setBlurRadius(5)
            self.setGraphicsEffect(fx)

    def __moveHandleBottomRightTo(self, point):
        delta = point - self.__handlePos
        self.__handlePoly.translate(delta.x(), delta.y())
        self.__handlePos = point

    def setHeaderRect(self, rect):
        myRect = self.boundingRect()
        self.__headerContentRect = rect.adjusted(0,0,0,0)

        rect.setX(0); rect.setY(0)
        myRect.setX(0); myRect.setY(0)

        if rect.bottom() >= (myRect.bottom()-self.__handleSize):
            myRect.setBottom(rect.bottom() + self.__handleSize)
        if rect.right() >= myRect.right():
            myRect.setRight(rect.right())
        else:
            rect.setRight(myRect.right())
        self.__headerRect = rect
        self.__moveHandleBottomRightTo(myRect.bottomRight())
        self.setRect(myRect)
        self.update()

    def mousePressEvent(self, event):
        pos         = event.pos()
        bottomRight = self.boundingRect().bottomRight()
        x, y        = bottomRight.x(), bottomRight.y()
        rect = QtCore.QRectF(x-5, y-5, x+5, y+5)
        if self.__handlePoly.containsPoint(pos, QtCore.Qt.OddEvenFill):
            self.__resizing = True
        else:
            QtGui.QGraphicsRectItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.__resizing:
            delta = event.pos() - event.lastPos()
            bottomRight = self.boundingRect().bottomRight() + delta
            newRect = QtCore.QRectF(0.,0., bottomRight.x(), bottomRight.y())
            if newRect.contains(self.__headerContentRect.adjusted(0,0,0,self.__handleSize)):
                self.setRect(newRect)
                self.__headerRect = QtCore.QRectF(0.,0., bottomRight.x(), self.__headerContentRect.height())
                self.__moveHandleBottomRightTo(newRect.bottomRight())
        else:
            QtGui.QGraphicsRectItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.__resizing:
            self.__resizing = False
        else:
            QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)

    def paint(self, painter, paintOptions, widget):
        myRect = self.boundingRect()

        painter.fillRect(self.__headerRect, QtGui.QColor(230, 180, 10))
        gradTop = self.__headerRect.bottomLeft()
        gradBot = gradTop + QtCore.QPointF(0,10)
        gradient = QtGui.QLinearGradient(gradTop,gradBot )
        gradient.setColorAt(0, QtGui.QColor(150, 120, 10))
        gradient.setColorAt(1, QtGui.QColor(230, 230, 100))
        brush = QtGui.QBrush(gradient)

        bottomRect = myRect.adjusted(0,self.__headerRect.bottom(),0,0)
        painter.fillRect(bottomRect, brush)


        if not safeEffects:
            oldPen = painter.pen()
            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(10,10,10,100))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawRect(myRect.adjusted(0.5,0.5,-0.5,-0.5))
            painter.setPen(oldPen)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(150, 120, 10)))
        painter.drawConvexPolygon(self.__handlePoly)





class QGraphicsEmitingTextItem(QtGui.QGraphicsTextItem):
    """ Text annotation on the data flow """

    def wrap(method):
        def wrapped(self, *args, **kwargs):
            v = method(self, *args, **kwargs)
            self.geometryModified.emit(self.boundingRect())
        return wrapped

    #missing signals
    geometryModified = QtCore.pyqtSignal(QtCore.QRectF)

    # setDefaultTextColor = wrap(QtGui.QGraphicsTextItem.setDefaultTextColor)
    setDocument = wrap(QtGui.QGraphicsTextItem.setDocument)
    setFont = wrap(QtGui.QGraphicsTextItem.setFont)
    setHtml = wrap(QtGui.QGraphicsTextItem.setHtml)
    # setOpenExternalLinks = wrap(QtGui.QGraphicsTextItem.setOpenExternalLinks)
    setPlainText = wrap(QtGui.QGraphicsTextItem.setPlainText)
    # setTabChangesFocus = wrap(QtGui.QGraphicsTextItem.setTabChangesFocus)
    # setTextCursor = wrap(QtGui.QGraphicsTextItem.setTextCursor)
    # setTextInteractionFlags = wrap(QtGui.QGraphicsTextItem.setTextInteractionFlags)
    setTextWidth = wrap(QtGui.QGraphicsTextItem.setTextWidth)

    dragEnterEvent = wrap(QtGui.QGraphicsTextItem.dragEnterEvent)
    dragLeaveEvent = wrap(QtGui.QGraphicsTextItem.dragLeaveEvent)
    dragMoveEvent = wrap(QtGui.QGraphicsTextItem.dragMoveEvent)
    dropEvent = wrap(QtGui.QGraphicsTextItem.dropEvent)
    # focusInEvent = wrap(QtGui.QGraphicsTextItem.focusInEvent)
    # focusOutEvent = wrap(QtGui.QGraphicsTextItem.focusOutEvent)
    # hoverEnterEvent = wrap(QtGui.QGraphicsTextItem.hoverEnterEvent)
    # hoverLeaveEvent = wrap(QtGui.QGraphicsTextItem.hoverLeaveEvent)
    # hoverMoveEvent = wrap(QtGui.QGraphicsTextItem.hoverMoveEvent)
    inputMethodEvent = wrap(QtGui.QGraphicsTextItem.inputMethodEvent)
    inputMethodQuery = wrap(QtGui.QGraphicsTextItem.inputMethodQuery)
    keyPressEvent = wrap(QtGui.QGraphicsTextItem.keyPressEvent)
    keyReleaseEvent = wrap(QtGui.QGraphicsTextItem.keyReleaseEvent)
    mouseDoubleClickEvent = wrap(QtGui.QGraphicsTextItem.mouseDoubleClickEvent)
    mouseMoveEvent = wrap(QtGui.QGraphicsTextItem.mouseMoveEvent)
    mousePressEvent = wrap(QtGui.QGraphicsTextItem.mousePressEvent)
    mouseReleaseEvent = wrap(QtGui.QGraphicsTextItem.mouseReleaseEvent)

class GraphicalAnnotation(MemoRects, qtgraphview.Vertex):
    """ Text annotation on the data flow """

    __def_string__ = u"click to edit"

    def __init__(self, annotation, graphadapter, parent=None):
        """ Create a nice annotation """
        MemoRects.__init__(self, QtCore.QRectF())
        qtgraphview.Vertex.__init__(self, annotation, graphadapter)
        self.__textItem = QGraphicsEmitingTextItem(self.__def_string__, self)
        self.__textItem.geometryModified.connect(self.setHeaderRect)
        self.__textItem.geometryModified.connect(self.__onTextModified)
        self.__textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setZValue(-5)

    annotation = baselisteners.GraphElementListenerBase.get_observed

    def initialise_from_model(self):
        self.annotation().get_ad_hoc_dict().simulate_full_data_change(self, self.annotation())

    #####################
    # ----Qt World----  #
    #####################
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsTextItem,
                              "itemChange")

    def __onTextModified(self):
        self.deaf(True)
        text = unicode(self.__textItem.toPlainText())
        if(text != self.__def_string__):
            self.store_view_data(text=text)
        self.deaf(False)

    def setRect(self, rect):
        self.deaf(True)
        p2 = rect.width(), rect.height()
        self.store_view_data(rectP2=p2)
        MemoRects.setRect(self, rect)
        self.deaf(False)

    #########################
    # ----Other things----  #
    #########################
    def notify(self, sender, event):
        if event:
            if event[0] == "metadata_changed":
                if event[1] == "text":
                    self.set_text(event[2])
                    return
                elif event[1] == "rectP2":
                    rect = QtCore.QRectF(0,0,event[2][0],event[2][1])
                    MemoRects.setRect(self,rect)
                    self.setHeaderRect(self.__textItem.boundingRect())
        qtgraphview.Vertex.notify(self, sender, event)

    def set_text(self, text):
        if text == u"" :
            text = self.__def_string__
        self.__textItem.setPlainText(text)

    def store_view_data(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.vertex().get_ad_hoc_dict().set_metadata(k, v)

    def get_view_data(self, key):
        return self.vertex().get_ad_hoc_dict().get_metadata(key)
