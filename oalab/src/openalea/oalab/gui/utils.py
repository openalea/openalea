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

import openalea.oalab
from openalea.vpltk.qt import QtGui
from openalea.core.customexception import CustomException, cast_error
from openalea.deploy.shared_data import shared_data

def get_shared_data(filename):
    return shared_data(openalea.oalab, filename)

def qicon(filename):
    path = get_shared_data('icons/%s' % filename)
    if filename.startswith(':/'):
        return QtGui.QIcon(filename)
    elif path:
        return QtGui.QIcon(path)
    else:
        return QtGui.QIcon(":/images/resources/%s" % filename)


class ModalDialog(QtGui.QDialog):
    def __init__(self, widget, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setModal(True)

        _bbox = QtGui.QDialogButtonBox
        bbox = _bbox(_bbox.Ok | _bbox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)

        ok = bbox.button(_bbox.Ok)
        ok.setDefault(True)

        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.addWidget(widget)
        layout.addWidget(bbox)


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
