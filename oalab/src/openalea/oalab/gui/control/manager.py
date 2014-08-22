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
from openalea.oalab.service.qt_control import qt_editor


class ControlManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QVBoxLayout(self)

        self._manager = ControlManager()

        self.model = ControlModel(self._manager)

        self.view = ControlView()
        self.view.setModel(self.model)
        self.view.controlsSelected.connect(self.on_controls_selected)

        self.model.rowsInserted.connect(self.view.onRowsInserted)

        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(QtGui.QLabel("Global controls"))
        self._layout.addWidget(self.view)

        self._l_edit = QtGui.QLabel("Control editor")
        self._l_no_edit = QtGui.QWidget()

        self._layout.addWidget(self._l_edit)
        self._layout.addWidget(self._l_no_edit)

        me = QtGui.QSizePolicy.MinimumExpanding
        self._l_no_edit.setSizePolicy(QtGui.QSizePolicy(me, me))

        self._i = 1

        self._index = None
        self._widget_edit = None

    def on_controls_selected(self, controls):
        if self._widget_edit:
            widget = self._widget_edit()
            self._layout.removeWidget(widget)
            widget.close()
            self._widget_edit = None
            self._l_no_edit.show()
            del widget

        if not controls:
            return

        widget = QtGui.QWidget()
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        size = self._l_no_edit.size()
        widget.setMinimumSize(size.width(), size.height())
        widget.setMaximumSize(size.width(), size.height())
        self._l_no_edit.hide()

        layout = QtGui.QVBoxLayout(widget)
        for control in controls:
            subwidget = qt_editor(control, shape='large', preferred=control.widget)
            layout.addWidget(subwidget)
        self._layout.addWidget(widget)
        self._widget_edit = weakref.ref(widget)
