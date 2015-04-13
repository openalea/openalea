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
from openalea.oalab.gui.control.manager import ControlManagerWidget
from openalea.core.service.ipython import interpreter as get_interpreter


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

    def __init__(self):
        AbstractListener.__init__(self)
        super(WorldBrowser, self).__init__()
        self.world = None

        QtCore.QObject.connect(self.tree, QtCore.SIGNAL('doubleClicked(const QModelIndex&)'), self.show_world_object)

        actionClearWorld = QtGui.QAction(QtGui.QIcon(":/images/resources/plant.png"), "Clear World", self)
        actionClearWorld.triggered.connect(self.clear)
        self._actions = [["Project", "World", actionClearWorld, 0]]

    def initialize(self):
        from openalea.oalab.world.world import World
        from openalea.core.service.ipython import interpreter
        world = World()
        world.update_namespace(interpreter())
        self.set_world(world)

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return self.actions()

    def notify(self, sender, event=None):
        signal, data = event
        print signal
        if signal == 'world_changed':
            self.set_world(data)
            self.refresh()
        elif signal == 'world_object_changed':
            world = data[0]
            self.set_world(world)
            self.refresh()
        elif signal == 'world_sync':
            self.refresh()

    def show_world_object(self, index):
        item = index.model().itemFromIndex(index)
        world_name = item.text()
        if world_name in self.world:
            print "World object named ", world_name, " : ", self.world[world_name]

    def clear(self):
        if self.world:
            self.world.clear()

    def refresh(self):
        if self.world is not None:
            self.model.set_world(self.world)
            self.tree.expandAll()

    def set_world(self, world):
        if self.world is world:
            return
        if self.world:
            self.world.unregister_listener(self)
        self.world = world
        self.world.register_listener(self)


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


