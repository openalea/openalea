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
from openalea.oalab.utils import ModalDialog, make_error_dialog
from openalea.vpltk.qt import QtGui, QtCore


from openalea.oalab.service.mimedata import (possible_conv, compatible_mime,
                                             decode_function, decode_plugin,
                                             qtencode, qtdecode, quick_check)


def encode_to_qmimedata(data, mimetype):
    _possible_conv = possible_conv(data, mimetype)

    qmimedata = QtCore.QMimeData()
    if mimetype in _possible_conv:
        for mimetype_in, mimetype_out in _possible_conv[mimetype]:
            qmimedata = qtencode(data, qmimedata, mimetype_in, mimetype_out)
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
    """
    Adapt widget to support OpenAleaLab drag and drop.
    """

    def __init__(self, widget, **kwds):
        self.widget = widget
        self._kwds = kwds
        self._drop_callbacks = {}
        self._drop_kwds = {}

        self._compatible = None

        # Drop part
        self.widget.setAcceptDrops(True)
        if isinstance(widget, (QtGui.QPlainTextEdit, QtGui.QTextEdit)):
            self.widget.canInsertFromMimeData = self.can_insert_from_mime_data
            self.widget.insertFromMimeData = self.insert_from_mime_data
        else:
            self.widget.dragEnterEvent = self.drag_enter_event
            self.widget.dropEvent = self.drop_event
            self.widget.dragLeaveEvent = self.drag_leave_event

    def add_drop_callback(self, mimetype_out, callback, **kwds):
        self._drop_kwds[mimetype_out] = kwds
        self._drop_callbacks[mimetype_out] = callback

        conv = decode_function(mimetype_out)
        if conv and conv not in self._drop_callbacks:
            self.add_drop_callback(conv, callback, **kwds)

    def insert_from_mime_data(self, source):
        cursor = self.widget.textCursor()
        rect = self.widget.cursorRect()
        pos = self.widget.viewport().mapToGlobal(rect.center())
        possible_conv, selected = self._drop(source, pos=pos)

        # If not explicitly defined, use widget default drag and drop
        if not possible_conv:
            self._compatible = None
            return super(self.widget.__class__, self.widget).insertFromMimeData(source)

        for mimetype_in, mimetype_out in possible_conv[selected]:
            try:
                data, kwds = qtdecode(source, mimetype_in, mimetype_out)
            except CustomException as e:
                make_error_dialog(e)
            else:
                kwds['mimedata'] = source
                kwds['cursor'] = cursor
                self._drop_callbacks[selected](data, **kwds)
            self._compatible = None

    def _compatible_mime(self, mimetype_in_list):
        return compatible_mime(mimetype_in_list, self._drop_callbacks.keys())

    def can_insert_from_mime_data(self, source):
        default = super(self.widget.__class__, self.widget).canInsertFromMimeData(source)
        self._compatible = self._compatible_mime(source.formats())
        return bool(self._compatible) or default

    def drag_enter_event(self, event):
        mimedata = event.mimeData()
        self._compatible = self._compatible_mime(mimedata.formats())

        if self._compatible:
            event.acceptProposedAction()
            return super(self.widget.__class__, self.widget).dragEnterEvent(event)
        else:
            return super(self.widget.__class__, self.widget).dragEnterEvent(event)

    def drag_leave_event(self, event):
        self._compatible = None
        return super(self.widget.__class__, self.widget).dragLeaveEvent(event)

    def drag_move_event(self, event):
        if self._compatible:
            event.acceptProposedAction()
        else:
            return super(self.widget.__class__, self.widget).dragMoveEvent(event)

    def _labels(self, possible_conv):
        labels = {}
        for all_conv in possible_conv.values():
            for conv in all_conv:
                plugin = decode_plugin(conv)
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
        if not self._compatible:
            return {}, None

        for k, g in itertools.groupby(self._compatible, lambda data: data[1]):
            conv = []
            for mimetype_in, mimetype_out in list(g):
                ok = quick_check(mimedata, mimetype_in, mimetype_out)

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
            self._compatible = None
        for mimetype_in, mimetype_out in possible_conv[selected]:
            try:
                data, kwds = qtdecode(mimedata, mimetype_in, mimetype_out)
                kwds['mimedata'] = mimedata
                self._drop_callbacks[selected](data, **kwds)
            except CustomException as e:
                make_error_dialog(e)
            else:
                event.acceptProposedAction()
                return QtGui.QWidget.dropEvent(self.widget, event)
            self._compatible = None
