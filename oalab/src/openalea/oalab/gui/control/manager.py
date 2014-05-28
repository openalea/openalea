
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener

from openalea.oalab.gui.control.model_view import ControlModel, ControlDelegate
from openalea.oalab.gui.control.editor import ControlEditorDialog
from openalea.oalab.control.manager import ControlManager

class ControlManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QHBoxLayout(self)

        self._manager = ControlManager()

        self.model = ControlModel(self._manager)

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