class WorldControlPanel(QtGui.QWidget, AbstractListener):
    StyleTableView = 0
    StylePanel = 1
    DEFAULT_STYLE = StyleTableView

    attributeChanged = QtCore.Signal(str, dict)

    def __init__(self, parent=None, style=None):
        AbstractListener.__init__(self)
        QtGui.QWidget.__init__(self, parent=parent)

        self.world = None
        self.model = WorldModel()

        if style is None:
            style = self.DEFAULT_STYLE
        self.style = style

        self._manager = {}

        self._cb_world_object = QtGui.QComboBox()
        p = QtGui.QSizePolicy
        self._cb_world_object.setSizePolicy(p(p.Expanding, p.Maximum))
        self._cb_world_object.currentIndexChanged.connect(self._selected_object_changed)

        self._current = None
        self._default_manager = self._create_manager()

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_control'] = self

        actionClearWorld = QtGui.QAction(QtGui.QIcon(":/images/resources/plant.png"), "Clear World", self)
        actionClearWorld.triggered.connect(self.clear)
        self._actions = [["Project", "World", actionClearWorld, 0]]

        if self.style == self.StylePanel:
            from openalea.oalab.service.qt_control import edit
            self._view = edit(self._default_manager)
            self._qt_control = {}
            for control, editor in self._view.editor.items():
                self._qt_control[control.name] = editor
        else:
            self._view = ControlManagerWidget(manager=self._default_manager)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self._cb_world_object)
        self._layout.addWidget(self._view)
        # self.setLayout(self._layout)

    def set_properties(self, properties):
        self._view.set_properties(properties)

    def properties(self):
        return self._view.properties()

    def __getitem__(self, key):
        return self._manager[self._current].control(name=key)

    def initialize(self):
        from openalea.oalab.world.world import World
        from openalea.core.service.ipython import interpreter
        world = World()
        world.update_namespace(interpreter())
        self.set_world(world)

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return self.actions()

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_changed':
            print "WorldControlPanel < ", signal
            self.set_world(data)
            self.refresh()
        elif signal == 'world_object_changed':
            print "WorldControlPanel < ", signal
            world, old_object, world_object = data
            self.set_world(world)
            self.refresh()
        elif signal == 'world_object_item_changed':
            print "WorldControlPanel < ", signal
            world, world_object, item, old, new = data
            self.refresh_manager(world_object)
            self.refresh()
        elif signal == 'world_sync':
            print "WorldControlPanel < ", signal, data
            self.clear()
            self.set_world(data)
            self.refresh()

    def clear(self):
        if self.world:
            self.world.clear()
        self._cb_world_object.clear()
        self._manager.clear()
        self._current = None

        if self.style == self.StylePanel:
            from openalea.oalab.service.qt_control import edit
            self._view = edit(self._default_manager)
            self._qt_control = {}
            for control, editor in self._view.editor.items():
                self._qt_control[control.name] = editor
        else:
            self._view.model.set_manager(self._default_manager)
        self.refresh()

    def set_world(self, world):
        print "WorldControlPanel < set_world"
        if self.world:
            self.world.unregister_listener(self)
        self.world = world
        self.world.register_listener(self)
        self.model.set_world(world)
        for object_name in world.keys():
            if object_name not in self._manager:
                manager = self._create_manager(world[object_name])
                self._manager[object_name] = manager
                self._cb_world_object.addItem(object_name)
            self.refresh_manager(world[object_name])
        # if self._current:
        #     print "WorldControlPanel > set_manager",self._current
        #     object_manager = self._manager[self._current]
        #     object_manager.disable_followers()
        #     self._set_manager(object_manager)
        #     object_manager.enable_followers()

    def _create_manager(self, world_object=None):
        from openalea.core.control.manager import ControlContainer
        manager = ControlContainer()

        if world_object:
            for attribute in world_object.attributes:
                attribute_manager = manager.add(
                    attribute['name'],
                    interface=attribute['interface'],
                    value=attribute['value'],
                    alias=attribute['name'])
                if '_alpha' in attribute['name']:
                    attribute_manager.interface.step = 0.1
                    attribute_manager.interface.min = 0
                    attribute_manager.interface.max = 1
                elif 'alphamap' in attribute['name']:
                    attribute_manager.interface.enum = ['constant', 'linear']
                elif 'plane_position' in attribute['name']:
                    for i, axis in enumerate(['x', 'y', 'z']):
                        if axis in attribute['name']:
                            attribute_manager.interface.min = 0
                            attribute_manager.interface.max = world_object.data.shape[i] - 1
                elif 'intensity' in attribute['name']:
                    import numpy as np
                    if isinstance(world_object.data, np.ndarray):
                        attribute_manager.interface.min = int(np.min(world_object.data))
                        attribute_manager.interface.max = int(np.max(world_object.data))

                manager.register_follower(attribute['name'], self._attribute_changed(attribute['name']))

        return manager

    def _selected_object_changed(self, idx):
        if idx != -1:
            self.select_world_object(self._cb_world_object.itemText(idx))

    def _set_manager(self, manager):
        if self.style == self.StylePanel:
            from openalea.oalab.service.qt_control import edit
            self._view = edit(manager)
            # self._qt_control = {}
            # for control, editor in self._view.editor.items():
            #     self._qt_control[control.name] = editor
            #     # editor.set(control)
            # for c_id, weakref in self._qt_control.items():
            #     control = manager.control(name=c_id)
            #     editor = weakref()
            #     if editor and control:
            #         editor.set(control)
        else:
            self._view.model.set_manager(manager)

    def select_world_object(self, object_name):
        if object_name != self._current:
            self._current = object_name
            object_manager = self._manager[object_name]
            object_manager.disable_followers()
            self._set_manager(object_manager)
            object_manager.enable_followers()

    def refresh_manager(self, world_object):
        object_name = world_object.name
        print "WorldControlPanel < refresh_manager ", object_name
        if [c.name for c in self._manager[object_name].controls()] != [a['name'] for a in world_object.attributes]:
            object_manager = self._manager[object_name]
            object_manager.disable_followers()
            object_manager = self._create_manager(world_object)
            if self._current == object_name:
                print "WorldControlPanel > set_manager ", object_name
                self._set_manager(object_manager)
                object_manager.enable_followers()
            self._manager[object_name] = object_manager
        else:
            for a in world_object.attributes:
                if a['value'] != self._manager[object_name].control(a['name']).value:
                    self._manager[object_name].control(a['name']).set_value(a['value'])

    def refresh(self):
        if self.world is not None:
            self.model.set_world(self.world)

    def _attribute_changed(self, attribute_name):
        def _changed(old, new):
            self._obejct_attribute_changed(attribute_name, old, new)
        return _changed

    def _obejct_attribute_changed(self, attribute_name, old, new):
        print attribute_name, " : ", old, " --> ", new
        self.world[self._current].set_attribute(attribute_name, new)


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
