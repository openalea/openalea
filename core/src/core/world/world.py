# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s): Guillaume Baty <guillaume.baty@inria.fr>
#                            Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

__all__ = [
    'World',
    'WorldObject'
]

from openalea.core.scene.vplscene import VPLScene
from openalea.core.observer import Observed, AbstractListener

# from collections import OrderedDict
# from openalea.core.observer import Observed
# class World(OrderedDict, Observed):


class Transform(object):

    def __init__(self, function, data):
        self._function = function
        self._data = data

    def __call__(self, data=None):
        if data is None:
            data = self._data
        return self._function(data)


class World(VPLScene, AbstractListener):

    """
    Contain objects of the world.

    When world changes, several events can be notified to listeners:
        - world_object_changed(world, changes)
        - world_object_replaced(world, key, old_object, new_object)
        - world_object_added(world, key, new_object)
        - world_object_removed(world, old_object)

    A generic "world_changed" event is also notified for all previous changes.

    .. warning::

        currently only world_changed event is implemented

    """

    def __init__(self):
        VPLScene.__init__(self)
        AbstractListener.__init__(self)
        self.count = 0

    def _emit_world_object_changed(self, old, new):
        """
        Notify listeners with world_object_changed event
        """
        if not self._block:
            self.notify_listeners(('world_object_changed', (self, old, new)))

    def _emit_world_object_removed(self, old):
        """
        Notify listeners with world_object_removed event
        """
        if not self._block:
            self.notify_listeners(('world_object_removed', (self, old)))

    def _emit_world_object_item_changed(self, obj, item, old, new):
        """
        Notify listeners with world_object_item_changed event
        """
        if not self._block:
            self.notify_listeners(('world_object_item_changed', (self, obj, item, old, new)))

    def __setitem__(self, key, value):
        if key in self:
            old = self[key]
            old.unregister_listener(self)
        else:
            old = None
        if not isinstance(value, WorldObject):
            world_obj = WorldObject(key, value)
        else:
            world_obj = value
        world_obj.register_listener(self)
        # VPLScene.__setitem__(self, key, world_obj)
        super(VPLScene, self).__setitem__(key, world_obj)
        self._emit_world_object_changed(old, world_obj)

    def __delitem__(self, key):
        if key in self:
            old = self[key]
            super(VPLScene, self).__delitem__(key)
            self._emit_world_object_removed(old)

    def sync(self):
        if not self._block:
            self.notify_listeners(('world_sync', self))

    def add(self, data, name=None, **kwargs):
        """
        arguments:

          - transform: method used to convert object before representing it
          - _repr_*: define method used to convert object to a specific format (html, vtk, ...)
        """
        if name is None:
            name = 'data_%03d' % self.count
            self.count += 1
        obj = WorldObject(name, data, **kwargs)

        # Parse world.add arguments to find transformation functions
        for key in kwargs:
            if key.startswith('_repr_') or key == 'transform':
                transform = kwargs.get(key, None)
                if transform:
                    t = Transform(transform, data)
                    setattr(obj, key, t)
        self[name] = obj
        return obj

    def remove(self, name):
        if name in self:
            del self[name]

    def change_object_attribute(self, name, attribute):
        attribute_name = attribute['name']
        attribute_value = attribute['value']
        self[name].set_attribute(attribute_name, attribute_value)

    def notify(self, sender, event=None):
        signal, data = event
        if event == 'world_object_data_changed':
            world_obj, old, new = data
            #self._emit_value_changed(old, new)
            self._emit_world_object_changed(old, world_obj)
        elif signal == 'world_object_attribute_changed':
            world_obj, old, new = data
            self._emit_world_object_item_changed(world_obj, 'attribute', old, new)

    def update_namespace(self, interpreter):
        interpreter.user_ns['world'] = self

    def __hash__(self):
        return id(self)


class WorldObject(Observed):

    """
    Object of the world.

    WorldObject contains :
        - name : world object identifier
        - data : the object itself
        - attributes : list of (name, Interface, value)

    WorldObject provides meta-information like ...
        - origin
        - time required to compute object
        - visibility in scene
        - date when object has been added to scene


    """

    def __init__(self, name, data, **kwargs):
        """
        :param name: object identifier
        :param data: object to store
        """
        super(WorldObject, self).__init__()

        self._name = name
        self._data = data
        self._attributes = []

        self._silent = False

        self.model_id = kwargs.pop('model_id', None)
        self.output_id = kwargs.pop('output_id', None)
        self.in_scene = kwargs.pop('in_scene', True) or True
        self.kwargs = kwargs

    def __setitem__(self, key, value):
        self.set_attribute(key, value)

    def __getitem__(self, key):
        attribute_names = [a['name'] for a in self._attributes]
        try:
            attribute = self._attributes[attribute_names.index(key)]
        except ValueError:
            raise KeyError(str(key))
        else:
            return attribute['value']

    @property
    def obj(self):
        return self.data

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @property
    def attributes(self):
        return self._attributes

    @property
    def silent(self):
        return self._silent

    @obj.setter
    def obj(self, data):
        self.data = data

    @data.setter
    def data(self, data):
        self.notify_listeners(('world_object_data_changed', (self, self._data, data)))
        self._data = data

    @silent.setter
    def silent(self, value):
        self._silent = value

    def attribute(self, key):
        attribute_names = [a['name'] for a in self._attributes]
        try:
            attribute = self._attributes[attribute_names.index(key)]
        except ValueError:
            raise KeyError(str(key))
        else:
            return attribute

    def set_attribute(self, name, value, interface=None, label=None, constraints=None):
        attribute_names = [a['name'] for a in self._attributes]
        try:
            attribute = self._attributes[attribute_names.index(name)]
        except ValueError:
            if interface is None:
                from openalea.core.service.interface import guess_interface
                interfaces = guess_interface(value)
                if len(interfaces):
                    interface = interfaces[0]
            self._attributes.append(
                dict(
                    name=name,
                    value=value,
                    interface=interface,
                    label=label,
                    constraints=constraints))
            self.notify_listeners(('world_object_attribute_changed', (self, None, self._attributes[-1])))
        else:
            from copy import copy
            old_attribute = copy(attribute)
            if interface is not None:
                attribute['interface'] = interface
            if label is not None:
                attribute['label'] = label
            if constraints:
                attribute['constraints'] = constraints
            attribute['value'] = value
            if attribute['value'] != old_attribute['value']:
                self.notify_listeners(('world_object_attribute_changed', (self, old_attribute, attribute)))

    def get(self, name, default_value=None):
        attribute_names = [a['name'] for a in self._attributes]
        try:
            attribute = self._attributes[attribute_names.index(name)]
        except ValueError:
            return default_value
        else:
            return attribute['value']

    def notify_listeners(self, event=None):
        if not self._silent:
            super(WorldObject, self).notify_listeners(event)
