
from collections import OrderedDict
from openalea.core.singleton import Singleton
from openalea.core.observer import Observed
import warnings


class VPLScene(OrderedDict, Observed):

    """
    Scene for OALab. Singleton.

    This class inherit from ordered dict.
    This scene also inherits from Observed, especially to know when Scene has changed.
    (Notify listeners with world_changed event)
    """

    __metaclass__ = Singleton

    def __init__(self, *args, **kwds):
        OrderedDict.__init__(self, *args, **kwds)
        Observed.__init__(self)
        self._block = False
        self._emit_world_sync()

    def add(self, name="unnamed object", obj="None"):
        """
        Add a new object in the scene.

        :param name: name of the object to add in the scene
        :param obj: object to add
        """
        name = self._check_if_name_is_unique(name)
        self[name] = obj

    def block(self):
        """
        Block sent of signals.
        Useful to add many objects in the scene without refresh the viewer
        """
        self._block = True

    def release(self):
        """
        Release signals sending and update scene.
        """
        self._block = False
        self.update()

    def getScene(self):
        """
        :return: the scene (ordered dict)
        """
        return self

    def rename(self, oldname, newname):
        """
        Try to rename object named 'oldname' in 'newname'.

        :param oldname: str of the name of scene component to access
        :param newname: str of the name to set
        """
        obj = None
        try:
            obj = self[oldname]
        except:
            warnings.warn("scene[%s] doesn't exist." % oldname)

        if obj is not None:
            self.add(name=newname, obj=obj)
            del self[oldname]

    def reset(self):
        """
        clear the scene
        """
        self.clear()

    def _check_if_name_is_unique(self, name):
        """
        Check if an sub_scene with the name 'name' is alreadey register
        in the VPLScene.

        If it is the case, the name is changed ("_1" is append).
        This is realize until the name becomes unique.

        :param name: name to check unicity

        TODO : remove this method if we want unicity of name,
        like in a classical dict
        """
        return name

        '''
        while name in self:
            try:
                end = name.split("_")[-1]
                l = len(end)
                end = int(end)
                end += 1
                name = name[0:-l] + str(end)
            except:
                name += "_1"
        return name
        '''

    def __setitem__(self, key, value):
        super(VPLScene, self).__setitem__(key, value)
        self._emit_world_sync()

    def update(self):
        super(VPLScene, self).update()
        self._emit_world_sync()

    def __delitem__(self, key):
        super(VPLScene, self).__delitem__(key)
        self._emit_world_sync()

    def popitem(self, last=True):
        super(VPLScene, self).popitem(last)
        self._emit_world_sync()

    def clear(self):
        super(VPLScene, self).clear()
        self._emit_world_sync()

    def __reversed__(self):
        super(VPLScene, self).__reversed__()
        self._emit_world_sync()

    def __reduce__(self):
        super(VPLScene, self).__reduce__()
        self._emit_world_sync()

    def _emit_value_changed(self, old, new):
        """
        Notify listeners with world_changed event
        """
        if not self._block:
            self.notify_listeners(('world_changed', self))

    def _emit_world_sync(self):
        """
        Notify listeners with world_changed event
        """
        if not self._block:
            self.notify_listeners(('world_sync', self))

Scene = VPLScene
