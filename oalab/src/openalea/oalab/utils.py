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
from openalea.oalab.widget import resources_rc


def get_shared_data(filename):
    return shared_data(openalea.oalab, filename)


def qicon(filename, default=None, paths=None):
    if isinstance(filename, QtGui.QIcon):
        return filename

    if not filename:
        if default is None:
            default = get_shared_data('icons/oxygen_application-x-desktop.png')
        return qicon(default, default)
    elif filename.startswith(':/'):
        return QtGui.QIcon(filename)
    else:
        _paths = [Path(filename)]
        if paths:
            _paths += [Path(p) / filename for p in paths]

        found = None
        for path in _paths:
            if path.isfile():
                found = path
                break

        if found is None:
            for path in (filename, 'icons/%s' % filename):
                path = get_shared_data(path)
                if path and path.isfile():
                    found = path
                    break

        if found:
            return QtGui.QIcon(found)
        else:
            return qicon(":/images/resources/%s" % filename)


def obj_icon(obj_lst, rotation=0, size=(64, 64), default=None, paths=None):
    if not isinstance(obj_lst, (list, tuple)):
        obj_lst = [obj_lst]

    _obj_icon = None
    for obj in obj_lst:
        if hasattr(obj, 'icon'):
            _obj_icon = obj.icon
            break

    if _obj_icon:
        icon = qicon(_obj_icon, default=default, paths=paths)
    else:
        icon = qicon(None, default)

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

    def set_valid(self, validity):
        ok = self.bbox.button(QtGui.QDialogButtonBox.Ok)
        if ok:
            ok.setEnabled(validity)


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


def raw_input_dialog(prompt=None, size=None):
    _widget = QtGui.QWidget()
    _layout = QtGui.QVBoxLayout(_widget)
    _line = QtGui.QLineEdit()

    _layout.addWidget(QtGui.QLabel("Input ?"))
    _layout.addWidget(_line)

    dialog = ModalDialog(_widget)
    if dialog.exec_() and _line.text():
        return _line.text()
    else:
        return u'\n'


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
