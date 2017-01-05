# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s): Julien Coste <julien.coste@inria.fr>
#                            Guillaume Cerutti <guillaume.cerutti@inria.fr>
#                            Guillaume Baty <guillaume.baty@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__revision__ = ""

import weakref

from Qt import QtWidgets, QtGui, QtCore

from openalea.core.observer import AbstractListener
from openalea.core.service.ipython import interpreter as get_interpreter

from openalea.oalab.control.manager import ControlManagerWidget
from openalea.oalab.service.drag_and_drop import add_drop_callback

class GenericWorldBrowser(QtWidgets.QWidget):

    def __init__(self):
        super(GenericWorldBrowser, self).__init__()
        layout = QtWidgets.QGridLayout()
        self.model = WorldModel()
        self.tree = QtWidgets.QTreeView()
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

        actionClearWorld = QtWidgets.QAction(QtGui.QIcon(":/images/resources/plant.png"), "Clear World", self)
        actionClearWorld.triggered.connect(self.clear)
        self._actions = [["Project", "World", actionClearWorld, 0]]

        add_drop_callback(self, 'openalea/interface.IImage', self.drop_object)

    def initialize(self):
        from openalea.core.world.world import World
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
        # print signal
        if signal == 'world_changed':
            self.set_world(data)
            self.refresh()
        elif signal == 'world_object_removed':
            world = data[0]
            self.set_world(world)
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

    def drop_object(self, obj, **kwargs):
        self.world.add(obj, **kwargs)

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

