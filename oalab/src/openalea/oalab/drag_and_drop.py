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
"""
This module define classes to manage drag and drop in a universal way: approach is the same for all widgets.
It provides 2 main classes:

DragHandler: knows how to transform python object to QMimeData and be able to create a drag action
DropHandler: knows how to convert a QMimeData to a python object compatible with widget 
DropSelector*: Widgets used if more than one drop type are available. Allow user to choose which drop type to use.
"""

import itertools

from openalea.core.customexception import CustomException
from openalea.oalab.mimedata import MimeCodecManager

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.utils import ModalDialog, make_error_dialog

mcm = MimeCodecManager()


def encode_to_qmimedata(data, mimetype):
    possible_conv = {}
    for k, g in itertools.groupby(mcm._registry_encode, lambda data: data[0]):
        possible_conv[k] = list(g)

    qmimedata = QtCore.QMimeData()
    if mimetype in possible_conv:
        for mimetype_in, mimetype_out in possible_conv[mimetype]:
            qmimedata = mcm.qtencode(data, qmimedata, mimetype_in, mimetype_out)
    return qmimedata


class DropSelectorWidget(QtGui.QWidget):

    def __init__(self, lst, labels=None):
        QtGui.QWidget.__init__(self)

        if labels is None:
            labels = {}

        self._layout = QtGui.QVBoxLayout(self)

        self._cb = QtGui.QComboBox()
        self._lst = lst
        for i, mimetype in enumerate(self._lst):
            self._cb.addItem(labels.get(mimetype, mimetype))

        self._layout.addWidget(QtGui.QLabel("Drop as ..."))
        self._layout.addWidget(self._cb)

    def mimetype(self):
        return self._lst[self._cb.currentIndex()]


class DropSelectorMenu(QtGui.QMenu):

    def __init__(self, lst, labels=None, tooltip=None):
        QtGui.QMenu.__init__(self)

        if labels is None:
            labels = {}
        if tooltip is None:
            tooltip = {}

        self._mimetype = None
        self._action = {}
        lst.sort()
        for mimetype in sorted(lst):
            label = labels.get(mimetype, mimetype)
            action = QtGui.QAction(label, self)
            tt = '%s (%s)' % (label, mimetype)
            action.setToolTip(tt)
            action.triggered.connect(self._triggered)
            self._action[action] = mimetype
            self.addAction(action)

    def _triggered(self):
        action = self.sender()
        self._mimetype = self._action[action]

    def mimetype(self):
        return self._mimetype


class DragHandler(object):

    def __init__(self, widget, **kwds):
        self.widget = widget
        self._kwds = kwds
        self._drag_format = []
        self._drag_kwds = {}

        if isinstance(widget, QtGui.QStandardItemModel):
            self.mimeTypes = self.mime_types

    def mime_types(self):
        return self._drag_format

    def add_drag_format(self, mimetype_out, **kwds):
        self._drag_format.append(mimetype_out)
        self._drag_kwds[mimetype_out] = kwds


class DropHandler(object):

    def __init__(self, widget, **kwds):
        self.widget = widget
        self._kwds = kwds
        self._drop_callbacks = {}
        self._drop_kwds = {}

        mcm.init()

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
        self._drop_kwds[mimetype_out] = kwds
        self._drop_callbacks[mimetype_out] = callback

        for conv in mcm._registry_decode:
            if conv[1].startswith(mimetype_out):
                if conv[1] not in self._drop_callbacks:
                    self.add_drop_callback(conv[1], callback, **kwds)

    def insert_from_mime_data(self, source):
        cursor = self.widget.textCursor()
        rect = self.widget.cursorRect()
        pos = self.widget.viewport().mapToGlobal(rect.center())
        possible_conv, selected = self._drop(source, pos=pos)
        if possible_conv is None:
            return
        for mimetype_in, mimetype_out in possible_conv[selected]:
            try:
                data, kwds = mcm.qtdecode(source, mimetype_in, mimetype_out)
            except CustomException, e:
                make_error_dialog(e)
            else:
                kwds['mimedata'] = source
                kwds['cursor'] = cursor
                self._drop_callbacks[selected](data, **kwds)

    def _compatibe_mime(self, mimetype_in_list):
        return mcm.compatible_mime(mimetype_in_list, self._drop_callbacks.keys())

    def can_insert_from_mime_data(self, source):
        self._compatible = self._compatibe_mime(source.formats())
        return bool(self._compatible)

    def drag_enter_event(self, event):
        mimedata = event.mimeData()
        self._compatible = mcm.compatible_mime(mimedata.formats(), mimetype_out_list=self._drop_callbacks.keys())

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

    def _labels(self, possible_conv):
        labels = {}
        for all_conv in possible_conv.values():
            for conv in all_conv:
                plugin = mcm._registry_decode_plugin[conv]
                if hasattr(plugin, 'mimetype_desc'):
                    for mimetype, desc in plugin.mimetype_desc.items():
                        if 'title' in desc:
                            labels[mimetype] = desc['title']
        return labels

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
                ok = mcm.quick_check(mimedata, mimetype_in, mimetype_out)

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
            labels = self._labels(possible_conv)

            #for k:'%s (%s)' % (self._drop_kwds[k]['title'], k) for k in keys}
            selector = DropSelectorMenu(keys, labels)
            if selector.exec_(pos):
                selected = selector.mimetype()
            else:
                return None, None
        return possible_conv, selected

    def drop_event(self, event):
        mimedata = event.mimeData()
        pos = self.widget.mapToGlobal(event.pos())
        possible_conv, selected = self._drop(mimedata, pos)
        if possible_conv is None:
            return
        for mimetype_in, mimetype_out in possible_conv[selected]:
            try:
                data, kwds = mcm.qtdecode(mimedata, mimetype_in, mimetype_out)
                kwds['mimedata'] = mimedata
                self._drop_callbacks[selected](data, **kwds)
            except CustomException, e:
                make_error_dialog(e)
            else:
                event.acceptProposedAction()
                return QtGui.QWidget.dropEvent(self.widget, event)
