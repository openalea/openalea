# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener

from openalea.oalab.gui.control.model_view import ControlModel, ControlView
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.service.control import edit_qt, qt_paint_function

def preview(control, size):
    paint = qt_paint_function(control)
    if paint:
        pixmap = QtGui.QPixmap(size)
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        paint(control, painter, pixmap.rect(), None)
        painter.end()
        widget = QtGui.QLabel()
        widget.setPixmap(pixmap)
        return widget
    else:
        widget = edit_qt(control, shape='small')
        if widget:
            return widget
        else:
            return QtGui.QLabel(unicode(control.value))

def edit(control, size):
    widget = edit_qt(control, shape='small')
    return widget

class ControlManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QVBoxLayout(self)

        self._manager = ControlManager()

        self.model = ControlModel(self._manager)
        self.model_tagged = ControlModel(self._manager)

        self.view = ControlView()
        self.view.setModel(self.model)


        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(QtGui.QLabel("Global controls"))
        self._layout.addWidget(self.view)

        self._i = 1

        self._index = None


class ControlPanel(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QHBoxLayout(self)
        self.setAcceptDrops(True)

    def sizeHint(self):
        return QtCore.QSize(300, 300)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('openalealab/control'):
            event.acceptProposedAction()
        else:
            return QtGui.QWidget.dragEnterEvent(self, event)

    def dropEvent(self, event):
        source = event.mimeData()
        if source.hasFormat('openalealab/control'):
            from openalea.oalab.service.mimetype import decode
            control = decode('openalealab/control', source.data('openalealab/control'))
            widget = preview(control, (300, 300))
            if widget:
                self._layout.addWidget(widget)
                event.acceptProposedAction()
        else:
            return QtGui.QWidget.dropEvent(self, event)
