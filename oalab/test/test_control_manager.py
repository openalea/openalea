
from openalea.vpltk.qt import QtGui
from openalea.oalab.gui.stdcontrolwidget import IntSpinBox
from openalea.core.observer import AbstractListener, Observed
from openalea.oalab.service.control import discover_qt_controls, edit_qt
from openalea.oalab.service.interface import interface
from openalea.oalab.control.control import Control

class ControlManager(Observed):

    def __init__(self):
        Observed.__init__(self)
        self._controls = []

    def add_control(self, name, interface, widget):
        self._controls.append([name, interface, widget])
        self.notify_listeners(('ControlManagerChanged', None))

    controls = property(fget=lambda self:self._controls)

class Dialog(QtGui.QDialog):
    def __init__(self, name='default'):
        QtGui.QDialog.__init__(self)

        self.e_name = QtGui.QLineEdit(name)
        self.cb_interface = QtGui.QComboBox()
        self.cb_widget = QtGui.QComboBox()

        self._layout = QtGui.QFormLayout(self)
        self._layout.addRow(QtGui.QLabel(u'Name'), self.e_name)
        self._layout.addRow(QtGui.QLabel(u'Interface'), self.cb_interface)
        self._layout.addRow(QtGui.QLabel(u'Widget'), self.cb_widget)

        self._interfaces = []

        controls = discover_qt_controls()
        for iname, widgets in controls.items() :
            self._interfaces.append(iname)
            self.cb_interface.addItem(iname)

        self.cb_interface.currentIndexChanged.connect(self.refresh)

        self.refresh()


    def refresh(self):
        controls = discover_qt_controls()
        self.cb_widget.clear()
        for widget in controls[str(self.cb_interface.currentText())]:
            self.cb_widget.addItem(str(widget.name))

    def control(self):
        return [
            self.e_name.text(),
            self.cb_interface.currentText(),
            self.cb_widget.currentText()
            ]


class ControlManagerWidget(QtGui.QWidget, AbstractListener):
    def __init__(self, manager):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QHBoxLayout(self)

        self._manager = manager

        self.model = QtGui.QStandardItemModel()

        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.view.pressed.connect(self.on_control_selected)
        self.view.setEditTriggers(self.view.SelectedClicked)
        self.view.setDragEnabled(True)
        self.view.setDragDropMode(self.view.DragOnly)

        self._layout.addWidget(self.view)

#         self.w = QtGui.QWidget()
#         self.l = QtGui.QHBoxLayout(self.w)
#         self.w.show()

        self._i = 1



    def on_control_selected(self, idx):
        cnum = idx.row()
        name, _interface, widget = self._manager.controls[cnum]
        control = Control(interface(_interface), name=name)
        print 'disp', control
#         self.l.addWidget(edit_qt(control))

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction("New control", menu)
        action.triggered.connect(self.new_control)
        menu.addAction(action)
        menu.exec_(event.globalPos())

    def _create_control(self, control):
        args = [QtGui.QStandardItem(a) for a in control]
        self.model.appendRow(args)

    def new_control(self):
        dial = Dialog('control_%d' % self._i)
        dial.exec_()
        self._manager.add_control(*dial.control())
        self._i += 1

    def notify(self, sender, event):
        signal, data = event
        if signal == 'ControlManagerChanged':
            self.model.clear()
            for control in sender.controls:
                self._create_control(control)

if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    cm = ControlManager()

    w = ControlManagerWidget(cm)
    w.initialise(cm)
    w.show()

    def drop(event):
        print event
        event.mimeData()
        event.acceptProposedAction()


    cm.add_control('a', 'IInt', 'IntSpinBox')
    cm.add_control('b', 'IInt', 'IntSlider')

#     w = Dialog()
#     w.show()
    w.raise_()

    if instance is None :
        app.exec_()


