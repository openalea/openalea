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
import itertools

from openalea.core.customexception import CustomException
from openalea.oalab.mimedata import MimeCodecManager

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.gui.utils import ModalDialog, make_error_dialog


class DropSelector(QtGui.QWidget):

    def __init__(self, lst, labels=None):
        QtGui.QWidget.__init__(self)

        if labels is None:
            labels = lst

        self._layout = QtGui.QVBoxLayout(self)

        self._cb = QtGui.QComboBox()
        self._lst = lst
        for i, mimetype in enumerate(self._lst):
            self._cb.addItem(labels[i])

        self._layout.addWidget(QtGui.QLabel("Drop as ..."))
        self._layout.addWidget(self._cb)

    def mimetype(self):
        return self._lst[self._cb.currentIndex()]


class DragHandler(object):
    conv = MimeCodecManager()
    conv.init()

    def __init__(self, widget, **kwargs):
        self.widget = widget
        self.kwargs = kwargs
        self.drag_format = []

        if isinstance(widget, QtGui.QStandardItemModel):
            self.mimeTypes = self.mime_types

    def mime_types(self):
        return self.drag_format

    def add_drag_format(self, mimetype_out, **kwds):
        self.drag_format.append(mimetype_out)

    def encode(self, data, mimetype):

        possible_conv = {}
        for k, g in itertools.groupby(self.conv._registry, lambda data: data[0]):
            possible_conv[k] = list(g)

        qmimedata = QtCore.QMimeData()
        if mimetype in possible_conv:
            for mimetype_in, mimetype_out in possible_conv[mimetype]:
                raw_data = self.conv.encode(data, mimetype_in, mimetype_out)
                qmimedata.setData(mimetype_out, raw_data)
        return qmimedata


class DropHandler(object):
    conv = MimeCodecManager()
    conv.init()

    def __init__(self, widget, **kwargs):
        self.widget = widget
        self.kwargs = kwargs
        self.drop_callbacks = {}
        self._labels = {}

        # Drop part
        self.widget.setAcceptDrops(True)
        if isinstance(widget, QtGui.QPlainTextEdit):
            self.widget.canInsertFromMimeData = self.can_insert_from_mime_data
            self.widget.insertFromMimeData = self.insert_from_mime_data
        else:
            self.widget.dragEnterEvent = self.drag_enter_event
            self.widget.dropEvent = self.drop_event
            self.widget.dragLeaveEvent = self.drag_leave_event

    def add_drop_callback(self, mimetype_out, callback, **kwds):
        if 'title' in kwds:
            self._labels[mimetype_out] = kwds.pop('title')
        else:
            self._labels[mimetype_out] = mimetype_out
        self.drop_callbacks[mimetype_out] = callback

    def insert_from_mime_data(self, source):
        cursor = self.widget.textCursor()
        rect = self.widget.cursorRect()
        pos = self.widget.viewport().mapToGlobal(rect.center())
        possible_conv, selected = self._drop(source, pos=pos)
        for mimetype_in, mimetype_out in possible_conv[selected]:
            try:
                data, kwds = self.conv.qtdecode(source, mimetype_in, mimetype_out)
            except CustomException, e:
                make_error_dialog(e)
            else:
                kwds['mimedata'] = source
                kwds['cursor'] = cursor
                self.drop_callbacks[selected](data, **kwds)

    def can_insert_from_mime_data(self, source):
        self._compatible = self.conv.compatible_mime(source.formats(), mimetype_out_list=self.drop_callbacks.keys())
        return bool(self._compatible)

    def drag_enter_event(self, event):
        mimedata = event.mimeData()
        self._compatible = self.conv.compatible_mime(mimedata.formats(), mimetype_out_list=self.drop_callbacks.keys())

        if self._compatible:
            event.acceptProposedAction()
            return QtGui.QWidget.dragEnterEvent(self.widget, event)
        else:
            return QtGui.QWidget.dragEnterEvent(self.widget, event)

    def drag_leave_event(self, event):
        self._compatible = None
        return QtGui.QWidget.dragLeaveEvent(self.widget, event)

    def drag_move_event(self, event):
        if self._compatible:
            event.acceptProposedAction()
        else:
            event.ignore()

    def _drop(self, mimedata, pos=None):
        # Check all conversion available
        # Use quick_check method to check more than mimetype
        # For example, a "text/uri-list" mimetype is a valid mimetype for an image reader
        # but ... if corresponding file is not an image, quick_check should return False.
        # In this case, we do not add conversion to compatible list.
        possible_conv = {}
        for k, g in itertools.groupby(self._compatible, lambda data: data[1]):
            conv = []
            for mimetype_in, mimetype_out in list(g):
                ok = self.conv.quick_check(mimedata, mimetype_in, mimetype_out)

                if ok:
                    conv.append((mimetype_in, mimetype_out))
            if conv:
                possible_conv[k] = conv

        nb_choice = len(possible_conv.keys())
        if nb_choice == 0:
            return None, None
        elif nb_choice == 1:
            selected = possible_conv.keys()[0]
        else:
            keys = sorted(possible_conv.keys())
            labels = [self._labels[k] for k in keys]
            selector = DropSelector(keys, labels)
            dialog = ModalDialog(selector)
            if pos:
                dialog.move(pos)
            if dialog.exec_():
                selected = selector.mimetype()
            else:
                return None, None
        return possible_conv, selected

    def drop_event(self, event):
        mimedata = event.mimeData()
        pos = self.widget.mapToGlobal(event.pos())
        possible_conv, selected = self._drop(mimedata, pos)
        for mimetype_in, mimetype_out in possible_conv[selected]:
            try:
                data, kwds = self.conv.qtdecode(mimedata, mimetype_in, mimetype_out)
                kwds['mimedata'] = mimedata
                self.drop_callbacks[selected](data, **kwds)
            except CustomException, e:
                make_error_dialog(e)
            else:
                event.acceptProposedAction()
                return QtGui.QWidget.dropEvent(self.widget, event)
