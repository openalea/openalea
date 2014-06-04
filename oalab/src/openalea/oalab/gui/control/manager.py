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

import weakref

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener

from openalea.oalab.gui.control.model_view import ControlModel, ControlView
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.service.control import edit_qt, qt_paint_function


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
        self.view.pressed.connect(self.on_control_selected)
#         self.view.setIndexWidget(QtGui.QLabel("salut"))

#         self.view_tagged = ControlView()
#         self.view_tagged.setModel(self.model_tagged)
#         self.view_tagged.pressed.connect(self.on_tagged_control_selected)

        self.l_tagged_control_name = QtGui.QLabel()
        self.showTag(None)

        self._layout.addWidget(QtGui.QLabel("Global controls"))
        self._layout.addWidget(self.view)
#         self._layout.addWidget(self.l_tagged_control_name)
#         self._layout.addWidget(self.view_tagged)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._widget_preview = QtGui.QLabel()
        self._widget_preview.setMinimumHeight(100)
        self._widget_preview.setMinimumWidth(300)

        self._widget_edit = QtGui.QWidget()
        self._widget_edit.setMinimumHeight(300)
        self._widget_edit.setMinimumWidth(300)

        self._l_edit = QtGui.QLabel("No control selected")
        self.pb_apply = QtGui.QPushButton("Apply")

        self._layout_edit = QtGui.QVBoxLayout(self._widget_edit)
        self._layout_edit.addWidget(self._l_edit)

        self._layout.addWidget(self._widget_preview)
        self._layout.addWidget(self._widget_edit)
        self._layout.addWidget(self.pb_apply)
        self.pb_apply.hide()
        self.pb_apply.clicked.connect(self.apply)


        self._i = 1

        self.widget_ref = None
        self._index = None
        self.view.delegate.external_edit_required.connect(self.edit_external)

    def edit_external(self, index):
        if self.widget_ref:
            self._layout_edit.removeWidget(self.widget_ref())
            self.widget_ref().close()

        self._index = index
        control = self.model.control(index)
        self.pb_apply.show()
        widget = edit_qt(control, shape='large')
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._l_edit.setText('Editing control "%s"' % control.name)
        self._layout_edit.addWidget(widget)
        self.widget_ref = weakref.ref(widget)

    def on_control_selected(self, index):
        self._on_control_selected(index, self.model)

    def on_tagged_control_selected(self, index):
        self._on_control_selected(index, self.model_tagged)

    def _on_control_selected(self, index, model):
        control = model.control(index)
        self.preview(control)

    def showTag(self, model_uid=None):
        if model_uid is None :
            self.l_tagged_control_name.setText("Local controls")
            self.model_tagged.set(False)
        else :
            self.l_tagged_control_name.setText("%s controls" % model_uid)
            self.model_tagged.set(model_uid)

    def apply(self):
        if self.widget_ref:
            control = self.model.control(self._index)
            self.widget_ref().apply(control)
            self.model.dataChanged.emit(self._index, self._index)

    def preview(self, control):
        paint = qt_paint_function(control)
        if paint:
            pixmap = QtGui.QPixmap(self._widget_preview.size())
            painter = QtGui.QPainter()
            painter.begin(pixmap)
            paint(control, painter, pixmap.rect(), None)
            painter.end()
            self._widget_preview.setPixmap(pixmap)
