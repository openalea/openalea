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

from openalea.oalab.scene.vplscene import VPLScene
from openalea.core.observer import Observed, AbstractListener

# from collections import OrderedDict
# from openalea.core.observer import Observed
# class World(OrderedDict, Observed):


class World(VPLScene, AbstractListener):

    """
    Contain objects of the world.

    When world changes, it notifies all listeners with these events:
        - WorldObjectChanged(scene, changes)
        - WorldObjectReplaced(scene, key, old_object, new_object)
        - WorldObjectAdded(scene, key, new_object)
        - WorldObjectRemoved(scene, old_object)
        - WorldObjectIndexChanged(scene, old_idx, new_idx)

    A generic "world_changed" event is also notified for all previous changes.

    .. warning::

        currently only world_changed event is implemented

    """

    def __init__(self):
        VPLScene.__init__(self)
        AbstractListener.__init__(self)
        self.count = 0

    def __setitem__(self, key, value):
        if not isinstance(value, WorldObject):
            world_obj = WorldObject(value)
        else:
            world_obj = value
        world_obj.register_listener(self)
        VPLScene.__setitem__(self, key, world_obj)

    def sync(self):
        if not self._block:
            self.notify_listeners(('world_sync', self))

    def add(self, data, transform=None, name=None, **kwargs):
        if name is None:
            name = 'data_%03d' % self.count
            self.count += 1
        obj = WorldObject(data, **kwargs)
        if transform:
            def f():
                return transform(data)
            obj._repr_geom_ = f
        self[name] = obj

    def notify(self, sender, event=None):
        signal, data = event
        if event == 'world_object_changed':
            world, old, new = data
            self._emit_value_changed(old, new)

    def update_namespace(self, interpreter):
        interpreter.user_ns['world'] = self

    def __hash__(self):
        return id(self)


class WorldObject(Observed):

    """
    Object of the world.

    WorldObject provides meta-information like ...
        - origin
        - time required to compute object
        - visibility in scene
        - date when object has been added to scene
    """

    def __init__(self, obj, model_id=None, output_id=None, transform=None, **kwargs):
        """
        :param obj: object to store
        :param model_id: identifier of the model used to create this object
        :param output_id: identifier of output of the model used to create this object
        :param in_scene: set to True if it is a part of the scene (so it is viewable)
        """
        super(WorldObject, self).__init__()

        self._obj = obj
        self.model_id = model_id
        self.output_id = output_id
        self.in_scene = True
        self.kwargs = kwargs

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, obj):
        self.notify_listeners(('world_object_changed', (self, self._obj, obj)))
        self._obj = obj
