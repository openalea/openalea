
import weakref

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.gui.stdcontrolwidget import IntSpinBox
from openalea.core.observer import AbstractListener, Observed
from openalea.oalab.service.control import discover_qt_controls, edit_qt, qt_editors
from openalea.oalab.service.interface import get_interface
from openalea.oalab.service.mimetype import encode, decode
from openalea.oalab.control.control import Control
from openalea.oalab.control.manager import ControlManager

class ControlDelegate(QtGui.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        model = index.model()
        control = model.control(index)
        widget = edit_qt(control)
        widget.setParent(parent)
        return widget

    def setEditorData(self, editor, index):
        pass

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
        args = [QtGui.QStandardItem(a) for a in [control.name, str(control.value())]]
        self.appendRow(args)

    def notify(self, sender, event):
        signal, data = event
        if signal == 'ControlManagerChanged':
            self.clear()
            for control in sender.controls.values():
                self._create_control(control)

    def control(self, index):
        cnum = index.row()
        name = self.item(cnum, 0).text()
        return self._manager.control(name)

class ControlEditorDialog(QtGui.QDialog):
    def __init__(self, name='default'):
        QtGui.QDialog.__init__(self)

        self._interfaces = []
        self._constraints = None

        self.e_name = QtGui.QLineEdit(name)
        self.cb_interface = QtGui.QComboBox()
        self.cb_widget = QtGui.QComboBox()


        self._layout = QtGui.QVBoxLayout(self)


        widget = QtGui.QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        self._layout_control = QtGui.QFormLayout(widget)
        self._layout_control.addRow(QtGui.QLabel(u'Name'), self.e_name)
        self._layout_control.addRow(QtGui.QLabel(u'Interface'), self.cb_interface)
        self._layout_control.addRow(QtGui.QLabel(u'Widget'), self.cb_widget)

        self._l_constraints = QtGui.QLabel("Constraints")

        self._layout.addWidget(QtGui.QLabel("Control"))
        self._layout.addWidget(widget)
        self._layout.addWidget(self._l_constraints)
        self._layout.addStretch()


        controls = discover_qt_controls()
        for iname, widgets in controls.items() :
            self._interfaces.append(iname)
            self.cb_interface.addItem(iname)

        self.cb_interface.currentIndexChanged.connect(self.refresh)
        self.cb_widget.currentIndexChanged.connect(self.on_widget_changed)

        self.refresh()

    def on_widget_changed(self):
        widget_name = self.cb_widget.currentText()
        interface_name = self.cb_interface.currentText()
        qt_controls = discover_qt_controls()[interface_name]
        widget = None

        for plugin in qt_controls :
            if widget_name == plugin.name:
                widget = plugin.load()
                break

        if self._constraints:
            widget = self._constraints()
            self._layout.removeWidget(widget)
            widget.close()
            self._constraints = None
            self._l_constraints.hide()

        if widget and hasattr(widget, 'edit_constraints'):
            widget_constraints = widget.edit_constraints()
            widget_constraints.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self._layout.addWidget(widget_constraints)
            self._l_constraints.show()

            self._constraints = weakref.ref(widget_constraints)

    def refresh(self):
        iname = str(self.cb_interface.currentText())
        editors = qt_editors(iname)
        self.cb_widget.clear()
        for widget in editors:
            self.cb_widget.addItem(str(widget.name))

    def control(self):
        return [
            self.e_name.text(),
            self.cb_interface.currentText(),
            None,
            self.cb_widget.currentText(),
            self.constraints()
            ]

    def constraints(self):
        if self._constraints:
            return self._constraints().constraints()
        else:
            return {}


class ControlManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self, manager):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QHBoxLayout(self)

        self._manager = manager

        self.model = ControlModel(manager)

        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.view.pressed.connect(self.on_control_selected)
        self.view.setEditTriggers(self.view.AllEditTriggers)
        self.view.setDragEnabled(True)
        self.view.setDragDropMode(self.view.DragOnly)
        self.view.setSortingEnabled(True)
        self.view.setItemDelegateForColumn(1, ControlDelegate())

        self._layout.addWidget(self.view)

        self._i = 1

    def on_control_selected(self, index):
        print self.model.control(index)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction("New control", menu)
        action.triggered.connect(self.new_control)
        menu.addAction(action)
        menu.exec_(event.globalPos())

    def new_control(self):
        dial = ControlEditorDialog('control_%d' % self._i)
        dial.exec_()
        self._manager.add_control(dial.control())
        self._i += 1


if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    cm = ControlManager()

    w = ControlManagerWidget(cm)
    w.show()

    cm.add_control(Control('a', 'IInt', widget='IntSpinBox'))
    c2 = Control('b', 'IInt', widget='IntSlider')
    c2.interface.min = 0
    c2.interface.max = 100
    cm.add_control(c2)

#     from openalea.oalab.editor.text_editor import TextEditor
#     from openalea.oalab.editor.highlight import Highlighter
#     text = TextEditor()
#     Highlighter(text)
#     text.show()
#     text.raise_()

#     w = Dialog()
#     w.show()
    w.raise_()

    if instance is None :
        app.exec_()


    print cm.namespace()