class WorldControlPanel(QtWidgets.QWidget, AbstractListener):
    StyleTableView = 0
    StylePanel = 1
    DEFAULT_STYLE = StylePanel

    attributeChanged = QtCore.Signal(str, dict)

    def __init__(self, parent=None, style=None):
        AbstractListener.__init__(self)
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.world = None
        self.model = WorldModel()

        if style is None:
            style = self.DEFAULT_STYLE
        self.style = style

        self._manager = {}

        self._cb_world_object = QtWidgets.QComboBox()
        p = QtWidgets.QSizePolicy
        self._cb_world_object.setSizePolicy(p(p.Expanding, p.Maximum))
        self._cb_world_object.currentIndexChanged.connect(self._selected_object_changed)

        self._current = None
        self._default_manager = self._create_manager()

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_control'] = self

        actionClearWorld = QtWidgets.QAction(QtGui.QIcon(":/images/resources/plant.png"), "Clear World", self)
        actionClearWorld.triggered.connect(self.clear)
        self._actions = [["Project", "World", actionClearWorld, 0]]

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addWidget(self._cb_world_object)

        if self.style == self.StyleTableView:
            self._view = ControlManagerWidget(manager=self._default_manager)
            self._layout.addWidget(self._view)
        elif self.style == self.StylePanel:
            self._view = None
            self._set_manager(self._default_manager)
        else:
            raise NotImplementedError('style %s' % self.style)

    def set_properties(self, properties):
        if self.style == self.StyleTableView:
            self._view.set_properties(properties)

    def properties(self):
        if self.style == self.StyleTableView:
            return self._view.properties()
        else:
            return []

    def set_style(self, style):
        if style == self.style:
            return

        world = self.world
        self.clear()
        if self.style == self.StyleTableView:
            view = self._view
        elif self.style == self.StylePanel:
            if self._view and self._view():
                view = self._view()
            else:
                return

        # Remove old view
        view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._layout.removeWidget(view)
        view.close()
        del view
        self._view = None

        self.style = style
        if style == self.StyleTableView:
            self._view = ControlManagerWidget(manager=self._default_manager)
            self._layout.addWidget(self._view)

        self.set_world(world)

    def __getitem__(self, key):
        return self._manager[self._current].control(name=key)

    def initialize(self):
        from openalea.core.world.world import World
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
            self.refresh()
        elif signal == 'world_object_removed':
            self.refresh()
        elif signal == 'world_object_changed':
            world, old_object, world_object = data
            self.refresh_manager(world_object)
        elif signal == 'world_object_item_changed':
            world, world_object, item, old, new = data
            self.refresh_manager(world_object)
            #self.refresh_item(world_object, item, old, new)
        elif signal == 'world_sync':
            self.refresh()

    def clear_managers(self):
        self._current = None
        self._cb_world_object.clear()
        for name, manager in self._manager.items():
            manager.clear_followers()
            del self._manager[name]
        self._set_manager(self._default_manager)

    def clear(self):
        self.clear_managers()
        if self.world:
            self.world.unregister_listener(self)
            self.world = None

    def set_world(self, world):
        self.clear()

        self.world = world
        self.world.register_listener(self)

        if self.style == self.StyleTableView:
            self.model.set_world(world)

        for object_name in world.keys():
            self.refresh_manager(world[object_name])

    def _fill_manager(self, manager, world_object):
        if world_object:
            for attribute in world_object.attributes:
                manager.add(
                    attribute['name'],
                    interface=attribute['interface'],
                    value=attribute['value'],
                    label=attribute['label'],
                    constraints=attribute['constraints']
                )
                manager.register_follower(attribute['name'], self._attribute_changed(world_object, attribute['name']))

    def _get_manager(self, world_object):
        object_name = world_object.name
        if object_name not in self._manager:
            manager = self._create_manager(world_object)
            self._manager[object_name] = manager
            self._cb_world_object.addItem(object_name)
        return self._manager[object_name]

    def _create_manager(self, world_object=None):
        from openalea.core.control.manager import ControlContainer
        manager = ControlContainer()
        self._fill_manager(manager, world_object)
        return manager

    def _selected_object_changed(self, idx):
        if idx != -1:
            self.select_world_object(self._cb_world_object.itemText(idx))

    def _set_manager(self, manager):
        if self.style == self.StylePanel:
            view = self._view
            if self._view is not None:
                view = self._view()
            if view:
                self._layout.removeWidget(view)
                view.close()
                del view
            from openalea.oalab.service.qt_control import edit
            view = edit(manager)
            view.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self._view = weakref.ref(view)
            self._layout.addWidget(view)
            view.show()
            self.repaint()
        elif self.style == self.StyleTableView:
            self._view.model.set_manager(manager)
        else:
            raise NotImplementedError('style %s' % self.style)

    def select_world_object(self, object_name):
        if object_name != self._current:
            self._current = object_name
            object_manager = self._manager[object_name]
            object_manager.disable_followers()
            self._set_manager(object_manager)
            object_manager.enable_followers()

    def refresh_item(self, world_object, item, old, new):
        object_name = world_object.name
        if item == 'attribute':
            manager = self._get_manager(world_object)
            attr_name = new['name']
            attr_value = new['value']
            control = manager.control(name=attr_name)
            if control:
                control.value = attr_value
        else:
            self.refresh_manager(world_object)

    def refresh_manager(self, world_object):
        object_name = world_object.name
        object_manager = self._get_manager(world_object)

        manager_attr_names = [c.name for c in self._manager[object_name].controls()]
        object_attr_names = [a['name'] for a in world_object.attributes]
        if manager_attr_names != object_attr_names:
            object_manager.clear_followers()
            object_manager.clear()
            self._fill_manager(object_manager, world_object)
            if self._current == object_name:
                self._set_manager(object_manager)
                object_manager.enable_followers()
        else:
            for a in world_object.attributes:
                if a['value'] != self._manager[object_name].control(a['name']).value:
                    self._manager[object_name].control(a['name']).set_value(a['value'])

    def refresh(self):
        if self.world is not None:
            self.set_world(self.world)

    def _attribute_changed(self, world_object, attribute_name):
        def _changed(old, new):
            self._object_attribute_changed(world_object.name, attribute_name, old, new)
        return _changed

    def _object_attribute_changed(self, object_name, attribute_name, old, new):
        self.world[object_name].set_attribute(attribute_name, new)

def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)

    from openalea.core.world import World

    world = World()
    world["obj1"] = "plop"
    world["obj2"] = "plop2"

    obj1 = world["obj1"]
    obj2 = world["obj2"]

    obj1.set_attribute('a1', 1, 'IInt')
    obj1.set_attribute('a2', True, 'IBool')

    obj2.set_attribute('b1', 2.34, 'IFloat')

    wid1 = WorldControlPanel(style=WorldControlPanel.StylePanel)
    wid1.set_world(world)
    wid1.show()

    wid2 = WorldControlPanel(style=WorldControlPanel.StyleTableView)
    wid2.set_world(world)
    wid2.show()

    app.exec_()

if __name__ == "__main__":
    main()
