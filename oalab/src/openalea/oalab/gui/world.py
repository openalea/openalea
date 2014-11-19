# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = ""

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener
from openalea.oalab.session.session import Session


class GenericWorldBrowser(QtGui.QWidget):

    def __init__(self):
        super(GenericWorldBrowser, self).__init__()
        layout = QtGui.QGridLayout()
        self.model = WorldModel()
        self.tree = QtGui.QTreeView()
        self.tree.setModel(self.model)
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def set_world(self, world):
        self.model.set_world(world)
        self.tree.expandAll()


class WorldBrowser(GenericWorldBrowser, AbstractListener):

    def __init__(self, world=None):
        AbstractListener.__init__(self)
        super(WorldBrowser, self).__init__()
        if world:
            self.set_world(self.world)
        else:
            session = Session()
            if session.world:
                self.set_world(self.world)

        QtCore.QObject.connect(self.tree, QtCore.SIGNAL('doubleClicked(const QModelIndex&)'), self.show_world_object)

        actionClearWorld = QtGui.QAction(QtGui.QIcon(":/images/resources/plant.png"), "Clear World", self)
        actionClearWorld.triggered.connect(self.clear)
        self._actions = [["Project", "World", actionClearWorld, 0]]

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return self.actions()

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'WorldChanged':
            self.set_world(data)

    def show_world_object(self, index):
        item = index.model().itemFromIndex(index)
        world_name = item.text()
        if world_name in self.world:
            print "World object named ", world_name, " : ", self.world[world_name]

    def clear(self):
        if self.world:
            self.world.clear()

    def set_world(self, world):
        if self.world is world:
            return
        if self.world:
            self.world.unregister_listener(self)
        self.world = world
        self.world.register_listener(self)
        self.model.set_world(self.world)
        self.tree.expandAll()


class WorldModel(QtGui.QStandardItemModel):

    def set_world(self, world={}):
        self.clear()
        parentItem = self.invisibleRootItem()
        self.setHorizontalHeaderLabels(["World Objects", "Type"])
        world_objects = world.keys()
        for world_object in world_objects:
            item1 = QtGui.QStandardItem(world_object)
            objtype = type(world[world_object].obj).__name__
            item2 = QtGui.QStandardItem(str(objtype))
            parentItem.appendRow([item1, item2])


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    world = dict()
    world["obj1"] = "plop"
    world["obj2"] = "plop2"
    world["obj3"] = "plop3"
    world["obj4"] = "plop4"
    world["obj5"] = "plop5"
    wid = GenericWorldBrowser()
    wid.set_world(world)
    wid.show()
    app.exec_()


if __name__ == "__main__":
    main()
