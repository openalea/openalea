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

from Qt import QtWidgets, QtGui, QtCore

from openalea.core.control.manager import ControlContainer
from openalea.core.control.pyserial import save_controls
from openalea.core.observer import AbstractListener
from openalea.core.path import path
from openalea.oalab.control.editor import ControlEditor
from openalea.oalab.service.drag_and_drop import add_drag_format, encode_to_qmimedata
from openalea.oalab.service.qt_control import qt_painter, qt_editor
from openalea.oalab.utils import ModalDialog


class ControlView(QtWidgets.QTreeView):
    controlsSelected = QtCore.Signal(list)

    def __init__(self):
        QtWidgets.QTreeView.__init__(self)
        self.setEditTriggers(self.DoubleClicked)
        self.setSelectionMode(self.SingleSelection)
        self.setSelectionBehavior(self.SelectRows)
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragOnly)
        self.setSortingEnabled(False)
        self.delegate = ValueControlDelegate()
        self.delegate0 = NameControlDelegate()
        self.setItemDelegateForColumn(0, self.delegate0)
        self.setItemDelegateForColumn(1, self.delegate)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(False)
        self._selected_indexes = None

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        action = QtWidgets.QAction("New control", menu)
        action.triggered.connect(self.new_control)
        menu.addAction(action)

        if self.selectedIndexes():
            self._selected_indexes = self.selectedIndexes()
            action = QtWidgets.QAction("Delete control", menu)
            action.triggered.connect(self.delete_control)
            menu.addAction(action)

        action = QtWidgets.QAction("Import L-Py controls", menu)
        action.triggered.connect(self.import_lpy)
        menu.addAction(action)
        action = QtWidgets.QAction("Export L-Py controls", menu)
        action.triggered.connect(self.export_lpy)
        menu.addAction(action)

        action = QtWidgets.QAction("Save controls", menu)
        action.triggered.connect(self.save_controls)
        menu.addAction(action)

        action = QtWidgets.QAction("Load controls", menu)
        action.triggered.connect(self.load_controls)
        menu.addAction(action)

        menu.exec_(event.globalPos())

    def new_control(self):
        editor = ControlEditor('control')
        dialog = ModalDialog(editor)
        if dialog.exec_():
            control = editor.control()
            if self.model()._manager.control(control.name):
                QtWidgets.QMessageBox.information(self, 'Error on adding control',
                                              'A control with name %s already exists' % control.name)
            else:
                self.model().add_control(control)

    def delete_control(self):
        if self._selected_indexes is None:
            return
        self.model().remove_controls(self._selected_indexes)
        self._selected_indexes = None

    def save_controls(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Select python file')
        if filename:
            save_controls(self.model()._manager.controls(), filename)

    def load_controls(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Select python file')
        if filename:
            if path(filename).exists():
                self.model()._manager.clear()
                code = file(filename, 'r').read()
                exec(code)

    def import_lpy(self):
        from openalea.plantlab.lpycontrol import import_lpy_controls
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Select L-Py file')
        if filename:
            import_lpy_controls(filename)

    def export_lpy(self):
        from openalea.plantlab.lpycontrol import export_lpy_controls
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Select L-Py file')
        if filename:
            mcontrols = [(c.name, c.interface, c.value) for c in self.model()._manager.controls()]
            export_lpy_controls(mcontrols, filename)

    def selectionChanged(self, selected, deselected):
        rows = set()
        for index in selected.indexes():
            rows.add(index.row())
        controls = []
        for row in rows:
            index = self.model().createIndex(row, 1)
            controls.append(self.model().control(index))
        self.controlsSelected.emit(controls)
        return QtWidgets.QTreeView.selectionChanged(self, selected, deselected)

    def onRowsInserted(self, *args, **kwargs):
        self.resizeColumnToContents(0)


class ValueControlDelegate(QtWidgets.QStyledItemDelegate):

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
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def setModelData(self, editor, model, index):
        model.setData(index, str(editor.value()), QtCore.Qt.DisplayRole)
        model.setData(index, editor.value(), QtCore.Qt.EditRole)
        control = model.control(index)
        editor.set(control, False, False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def external_edition(self, index):
        self.external_edit_required.emit(index)


class NameControlDelegate(QtWidgets.QStyledItemDelegate):

    def setEditorData(self, editor, index):
        control = index.model().control(index)
        editor.setText(control.name)

    def setModelData(self, editor, model, index):
        control = model.control(index)
        control.name = editor.text()
        QtWidgets.QStyledItemDelegate.setModelData(self, editor, model, index)


class ControlModel(QtGui.QStandardItemModel, AbstractListener):

    def __init__(self, manager=None):
        QtGui.QStandardItemModel.__init__(self)
        AbstractListener.__init__(self)

        self._headers = [u'Name', u'Value']
        self.setHorizontalHeaderLabels(self._headers)

        self._control_index = {}
        self._index_control = {}
        self._manager = None
        self.set_manager(manager)

        add_drag_format(self, "openalealab/control")

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

    def mimeData(self, indices):
        for index in indices:
            control = self.control(index)
        return encode_to_qmimedata(control, "openalealab/control")

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole and index.column() == 0:
            return unicode(self.control(index).label)
        elif role == QtCore.Qt.DisplayRole and index.column() == 1:
            return unicode(self.control(index).value)
        else:
            return QtGui.QStandardItemModel.data(self, index, role)

    def _create_control(self, control):
        args = [QtGui.QStandardItem(a) for a in [control.name, str(control.value)]]
        self._control_index[control] = self.rowCount()
        self._index_control[self.rowCount()] = control
        self.appendRow(args)

        # Example of child for a control. Could be used to display a preview
        # name = args[0]
        # name.appendRow(QtGui.QStandardItem("test"))

    def notify(self, sender, event):
        signal, data = event
        if isinstance(sender, ControlContainer):
            if signal == 'state_changed':
                self.refresh()
            # Refresh index corresponding to changed control
            elif signal in ('control_value_changed', 'control_name_changed'):
                control, value = data
                if control in self._control_index:
                    index = self.createIndex(self._control_index[control], 1, object=0)
                    self.dataChanged.emit(index, index)

    def refresh(self):
        self.clear()
        if self._manager:
            for control in self._manager.controls():
                self._create_control(control)

    def clear(self):
        self._control_index = {}
        self._index_control = {}
        QtGui.QStandardItemModel.clear(self)

    def control(self, index):
        return self._index_control[index.row()]

    def add_control(self, control):
        self._manager.add_control(control)

    def remove_controls(self, indices):
        controls = set()
        for index in indices:
            controls.add(self.control(index))
        for control in controls:
            self._manager.remove_control(control)
