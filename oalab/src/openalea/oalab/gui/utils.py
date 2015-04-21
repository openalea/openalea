# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <Guillaume.Baty@inria.fr>
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

__all__ = ['qicon']

import pickle
import openalea.oalab
from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.compat import orientation_qt, orientation_int
from openalea.core.customexception import CustomException, cast_error
from openalea.deploy.shared_data import shared_data
from openalea.core.path import path as Path


def get_shared_data(filename):
    return shared_data(openalea.oalab, filename)


def qicon(filename):
    if filename is None:
        return QtGui.QIcon(get_shared_data('icons/oxygen_application-x-desktop.png'))
    if filename.startswith(':/'):
        return QtGui.QIcon(filename)
    else:
        path = Path(filename)
        if not path.isfile():
            path = get_shared_data(filename)
            if path is None:
                path = get_shared_data('icons/%s' % filename)

        if path:
            return QtGui.QIcon(path)
        else:
            return QtGui.QIcon(":/images/resources/%s" % filename)


def obj_icon(obj, rotation=0, size=(64, 64), applet=None):
    if hasattr(applet, 'icon'):
        applet_icon = applet.icon
    else:
        applet_icon = None

    if applet_icon:
        icon = qicon(applet_icon)
    elif hasattr(obj, 'icon'):
        icon = qicon(obj.icon)
    else:
        icon = qicon('oxygen_application-x-desktop.png')

    if rotation:
        pix = icon.pixmap(*size)
        transform = QtGui.QTransform()
        transform.rotate(rotation)
        pix = pix.transformed(transform)
        icon = QtGui.QIcon(pix)
    return icon


class ModalDialog(QtGui.QDialog):

    def __init__(self, widget, parent=None, buttons=None):
        QtGui.QDialog.__init__(self, parent)

        _bbox = QtGui.QDialogButtonBox
        if buttons is None:
            buttons = _bbox.Ok | _bbox.Cancel

        self.setContentsMargins(0, 0, 0, 0)
        self.setModal(True)

        self.bbox = _bbox(buttons)
        self.bbox.accepted.connect(self.accept)
        self.bbox.rejected.connect(self.reject)

        ok = self.bbox.button(_bbox.Ok)
        if ok:
            ok.setDefault(True)

        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.addWidget(widget)
        layout.addWidget(self.bbox)


class Splitter(QtGui.QSplitter):

    ORIENTATION = QtCore.Qt.Vertical

    def __init__(self, parent=None):
        QtGui.QSplitter.__init__(self, parent=parent)
        self._applets = []

        self._action_clear = QtGui.QAction('Clear', self)
        self._action_clear.triggered.connect(self.clear)

        self._action_switch = QtGui.QAction('Change orientation', self)
        self._action_switch.triggered.connect(self.toggle_orientation)

    def menu_actions(self):
        return [self._action_clear, self._action_switch]

    def toggle_orientation(self):
        self.setOrientation(int(not self.orientation()))

    def clear(self):
        for widget in self.children():
            widget.close()

    def set_properties(self, properties):
        orientation = orientation_qt(properties.get('orientation', self.ORIENTATION))
        self.setOrientation(orientation)
        self.icon = properties.get('icon', None)
        state = properties.get('state', None)
        if state:
            self.restoreState(pickle.loads(state))

    def properties(self):
        orientation = orientation_int(self.orientation())
        return dict(
            orientation=orientation,
            state=pickle.dumps(str(self.saveState())),
            icon=self.icon,
        )


def password():
    _widget = QtGui.QWidget()
    _layout = QtGui.QVBoxLayout(_widget)
    _password = QtGui.QLineEdit()
    _password.setEchoMode(QtGui.QLineEdit.Password)

    _layout.addWidget(QtGui.QLabel("Password ?"))
    _layout.addWidget(_password)

    dialog = ModalDialog(_widget)
    if dialog.exec_():
        return _password.text()


def make_error_dialog(e, parent=None, icon=QtGui.QMessageBox.Critical):
    if not isinstance(e, CustomException):
        e = cast_error(e, CustomException)

    mbox = QtGui.QMessageBox(parent)
    mbox.setDetailedText(e.getDesc())
    mbox.setText(e.getMessage())
    mbox.setWindowTitle(e.getTitle())
    mbox.setStandardButtons(QtGui.QMessageBox.Ok)
    mbox.setDefaultButton(QtGui.QMessageBox.Ok)
    mbox.setIcon(QtGui.QMessageBox.Information)

    return mbox.exec_()


def make_info_dialog(e, parent=None):
    return make_error_dialog(e, parent, icon=QtGui.QMessageBox.Information)
