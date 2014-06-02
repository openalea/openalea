
import weakref

from openalea.vpltk.qt import QtGui, QtCore

from openalea.core.observer import AbstractListener
from openalea.oalab.service.control import edit_qt
from openalea.oalab.service.mimetype import encode
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.gui.control.editor import ControlEditorDialog

class ControlView(QtGui.QTreeView):
    def __init__(self):
        QtGui.QTreeView.__init__(self)
        self.setEditTriggers(self.DoubleClicked)
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragOnly)
        self.setSortingEnabled(True)
        self.setItemDelegateForColumn(1, ControlDelegate())
        self.setHeaderHidden(False)
        self._i = 1

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction("New control", menu)
        action.triggered.connect(self.new_control)
        menu.addAction(action)
        menu.exec_(event.globalPos())

    def new_control(self):
        dial = ControlEditorDialog('control_%d' % self._i)
        dial.exec_()
        self.model().add_control(dial.control())
        self._i += 1

class ControlDelegate(QtGui.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        model = index.model()
        control = model.control(index)
        widget = edit_qt(control)
        widget.setParent(parent)
        return widget

    def setEditorData(self, editor, index):
        model = index.model()
        control = model.control(index)
        # Force editor refresh
        control.notify_change()

    def paint(self, painter, option, index):
        model = index.model()
        control = model.control(index)
#
# #         paint_cell = get_paint_function(item.datum, self.custom)
# #         if paint_cell :
# #             ok = paint_cell(self, painter, option, index, item.datum)
# #             if not ok :
# #                 QtGui.QStyledItemDelegate.paint(self, painter, option, index)
# #         else :
        QtGui.QStyledItemDelegate.paint(self, painter, option, index)

    def setModelData(self, editor, model, index):
        model.setData(index, str(editor.value()), QtCore.Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class ControlModel(QtGui.QStandardItemModel, AbstractListener):
    def __init__(self, manager):
        QtGui.QStandardItemModel.__init__(self)
        AbstractListener.__init__(self)

        self._current_model = None

        self._headers = [u'Name', u'Value']
        self.setHorizontalHeaderLabels(self._headers)
        self._manager = manager
        self.initialise(manager)

    def set(self, model_id=None):
        self._current_model = model_id
        self.refresh(model_id)

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

    def mimeData(self, indexes):
        for index in indexes:
            control = self.control(index)
        mimetype, mimedata = encode(control)
        qmime_data = QtCore.QMimeData()
        qmime_data.setData(mimetype, mimedata)
        qmime_data.setText(mimedata)
        return qmime_data

    def _create_control(self, control):
        args = [QtGui.QStandardItem(a) for a in [control.name, str(control.value)]]
        self.appendRow(args)

        # Example of child for a control. Could be used to display a preview
        # name = args[0]
        # name.appendRow(QtGui.QStandardItem("test"))

    def notify(self, sender, event):
        signal, data = event
        if isinstance(sender, ControlManager) and signal == 'state_changed':
            control, model = data
            if model == self._current_model:
                self.refresh(model)

    def refresh(self, model=None):
        self.clear()
        for control in self._manager.controls(model).values():
            self._create_control(control)

    def control(self, index):
        cnum = index.row()
        name = self.item(cnum, 0).text()
        return self._manager.control(name, model=self._current_model)

    def add_control(self, control):
        self._manager.add_control(control, model=self._current_model)
