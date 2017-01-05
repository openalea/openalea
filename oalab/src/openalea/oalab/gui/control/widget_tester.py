# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
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


from Qt import QtGui, QtWidgets

import openalea.oalab.service.qt_control as scontrol

from openalea.core.service.interface import new_interface, interfaces, load_interfaces
from openalea.core.control import Control
from openalea.core.control.manager import ControlManager
from openalea.oalab.gui.control.qcontainer import QControlContainer
from openalea.oalab.gui.control.model_view import ControlView, ControlModel

from openalea.vpltk.qt.designer import generate_pyfile_from_uifile

generate_pyfile_from_uifile(__name__)

from openalea.oalab.gui.control.designer._widget_tester import Ui_WidgetTester

class ControlWidgetTester(Ui_WidgetTester, QtWidgets.QWidget):

    def __init__(self, control, edit_mode='edit'):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        text = 'interface: %s, preferred widget: %s, edit mode: %s' % (control.interface, control.widget, edit_mode)
        self.l_title.setText(text)

        self._control = control

        self._qcontainer = QControlContainer()
        self._qcontainer.add_control(self._control)
        self._qcontainer.create_actions(self)

#        m = getattr(scontrol, '%s_qt' % edit_mode)
        m = getattr(scontrol, 'qt_editor')

        self._qtcontrols = []

        valid_widget_shape = None
        for shape in ['vline', 'hline', 'small', 'large', 'responsive']:
            layout = getattr(self, 'l_%s' % shape)
            widget = m(self._control, shape=shape)
            if widget:
                layout.addWidget(widget)
                valid_widget_shape = shape
                self._qtcontrols.append(widget)
            else:
                layout.addWidget(QtWidgets.QLabel("X"))

        if valid_widget_shape:
            self._test_widget = m(self._control, shape=valid_widget_shape)
            self.layout_sample.addWidget(self._test_widget)
            self.cb_read.toggled.connect(self.on_mode_changed)
            self.cb_apply.toggled.connect(self.on_mode_changed)

        self._model = ControlModel(manager=self._qcontainer)
        self._view = ControlView()
        self._view.setModel(self._model)
        self._view.hideColumn(0)
        self.l_large_box.addWidget(self._view, 1, 1, 2, 1)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addActions(self._qcontainer.actions())
        menu.exec_(event.pos())

    def on_mode_changed(self, state):
        autoread = self.cb_read.isChecked()
        autoapply = self.cb_apply.isChecked()
        for widget in self._qtcontrols:
            widget.autoapply(self._control, autoapply)
            widget.autoread(self._control, autoread)
