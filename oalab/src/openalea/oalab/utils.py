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

from Qt import QtWidgets, QtGui, QtCore

from openalea.vpltk.qt.compat import orientation_qt, orientation_int

from openalea.core.customexception import CustomException, cast_error
from openalea.core.path import path as Path
from openalea.core.formatting.util import icon_path

from openalea.deploy.shared_data import shared_data

from openalea.oalab.widget import resources_rc

DEFAULT_SCALE = (256, 256)

def get_shared_data(filename):
    return shared_data(openalea.oalab, filename)

def qicon(filename, default=None, paths=None, save_filepath=None, packages=None):
    if isinstance(filename, QtGui.QIcon):
        return filename

    if not filename:
        if default is None:
            default = get_shared_data('icons/oxygen_application-x-desktop.png')
        return qicon(default, default, save_filepath=save_filepath)
    elif filename.startswith(':/'):
        pixmap = QtGui.QPixmap(filename).scaled(*DEFAULT_SCALE, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        icon = QtGui.QIcon(pixmap)
        if save_filepath:
            icon.addFile(save_filepath)
            pixmap.save(save_filepath)
        return icon
    else:
        if packages is None:
            packages = [openalea.core, openalea.oalab]
        found = icon_path(filename, default=default, paths=paths, packages=packages)
        if found:
            pixmap = QtGui.QPixmap(found).scaled(*DEFAULT_SCALE, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            icon = QtGui.QIcon(pixmap)
            if save_filepath:
                icon.addFile(save_filepath)
                pixmap.save(save_filepath)
            return icon
        else:
            return qicon(":/images/resources/%s" % filename, save_filepath=save_filepath)

def obj_icon(obj_lst, rotation=0, size=(64, 64), default=None, paths=None, save_filepath=None, packages=None):
    if not isinstance(obj_lst, (list, tuple)):
        obj_lst = [obj_lst]

    _obj_icon = None
    for obj in obj_lst:
        if hasattr(obj, 'icon'):
            _obj_icon = obj.icon
            break

    if _obj_icon:
        icon = qicon(_obj_icon, default=default, paths=paths, save_filepath=save_filepath, packages=packages)
    else:
        icon = qicon(None, default, save_filepath=save_filepath, packages=packages)

    if rotation:
        pix = icon.pixmap(*size)
        transform = QtGui.QTransform()
        transform.rotate(rotation)
        pix = pix.transformed(transform)
        icon = QtGui.QIcon(pix)
    return icon

def qicon_path(obj, savedir, default=None, paths=None, packages=None):
    """
    If icon is pysically on disk, return path.
    Else, save image in project dir and return it
    """
    ext = '.png'
    icon_path = savedir / "._icon" + ext
    icon = obj_icon(obj, save_filepath=icon_path, paths=paths, default=default, packages=packages)
    return icon_path

class ModalDialog(QtWidgets.QDialog):

    def __init__(self, widget, parent=None, buttons=None):
        QtWidgets.QDialog.__init__(self, parent)

        _bbox = QtWidgets.QDialogButtonBox
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

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.addWidget(widget)
        layout.addWidget(self.bbox)

    def set_valid(self, validity):
        ok = self.bbox.button(QtWidgets.QDialogButtonBox.Ok)
        if ok:
            ok.setEnabled(validity)

class Splitter(QtWidgets.QSplitter):

    ORIENTATION = QtCore.Qt.Vertical

    def __init__(self, parent=None):
        QtWidgets.QSplitter.__init__(self, parent=parent)
        self._applets = []

        self._action_clear = QtWidgets.QAction('Clear', self)
        self._action_clear.triggered.connect(self.clear)

        self._action_switch = QtWidgets.QAction('Change orientation', self)
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
    _widget = QtWidgets.QWidget()
    _layout = QtWidgets.QVBoxLayout(_widget)
    _password = QtWidgets.QLineEdit()
    _password.setEchoMode(QtWidgets.QLineEdit.Password)

    _layout.addWidget(QtWidgets.QLabel("Password ?"))
    _layout.addWidget(_password)

    dialog = ModalDialog(_widget)
    if dialog.exec_():
        return _password.text()

def raw_input_dialog(prompt=None, size=None):
    _widget = QtWidgets.QWidget()
    _layout = QtWidgets.QVBoxLayout(_widget)
    _line = QtWidgets.QLineEdit()

    _layout.addWidget(QtWidgets.QLabel("Input ?"))
    _layout.addWidget(_line)

    dialog = ModalDialog(_widget)
    if dialog.exec_() and _line.text():
        return _line.text()
    else:
        return u'\n'

def make_error_dialog(e, parent=None, icon=QtWidgets.QMessageBox.Critical):
    if not isinstance(e, CustomException):
        e = cast_error(e, CustomException)

    mbox = QtWidgets.QMessageBox(parent)
    mbox.setDetailedText(e.getDesc())
    mbox.setText(e.getMessage())
    mbox.setWindowTitle(e.getTitle())
    mbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    mbox.setDefaultButton(QtWidgets.QMessageBox.Ok)
    mbox.setIcon(QtWidgets.QMessageBox.Information)

    return mbox.exec_()

def make_info_dialog(e, parent=None):
    return make_error_dialog(e, parent, icon=QtWidgets.QMessageBox.Information)
