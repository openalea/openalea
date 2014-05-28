
import weakref

from openalea.vpltk.qt import QtGui, QtCore

from openalea.core.observer import AbstractListener
from openalea.oalab.service.control import edit_qt
from openalea.oalab.service.mimetype import encode
from openalea.oalab.control.manager import ControlManager

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
    def __init__(self, manager, *args, **kwargs):
        QtGui.QStandardItemModel.__init__(self, *args, **kwargs)
        AbstractListener.__init__(self)

        self._manager = manager
        self.initialise(manager)

    def flags(self, index):
        default_flags = QtGui.QStandardItemModel.flags(self, index)
        if (index.isValid()):
            return QtCore.Qt.ItemIsDragEnabled | default_flags
        else:
            return QtCore.Qt.ItemIsDropEnabled | default_flags

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

    def notify(self, sender, event):
        signal, data = event
        if isinstance(sender, ControlManager) and signal == 'state_changed':
            self.clear()
            for control in sender.controls.values():
                self._create_control(control)

    def control(self, index):
        cnum = index.row()
        name = self.item(cnum, 0).text()
        return self._manager.control(name)
