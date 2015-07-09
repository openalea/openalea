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

from openalea.oalab.utils import Splitter
from openalea.oalab.control.model_view import ControlModel, ControlView
from openalea.core.control.manager import ControlManager
from openalea.oalab.service.qt_control import qt_editor


class ControlManagerWidget(Splitter, AbstractListener):

    def __init__(self, manager=None, parent=None):
        AbstractListener.__init__(self)
        Splitter.__init__(self, parent=parent)

        if manager is None:
            self._manager = ControlManager()
        else:
            self._manager = manager

        self.model = ControlModel(self._manager)

        self.view = ControlView()
        self.view.setModel(self.model)
        self.view.controlsSelected.connect(self.on_controls_selected)

        self.model.rowsInserted.connect(self.view.onRowsInserted)

        self.addWidget(self.view)

        self._i = 1

        self._index = None
        self._widget_edit = None

    def on_controls_selected(self, controls):
        if self._widget_edit:
            widget = self._widget_edit()
            widget.close()
            self._widget_edit = None
            del widget

        if not controls:
            return

        widget = QtGui.QWidget()
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        layout = QtGui.QVBoxLayout(widget)
        for control in controls:
            subwidget = qt_editor(control, shape='large', preferred=control.widget)
            layout.addWidget(subwidget)
        self.addWidget(widget)
        self._widget_edit = weakref.ref(widget)
