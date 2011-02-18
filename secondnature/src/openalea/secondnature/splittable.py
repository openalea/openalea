# -*- python -*-
#
#       OpenAlea.SecondNature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
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

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from PyQt4 import QtGui, QtCore
from openalea.visualea.splitterui import SplittableUI, DraggableWidget, RubberBandScrollArea




# class Header(QtGui.QFrame):
#      """Implementation of the area that holds the menu and toolbar area

#      Obeys to Qt naming convention.
#      """

#      __ideal_height__ = 27 # this is fixed, never got it right otherwise.
#      widgetMenuRequest = QtCore.pyqtSignal(QtCore.QPoint)


#      def __init__(self, parent=None, windowsflags=QtCore.Qt.Widget):
#          QtGui.QFrame.__init__(self, parent, windowsflags)
#          self.__lay = QtGui.QHBoxLayout()
#          self.__lay.setContentsMargins(1,1,1,1)
#          self.__lay.setSpacing(1)

#          self.__but = QtGui.QPushButton("Win")
#          self.__but.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
#          self.__but.clicked.connect(self.__onButtonClicked)

#          self.__lay.addWidget(self.__but)

#          self.headerScr = RubberBandScrollArea()
#          # -- lock scrolling to X --
#          self.headerScr.setYScrollable(False)
#          # -- appearance --
#          self.headerScr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#          self.headerScr.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#          self.headerScr.setFrameShape(QtGui.QFrame.NoFrame)
#          self.headerScr.setFrameShadow(QtGui.QFrame.Sunken)

#          self.__lay.addWidget(self.headerScr)
#          self.__fixSize()
#          self.setLayout(self.__lay)

#      def setToolbar(self, toolbar):
#          """Set the widget held by the scrollable
#          toolbar area to the right.

#          :Parameters:
#           - `toolbar` (QtGui.QWidget) - the widget that serves as a toolbar.
#          """
#          self.headerScr.setWidget(toolbar)
#          self.__fixSize()

#      def toolbar(self):
#          """Retreive the toolbar widget"""
#          self.headerScr.widget()

#      def __fixSize(self):
#          """Forces all subwidgets to a decent size. Private."""
#          szY = self.__ideal_height__
#          self.__but.setMaximumHeight(szY)
#          self.__but.setMinimumHeight(szY)
#          self.setMaximumHeight(szY+5)
#          self.setMinimumHeight(szY+5)

#      def __onButtonClicked(self, checked):
#          origin = self.__but.geometry().bottomLeft()
#          origin = self.mapToGlobal(origin)
#          self.widgetMenuRequest.emit(origin)

class CustomSplittable(SplittableUI):

    paneMenuRequest = QtCore.pyqtSignal(int, QtCore.QPoint)

    def _raise_overlays(self, paneId):
        SplittableUI._raise_overlays(self, paneId)
        tb  = self._g.get_property(paneId, "toolButtonWidget")
        tb.raise_()

    def _split_parent(self, paneId, direction, amount):
        w = SplittableUI._split_parent(self, paneId, direction, amount)
        self._remove_toolbutton(paneId)
        return w

    def _install_child(self, paneId, widget, **kwargs):
        w = SplittableUI._install_child(self, paneId, widget, **kwargs)
        if not kwargs.get("noToolButton", False):
            self._install_toolbutton(paneId)
        return w

    def _uninstall_child(self, paneId):
        w = SplittableUI._uninstall_child(self, paneId)
        self._remove_toolbutton(paneId)
        return w

    def _install_toolbutton(self, paneId):
        g = self._g
        toolbutton = CustomSplittable.ToolButton(paneId, self)
        toolbutton.show()
        toolbutton.clicked.connect(self.paneMenuRequest)
        g.set_property(paneId, "toolButtonWidget", toolbutton)

    def _remove_toolbutton(self, paneId):
        g = self._g
        if not g.has_property(paneId, "toolButtonWidget"):
            return
        toolbut = g.pop_property(paneId, "toolButtonWidget")
        toolbut.close()


    class ToolButton(QtGui.QWidget, DraggableWidget):

        clicked = QtCore.pyqtSignal(int, QtCore.QPoint)
        __ideal_height__ = 10

        def __init__(self, refVid, parent):
            QtGui.QWidget.__init__(self, parent)
            DraggableWidget.__init__(self)
            self.vid = refVid
            self.setFixedHeight(self.__ideal_height__)
            self.setFixedWidth(self.__ideal_height__)

        def mouseReleaseEvent(self, event):
            ret = DraggableWidget.mouseReleaseEvent(self, event)
            if self.rect().contains(event.pos()):
                self.clicked.emit(self.vid, self.mapToParent(event.pos()))
            return ret

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            if self._hovered:
                brush   = QtGui.QBrush(QtGui.QColor(120,190,255,200))
            else:
                brush   = QtGui.QBrush(QtGui.QColor(120,190,255,70))
            painter.setBrush(brush)

            pen = painter.pen()
            pen.setColor(QtGui.QColor(0,0,0,255))
            pen.setWidth(1)
            painter.setPen(pen)

            adj = pen.width()
            rect = self.contentsRect().adjusted(adj,adj,-adj,-adj)
            painter.drawEllipse(rect)

            center = rect.center()
            x = center.x()+adj
            y = center.y()+adj
            ls = [QtCore.QPoint(x, rect.top()+1+adj),
                  QtCore.QPoint(x, rect.bottom()-1),
                  QtCore.QPoint(rect.left()+1+adj, y),
                  QtCore.QPoint(rect.right()-1, y)]
            painter.drawLines(ls)


    class GeometryComputingVisitor(SplittableUI.GeometryComputingVisitor):
        def layout_pane(self, geom, vid):
            igF, igS = super(self.__class__, self).layout_pane(geom, vid)

            tb = self.g.get_property(vid, "toolButtonWidget")
            th = CustomSplittable.ToolButton.__ideal_height__
            if geom.height() <  th or geom.width() < th:
                tb.hide()
            else:
                tb.show()

            tb.move(geom.left()+1, geom.top()+1)
            return False, False #don't ignore first or second child

