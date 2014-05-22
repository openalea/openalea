
from openalea.vpltk.qt import QtGui
from openalea.oalab.gui.stdcontrolwidget import IntSpinBox

from openalea.core import Node, Factory, IBool, IInt, IStr, IEnumStr
from openalea.core.node import FuncNode
from openalea.core.traitsui import View, Group, Item
from openalea.visualea.node_widget import DefaultNodeWidget

view = View(
    Group('New control', Item('name'), Item('interface'), layout="-")
    )

inputs = [
    {'interface': IStr, 'name': 'name', 'value': 'variable', 'desc': ''},
    {'interface': IEnumStr, 'name': 'interface', 'value': 'IInt', 'desc': ''},
    ]

def f(*args, **kargs):
    print 'f', args, kargs

node_factory = Factory(name='toto',
                authors=' (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='test_control_manager',
                nodeclass='f',
                inputs=inputs,
                view=view,
                )


class ControlManager(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QHBoxLayout(self)

        self.view = QtGui.QTreeView()
        self.model = QtGui.QStandardItemModel()
        self.view.setModel(self.model)

        self._layout.addWidget(self.view)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        action = QtGui.QAction("New control", menu)
        action.triggered.connect(self.new_control)
        menu.addAction(action)
        menu.exec_(event.globalPos())

    def new_control(self):
        pass



if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    win = ControlManager()
    win.show()

    node = node_factory.instantiate()
    w = DefaultNodeWidget(node, parent=None)
    w.show()

    if instance is None :
        app.exec_()


