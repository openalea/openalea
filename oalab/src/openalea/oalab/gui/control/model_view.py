# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
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
from openalea.vpltk.qt.compat import to_qvariant

from openalea.core.observer import AbstractListener
from openalea.oalab.service.control import qt_painter, qt_editor
from openalea.oalab.service.mimetype import encode
from openalea.oalab.control.manager import ControlContainer
from openalea.oalab.gui.control.editor import ControlEditor
from openalea.oalab.gui.utils import ModalDialog

class ControlView(QtGui.QTreeView):
    controlsSelected = QtCore.Signal(list)

    def __init__(self):
        QtGui.QTreeView.__init__(self)
        self.setEditTriggers(self.DoubleClicked)
        self.setSelectionMode(self.SingleSelection)
        self.setSelectionBehavior(self.SelectRows)
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragOnly)
        self.setSortingEnabled(True)
        self.delegate = ControlDelegate()
        self.setItemDelegateForColumn(1, self.delegate)
        self.setHeaderHidden(False)
        self._i = 1

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction("New control", menu)
        action.triggered.connect(self.new_control)
        menu.addAction(action)
        menu.exec_(event.globalPos())

    def new_control(self):
        editor = ControlEditor('control_%d' % self._i)
        dialog = ModalDialog(editor)
        if dialog.exec_():
            self.model().add_control(editor.control())
        self._i += 1

    def selectionChanged(self, selected, deselected):
        rows = set()
        for index in selected.indexes():
            rows.add(index.row())
        controls = []
        for row in rows:
            index = self.model().createIndex(row, 1)
            controls.append(self.model().control(index))
        self.controlsSelected.emit(controls)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            print 'rm'

class ControlDelegate(QtGui.QStyledItemDelegate):

    external_edit_required = QtCore.Signal(QtCore.QModelIndex)

    def createEditor(self, parent, option, index):
        model = index.model()
        control = model.control(index)
        widget = qt_editor(control, shape='hline', preferred=control.widget)
        if widget is None:
            self.external_edition(index)
        else:
            widget.setParent(parent)
            widget.set(control, True, True)
        return widget

    def setEditorData(self, editor, index):
        pass

    def paint(self, painter, option, index):
        model = index.model()
        control = model.control(index)
        paint = qt_painter(control, shape='hline')
        if paint:
            paint(control, painter, option.rect, option)
        else:
            QtGui.QStyledItemDelegate.paint(self, painter, option, index)

    def setModelData(self, editor, model, index):
        model.setData(index, str(editor.value()), QtCore.Qt.DisplayRole)
        model.setData(index, editor.value(), QtCore.Qt.EditRole)
        control = model.control(index)
        editor.set(control, False, False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def external_edition(self, index):
        self.external_edit_required.emit(index)

class ControlModel(QtGui.QStandardItemModel, AbstractListener):
    def __init__(self, manager=None):
        QtGui.QStandardItemModel.__init__(self)
        AbstractListener.__init__(self)

        self._headers = [u'Name', u'Value']
        self.setHorizontalHeaderLabels(self._headers)

        self._control_index = {}
        self._manager = None
        self.set_manager(manager)

    def set_manager(self, manager=None):
        if manager is self._manager:
            return
        if self._manager:
            self._manager.unregister_listener(self)
        self._manager = manager
        if manager is not None:
            self._manager.register_listener(self)
        self.refresh()

    def flags(self, index):
        default_flags = QtGui.QStandardItemModel.flags(self, index)
        if (index.isValid()):
            return QtCore.Qt.ItemIsDragEnabled | default_flags
        else:
            return QtCore.Qt.ItemIsDropEnabled | default_flags

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[col]
        return None

    def supportedDragActions(self, *args, **kwargs):
        return QtGui.QStandardItemModel.supportedDragActions(self, *args, **kwargs)

    def mimeTypes(self):
        return ["openalealab/control"]

    def mimeData(self, indices):
        for index in indices:
            control = self.control(index)
        mimetype, mimedata = encode(control)
        qmime_data = QtCore.QMimeData()
        qmime_data.setData(mimetype, mimedata)
        qmime_data.setText(mimedata)
        return qmime_data

    def data (self, index, role):
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            return unicode(self.control(index).value)
        else:
            return QtGui.QStandardItemModel.data(self, index, role)

    def _create_control(self, control):
        args = [QtGui.QStandardItem(a) for a in [control.name, str(control.value)]]
        self._control_index[control] = self.rowCount()
        self.appendRow(args)

        # Example of child for a control. Could be used to display a preview
        # name = args[0]
        # name.appendRow(QtGui.QStandardItem("test"))

    def notify(self, sender, event):
        signal, data = event
        if isinstance(sender, ControlContainer):
            if signal == 'state_changed':
                self.refresh()
            elif signal == 'control_value_changed':
                control, value = data
                if control in self._control_index:
                    index = self.createIndex(self._control_index[control], 1, object=0)
                    self.dataChanged.emit(index, index)

    def refresh(self):
        self.clear()
        if self._manager:
            for control in self._manager.controls().values():
                self._create_control(control)

    def control(self, index):
        cnum = index.row()
        name = self.item(cnum, 0).text()
        return self._manager.control(name)

    def add_control(self, control):
        self._manager.add_control(control)
