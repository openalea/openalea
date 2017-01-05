# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013-2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Bâty <guillaume.baty@inria.fr>
#
#       File contributor(s): Julien Coste <julien.coste@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core import settings
from openalea.core.path import path
from openalea.core.customexception import CustomException
from openalea.core.service.plugin import debug_plugin, plugins
from openalea.core.service.plugin import plugin_instance_exists, plugin_instance, plugins

from openalea.oalab.utils import ModalDialog, qicon
from openalea.oalab.widget import resources_rc

from Qt import QtWidgets, QtGui, QtCore

class ParadigmCreator(QtCore.QObject):
    paradigm_clicked = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self)
        self._parent = parent
        self.reload()

    def reload(self):
        self.dtype = None

        self._name_to_applet = {}
        self._name_to_action = {}
        self._action_to_name = {}

        for plugin in plugins('oalab.plugin', criteria=dict(implement='IParadigmApplet')):
            applet = debug_plugin('oalab.plugin', func=plugin)
            if applet:
                name = applet.default_name
                self._name_to_applet[name] = applet
                action = QtWidgets.QAction(qicon(applet.icon), "New " + name, self._parent)
                action.triggered.connect(self._on_action_triggered)
                self._name_to_action[name] = action
                self._action_to_name[action] = name

    def applet(self, obj, dtype, mimetype=None):
        applet_class = None
        if dtype in self._name_to_applet:
            # Check in paradigm.default_name
            applet_class = self._name_to_applet[dtype]
        else:
            # Check in paradigm.extension
            for value in self._name_to_applet.values():
                if dtype == value.extension:
                    applet_class = value
        if applet_class is None:
            applet_class = self._name_to_applet["Textual"]

        return applet_class(data=obj).instantiate_widget()

    def actions(self):
        return self._action_to_name.keys()

    def action(self, paradigm):
        """
        action("Python") -> QAction "New Python" or None
        """
        return self._name_to_action.get(paradigm)

    def _on_action_triggered(self):
        try:
            self.dtype = self._action_to_name[self.sender()]
        except KeyError:
            self.dtype = None

        self.paradigm_clicked.emit(self.dtype)


class ParadigmInfoSelector(QtWidgets.QWidget):

    validity_changed = QtCore.Signal(bool)

    def __init__(self, name, categories, dtypes, project=None, parent=None):
        super(ParadigmInfoSelector, self).__init__(parent=parent)

        self._valid = True

        self.project = project
        self.categories = categories
        self.dtypes = dtypes

        layout = QtWidgets.QFormLayout(self)

        self.l_categories = QtWidgets.QLabel("Select in which category you want to add this file: ")
        self.l_dtypes = QtWidgets.QLabel("Data type")
        self.l_name = QtWidgets.QLabel("Name: ")
        self.l_notes = QtWidgets.QLabel("Note:")
        self.l_info = QtWidgets.QLabel("All is ok")

        # Category selector
        if len(self.categories) > 1:
            self.cb_categories = QtWidgets.QComboBox(self)
            self.cb_categories.addItems(categories)
            if 'model' in categories:
                self.cb_categories.setCurrentIndex(categories.index('model'))
            self.cb_categories.currentIndexChanged.connect(self.check)

            layout.addRow(self.l_categories, self.cb_categories)

        if len(self.dtypes) > 1:
            # Dtype selector
            self.cb_dtypes = QtWidgets.QComboBox(self)
            self.cb_dtypes.addItems(dtypes)
            self.cb_dtypes.setCurrentIndex(0)
            self.cb_dtypes.currentIndexChanged.connect(self.check_data)

            layout.addRow(self.l_dtypes, self.cb_dtypes)

        self.line = QtWidgets.QLineEdit(name)
        self.line.textChanged.connect(self.check)
        layout.addRow(self.l_name, self.line)
        layout.addRow(self.l_notes, self.l_info)
        self.setLayout(layout)

        self.check()

    def _show_error(self, error):
        if isinstance(error, CustomException):
            message = error.getMessage()
        elif isinstance(error, Warning):
            message = error.message
        else:
            message = None
        if message:
            self.l_info.setText(message)
            self.l_notes.show()
            self.l_info.show()
        else:
            self.l_notes.hide()
            self.l_info.hide()

    def check(self):
        old_valid = self._valid

        name = self.name()
        category = self.category()
        dtype = self.dtype()
        if self.project is not None:
            err = self.project.valid_item_name(category, name)
            if isinstance(err, CustomException):
                self._valid = False
            else:
                self._valid = True

        self._show_error(err)
        if old_valid != self._valid:
            self.validity_changed.emit(self._valid)

    def is_valid(self):
        return self._valid

    def category(self):
        if len(self.categories) == 1:
            return self.categories[0]
        elif len(self.categories) > 1:
            return str(self.cb_categories.currentText())
        else:
            return None

    def name(self):
        return str(self.line.text())

    def dtype(self):
        if len(self.dtypes) == 1:
            return self.dtypes[0]
        elif len(self.dtypes) > 1:
            return str(self.cb_dtypes.currentText())
        else:
            return None
